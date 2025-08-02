### 🧠 O que é o `langgraph`?

O `langgraph` é usado para **definir fluxos de execução (graphs)** com **nós (nodes)** que representam ações/funções. Ele é útil para construir **MCPs (multi-component pipelines)** que tomam decisões, respondem, ou passam por etapas definidas.

---

### 🧪 Exemplo básico: Fluxo com duas etapas

Vamos simular um mini-assistente que:

1. **Recebe uma pergunta**.
2. **Decide se é uma saudação ou uma pergunta real**.
3. **Responde adequadamente**.

---

### ✅ Código completo (explicado)

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Função 1: classifica o tipo de mensagem
def classificar(state):
    mensagem = state["mensagem"]
    if "oi" in mensagem.lower():
        return {"tipo": "saudacao", "mensagem": mensagem}
    else:
        return {"tipo": "pergunta", "mensagem": mensagem}

# Função 2: responde a saudações
def responder_saudacao(state):
    return {"mensagem": "Olá! Em que posso te ajudar hoje?"}

# Função 3: responde perguntas gerais usando o LLM
def responder_pergunta(state):
    mensagem = state["mensagem"]
    resposta = llm.invoke(f"Responda educadamente: {mensagem}")
    return {"mensagem": resposta.content}

# Montar o grafo
builder = StateGraph(dict)  # schema é um dicionário simples

builder.add_node("classificar", classificar)
builder.add_node("saudacao", responder_saudacao)
builder.add_node("resposta", responder_pergunta)

# Condição para decidir o próximo passo
builder.add_conditional_edges(
    "classificar",
    lambda state: state["tipo"],
    {
        "saudacao": "saudacao",
        "pergunta": "resposta"
    }
)

# Fins do fluxo
builder.set_entry_point("classificar")
builder.set_finish_point("saudacao")
builder.set_finish_point("resposta")

graph = builder.compile()

# Testar com duas mensagens diferentes
entrada1 = {"mensagem": "Oi, tudo bem?"}
entrada2 = {"mensagem": "O que é LangGraph?"}

print("Teste 1:", graph.invoke(entrada1)["mensagem"])
print("Teste 2:", graph.invoke(entrada2)["mensagem"])
```

---

### 🧩 Explicando a estrutura:

| Parte                   | O que faz                                      |
| ----------------------- | ---------------------------------------------- |
| `classificar`           | Decide se a entrada é "saudação" ou "pergunta" |
| `responder_saudacao`    | Dá uma resposta fixa                           |
| `responder_pergunta`    | Usa o modelo LLM para gerar uma resposta       |
| `add_conditional_edges` | Direciona o fluxo com base no tipo detectado   |

---

### 🧠 Quer saber mais?

Se quiser evoluir, você pode depois:

-   Adicionar memória (estado acumulado).
-   Criar fluxos com loops.
-   Integrar com APIs externas.

Se quiser, posso montar um exemplo que conversa com Gmail ou banco de dados usando o mesmo `langgraph`.

Quer isso?
