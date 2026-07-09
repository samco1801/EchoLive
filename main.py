from core.live import LiveClient
from core.config import Config


def main():

    config = Config()

    username = config.get("username")

    live = LiveClient(username)

    live.connect()


if __name__ == "__main__":
    main()
    