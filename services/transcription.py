from PySide6.QtCore import QObject, Signal


class TranscriptService(QObject):
    text_received = Signal(str)
    status_changed = Signal(str)

    def receive_text(self, text):
        if not text:
            return

        self.text_received.emit(text)
        self.status_changed.emit("Transcrevendo")

    def stop(self):
        self.status_changed.emit("Pausado")

    def start(self):
        self.status_changed.emit("Transcrevendo")