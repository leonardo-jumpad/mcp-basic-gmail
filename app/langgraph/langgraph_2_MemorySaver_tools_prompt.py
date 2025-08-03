import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 2. Inicializa o modelo OpenAI
model = ChatOpenAI(model="gpt-4", api_key=api_key)

# 3. Cria o memory saver para guardar o histórico da conversa
memory = MemorySaver()

# Prompt do sistema / estado inicial do agente
# Agente criado com prompt mais detalhado orientando o uso da ferramenta
system_prompt = """
Você é um agente que pode usar ferramentas para resolver perguntas.
Quando o usuário fornecer um número, você pode usar a ferramenta 'dobrar_numero' para dobrá-lo.
"""

# Ferramenta simples: dobrar número
@tool
def dobrar_numero(numero: float) -> str:
    return f"O dobro de {numero} é {numero * 2}"

# 4. Lista de ferramentas (adicione suas funções aqui)
tools = [dobrar_numero]

# 5. Configuração correta para thread_id para manter contexto
config = {"configurable": {"thread_id": "main_thread"}}

# 6. Cria o agente com React Agent, memória e ferramentas
agent_executor = create_react_agent(
    model=model,
    tools=tools,
    state_modifier=system_prompt,  # Prompt inicial do agente
    checkpointer=memory,
)

# Função que simula o fluxo da imagem:
def executar_fluxo_entrada(usuario_input: str):
    # 1. Input do usuário é enviado para o prompt
    print(f"Input do usuário: {usuario_input}")

    # 2. O agente coordena e toma decisões
    result = agent_executor.invoke(
        {"messages": [("user", usuario_input)]},
        config=config
    )
    
    # 3. Atualiza prompt com a resposta
    resposta_agente = result["messages"][-1].content

    # 4. Armazena tudo na memória (já feito pelo MemorySaver internamente)

    # 5. Responde para o usuário
    print("\nResposta do agente:")
    print(resposta_agente)

    # 6. Exibe a conversa completa (short-term memory)
    print("\n--- Conversa completa ---")
    for msg in result["messages"]:
        if hasattr(msg, 'content'):
            tipo = "Usuário" if msg.__class__.__name__ == "HumanMessage" else "Agente"
            print(f"{tipo}: {msg.content}")

    # Informações detalhadas
    print(f"\n--- Informações detalhadas ---")
    print(f"Total de tokens usados: {result['messages'][-1].usage_metadata['total_tokens']}")
    print(f"Modelo usado: {result['messages'][-1].response_metadata['model_name']}")

# Exemplo de execução:
if __name__ == "__main__":
    executar_fluxo_entrada("Qual é o dobro de 8?")


# Vou estruturar o fluxo com:
# User Input (Entrada do usuário)
# Agent (que decide a ação a tomar)
# Action Tools (ferramentas para ações)
# Atualização do Prompt com a resposta da ferramenta
# Memória de curto prazo armazenando o contexto
# Resposta final para o usuário