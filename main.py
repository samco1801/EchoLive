import asyncio

from core.config import Config
from core.live import LiveClient
from ui.console import Console


def main():

    config = Config()

    username = config.get("username")

    live = LiveClient(username)

    console = Console(live)

    live.stats.on_update = console.draw

    console.draw()

    try:

        live.connect()

    except KeyboardInterrupt:

        print("\n\nCerrando aplicación...")

        try:
            asyncio.run(live.shutdown())
        except RuntimeError:
            pass

        print("👋 Hasta luego.")


if __name__ == "__main__":
    main()