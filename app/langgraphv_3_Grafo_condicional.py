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
