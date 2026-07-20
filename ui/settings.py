import asyncio
import threading

import customtkinter as ctk

from core.tts import speak_preview
from ui.widgets import Card


# Voces recomendadas de edge-tts en español. Puedes añadir más aquí siempre
# que existan en la lista oficial de voces de Microsoft Edge TTS.
VOICE_OPTIONS = {
    "Dalia (Mujer, México)": "es-MX-DaliaNeural",
    "Jorge (Hombre, México)": "es-MX-JorgeNeural",
    "Salomé (Mujer, Colombia)": "es-CO-SalomeNeural",
    "Gonzalo (Hombre, Colombia)": "es-CO-GonzaloNeural",
    "Elvira (Mujer, España)": "es-ES-ElviraNeural",
    "Álvaro (Hombre, España)": "es-ES-AlvaroNeural",
    "Elena (Mujer, Argentina)": "es-AR-ElenaNeural",
    "Tomás (Hombre, Argentina)": "es-AR-TomasNeural",
    "Paloma (Mujer, Latino EE.UU.)": "es-US-PalomaNeural",
    "Alonso (Hombre, Latino EE.UU.)": "es-US-AlonsoNeural",
}

VOICE_ID_TO_LABEL = {v: k for k, v in VOICE_OPTIONS.items()}


def _percent_to_str(value: float) -> str:
    return f"{int(round(value)):+d}%"


def _str_to_percent(value: str, default: int = 0) -> int:
    try:
        return int(str(value).replace("%", "").replace("+", ""))
    except (ValueError, TypeError):
        return default


