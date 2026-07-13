import asyncio

from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError
from TikTokLive.events import ConnectEvent, CommentEvent

from core.filter import CommentFilter
from core.queue import CommentQueue
from core.stats import Stats
from core.tts import TTS


class LiveClient:

    def __init__(self, username: str):

        self.username = username
        self.client = TikTokLiveClient(unique_id=username)

        self.tts = TTS()
        self.comment_queue = CommentQueue(self.tts)
        self.comment_filter = CommentFilter()
        self.stats = Stats()

        self.room_id = "-"

        # Registrar eventos
        self.client.on(ConnectEvent, self.on_connect)
        self.client.on(CommentEvent, self.on_comment)

    def connect(self):

        print("--------------------------------")
        print("EchoLive")
        print("--------------------------------")
        print(f"Intentando conectar con @{self.username}...\n")

        try:
            self.client.run()

        except UserOfflineError:
            print("❌ El usuario no está en directo.")

        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    async def on_connect(self, event: ConnectEvent):

        self.room_id = event.room_id

        await self.comment_queue.start()

        self.stats.refresh()

    async def on_comment(self, event: CommentEvent):

        self.stats.comment_received()

        if self.comment_filter.is_valid(event.comment):

            self.stats.comment_read(
                event.user.nickname,
                event.comment
            )

            await self.comment_queue.add(event.comment)

        else:

            self.stats.comment_filtered()

    async def shutdown(self):

        print("\n🔴 Cerrando EchoLive...")

        await self.comment_queue.stop()

        try:
            await self.client.disconnect()
        except Exception:
            pass

        print("✅ Desconectado de TikTok.")