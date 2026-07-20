import re
import emoji


class TextSanitizer:

    def sanitize(self, text: str) -> str:

        text = emoji.replace_emoji(text, replace="")

        text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"\s+([.,!?;:])", r"\1", text)

        text = text.strip()

        return text