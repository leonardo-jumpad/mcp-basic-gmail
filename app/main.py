from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# Carrega as variáveis do .env
load_dotenv()

# Inicializa o modelo com a chave já presente no ambiente
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Faz uma pergunta
pergunta = "O que é LangChain?"
resposta = llm.invoke(pergunta)

# Exibe a resposta
print(resposta.content)
