import requests
# Utilizado para acessar a API
import html
# Utilizado para transformar o texto codificado em texto legível
import random
# Utilizado para embaralhar as alternativas das perguntas
from urllib.parse import unquote
# Utilizado para garantir que perguntas ou alternativas que vem codificadas da url fiquem legíveis

PULOS_MAX = 3
MAX_REPETIDAS = 10
# São váriaveis constantes

pulos_restantes = PULOS_MAX
premio_total = 0.0
perguntas_vistas = set()
# perguntas_vistas é utilizado para não repetir perguntas
# Variáveis utilizadas no jogo

perguntas_baixadas = {
    'easy': [],
    'medium': [],
    'hard': []
}
# perguntas_baixadas é uma variável que serve para que o jogo funcione sem internet, ou seja, as perguntas serão baixadas quando o jogo iniciar.

def obter_token():
    try:
        resposta = requests.get('https://tryvia.ptr.red/api_token.php?command=request')
        if resposta.status_code == 200:
            return resposta.json().get("token")
    except requests.RequestException:
        print(" Erro ao obter token da API.")
        return None
# Função que busca token na API para que o código consiga obter perguntas
# Caso a API seja bem sucedida, ou seja, o status for igual a 200 ela extrai o token, caso der erro, o código fala para o jogador que ocorreu um erro

def obter_perguntas(token, dificuldade, quantidade):
    perguntas = []
    while len(perguntas) < quantidade:
        try:
            resposta = requests.get(
                'https://tryvia.ptr.red/api.php',
                params={
                    'amount': quantidade - len(perguntas),
                    'type': 'multiple',
                    'difficulty': dificuldade,
                    'token': token
                }
            )
            dados = resposta.json()
            perguntas.extend(dados.get("results", []))
        except requests.RequestException:
            print(" Erro ao buscar perguntas.")
            break

    return perguntas
# Função para que o jogo funcione online
# A função pega a resposta da API (results) e transforma em perguntas para ser jogado
# Caso ocorra algum problema na API ou na busca do código o jogo retorna isso para o jogador

def mostrar_regras():
    nome = input('Qual seu nome? ')
    print(f'\n Olá, {nome}! Vou lhe mostrar as regras do jogo Show do Bitcoin:\n'
          '\n - O jogo começará com perguntas fáceis e, conforme o jogador avança, a dificuldade aumentará.\n'
          '- Cada pergunta possui uma pontuação: quanto mais difícil a pergunta, mais pontos você poderá ganhar.\n'
          '- A pontuação de cada pergunta será exibida na tela.\n'
          '- Se precisar de ajuda, você pode pressionar a tecla "P" para pular a pergunta, mas atenção: você só pode pular até 3 perguntas por partida.\n'
          '- Se precisar de ajuda, pressione a tecla "D". Nesse caso, você receberá metade do prêmio acumulado e o jogo será encerrado.\n'
          '- Se errar a resposta, você receberá apenas 10% do valor acumulado.\n')
    print('---' * 10)
# É mostrado ao jogador todas as regras para que o jogo inicie

def embaralhar_alternativas(pergunta):
    correta = html.unescape(unquote(pergunta["correct_answer"]))
    incorretas = [html.unescape(unquote(alt)) for alt in pergunta["incorrect_answers"]]
    todas = incorretas + [correta]
    random.shuffle(todas)
    return todas, todas.index(correta)
# O jogo embaralha as alternativas para que caso o jogador queira jogar novamente as alternativas não apareçam no mesmo lugar

def exibir_pergunta(pergunta, valor):
    global pulos_restantes, premio_total
