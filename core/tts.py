import os

import edge_tts
from playsound3 import playsound


class TTS:

    def __init__(self):
        self.voice = "es-CO-GonzaloNeural"

    async def speak(self, text: str):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="-20%",
            volume="+0%",
            pitch="+0Hz"
        )

        await communicate.save("temp.mp3")

        playsound("temp.mp3")

        os.remove("temp.mp3")