from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit
)


class AssistantPanel(QWidget):
    action_requested = Signal(str, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("✦ Assistente Autex")
        title.setObjectName("assistantTitle")

        subtitle = QLabel(
            "Selecione uma palavra ou faça uma pergunta sobre a aula."
        )
        subtitle.setObjectName("assistantSubtitle")
        subtitle.setWordWrap(True)

        self.selected_word = QLabel(
            "Nenhum termo selecionado"
        )
        self.selected_word.setObjectName("selectedWord")
        self.selected_word.setWordWrap(True)

        self.explain_button = QPushButton(
            "✦  Explicar conceito"
        )

        self.search_button = QPushButton(
            "⌕  Pesquisar significado"
        )

        self.context_button = QPushButton(
            "◉  Relacionar com a aula"
        )

        self.answer = QTextEdit()
        self.answer.setReadOnly(True)
        self.answer.setPlaceholderText(
            "A resposta da IA aparecerá aqui..."
        )

        self.question = QLineEdit()
        self.question.setPlaceholderText(
            "Pergunte algo sobre a aula..."
        )

        self.ask_button = QPushButton(
            "Enviar pergunta"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.selected_word)

        layout.addSpacing(8)

        layout.addWidget(self.explain_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.context_button)

        layout.addWidget(self.answer, 1)

        layout.addWidget(self.question)
        layout.addWidget(self.ask_button)

        self.explain_button.clicked.connect(
            lambda: self.request_action("explain")
        )

        self.search_button.clicked.connect(
            lambda: self.request_action("search")
        )

        self.context_button.clicked.connect(
            lambda: self.request_action("context")
        )

        self.ask_button.clicked.connect(
            lambda: self.request_action("ask")
        )

        self.question.returnPressed.connect(
            lambda: self.request_action("ask")
        )

    def set_selected_word(self, word):
        self.selected_word.setText(
            f"Termo selecionado\n\n{word}"
        )

    def set_answer(self, text):
        self.answer.setMarkdown(text)

    def request_action(self, action):
        word = self.selected_word.text()

        question = self.question.text()

        if action == "ask":
            self.action_requested.emit(
                action,
                question
            )
            return

        if word == "Nenhum termo selecionado":
            return

        self.action_requested.emit(
            action,
            word
        )