import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# Modelo base
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# ---------- FERRAMENTAS (AGENTES FUNCIONAIS) ----------

def planejar_viagem(_):
    return "Destino: Lisboa, Datas: 10 a 17 de dezembro, Orçamento: R$5000"

def buscar_voos(_):
    return "Voo LATAM, ida e volta por R$3200"

def buscar_hotel(_):
    return "Hotel Solar do Castelo, 7 diárias por R$1700"

# Criar ferramentas como agentes
tools = [
    Tool(
        name="PlanejadorDeViagem",
        func=planejar_viagem,
        description="Cria um plano de viagem com destino, datas e orçamento"
    ),
    Tool(
        name="BuscaVoos",
        func=buscar_voos,
        description="Busca voos baseados no plano de viagem"
    ),
    Tool(
        name="BuscaHotel",
        func=buscar_hotel,
        description="Sugere hotel baseado no plano e orçamento"
    ),
]

# ---------- AGENTE ORQUESTRADOR ----------

orquestrador = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Execução orquestrada
resposta = orquestrador.run("Quero planejar uma viagem em dezembro")
print("\n🧳 Plano de viagem final:\n", resposta)
