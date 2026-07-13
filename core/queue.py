import asyncio


class CommentQueue:

    def __init__(self, tts):

        self.queue = asyncio.Queue()
        self.tts = tts

        self.running = False
        self.worker_task = None

    async def add(self, text: str):

        await self.queue.put(text)

    def size(self):

        return self.queue.qsize()

    async def start(self):

        if self.worker_task is None:

            self.running = True

            self.worker_task = asyncio.create_task(self.worker())

    async def stop(self):

        if not self.running:
            return

        print("\n⏳ Esperando comentarios pendientes...")

        self.running = False

        # Despierta al worker si está esperando
        await self.queue.put(None)

        if self.worker_task:
            await self.worker_task

        print("✅ Worker detenido.")

    async def worker(self):

        print("🟢 Worker de comentarios iniciado.")

        while self.running:

            text = await self.queue.get()

            if text is None:
                break

            try:

                await self.tts.speak(text)

            except Exception as e:

                print(f"❌ Error al reproducir comentario: {e}")

            finally:

                self.queue.task_done()