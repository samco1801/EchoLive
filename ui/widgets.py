import customtkinter as ctk


class Card(ctk.CTkFrame):
    """Tarjeta base con título e icono de color opcional. El color de acento
    tiñe el título y el borde de la tarjeta, para diferenciar cada sección
    de un vistazo (conexión, estadísticas, configuración, comentarios)."""

    def __init__(self, master, title, accent=None):

        super().__init__(
            master,
            corner_radius=18,
            border_width=2,
            border_color=accent if accent else ("gray70", "#2E2E3A")
        )

        self.accent = accent

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(99, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(18, 6), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        if accent:
            dot = ctk.CTkFrame(
                header,
                width=10,
                height=10,
                corner_radius=5,
                fg_color=accent
            )
            dot.grid(row=0, column=0, padx=(0, 10))

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 20, "bold"),
            text_color=accent if accent else None,
            anchor="w"
        )

        title_label.grid(row=0, column=1, sticky="w")