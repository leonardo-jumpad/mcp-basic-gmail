# api

from github import Github
import os
from dotenv import load_dotenv

# 1. Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Configurações do GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")  # Ex: "seu-usuario"
GITHUB_REPO = os.getenv("GITHUB_REPO")    # Ex: "nome-do-repo"

# 3. Conecta-se ao GitHub
g = Github(GITHUB_TOKEN)

# 4. Acessa o repositório
repo = g.get_user(GITHUB_OWNER).get_repo(GITHUB_REPO)

# 5. Cria uma issue
def criar_issue(titulo: str, corpo: str):
    issue = repo.create_issue(title=titulo, body=corpo)
    print("✅ Issue criada com sucesso:", issue.html_url)

# 6. Exemplo de uso
if __name__ == "__main__":
    criar_issue("Exemplo de Issue criada com Python", "Esta issue foi criada usando PyGithub via script MCP simples.")
