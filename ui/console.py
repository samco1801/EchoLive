import asyncio
import os


class Console:

    def __init__(self, live):

        self.live = live

    @staticmethod
    def clear():

        os.system("cls" if os.name == "nt" else "clear")

    async def run(self):

        while True:

            self.draw()

            await asyncio.sleep(0.5)

    def draw(self):

        self.clear()

        print("=" * 50)
        print("               EchoLive v0.3")
        print("=" * 50)
        print()

        print("Estado............. 🟢 Conectado")
        print(f"Usuario............ @{self.live.username}")
        print(f"Room ID............ {self.live.room_id}")

        print("\n" + "-" * 50)

        print("📊 Estadísticas\n")

        print(f"Comentarios recibidos : {self.live.stats.received}")
        print(f"Comentarios leídos    : {self.live.stats.read}")
        print(f"Comentarios filtrados : {self.live.stats.filtered}")
        print(f"En cola              : {self.live.comment_queue.size()}")

        print("\n" + "-" * 50)

        print("👤 Último usuario")
        print(self.live.stats.last_user)

        print("\n💬 Último comentario")
        print(self.live.stats.last_comment)

        print("\n" + "=" * 50)