class SettingsWindow(ctk.CTkToplevel):
    """Ventana de configuración: voz, velocidad, volumen y filtros de
    comentarios, sin tener que tocar config.json a mano."""

    def __init__(self, master, config, controller=None):

        super().__init__(master)

        self.config = config
        self.controller = controller

        self.title("Configuración - EchoLive")
        self.geometry("520x760")
        self.minsize(460, 500)
        self.resizable(True, True)

        # Que la ventana quede al frente de la principal
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenido con scroll: así, sin importar la resolución de pantalla
        # o cuánto crezca el contenido, los botones de abajo nunca quedan
        # cortados fuera de la ventana.
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.scroll_area.grid_columnconfigure(0, weight=1)

        tts_data = self.config.get_section("tts")
        filters_data = self.config.get_section("filters")

        self._build_voice_card(tts_data)
        self._build_filters_card(filters_data)
        self._build_actions()

    # ------------------------------------------------------------------
    # Tarjeta de voz
    # ------------------------------------------------------------------

    def _build_voice_card(self, tts_data):

        card = Card(self.scroll_area, "🔊 Voz", accent="#25F4EE")
        card.grid(row=0, column=0, padx=5, pady=(5, 10), sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        # Activar/desactivar TTS

        self.tts_enabled_var = ctk.BooleanVar(
            value=tts_data.get("enabled", True)
        )

        enabled_switch = ctk.CTkSwitch(
            card,
            text="Leer comentarios en voz alta",
            variable=self.tts_enabled_var,
            onvalue=True,
            offvalue=False
        )

        enabled_switch.grid(
            row=1, column=0, padx=20, pady=(5, 15), sticky="w"
        )

        # Selector de voz

        voice_label = ctk.CTkLabel(card, text="Voz", anchor="w")
        voice_label.grid(row=2, column=0, padx=20, sticky="w")

        current_voice_id = tts_data.get("voice", "es-CO-GonzaloNeural")
        current_voice_label = VOICE_ID_TO_LABEL.get(
            current_voice_id,
            list(VOICE_OPTIONS.keys())[0]
        )

        self.voice_var = ctk.StringVar(value=current_voice_label)

        voice_menu = ctk.CTkOptionMenu(
            card,
            values=list(VOICE_OPTIONS.keys()),
            variable=self.voice_var
        )

        voice_menu.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Velocidad

        self.rate_value = _str_to_percent(tts_data.get("rate", "-20%"), -20)

        rate_label = ctk.CTkLabel(
            card, text=f"Velocidad ({self.rate_value:+d}%)", anchor="w"
        )
        rate_label.grid(row=4, column=0, padx=20, sticky="w")
        self.rate_label = rate_label

        self.rate_slider = ctk.CTkSlider(
            card,
            from_=-50,
            to=50,
            number_of_steps=100,
            command=self._on_rate_change
        )
        self.rate_slider.set(self.rate_value)
        self.rate_slider.grid(row=5, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Volumen

        self.volume_value = _str_to_percent(tts_data.get("volume", "+0%"), 0)

        volume_label = ctk.CTkLabel(
            card, text=f"Volumen ({self.volume_value:+d}%)", anchor="w"
        )
        volume_label.grid(row=6, column=0, padx=20, sticky="w")
        self.volume_label = volume_label

        self.volume_slider = ctk.CTkSlider(
            card,
            from_=-50,
            to=50,
            number_of_steps=100,
            command=self._on_volume_change
        )
        self.volume_slider.set(self.volume_value)
        self.volume_slider.grid(row=7, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Botón de probar voz

        self.test_button = ctk.CTkButton(
            card,
            text="🔈 Probar voz",
            fg_color="transparent",
            border_width=1,
            command=self._test_voice
        )
        self.test_button.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="ew")

    def _on_rate_change(self, value):
        self.rate_value = int(round(value))
        self.rate_label.configure(text=f"Velocidad ({self.rate_value:+d}%)")

    def _on_volume_change(self, value):
        self.volume_value = int(round(value))
        self.volume_label.configure(text=f"Volumen ({self.volume_value:+d}%)")

    def _test_voice(self):

        voice_id = VOICE_OPTIONS[self.voice_var.get()]
        rate_str = _percent_to_str(self.rate_value)
        volume_str = _percent_to_str(self.volume_value)

        self.test_button.configure(state="disabled", text="Reproduciendo...")

        def run():
            try:
                asyncio.run(
                    speak_preview(
                        "Así sonará tu voz en el directo.",
                        voice_id,
                        rate_str,
                        volume_str
                    )
                )
            finally:
                self.after(
                    0,
                    lambda: self.test_button.configure(
                        state="normal", text="🔈 Probar voz"
                    )
                )

        threading.Thread(target=run, daemon=True).start()

    # ------------------------------------------------------------------
    # Tarjeta de filtros
    # ------------------------------------------------------------------

    def _build_filters_card(self, filters_data):

        card = Card(self.scroll_area, "🧹 Filtros de comentarios", accent="#FFB74D")
        card.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        self.ignore_emojis_var = ctk.BooleanVar(
            value=filters_data.get("ignore_emojis", True)
        )
        ctk.CTkSwitch(
            card,
            text="Ignorar comentarios que sean solo emojis",
            variable=self.ignore_emojis_var
        ).grid(row=1, column=0, padx=20, pady=(5, 10), sticky="w")

        self.ignore_symbols_var = ctk.BooleanVar(
            value=filters_data.get("ignore_symbols", True)
        )
        ctk.CTkSwitch(
            card,
            text="Ignorar comentarios de solo símbolos",
            variable=self.ignore_symbols_var
        ).grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.ignore_repeated_var = ctk.BooleanVar(
            value=filters_data.get("ignore_repeated", True)
        )
        ctk.CTkSwitch(
            card,
            text="Ignorar comentarios repetidos seguidos",
            variable=self.ignore_repeated_var
        ).grid(row=3, column=0, padx=20, pady=10, sticky="w")

        max_length_label = ctk.CTkLabel(
            card, text="Largo máximo de comentario (caracteres)", anchor="w"
        )
        max_length_label.grid(row=4, column=0, padx=20, pady=(10, 5), sticky="w")

        self.max_length_entry = ctk.CTkEntry(card)
        self.max_length_entry.insert(
            0, str(filters_data.get("max_length", 200))
        )
        self.max_length_entry.grid(
            row=5, column=0, padx=20, pady=(0, 20), sticky="ew"
        )

    # ------------------------------------------------------------------
    # Guardar / cerrar
    # ------------------------------------------------------------------

    def _build_actions(self):

        actions_container = ctk.CTkFrame(self, fg_color="transparent")
        actions_container.grid(row=1, column=0, sticky="ew")
        actions_container.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            actions_container, text="", text_color="#4CD964"
        )
        self.status_label.grid(row=0, column=0, pady=(8, 0))

        buttons_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, padx=20, pady=16, sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            height=42,
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        )
        cancel_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            height=42,
            font=("Segoe UI", 14, "bold"),
            command=self._save
        )
        save_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def _save(self):

        try:
            max_length = int(self.max_length_entry.get())
        except ValueError:
            max_length = 200

        voice_id = VOICE_OPTIONS[self.voice_var.get()]
        rate_str = _percent_to_str(self.rate_value)
        volume_str = _percent_to_str(self.volume_value)

        tts_settings = {
            "enabled": self.tts_enabled_var.get(),
            "voice": voice_id,
            "rate": rate_str,
            "volume": volume_str,
        }

        filters_settings = {
            "ignore_emojis": self.ignore_emojis_var.get(),
            "ignore_symbols": self.ignore_symbols_var.get(),
            "ignore_repeated": self.ignore_repeated_var.get(),
            "max_length": max_length,
        }

        self.config.set_section("tts", tts_settings)
        self.config.set_section("filters", filters_settings)
        self.config.save()

        # Si ya hay un live conectado, aplicar los cambios sin reiniciar
        if self.controller and self.controller.live:
            self.controller.live.tts.update_settings(**tts_settings)
            self.controller.live.comment_filter.update_settings(**filters_settings)

        self.status_label.configure(text="✅ Configuración guardada")
        self.after(2000, lambda: self.status_label.configure(text=""))
