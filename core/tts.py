import os
import uuid

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

    def update_settings(self, enabled=None, voice=None, rate=None, volume=None):
        """Permite actualizar la voz/velocidad/volumen sin recrear el objeto,
        para que los cambios hechos en la ventana de Configuración se apliquen
        de inmediato aunque ya estés conectado al live."""

        if enabled is not None:
            self.enabled = enabled

        if voice is not None:
            self.voice = voice

        if rate is not None:
            self.rate = rate

        if volume is not None:
            self.volume = volume

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

        temp_file = f"temp_{uuid.uuid4().hex}.mp3"

        await communicate.save(temp_file)

        try:
            playsound(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


async def speak_preview(text: str, voice: str, rate: str, volume: str):
    """Función independiente usada por la ventana de Configuración para
    reproducir una muestra de voz sin depender de una conexión al live."""

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch="+0Hz"
    )

    temp_file = f"temp_{uuid.uuid4().hex}.mp3"

    await communicate.save(temp_file)

    try:
        playsound(temp_file)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)