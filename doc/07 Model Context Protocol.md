Claro! Vamos criar **um exemplo simples e fácil de entender** de como funcionaria o **Model Context Protocol (MCP)** na prática.

> 🧠 **Ideia principal**: um agente (uma IA ou LLM) recebe uma pergunta do usuário, percebe que precisa de uma calculadora externa (ferramenta), e a aciona via **MCP** para obter a resposta.

---

### ✅ Contexto do exemplo:

Você pergunta:
🗣️ _"Quanto é 20% de 150?"_

A LLM não calcula diretamente, mas envia essa pergunta para uma ferramenta chamada **CalculadoraDePorcentagem**, usando uma **mensagem no formato MCP**, e depois te dá a resposta.

---

### 📦 Estrutura simplificada do MCP (em Python simulado)

```python
# MCP SIMPLIFICADO - Exemplo didático

def calculadora_de_porcentagem(data):
    """Simula uma ferramenta externa chamada via MCP"""
    valor = data.get("valor")
    porcentagem = data.get("porcentagem")
    resultado = (porcentagem / 100) * valor
    return {
        "resultado": resultado,
        "detalhes": f"{porcentagem}% de {valor} é {resultado}"
    }

# ===== AGENTE COM SUPORTE A MCP =====

def agente_mcp(pergunta):
    """Agente que sabe quando invocar ferramentas externas via 'MCP'"""

    # Entendimento simples da pergunta
    if "porcento de" in pergunta:
        # Extração manual dos dados (simples para o exemplo)
        partes = pergunta.lower().replace("%", "").split(" de ")
        porcentagem = float(partes[0].split()[-1])
        valor = float(partes[1])

        # Comunicação via "MCP" - enviando contexto padronizado
        mensagem_mcp = {
            "tool": "CalculadoraDePorcentagem",
            "input": {
                "porcentagem": porcentagem,
                "valor": valor
            }
        }

        # Chamada simulada à ferramenta via protocolo
        resposta = calculadora_de_porcentagem(mensagem_mcp["input"])
        return resposta["detalhes"]

    else:
        return "Não entendi sua pergunta."

# ===== USO =====
resposta = agente_mcp("Quanto é 20% de 150?")
print("🤖 Resposta:", resposta)
```

---

### 🧪 Saída do código:

```
🤖 Resposta: 20.0% de 150.0 é 30.0
```

---

### 🧩 O que você aprendeu:

-   **O agente** entendeu o que você quer.
-   Ele formatou a informação no **estilo MCP** (com `"tool"` e `"input"`).
-   **Chamou uma ferramenta externa (calculadora)**.
-   **Recebeu o resultado** e entregou de volta ao usuário.

---

---

## ✅ O que é **MCP** (Model Context Protocol)

**MCP (Model Context Protocol)** é um protocolo open-source criado pela **Anthropic** para **padronizar como grandes modelos de linguagem (LLMs)** interagem com **ferramentas externas, APIs, bancos de dados e outros agentes**.

### ✨ Benefícios:

-   **Padroniza** a forma como modelos pedem ajuda de ferramentas.
-   **Facilita a colaboração entre agentes**, mesmo que sejam de empresas diferentes.
-   Permite que **LLMs executem ações no mundo real**, como buscar dados ou acionar APIs.

> 📦 MCP define a **estrutura da mensagem**: o que está sendo pedido, quem vai responder, e o que fazer com o resultado.

---

## 📘 Exemplo real: Quando usar MCP?

Você pergunta para um chatbot:

> 🧠 "Me diga se amanhã vai chover no Rio."

O modelo percebe que precisa chamar uma API de previsão do tempo.

-   Com MCP, ele **formata esse pedido de forma padronizada**, como:

```json
{
    "tool": "weather_api",
    "input": {
        "city": "Rio de Janeiro",
        "date": "2025-08-03"
    }
}
```

Depois, o resultado da ferramenta retorna com algo como:

```json
{
    "output": {
        "forecast": "Chuva leve"
    }
}
```

---

## 🚀 Tutorial: Codificando e executando um agente com suporte MCP (exemplo simples)

### ✅ Pré-requisitos:

-   Python instalado (versão 3.10+)
-   Ambiente virtual (opcional)
-   Editor de código (VS Code, por exemplo)

---

### 📂 Estrutura do projeto

```
projeto_mcp/
│
├── main.py                  ← Agente principal
├── tools/
│   └── weather.py           ← Ferramenta externa simulada (como uma API)
└── mcp/
    └── executor.py          ← Lógica do MCP (como executa a ferramenta)
```

---

### 📄 Arquivo `tools/weather.py`

```python
# Simula uma ferramenta externa que responde à previsão do tempo

def previsao_do_tempo(input_data):
    cidade = input_data.get("city")
    data = input_data.get("date")

    # Simula uma resposta
    return {
        "forecast": f"Chuva leve prevista para {cidade} no dia {data}."
    }
```

---

### 📄 Arquivo `mcp/executor.py`

