import threading

from core.live import LiveClient


class AppController:

    def __init__(self, home):

        self.home = home

        self.live = None
        self.live_thread = None

        # Evita que se disparen varios hilos/conexiones si el usuario
        # hace clic en "Conectar" mientras ya hay una conexión en curso.
        self.connecting = False

    def connect(self):

        if self.connecting:
            return

        username = self.home.username_entry.get().strip()

        if not username:
            return

        self.connecting = True

        self.home.status_label.configure(text="🟡 Conectando...")
        self.home.connect_button.configure(state="disabled")

        self.live = LiveClient(username)

        self.live.on_connected = self.live_connected
        self.live.on_disconnected = self.live_disconnected
        self.live.on_error = self.live_error
        self.live.on_stats = self.update_stats
        self.live.on_comment_callback = self.update_comment

        self.live_thread = threading.Thread(
            target=self.live.connect,
            daemon=True
        )

        self.live_thread.start()

    def live_connected(self):

        self.home.after(
            0,
            lambda: self.home.status_label.configure(
                text="🟢 Conectado"
            )
        )

    def live_disconnected(self):

        self.home.after(0, self._on_disconnected_ui)

    def _on_disconnected_ui(self):

        self.home.status_label.configure(text="⚪ Desconectado")
        self.home.connect_button.configure(state="normal")
        self.connecting = False

    def live_error(self, reason):

        self.home.after(0, lambda: self._on_error_ui(reason))

    def _on_error_ui(self, reason):

        if reason == "offline":
            self.home.status_label.configure(
                text="🔴 No está en directo ahora mismo"
            )
        else:
            self.home.status_label.configure(text="🔴 Error al conectar")

        self.home.connect_button.configure(state="normal")
        self.connecting = False

    def update_stats(self, stats, queue_size):

        self.home.after(
            0,
            lambda: self._update_stats_ui(stats, queue_size)
        )

    def _update_stats_ui(self, stats, queue_size):

        self.home.received_item.set(stats.received)
        self.home.read_item.set(stats.read)
        self.home.filtered_item.set(stats.filtered)
        self.home.queue_item.set(queue_size)

    def update_comment(self, user, comment):

        self.home.after(
            0,
            lambda: self._update_comment_ui(user, comment)
        )

    def _update_comment_ui(self, user, comment):

        self.home.last_user_label.configure(
            text=user
        )
        self.home.last_comment_label.configure(
            state="normal"
        )
        self.home.last_comment_label.delete(
            "1.0",
            "end"
        )
        self.home.last_comment_label.insert(
            "1.0",
            comment
        )
        self.home.last_comment_label.configure(
            state="disabled"
        )

    def shutdown(self):
        """Llamado al cerrar la ventana. Si hay una conexión activa, la
        cierra correctamente para que no queden hilos ni tareas de asyncio
        colgando cuando el programa termine."""

        if self.live:
            self.live.request_shutdown()
