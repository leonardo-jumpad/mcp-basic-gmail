from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()  # Carrega variáveis de ambiente, como OPENAI_API_KEY

# Define o schema (formato do estado)
class Estado(TypedDict):
    mensagem: str

# Modelo LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Função de transição
def responder_mensagem(state: Estado) -> Estado:
    mensagem = state["mensagem"]
    resposta = llm.invoke(f"Responda de forma educada: {mensagem}")
    return {"mensagem": resposta.content}

# Criar grafo com schema
builder = StateGraph(Estado)

# Adiciona o nó de resposta
builder.add_node("responder", responder_mensagem)

# Define entrada e fim
builder.set_entry_point("responder")
builder.set_finish_point("responder")

# Compila o grafo
graph = builder.compile()

# Executa com entrada inicial
estado_inicial = {"mensagem": "quero saber sobre langgraph"}
resultado = graph.invoke(estado_inicial)

print("Resposta do fluxo:")
print(resultado["mensagem"])
