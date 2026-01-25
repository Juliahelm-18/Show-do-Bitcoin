from api.trivia_api import obter_token, obter_perguntas
# Importa as funções responsáveis por se comunicar com a API de perguntas

from game.rules import mostrar_regras
# Importa a função que exibe as regras do jogo ao jogador

from game.rounds import jogar_rodada
# Importa a função responsável por executar cada rodada do jogo

from config import perguntas_baixadas
# Importa o dicionário que armazena as perguntas baixadas por dificuldade


def carregar_perguntas(token):
    """
    Carrega as perguntas da API antes do jogo iniciar.
    Isso permite que o jogo funcione offline após o carregamento.
    """
    fases = [
        ("easy", 3),
        ("medium", 3),
        ("hard", 4)
    ]
    # Define a quantidade de perguntas por dificuldade

    for dificuldade, qtd in fases:
        # Baixa mais perguntas do que o necessário para evitar repetições
        perguntas_baixadas[dificuldade] = obter_perguntas(
            token,
            dificuldade,
            qtd + 10
        )


def jogar():
    """
    Função principal do jogo.
    Controla o fluxo geral: regras, carregamento e execução das fases.
    """
    # Exibe as regras do jogo
    mostrar_regras()

    # Obtém o token da API
    token = obter_token()

    # Carrega as perguntas antes de iniciar o jogo
    carregar_perguntas(token)

    fases = [
        ("easy", [0.1, 0.1, 0.1]),
        ("medium", [0.1, 0.1, 0.1]),
        ("hard", [0.1, 0.1, 0.1, 0.1])
    ]
    # Define as fases do jogo e a premiação de cada pergunta

    for dificuldade, premiacoes in fases:
        # Executa cada rodada do jogo de acordo com a dificuldade
        jogar_rodada(
            perguntas_baixadas[dificuldade],
            premiacoes
        )
