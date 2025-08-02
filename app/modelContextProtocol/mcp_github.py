import requests

# Executor MCP que chama a ferramenta certa com base na mensagem MCP
def mcp_execute(message: dict) -> dict:
    tool = message.get("tool")
    input_data = message.get("input", {})

    if tool == "listar_issues_github":
        repo = input_data.get("repo")
        if not repo:
            return {"error": "Parâmetro 'repo' obrigatório"}

        url = f"https://api.github.com/repos/{repo}/issues"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": f"Erro API GitHub: {response.status_code}"}

        issues = response.json()
        # Extrair título e número das issues abertas (limitado a 5)
        lista = [{"numero": i["number"], "titulo": i["title"]} for i in issues[:5]]

        return {"output": lista}

    return {"error": "Ferramenta desconhecida."}


# Agente que constrói a mensagem MCP e chama o executor
def agente_mcp(pergunta: str):
    if "issues do github" in pergunta.lower():
        # Busca o nome do repositório na pergunta usando "repositório" ou depois da palavra "github"
        repo_nome = None
        partes = pergunta.lower().split()
        if "repositório" in partes:
            try:
                idx = partes.index("repositório")
                repo_nome = pergunta.split()[idx + 1]
            except IndexError:
                return "Informe o repositório no formato 'user/repo'."
        else:
            # tenta pegar o termo depois de "github"
            if "github" in partes:
                try:
                    idx = partes.index("github")
                    repo_nome = pergunta.split()[idx + 1]
                except IndexError:
                    return "Informe o repositório no formato 'user/repo'."

        if not repo_nome:
            return "Informe o repositório no formato 'user/repo'."

        mensagem = {
            "tool": "listar_issues_github",
            "input": {"repo": repo_nome}
        }

        resposta = mcp_execute(mensagem)
        if "error" in resposta:
            return f"Erro: {resposta['error']}"

        issues = resposta["output"]
        if not issues:
            return "Nenhuma issue encontrada."

        texto = "Issues abertas no repositório:\n"
        for i in issues:
            texto += f"- #{i['numero']}: {i['titulo']}\n"
        return texto

    return "Não entendi a pergunta."


if __name__ == "__main__":
    # Teste simples para listar issues do repo python/cpython
    print(agente_mcp("Me mostre as issues do github do repositório python/cpython"))
