from dotenv import load_dotenv
import os

# Verifica se o arquivo existe
caminho_arquivo = "app/langchain/info.txt"
if not os.path.exists(caminho_arquivo):
    print(f"Arquivo '{caminho_arquivo}' não encontrado. Crie o arquivo e adicione informações sobre LangChain.")
    exit(1)

from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# 1. Carrega variáveis do .env (ex: OPENAI_API_KEY)
load_dotenv()

# 2. Inicializa o LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Função que lê o conteúdo do arquivo .txt
def ler_arquivo_info(_):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        return conteudo
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}"

# 4. Cria ferramenta para leitura do .txt
ferramenta_info_txt = Tool(
    name="LeitorDeArquivoTXT",
    func=ler_arquivo_info,
    description="Use esta ferramenta para consultar informações armazenadas no arquivo info.txt. Ela retorna o conteúdo completo do arquivo."
)

# 5. Inicializa o agente com a ferramenta
agente = initialize_agent(
    tools=[ferramenta_info_txt],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 6. Consulta segura ao conteúdo do .txt
pergunta_segura = (
    "Use apenas a ferramenta LeitorDeArquivoTXT para ler o arquivo info.txt. "
    "Depois, responda resumidamente: O que é LangChain?"
)
conteudo_extraido = agente.invoke(pergunta_segura)

# 7. Novo prompt para formatar o conteúdo em 3 idiomas
prompt_formatado = f"""
Você recebeu este conteúdo extraído de um arquivo .txt:

\"\"\"{conteudo_extraido}\"\"\"

Agora formate essas informações de forma clara, didática e organizada, como se estivesse explicando para uma pessoa iniciante o que é LangChain.

Apresente a resposta em três idiomas: 

1. **Português (Brasil)**
2. **English (USA)**
3. **Español (Latinoamérica)**

Use uma linguagem simples, com tópicos numerados e exemplos se possível.
"""

# 8. Envia o prompt para o LLM formatar a resposta
resposta_final = llm.invoke(prompt_formatado)

# 9. Exibe a resposta formatada
print("\nResposta formatada em 3 idiomas:")
print(resposta_final.content)
