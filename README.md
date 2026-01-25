# Show do Bitcoin

Um jogo de perguntas e respostas em **Python**, inspirado no *Show do Milhão*, onde o jogador responde perguntas de múltipla escolha e acumula prêmios em **Bitcoin (BTC)**.

O projeto consome uma **API externa de trivia**, funciona **offline após o carregamento das perguntas** e foi desenvolvido com foco em **boas práticas**, **organização em camadas** e **modularização de código**.

---

## Funcionalidades

- Consumo de API de perguntas (Trivia API)
- Funcionamento offline após o carregamento inicial
- Três níveis de dificuldade:
  - Fácil
  - Médio
  - Difícil
- Sistema de pontuação progressiva
- Opções durante o jogo:
  - Pular perguntas (quantidade limitada)
  - Desistir e levar parte do prêmio
- Tratamento de perguntas repetidas
- Embaralhamento de alternativas
- Validação de entradas do usuário

---


### Descrição das Pastas
- **api/** → Comunicação com a API externa
- **game/** → Lógica principal do jogo e rodadas
- **utils/** → Funções auxiliares reutilizáveis
- **config.py** → Variáveis globais e configurações do jogo
- **main.py** → Ponto de entrada do programa

---

## Como Executar o Projeto

### 1️. Pré-requisitos
- Python **3.10 ou superior**
- Acesso à internet (apenas no início do jogo)

### 2️. Clone o repositório
```bash
git clone https://github.com/Juliahelm-18/Show-do-Bitcoin.git
```

### 3. Acesse a pasta do projeto
```bash
cd show_bitcoin
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Execute o jogo
```bash
python main.py
```

--- 

## Regras do Jogo
- O jogo começa com perguntas fáceis e avança para níveis mais difíceis
- Cada pergunta possui um valor em BTC
- Você pode:
    - Pular até um número limitado de perguntas
    - Desistir e levar 50% do prêmio acumulado
    - Se errar uma pergunta, você leva apenas 10% do prêmio
- O jogo termina quando:
    - Todas as fases são concluídas
    - O jogador erra uma pergunta
    - O jogador decide desistir

---

## Conceitos Aplicados
- Consumo de API REST
- Modularização de código
- Funções e escopo
- Estruturas de repetição e condicionais
- Manipulação de strings
- Estruturas de dados (list, set, dict)
- Organização em camadas
- Boas práticas em Python

---

## Observações
- As perguntas são carregadas no início do jogo para permitir funcionamento offline
- O projeto é indicado para fins acadêmicos e portfólio
- Código totalmente comentado para facilitar entendimento