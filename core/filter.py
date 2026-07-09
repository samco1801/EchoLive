import re

from core.config import Config


class CommentFilter:

    def __init__(self):

        config = Config()
        filters = config.get_section("filters")

        self.ignore_emojis = filters.get("ignore_emojis", True)
        self.ignore_symbols = filters.get("ignore_symbols", True)
        self.ignore_repeated = filters.get("ignore_repeated", True)
        self.max_length = filters.get("max_length", 200)

        self.last_comment = None

    def is_valid(self, text: str) -> bool:

        text = text.strip()

        if not text:
            return False

        if len(text) > self.max_length:
            return False

        if self.ignore_repeated:
            if text == self.last_comment:
                return False

            self.last_comment = text

        if self.ignore_symbols:
            if re.fullmatch(r"[^\w\s]+", text):
                return False

        if self.ignore_emojis:
            if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9]", text):
                return False

        return True