from dotenv import load_dotenv
import os

from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# Carrega a chave do .env
load_dotenv()

# Inicializa o modelo
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Ferramenta simples: uma calculadora
def calcular(expr: str) -> str:
    try:
        resultado = eval(expr)
        return f"O resultado de {expr} é {resultado}"
    except Exception as e:
        return f"Erro ao calcular: {str(e)}"

# Empacotando como ferramenta
ferramentas = [
    Tool(
        name="CalculadoraSimples",
        func=calcular,
        description="Útil para resolver expressões matemáticas. Exemplo: 2 + 2 * 5"
    )
]

# Inicializa o agente com a ferramenta
agente = initialize_agent(
    ferramentas,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Teste com uma pergunta que o LLM vai passar para a ferramenta
resposta = agente.invoke("Qual o resultado de 8 * (2 + 3)?")
print(resposta)
