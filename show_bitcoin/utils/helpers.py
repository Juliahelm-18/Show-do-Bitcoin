import html
# Utilizado para converter entidades HTML em texto legível

import random
# Utilizado para embaralhar as alternativas

from urllib.parse import unquote
# Utilizado para decodificar textos que vêm codificados na URL


def limpar_texto(texto):
    """
    Remove codificações HTML e URL de um texto,
    garantindo que perguntas e respostas fiquem legíveis.
    """
    return html.unescape(unquote(texto))


def embaralhar_alternativas(pergunta):
    """
    Embaralha as alternativas de uma pergunta e retorna
    a lista embaralhada e o índice da resposta correta.
    """
    # Trata o texto da alternativa correta
    correta = limpar_texto(pergunta["correct_answer"])

    # Trata o texto das alternativas incorretas
    incorretas = [
        limpar_texto(a) for a in pergunta["incorrect_answers"]
    ]

    # Junta todas as alternativas
    alternativas = incorretas + [correta]

    # Embaralha a ordem das alternativas
    random.shuffle(alternativas)

    # Retorna as alternativas e o índice da correta
    return alternativas, alternativas.index(correta)
