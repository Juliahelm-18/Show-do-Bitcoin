import requests
# Biblioteca utilizada para fazer requisições HTTP
# É ela que permite o acesso à API de perguntas


def obter_token():
    """
    Solicita um token à API.
    O token é usado para evitar perguntas repetidas durante o jogo.
    """
    try:
        # Faz uma requisição GET para obter o token da API
        resposta = requests.get(
            "https://tryvia.ptr.red/api_token.php?command=request"
        )

        # Verifica se a requisição foi bem-sucedida (status 200)
        if resposta.status_code == 200:
            # Retorna o token presente no JSON da resposta
            return resposta.json().get("token")

    # Trata erros de conexão, timeout, etc.
    except requests.RequestException:
        print("Erro ao obter token da API.")

    # Caso ocorra algum erro, retorna None
    return None


def obter_perguntas(token, dificuldade, quantidade):
    """
    Busca perguntas na API de acordo com a dificuldade e quantidade desejada.

    Parâmetros:
    - token: token fornecido pela API
    - dificuldade: 'easy', 'medium' ou 'hard'
    - quantidade: número de perguntas a serem buscadas
    """
    perguntas = []
    # Lista onde as perguntas serão armazenadas

    # Continua buscando perguntas até atingir a quantidade desejada
    while len(perguntas) < quantidade:
        try:
            # Faz a requisição GET para a API de perguntas
            resposta = requests.get(
                "https://tryvia.ptr.red/api.php",
                params={
                    # Quantidade restante de perguntas a buscar
                    "amount": quantidade - len(perguntas),

                    # Tipo de pergunta: múltipla escolha
                    "type": "multiple",

                    # Define a dificuldade das perguntas
                    "difficulty": dificuldade,

                    # Token para evitar perguntas repetidas
                    "token": token
                }
            )

            # Adiciona as perguntas retornadas pela API à lista
            perguntas.extend(resposta.json().get("results", []))

        # Caso ocorra erro de conexão com a API
        except requests.RequestException:
            print("Erro ao buscar perguntas.")
            break

    # Retorna a lista de perguntas obtidas
    return perguntas
