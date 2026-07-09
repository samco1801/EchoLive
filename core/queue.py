import asyncio


class CommentQueue:

    def __init__(self, tts):

        self.queue = asyncio.Queue()
        self.tts = tts

    async def add(self, text: str):

        await self.queue.put(text)

    async def worker(self):

        print("🟢 Worker de comentarios iniciado.")

        while True:

            text = await self.queue.get()

            try:

                await self.tts.speak(text)

            except Exception as e:

                print(f"❌ Error al reproducir comentario: {e}")

            finally:

                self.queue.task_done()