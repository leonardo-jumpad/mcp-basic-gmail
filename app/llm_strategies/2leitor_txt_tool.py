from langchain.tools import Tool

def ler_arquivo_txt(query: str):
    with open("app/llm_strategies/info.txt", "r") as f:
        texto = f.read()
    if query.lower() in texto.lower():
        return texto
    return "Não encontrei o termo no texto."

leitor_tool = Tool(
    name="LeitorTXT",
    func=ler_arquivo_txt,
    description="Lê um arquivo txt e responde com base no conteúdo. Use quando precisar de informações do arquivo."
)

# ReAct (Reasoning + Acting)