```python
# Executor MCP - invoca ferramentas com base no protocolo

from tools.weather import previsao_do_tempo

def mcp_execute(message):
    tool = message.get("tool")
    input_data = message.get("input")

    if tool == "weather_api":
        return {
            "output": previsao_do_tempo(input_data)
        }
    else:
        return {"error": "Ferramenta não reconhecida"}
```

---

### 📄 Arquivo `main.py`

```python
from mcp.executor import mcp_execute

def agente(pergunta):
    if "vai chover" in pergunta:
        cidade = "Rio de Janeiro"
        data = "2025-08-03"

        mensagem_mcp = {
            "tool": "weather_api",
            "input": {
                "city": cidade,
                "date": data
            }
        }

        resposta = mcp_execute(mensagem_mcp)
        return resposta["output"]["forecast"]

    return "Não entendi sua pergunta."

# ==== EXECUTAR ====
print("🤖", agente("Vai chover amanhã no Rio?"))
```

---

### 🧪 Como rodar:

1. Crie as pastas e arquivos acima.
2. No terminal, vá até a pasta do projeto:

```bash
cd projeto_mcp
python3 main.py
```

---

### 📤 Saída esperada:

```
🤖 Chuva leve prevista para Rio de Janeiro no dia 2025-08-03.
```

---

## 💡 Explicando tudo de novo em resumo:

| Componente         | O que faz                                                                          |
| ------------------ | ---------------------------------------------------------------------------------- |
| `main.py`          | É o **agente** (LLM ou IA) que entende a pergunta e decide qual ferramenta chamar. |
| `mcp/executor.py`  | É o executor do protocolo MCP: **envia os dados para a ferramenta correta**.       |
| `tools/weather.py` | É a **ferramenta externa simulada**, como se fosse uma API de clima.               |

---

Próximo passo: expandir esse exemplo com chamadas reais a APIs, ou usando o LangChain para integrar com agentes inteligentes.

---

# Exemplo MCP simples local (sem API)

## Objetivo:

Um agente que recebe uma pergunta, identifica qual ferramenta chamar, monta a mensagem MCP, envia para o executor que chama a função interna, e devolve a resposta.

---

### 1. Ferramentas internas

```python
# tools.py

def dobrar_numero(input_data):
    numero = input_data.get("numero", 0)
    resultado = numero * 2
    return {"resultado": resultado}

def inverter_texto(input_data):
    texto = input_data.get("texto", "")
    invertido = texto[::-1]
    return {"resultado": invertido}
```

---

### 2. Executor MCP

```python
# mcp_executor.py
from tools import dobrar_numero, inverter_texto

def mcp_execute(message: dict) -> dict:
    tool = message.get("tool")
    input_data = message.get("input", {})

    if tool == "dobrar_numero":
        return {"output": dobrar_numero(input_data)}
    elif tool == "inverter_texto":
        return {"output": inverter_texto(input_data)}
    else:
        return {"error": "Ferramenta desconhecida."}
```

---

### 3. Agente que chama MCP

```python
# main.py
from mcp_executor import mcp_execute

def agente_mcp(pergunta: str):
    if "dobrar" in pergunta:
        # Exemplo: "Dobrar 5"
        try:
            numero = int(pergunta.split()[-1])
        except:
            return "Número inválido."

        mensagem = {
            "tool": "dobrar_numero",
            "input": {"numero": numero}
        }
        resposta = mcp_execute(mensagem)
        return f"O dobro de {numero} é {resposta['output']['resultado']}"

    elif "inverter" in pergunta:
        # Exemplo: "Inverter olá mundo"
        texto = pergunta.replace("inverter", "").strip()
        mensagem = {
            "tool": "inverter_texto",
            "input": {"texto": texto}
        }
        resposta = mcp_execute(mensagem)
        return f"O texto invertido é: '{resposta['output']['resultado']}'"

    else:
        return "Não entendi a pergunta."

if __name__ == "__main__":
    perguntas = [
        "Dobrar 10",
        "Inverter Olá Mundo",
        "Dobrar abc",
        "Outra pergunta"
    ]

    for p in perguntas:
        print(f"Pergunta: {p}")
        print("Resposta:", agente_mcp(p))
        print()
```

---

## Como rodar?

1. Salve os 3 arquivos (`tools.py`, `mcp_executor.py`, `main.py`) na mesma pasta.
2. Execute no terminal:

```bash
python3 main.py
```

---

## Saída esperada

```
Pergunta: Dobrar 10
Resposta: O dobro de 10 é 20

Pergunta: Inverter Olá Mundo
Resposta: O texto invertido é: 'odnuM álO'

Pergunta: Dobrar abc
Resposta: Número inválido.

Pergunta: Outra pergunta
Resposta: Não entendi a pergunta.
```

---

# Explicação simples

-   O agente identifica qual ferramenta chamar a partir da pergunta.
-   Cria a mensagem MCP (com nome da ferramenta e dados de entrada).
-   Passa para o executor MCP que sabe como chamar a função certa.
-   A função interna processa e retorna o resultado dentro do formato MCP.
-   O agente formata e responde ao usuário.

---
