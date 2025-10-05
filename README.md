# ou Show do Milhão em Python

Um jogo de perguntas e respostas inspirado no **Show do Milhão**, desenvolvido em **Python**!  
O jogador deve responder corretamente perguntas de múltipla escolha para acumular prêmios.  
As perguntas são obtidas de uma API online e também ficam disponíveis offline depois do carregamento inicial.

---

## Sobre o jogo

O jogo começa com perguntas fáceis e vai aumentando a dificuldade conforme o jogador avança.  
Cada pergunta possui um valor em **R$**, e o jogador pode:

- **Responder** a pergunta;
- **Pular** (até 3 vezes por partida);
- **Desistir** (levando metade do prêmio acumulado);
- **Errar** (levando apenas 10% do prêmio acumulado).

Ao final, se acertar todas as perguntas, o jogador acumula **R$ 1.000.000! 💰**

---

## Funcionalidades principais

- ✅ Conexão com API de perguntas e respostas (`https://tryvia.ptr.red`)
- ✅ Funciona **offline** após baixar as perguntas
- ✅ Embaralhamento automático das alternativas
- ✅ Controle de pulos e desistência
- ✅ Sistema de pontuação e mensagens dinâmicas
- ✅ Mensagens coloridas e claras no terminal
- ✅ Tratamento de erros de conexão e repetição de perguntas

---

## Requisitos

- **Python 3.8+**
- Biblioteca **requests** instalada

Para instalar a dependência:

```bash
pip install requests
