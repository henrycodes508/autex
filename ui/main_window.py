from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from ui.components.transcript import TranscriptWidget
from ui.components.assistant_panel import AssistantPanel
from services.ai import AIService
from services.transcription import TranscriptService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Autex")
        self.resize(1280, 800)

        self.ai = AIService()
        self.transcription = TranscriptService()

        self.setup_ui()
        self.connect_signals()
        self.load_demo()

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("header")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(
            28, 18, 28, 18
        )

        logo = QLabel("AUTEX")
        logo.setObjectName("logo")

        lesson = QLabel("Cálculo I")
        lesson.setObjectName("headerLesson")

        live = QLabel("● AO VIVO")
        live.setObjectName("liveStatus")

        header_layout.addWidget(logo)
        header_layout.addSpacing(20)
        header_layout.addWidget(lesson)

        header_layout.addStretch()

        header_layout.addWidget(live)

        main_layout.addWidget(header)

        content = QWidget()

        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(
            24, 22, 24, 18
        )
        content_layout.setSpacing(20)

        transcript_area = QWidget()

        transcript_layout = QVBoxLayout(
            transcript_area
        )

        transcript_layout.setContentsMargins(
            0, 0, 0, 0
        )

        title = QLabel(
            "Transcrição da aula"
        )
        title.setObjectName("lessonTitle")

        subtitle = QLabel(
            "Toque em qualquer palavra para explorar o conteúdo."
        )
        subtitle.setObjectName("lessonSubtitle")

        self.transcript = TranscriptWidget()

        transcript_layout.addWidget(title)
        transcript_layout.addWidget(subtitle)
        transcript_layout.addSpacing(14)
        transcript_layout.addWidget(
            self.transcript,
            1
        )

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(
            QFrame.Shape.VLine
        )
        separator.setFrameShadow(
            QFrame.Shadow.Plain
        )

        self.assistant = AssistantPanel()

        content_layout.addWidget(
            transcript_area,
            7
        )

        content_layout.addWidget(
            separator
        )

        content_layout.addWidget(
            self.assistant,
            3
        )

        main_layout.addWidget(
            content,
            1
        )

        footer = QFrame()
        footer.setObjectName("footer")

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(
            24, 10, 24, 10
        )

        status = QLabel(
            "●  Transcrição ativa"
        )
        status.setObjectName("footerStatus")

        language = QLabel(
            "Português (Brasil)"
        )
        language.setObjectName("footerLanguage")

        footer_layout.addWidget(status)

        footer_layout.addStretch()

        footer_layout.addWidget(language)

        main_layout.addWidget(footer)

    def connect_signals(self):

        self.transcription.text_received.connect(
            self.transcript.add_text
        )

        self.transcript.word_selected.connect(
            self.handle_word_selection
        )

        self.assistant.action_requested.connect(
            self.handle_ai_action
        )

    def handle_word_selection(
        self,
        word,
        context
    ):
        self.assistant.set_selected_word(word)

        self.selected_context = context

    def handle_ai_action(
        self,
        action,
        value
    ):

        context = getattr(
            self,
            "selected_context",
            ""
        )

        if action == "explain":
            result = self.ai.explain(
                value,
                context
            )

        elif action == "search":
            result = self.ai.search(
                value
            )

        elif action == "context":
            result = self.ai.context(
                value,
                context
            )

        elif action == "ask":
            result = self.ai.ask(
                value,
                context
            )

        else:
            return

        self.assistant.set_answer(result)

    def load_demo(self):

        texts = [
            "Hoje vamos estudar derivadas.",
            "A derivada representa a taxa de variação de uma função.",
            "Vamos começar observando um exemplo simples.",
            "Considere a função f de x igual a x ao quadrado.",
            "A derivada dessa função é igual a dois x.",
            "Agora vamos entender por que isso acontece."
        ]

        for text in texts:
            self.transcription.receive_text(text)