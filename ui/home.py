import os

import customtkinter as ctk
from PIL import Image

from controller.app_controller import AppController
from core.config import Config
from ui.widgets import Card
from ui.stat_item import StatItem
from ui.settings import SettingsWindow

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

ACCENT_CYAN = "#25F4EE"
ACCENT_PINK = "#FE2C55"
ACCENT_GOLD = "#FFB74D"
ACCENT_GREEN = "#4CD964"


class HomeFrame(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, fg_color="transparent")

        self.config = Config()
        self.controller = AppController(self)

        self.grid_columnconfigure(0, weight=1, uniform="cols")
        self.grid_columnconfigure(1, weight=1, uniform="cols")

        self.grid_rowconfigure(1, weight=1, minsize=340)
        self.grid_rowconfigure(2, weight=1, minsize=340)

        self.create_header()
        self.create_connection_card()
        self.create_stats_card()

        self.create_settings_card()
        self.create_comment_card()

    # ------------------------------------------------------------------
    # Encabezado
    # ------------------------------------------------------------------

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=("gray85", "#181820")
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 20),
            sticky="ew"
        )

        header.grid_columnconfigure(1, weight=1)

        logo_path = os.path.join(ASSETS_DIR, "logo.png")

        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(64, 64)
            )

            logo_label = ctk.CTkLabel(header, image=logo_image, text="")
            logo_label.grid(row=0, column=0, rowspan=2, padx=(24, 16), pady=20)

        title = ctk.CTkLabel(
            header,
            text="EchoLive",
            font=("Segoe UI", 38, "bold"),
            anchor="w"
        )

        title.grid(
            row=0,
            column=1,
            pady=(20, 0),
            sticky="sw"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Convierte los comentarios de tu TikTok LIVE en voz, en tiempo real",
            font=("Segoe UI", 15),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        subtitle.grid(
            row=1,
            column=1,
            pady=(0, 20),
            sticky="nw"
        )

    # ------------------------------------------------------------------
    # Tarjeta de conexión
    # ------------------------------------------------------------------

    def create_connection_card(self):

        self.connection_card = Card(self, "🎤  Conexión", accent=ACCENT_CYAN)

        self.connection_card.grid(
            row=1,
            column=0,
            padx=(0, 10),
            pady=10,
            sticky="nsew"
        )

        self.connection_card.grid_columnconfigure(0, weight=1)

        # Usuario

        user_label = ctk.CTkLabel(
            self.connection_card,
            text="Usuario de TikTok",
            font=("Segoe UI", 13),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        user_label.grid(
            row=1,
            column=0,
            padx=24,
            pady=(10, 6),
            sticky="w"
        )

        self.username_entry = ctk.CTkEntry(
            self.connection_card,
            height=42,
            font=("Segoe UI", 14),
            placeholder_text="@usuario"
        )

        self.username_entry.grid(
            row=2,
            column=0,
            padx=24,
            sticky="ew"
        )

        username = self.config.get("username")

        if username:
            self.username_entry.insert(0, username)

        # Estado

        status_title = ctk.CTkLabel(
            self.connection_card,
            text="Estado",
            font=("Segoe UI", 13),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        status_title.grid(
            row=3,
            column=0,
            padx=24,
            pady=(24, 4),
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            self.connection_card,
            text="⚪ Desconectado",
            font=("Segoe UI", 17, "bold"),
            anchor="w"
        )

        self.status_label.grid(
            row=4,
            column=0,
            padx=24,
            sticky="w"
        )

        # Espaciador flexible para empujar el botón hacia abajo de forma
        # consistente sin importar la altura de la tarjeta.
        self.connection_card.grid_rowconfigure(5, weight=1)

        # Botón

        self.connect_button = ctk.CTkButton(
            self.connection_card,
            text="Conectar",
            height=44,
            font=("Segoe UI", 15, "bold"),
            command=self.controller.connect
        )

        self.connect_button.grid(
            row=6,
            column=0,
            padx=24,
            pady=(20, 24),
            sticky="ew"
        )

    # ------------------------------------------------------------------
    # Tarjeta de estadísticas
    # ------------------------------------------------------------------

    def create_stats_card(self):

        self.stats_card = Card(self, "📊  Estadísticas", accent=ACCENT_PINK)

        self.stats_card.grid(
            row=1,
            column=1,
            padx=(10, 0),
            pady=10,
            sticky="nsew"
        )

        self.stats_card.grid_columnconfigure(0, weight=1)
        self.stats_card.grid_columnconfigure(1, weight=1)

        self.received_item = StatItem(
            self.stats_card, "Recibidos", accent=ACCENT_CYAN, icon="📥"
        )
        self.received_item.grid(
            row=1, column=0, padx=(24, 12), pady=(14, 18), sticky="w"
        )

        self.read_item = StatItem(
            self.stats_card, "Leídos", accent=ACCENT_PINK, icon="🔊"
        )
        self.read_item.grid(
            row=1, column=1, padx=(12, 24), pady=(14, 18), sticky="w"
        )

        self.filtered_item = StatItem(
            self.stats_card, "Filtrados", accent=ACCENT_GOLD, icon="🧹"
        )
        self.filtered_item.grid(
            row=2, column=0, padx=(24, 12), pady=(0, 20), sticky="w"
        )

        self.queue_item = StatItem(
            self.stats_card, "En cola", accent=ACCENT_GREEN, icon="⏳"
        )
        self.queue_item.grid(
            row=2, column=1, padx=(12, 24), pady=(0, 20), sticky="w"
        )

        # Espaciador para que las estadísticas queden centradas en la
        # tarjeta en vez de pegadas arriba cuando la ventana crece.
        self.stats_card.grid_rowconfigure(0, weight=0)
        self.stats_card.grid_rowconfigure(3, weight=1)

    # ------------------------------------------------------------------
    # Tarjeta de configuración
    # ------------------------------------------------------------------

    def create_settings_card(self):

        self.settings_card = Card(self, "⚙️  Configuración", accent=ACCENT_GOLD)

        self.settings_card.grid(
            row=2,
            column=0,
            padx=(0, 10),
            pady=10,
            sticky="nsew"
        )

        self.settings_card.grid_columnconfigure(0, weight=1)

        description = ctk.CTkLabel(
            self.settings_card,
            text="Elige tu voz, ajusta el volumen y la velocidad,\ny configura los filtros de comentarios.",
            justify="left",
            font=("Segoe UI", 13),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        description.grid(
            row=1,
            column=0,
            padx=24,
            pady=(14, 14),
            sticky="w"
        )

        self.settings_card.grid_rowconfigure(2, weight=1)

        open_settings_button = ctk.CTkButton(
            self.settings_card,
            text="Abrir configuración",
            height=44,
            font=("Segoe UI", 15, "bold"),
            fg_color=ACCENT_GOLD,
            hover_color="#E09B32",
            text_color="#1A1A22",
            command=self.open_settings
        )

        open_settings_button.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="ew"
        )

    def open_settings(self):

        SettingsWindow(self, self.config, self.controller)

    # ------------------------------------------------------------------
    # Tarjeta de último comentario
    # ------------------------------------------------------------------

    def create_comment_card(self):

        self.comment_card = Card(self, "💬  Último comentario", accent=ACCENT_GREEN)

        self.comment_card.grid(
            row=2,
            column=1,
            padx=(10, 0),
            pady=10,
            sticky="nsew"
        )

        self.comment_card.grid_columnconfigure(0, weight=1)
        self.comment_card.grid_rowconfigure(4, weight=1)

        user_title = ctk.CTkLabel(
            self.comment_card,
            text="👤 Usuario",
            font=("Segoe UI", 13, "bold"),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        user_title.grid(
            row=1,
            column=0,
            padx=24,
            pady=(10, 4),
            sticky="w"
        )

        self.last_user_label = ctk.CTkLabel(
            self.comment_card,
            text="-",
            font=("Segoe UI", 15, "bold"),
            anchor="w"
        )

        self.last_user_label.grid(
            row=2,
            column=0,
            padx=24,
            sticky="w"
        )

        comment_title = ctk.CTkLabel(
            self.comment_card,
            text="💬 Comentario",
            font=("Segoe UI", 13, "bold"),
            text_color=("gray30", "gray70"),
            anchor="w"
        )

        comment_title.grid(
            row=3,
            column=0,
            padx=24,
            pady=(18, 4),
            sticky="w"
        )

        self.last_comment_label = ctk.CTkTextbox(
            self.comment_card,
            font=("Segoe UI", 14),
            wrap="word"
        )

        self.last_comment_label.grid(
            row=4,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew"
        )

        self.last_comment_label.insert("1.0", "-")
        self.last_comment_label.configure(state="disabled")
