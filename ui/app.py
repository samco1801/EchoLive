import os

import customtkinter as ctk

from ui.home import HomeFrame

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


class EchoLiveApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")

        theme_path = os.path.join(ASSETS_DIR, "theme.json")
        if os.path.exists(theme_path):
            ctk.set_default_color_theme(theme_path)
        else:
            ctk.set_default_color_theme("blue")

        self.title("EchoLive")
        self.geometry("1220x820")
        self.minsize(1080, 720)

        icon_path = os.path.join(ASSETS_DIR, "icon.ico")
        if os.path.exists(icon_path) and os.name == "nt":
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.home = HomeFrame(self)
        self.home.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Se ejecuta al cerrar la ventana (X, Alt+F4, etc). Si hay una
        conexión activa al live, la cierra correctamente antes de destruir
        la ventana, para evitar hilos colgando en segundo plano."""

        try:
            if self.home.controller:
                self.home.controller.shutdown()
        except Exception:
            pass

        self.destroy()
