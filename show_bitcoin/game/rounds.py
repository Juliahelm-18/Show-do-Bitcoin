from utils.helpers import limpar_texto, embaralhar_alternativas
# Importa funções auxiliares:
# - limpar_texto: trata textos vindos da API (HTML/URL encoding)
# - embaralhar_alternativas: mistura as alternativas e identifica a correta

from config import (
    perguntas_vistas,
    pulos_restantes,
    premio_total,
    MAX_REPETIDAS
)
# Importa variáveis globais de configuração e controle do jogo


def exibir_pergunta(pergunta, valor):
    """
    Exibe uma pergunta ao jogador, controla as opções de resposta
    e retorna o resultado da interação.
    """
    global pulos_restantes, premio_total
    # Permite modificar variáveis globais dentro da função

    # Limpa o enunciado da pergunta para garantir legibilidade
    enunciado = limpar_texto(pergunta["question"])

    # Verifica se a pergunta já foi exibida anteriormente
    if enunciado in perguntas_vistas:
        return "repetida"

    # Marca a pergunta como já utilizada
    perguntas_vistas.add(enunciado)

    # Embaralha as alternativas e obtém o índice da resposta correta
    alternativas, correta_idx = embaralhar_alternativas(pergunta)

    # Exibe a pergunta e sua pontuação
    print(f"\nPergunta valendo {valor} BTC:")
    print(enunciado)

    # Mostra as alternativas numeradas
    for i, alt in enumerate(alternativas, 1):
        print(f"{i}. {alt}")

    while True:
        # Solicita a resposta do jogador
        resposta = input("Resposta (1-4, P=pular, D=desistir): ").lower()

        # Opção de pular a pergunta
        if resposta == "p":
            if pulos_restantes > 0:
                pulos_restantes -= 1
                print(f"Pulos restantes: {pulos_restantes}")
                return "pular"
            print("Sem pulos restantes.")

        # Opção de desistência
        elif resposta == "d":
            print(f"Você levou {round(premio_total * 0.5, 2)} BTC.")
            exit()

        # Opções de resposta válidas
        elif resposta in ["1", "2", "3", "4"]:
            # Verifica se a resposta está correta
            if int(resposta) - 1 == correta_idx:
                premio_total += valor
                print(f"Resposta correta! Você tem por enquanto {round(premio_total, 2)} BTC.")
                return "correta"
            else:
                print("Resposta errada!")
                print(f"Você levou {round(premio_total * 0.1, 2)} BTC.")
                exit()


def jogar_rodada(perguntas, premiacoes):
    """
    Controla uma rodada do jogo para uma determinada dificuldade.
    """
    i = 0
    repetidas = 0
    # Contadores de progresso e controle de repetição

    while i < len(premiacoes):
        # Remove a próxima pergunta disponível
        pergunta = perguntas.pop(0)

        # Exibe a pergunta e obtém o resultado
        resultado = exibir_pergunta(pergunta, premiacoes[i])

        # Avança se a resposta estiver correta
        if resultado == "correta":
            i += 1

        # Controla perguntas repetidas
        elif resultado == "repetida":
            repetidas += 1
            if repetidas >= MAX_REPETIDAS:
                print("Muitas perguntas repetidas.")
                exit()
