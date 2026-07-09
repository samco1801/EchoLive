import json

from core.live import LiveClient


def main():

    with open("config/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    username = config["username"]

    live = LiveClient(username)

    live.connect()


if __name__ == "__main__":
    main()
    