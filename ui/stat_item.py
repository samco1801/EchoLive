import customtkinter as ctk


class StatItem(ctk.CTkFrame):
    """Una estadística individual: título pequeño arriba, valor grande abajo.
    Admite un color de acento para el valor y un ícono/emoji opcional."""

    def __init__(self, master, title, accent=None, icon=None):

        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        label_text = f"{icon}  {title}" if icon else title

        self.title = ctk.CTkLabel(
            self,
            text=label_text,
            anchor="w",
            font=("Segoe UI", 13),
            text_color=("gray30", "gray70")
        )

        self.title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.value = ctk.CTkLabel(
            self,
            text="0",
            font=("Segoe UI", 28, "bold"),
            text_color=accent if accent else None,
            anchor="w"
        )

        self.value.grid(
            row=1,
            column=0,
            sticky="w"
        )

    def set(self, value):

        self.value.configure(text=str(value))