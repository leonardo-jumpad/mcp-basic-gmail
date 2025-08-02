import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
#from tools import dobrar_numero, inverter_texto
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 2. Inicializa o modelo OpenAI
model = ChatOpenAI(model="gpt-4", api_key=api_key)

# 3. Cria o memory saver (sem parâmetros no construtor)
memory = MemorySaver()

system_prompt = """
Você é um agente que pode usar ferramentas para resolver perguntas.
"""
# Inserir a ferramenta no arquivo tools.py
# Ferramenta simples: dobrar número
@tool
def dobrar_numero(numero: float) -> str:
    return f"O dobro de {numero} é {numero * 2}"

# 4. Lista de ferramentas (adicione suas funções aqui)
tools = [dobrar_numero]

# 5. Configuração correta para thread_id
config = {"configurable": {"thread_id": "main_thread"}}

agent_executor = create_react_agent(
    model=model,
    tools=tools,
    state_modifier=system_prompt,  # Use state_modifier em vez de prompt
    checkpointer=memory,
)

# 6. Invoca com configuração de thread
result = agent_executor.invoke(
    {"messages": [("user", "Quem é você?")]},
    config=config
)
print(result)

# Extrai apenas a resposta do agente
resposta = result["messages"][-1].content
#print("Resposta do agente:", resposta)
# Exibe a conversa completa
print("\n--- Conversa completa ---")
for message in result["messages"]:
    if hasattr(message, 'content'):
        tipo = "Usuário" if message.__class__.__name__ == "HumanMessage" else "Agente"
        print(f"{tipo}: {message.content}")

# Ou ainda uma versão mais detalhada:
print(f"\n--- Informações detalhadas ---")
print(f"Total de tokens: {result['messages'][-1].usage_metadata['total_tokens']}")
print(f"Modelo usado: {result['messages'][-1].response_metadata['model_name']}")
print(f"Resposta: {result['messages'][-1].content}")