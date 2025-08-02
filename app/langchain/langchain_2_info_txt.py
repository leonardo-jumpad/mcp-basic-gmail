from dotenv import load_dotenv
import os
if not os.path.exists("app/langchain/info.txt"):
    print("Arquivo 'info.txt' não encontrado. Crie o arquivo e adicione informações sobre LangChain.")
    exit(1)
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# 1. Carrega variáveis do .env
load_dotenv()

# 2. Inicializa o LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define a função que lê o arquivo info.txt
def ler_arquivo_info(pergunta: str) -> str:
    try:
        with open("app/langchain/info.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        # Você pode melhorar isso com embeddings ou contexto, mas aqui vamos retornar o texto simples
        return f"Conteúdo do arquivo:\n{conteudo}"
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}"

# 4. Cria a ferramenta personalizada para acessar o .txt
ferramenta_info_txt = Tool(
    name="LeitorDeArquivoTXT",
    func=ler_arquivo_info,
    description="Use esta ferramenta para consultar informações armazenadas no arquivo info.txt. Ela retorna o conteúdo completo do arquivo."
)

# 5. Inicializa o agente com essa ferramenta
agente = initialize_agent(
    tools=[ferramenta_info_txt],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 6. Usa o agente para responder uma pergunta
resposta = agente.invoke("O que é LangChain?")
print("\nResposta do agente:")
print(resposta)

# Você construiu o seguinte fluxo:
# O agente recebe a pergunta: "O que é LangChain?"
# O agente raciocina e decide usar a ferramenta LeitorDeArquivoTXT para responder.
# A ferramenta lê o arquivo info.txt, retorna o conteúdo.
# O agente interpreta esse conteúdo e devolve como resposta final.