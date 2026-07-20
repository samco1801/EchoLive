import asyncio

from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError
from TikTokLive.events import ConnectEvent, CommentEvent, DisconnectEvent

from core.filter import CommentFilter
from core.queue import CommentQueue
from core.stats import Stats
from core.sanitizer import TextSanitizer
from core.tts import TTS


class LiveClient:

    def __init__(self, username: str):

        self.username = username
        self.client = TikTokLiveClient(unique_id=username)

        self.tts = TTS()
        self.comment_queue = CommentQueue(self.tts)
        self.comment_filter = CommentFilter()
        self.text_sanitizer = TextSanitizer()
        self.stats = Stats()

        self.room_id = "-"

        # Loop de asyncio en el que corre esta conexión (se guarda para
        # poder pedirle un shutdown limpio desde el hilo principal).
        self.loop = None

        self.on_connected = None
        self.on_disconnected = None
        self.on_error = None
        self.on_comment_callback = None
        self.on_stats = None

        # Registrar eventos
        self.client.on(ConnectEvent, self.on_connect)
        self.client.on(CommentEvent, self.on_comment)
        self.client.on(DisconnectEvent, self.on_disconnect_event)

    def connect(self):
        """Punto de entrada bloqueante (se corre en un hilo aparte). Crea su
        propio event loop y lo guarda en self.loop para poder pedirle luego
        una desconexión limpia desde el hilo principal."""

        try:
            asyncio.run(self._connect_async())
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    async def _connect_async(self):

        self.loop = asyncio.get_running_loop()

        print("--------------------------------")
        print("EchoLive")
        print("--------------------------------")
        print(f"Intentando conectar con @{self.username}...\n")

        try:
            await self.client.connect()

        except UserOfflineError:
            print("❌ El usuario no está en directo.")

            if self.on_error:
                self.on_error("offline")

            return

        except Exception as e:
            print(f"❌ Error inesperado: {e}")

            if self.on_error:
                self.on_error(str(e))

            return

        finally:
            await self.comment_queue.stop()

        # Si llegamos aquí sin excepción, el live terminó con normalidad
        # (el streamer salió del directo o se perdió la conexión).
        print("\n🔴 El directo terminó.")

        if self.on_disconnected:
            self.on_disconnected()

    async def on_connect(self, event: ConnectEvent):

        self.room_id = event.room_id

        await self.comment_queue.start()

        self.stats.refresh()

        if self.on_stats:
            self.on_stats(self.stats, self.comment_queue.size())

        if self.on_connected:
            self.on_connected()

    async def on_disconnect_event(self, event: DisconnectEvent):
        """Se dispara cuando la conexión con TikTok se cierra (el streamer
        salió del directo, o se perdió la conexión)."""

        if self.on_disconnected:
            self.on_disconnected()

    async def on_comment(self, event: CommentEvent):

        self.stats.comment_received()

        if self.comment_filter.is_valid(event.comment):

            # Limpiar el comentario
            text = self.text_sanitizer.sanitize(event.comment)

            # Si después de limpiarlo quedó vacío, no leerlo
            if not text:
                self.stats.comment_filtered()
                return

            self.stats.comment_read(
                event.user.nickname,
                text
            )

            if self.on_comment_callback:
                self.on_comment_callback(
                    event.user.nickname,
                    text
                )

            await self.comment_queue.add(text)

        else:

            self.stats.comment_filtered()

        if self.on_stats:
            self.on_stats(
                self.stats,
                self.comment_queue.size()
            )

    async def shutdown(self):

        print("\n🔴 Cerrando EchoLive...")

        await self.comment_queue.stop()

        try:
            await self.client.disconnect()
        except Exception:
            pass

        print("✅ Desconectado de TikTok.")

    def request_shutdown(self, timeout: float = 3.0):
        """Versión síncrona pensada para llamarse desde el hilo principal
        (por ejemplo al cerrar la ventana), usando el loop que quedó
        guardado en self.loop cuando arrancó la conexión."""

        if not self.loop or not self.loop.is_running():
            return

        try:
            future = asyncio.run_coroutine_threadsafe(
                self.client.disconnect(),
                self.loop
            )
            future.result(timeout=timeout)
        except Exception:
            pass
