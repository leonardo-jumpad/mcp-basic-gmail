# 🚀 Parte 1 – Tutorial básico **sem LangGraph**

Aqui você usa LangChain para chamar o modelo de linguagem direto, fazer perguntas e receber respostas simples.

### Código básico:

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

pergunta = "O que é LangChain?"

resposta = llm.invoke(pergunta)

print(resposta.content)
```

### O que está acontecendo?

-   Você cria um objeto `llm` com o modelo da OpenAI.
-   Usa `llm.invoke()` para mandar o prompt.
-   Recebe a resposta com `resposta.content`.
-   É uma chamada simples, direta, sem fluxo, memória ou ferramentas.

---

### LangGraph e LangGraph?

-   **Sem LangGraph:** você chama o LLM direto, resposta simples e sem fluxo.
-   **Com LangGraph:** você monta um grafo com estados, múltiplos nós e decisões — para agentes mais inteligentes.
-   Pode adicionar ferramentas e lógica condicional

# 🚀 Parte 2 – Exemplos com LangGraph

---

## Exemplo 1: Fluxo simples com um nó que responde

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict

class Estado(TypedDict):
    mensagem: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def responder(state: Estado) -> Estado:
    msg = state["mensagem"]
    resp = llm.invoke(f"Responda educadamente: {msg}")
    return {"mensagem": resp.content}

builder = StateGraph(Estado)
builder.add_node("responder", responder)
builder.set_entry_point("responder")
builder.set_finish_point("responder")

grafo = builder.compile()

entrada = {"mensagem": "O que é LangGraph?"}
saida = grafo.invoke(entrada)

print(saida["mensagem"])
```

**Explicação:**
Você cria um grafo com um nó, ele recebe um estado com a mensagem e responde. Fácil para entender a estrutura do grafo.

---

## Exemplo 2: Fluxo condicional simples

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict

class Estado(TypedDict):
    mensagem: str
    tipo: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def classificar(state: Estado) -> Estado:
    msg = state["mensagem"].lower()
    if "oi" in msg or "olá" in msg:
        return {"mensagem": state["mensagem"], "tipo": "saudacao"}
    else:
        return {"mensagem": state["mensagem"], "tipo": "pergunta"}

def responder_saudacao(state: Estado) -> Estado:
    return {"mensagem": "Olá! Como posso ajudar?" , "tipo": "fim"}

def responder_pergunta(state: Estado) -> Estado:
    resp = llm.invoke(f"Responda: {state['mensagem']}")
    return {"mensagem": resp.content, "tipo": "fim"}

builder = StateGraph(Estado)
builder.add_node("classificar", classificar)
builder.add_node("saudacao", responder_saudacao)
builder.add_node("resposta", responder_pergunta)

builder.add_conditional_edges(
    "classificar",
    lambda s: s["tipo"],
    {"saudacao": "saudacao", "pergunta": "resposta"},
)

builder.set_entry_point("classificar")
builder.set_finish_point("saudacao")
builder.set_finish_point("resposta")

grafo = builder.compile()

print(grafo.invoke({"mensagem": "Oi, tudo bem?", "tipo": ""})["mensagem"])
print(grafo.invoke({"mensagem": "O que é LangGraph?", "tipo": ""})["mensagem"])
```

**Explicação:**
Aqui o grafo decide para onde ir dependendo da mensagem: se for saudação, responde com texto fixo; se for pergunta, chama o LLM.

---

## Exemplo 3: Fluxo com ferramenta simples (dobrar número)

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.tools import tool
from typing import TypedDict

class Estado(TypedDict):
    mensagem: str
    numero: float

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

@tool
def dobrar_numero(numero: float) -> str:
    return f"O dobro de {numero} é {numero * 2}"

def responder(state: Estado) -> Estado:
    if "dobrar" in state["mensagem"]:
        resultado = dobrar_numero(state["numero"])
        return {"mensagem": resultado, "numero": state["numero"]}
    else:
        resp = llm.invoke(f"Responda: {state['mensagem']}")
        return {"mensagem": resp.content, "numero": state["numero"]}

builder = StateGraph(Estado)
builder.add_node("responder", responder)
builder.set_entry_point("responder")
builder.set_finish_point("responder")

grafo = builder.compile()

entrada = {"mensagem": "Por favor, dobre o número", "numero": 5}
saida = grafo.invoke(entrada)

print(saida["mensagem"])
```

**Explicação:**
Aqui o agente usa uma ferramenta para dobrar número, se a mensagem pedir. Caso contrário, usa o LLM.

---

---
