class AIService:

    def explain(self, text, context=""):
        return (
            f"**{text}**\n\n"
            "Este conceito está relacionado ao conteúdo apresentado "
            "na aula. Quando a API de inteligência artificial estiver "
            "conectada, o Autex poderá gerar uma explicação adaptada "
            "ao contexto da aula."
        )

    def search(self, text):
        return (
            f"### Pesquisa\n\n"
            f"Você selecionou **{text}**.\n\n"
            "Aqui serão exibidas informações e definições relevantes "
            "sobre esse termo."
        )

    def context(self, text, lesson_context):
        return (
            f"### Contexto da aula\n\n"
            f"O termo **{text}** apareceu durante a explicação.\n\n"
            f"> {lesson_context}\n\n"
            "A IA poderá relacionar esse conceito com os conteúdos "
            "explicados anteriormente pelo professor."
        )

    def ask(self, question, context):
        return (
            "### Resposta\n\n"
            f"**Pergunta:** {question}\n\n"
            "A resposta será gerada pela IA utilizando os trechos "
            "relevantes da aula como contexto."
        )