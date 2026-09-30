from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QScrollArea
)


class TranscriptBlock(QWidget):
    word_selected = Signal(str, str)

    def __init__(self, text):
        super().__init__()

        self.text = text

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)

        self.browser = QTextBrowser()
        self.browser.setOpenLinks(False)
        self.browser.setOpenExternalLinks(False)
        self.browser.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.browser.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.browser.anchorClicked.connect(self.select_word)

        layout.addWidget(self.browser)

        self.words = text.split()
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.add_word)

        self.timer.start(45)

    def add_word(self):
        if self.index >= len(self.words):
            self.timer.stop()
            return

        word = self.words[self.index]

        clean_word = word.strip(".,!?;:()[]{}\"'")

        html = self.browser.toHtml()

        if not html or "qt-" not in html:
            html = ""

        if not hasattr(self, "html_started"):
            self.html_started = True
            html = """
            <html>
            <head>
            <style>
            body {
                font-family: "Segoe UI";
                font-size: 23px;
                color: #e8edf3;
            }

            a {
                color: #e8edf3;
                text-decoration: none;
            }

            a:hover {
                color: #8ab4ff;
            }
            </style>
            </head>
            <body>
            """

        if self.index > 0:
            html += " "

        html += f'<a href="{clean_word}">{word}</a>'

        self.browser.setHtml(html)

        self.index += 1

        scrollbar = self.browser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def select_word(self, url):
        word = url.toString()

        self.word_selected.emit(word, self.text)


class TranscriptWidget(QWidget):
    word_selected = Signal(str, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("transcriptScroll")

        self.container = QWidget()

        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(4, 4, 12, 4)
        self.content_layout.setSpacing(14)
        self.content_layout.addStretch()

        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)

    def add_text(self, text):
        block = TranscriptBlock(text)

        block.word_selected.connect(
            self.word_selected.emit
        )

        self.content_layout.insertWidget(
            self.content_layout.count() - 1,
            block
        )

        QTimer.singleShot(
            100,
            self.scroll_to_bottom
        )

    def scroll_to_bottom(self):
        scrollbar = self.scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())