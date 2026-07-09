import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from TikTokLive.client.errors import UserOfflineError
from core.filter import CommentFilter
from core.queue import CommentQueue
from core.tts import TTS


class LiveClient:

    def __init__(self, username: str):
        self.username = username
        self.client = TikTokLiveClient(unique_id=username)

        self.tts = TTS()
        self.comment_queue = CommentQueue(self.tts)
        self.comment_filter = CommentFilter()

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
        print("🟢 EchoLive conectado correctamente al LIVE.")
        print(f"Room ID: {event.room_id}")
        asyncio.create_task(self.comment_queue.worker())

    async def on_comment(self, event: CommentEvent):
        print(f"\n💬 {event.user.nickname}")
        print(f"   {event.comment}")

        if self.comment_filter.is_valid(event.comment):
            await self.comment_queue.add(event.comment)
        else:
            print("🚫 Comentario filtrado.")