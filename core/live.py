from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from TikTokLive.client.errors import UserOfflineError


class LiveClient:

    def __init__(self, username: str):
        self.username = username
        self.client = TikTokLiveClient(unique_id=username)

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

    async def on_comment(self, event: CommentEvent):
        print(f"\n💬 {event.user.nickname}")
        print(f"   {event.comment}")