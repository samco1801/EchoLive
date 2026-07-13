class Stats:

    def __init__(self):

        self.received = 0
        self.read = 0
        self.filtered = 0

        self.last_user = ""
        self.last_comment = ""

        self.on_update = None

    def refresh(self):

        if self.on_update:
            self.on_update()

    def comment_received(self):

        self.received += 1
        self.refresh()

    def comment_read(self, user, comment):

        self.read += 1
        self.last_user = user
        self.last_comment = comment

        self.refresh()

    def comment_filtered(self):

        self.filtered += 1
        self.refresh()