# Variáveis estão em global para serem acessadas e modificadas dentro da função

    enunciado = html.unescape(unquote(pergunta["question"]))
    if enunciado in perguntas_vistas:
        return 'repetida'
    # Para que não ocorra perguntas repetidas

    perguntas_vistas.add(enunciado)
    alternativas, correta_idx = embaralhar_alternativas(pergunta)

    print(f"\n Pergunta valendo {valor} BTC:")
    # Mostra o valor da pergunta igual ao Show do Milhão
    print(enunciado)
    for i, alt in enumerate(alternativas, 1):
        print(f"  {i}. {alt}")
        # Enumera as alternativas para que facilite a resposta
    print(f" Se você desistir agora, levará {round(premio_total * 0.5, 2)} BTC.")
    while True:
        resposta = input("Sua resposta (1-4, P=pular, D=desistir): ").lower()
        # O lower é utilizado para que não corra quebra de código caso o jogador digite maiúsculo

        if resposta == 'p':
            if pulos_restantes > 0:
                pulos_restantes -= 1
                print(f" Você pulou. Pulos restantes: {pulos_restantes}")
                return 'pular'
            # Caso o jogador ainda tenha pulos restantes, o jogo pula a pergunta e mostra quantos pulos ainda restam
            else:
                print(" Você não tem mais pulos.")
        elif resposta == 'd':
            print(f" Você desistiu e levou {round(premio_total * 0.5, 2)} BTC.")
            exit()
            # Caso o jogador desista é mostrado seu prêmio final e o jogo é encerrado
        elif resposta in ['1', '2', '3', '4']:
            if int(resposta) - 1 == correta_idx:
                premio_total += valor
                print(" Resposta correta!")
                print(f" Prêmio acumulado: {round(premio_total, 2)} BTC")
                return 'correta'
            # Caso o jogador acerte a resposta é mostrado seu prêmio atual
            # É diminuido 1 da resposta, pois a contagem inicia no 0
            else:
                print(" Resposta errada!")
                print(f" Você leva apenas {round(premio_total * 0.1, 2)} BTC.")
                exit()
                # Caso o jogador erre a resposta é mostrado seu prêmio final conforme as regras
        else:
            print("Entrada inválida. Tente novamente.")
            # Caso não esteja em respostas válidas o jogo pede para que o jogador coloque uma resposta válida, evitando quebras de código

def jogar_rodada(quantidade, dificuldade, premiacoes):
    i = 0
    tentativas_repetidas = 0

    perguntas_disponiveis = perguntas_baixadas[dificuldade].copy()
    # O copy serve para copiar a lista e não modificar

    while i < quantidade:
        # Enquando não é respondido a quantidade de perguntas, o while continua
        pergunta = perguntas_disponiveis.pop(0)
        # Pega a primeira pergunta disponível da lista e depois a remove, evitando perguntas repetidas
        enunciado = html.unescape(unquote(pergunta["question"]))
        if enunciado in perguntas_vistas:
            # Verifica se a pergunta é repetida
            tentativas_repetidas += 1
            if tentativas_repetidas >= MAX_REPETIDAS:
                print(" Muitas perguntas repetidas. Encerrando o jogo.")
                print(f" Você ficou com {round(premio_total, 2)} BTC.")
                exit()
                # Caso haja muitas perguntas repetidas, o jogo entende e encerra
            continue
            # Pula o restante do código dentro do loop e tenta uma nova pergunta que não seja repetida

        resultado = exibir_pergunta(pergunta, premiacoes[i])
        # Chama a função para que consiga obter perguntas

        if resultado == 'correta':
            i += 1
        # Contabiliza que uma pergunta foi respondida corretamente e irá para a próxima
        elif resultado == 'pular':
            continue
        # Continua para a próxima iteração do while sem adicionar na variável i

def carregar_perguntas_antes_do_jogo(token):
    fases = [
        ('easy', 3),
        ('medium', 3),
        ('hard', 4)
    ]

    for dificuldade, quantidade in fases:
        total_para_baixar = quantidade + 10 
        # Margem para evitar repetições
        perguntas = obter_perguntas(token, dificuldade, total_para_baixar)
        if not perguntas:
            print(f" Não foi possível obter perguntas {dificuldade}.")
            exit()
        # Caso o jogo não consiga obter as perguntas, é avisado ao jogador e o jogo será encerrado
        perguntas_baixadas[dificuldade] = perguntas
        # Atribui a lista de perguntas à chave correspondente no dicionário
    print(" Perguntas carregadas com sucesso. Jogo funcionando offline!\n")
    # Avisa o jogador que o jogo está funcionando offline

def jogar():
    global premio_total, pulos_restantes
    # Váriavies globais para que o código consiga modificar
    mostrar_regras()
    # Mostra as regras para iniciar o jogo

    token = obter_token()
    # Obtém o token para que o jogo funcione

    carregar_perguntas_antes_do_jogo(token)
    # Chama a função para que funcione offline

    fases = [
        (" Perguntas fáceis", 'easy', [0.1, 0.2, 0.3]),
        (" Perguntas médias", 'medium', [0.4, 0.5, 0.6]),
        (" Perguntas difíceis", 'hard', [0.7, 0.8, 0.9, 1.0])
    ]
    # Lista para que as perguntas apareçam na ordem correta

    for titulo, dificuldade, premiacoes in fases:
        print(f"\n Iniciando {titulo}...")
        jogar_rodada(len(premiacoes), dificuldade, premiacoes)
        # Percorre cada fase do jogo chamando a função jogar_rodada

    print(f"\n Parabéns! Você completou o jogo com {round(premio_total, 2)} BTC.")


if __name__ == "__main__":
    jogar()
# Código para que as funções sejam utilizadas e o jogo funcione
