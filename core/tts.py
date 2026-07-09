import os

import edge_tts
from playsound3 import playsound

from core.config import Config


class TTS:

    def __init__(self):

        config = Config()
        tts = config.get_section("tts")

        self.enabled = tts.get("enabled", True)
        self.voice = tts.get("voice", "es-CO-GonzaloNeural")
        self.rate = tts.get("rate", "-20%")
        self.volume = tts.get("volume", "+0%")

    async def speak(self, text: str):

        if not self.enabled:
            return

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch="+0Hz"
        )

        await communicate.save("temp.mp3")

        playsound("temp.mp3")

        os.remove("temp.mp3")