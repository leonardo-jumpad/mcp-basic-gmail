# Tutorial MCP Gmail Sender

## 🎯 Objetivo

Este tutorial ensina como criar um sistema simples de envio de emails usando MCP (Model Context Protocol) com FastAPI.

## 📚 O que você vai aprender

-   ✅ Estrutura básica de uma aplicação FastAPI
-   ✅ Separação de responsabilidades em camadas
-   ✅ Como trabalhar com banco de dados SQLite
-   ✅ Integração com Gmail para envio de emails
-   ✅ Conceitos básicos de MCP (Model Context Protocol)
-   ✅ Como usar LangChain de forma simples

## 🏗️ Arquitetura Simples

```
📁 mcp-gmail-simple/
├── app/
│   ├── models/          # 📊 Definição das tabelas do banco
│   │   └── emailModel.py
│   ├── schemas/         # 📝 Validação de dados
│   │   └── email.py
│   ├── repositories/    # 🗄️ Acesso aos dados
│   │   └── emailRepository.py
│   ├── services/        # 🔧 Lógica de negócio
│   │   └── emailService.py
│   ├── tools/          # 🛠️ Ferramentas LangChain
│   │   └── mcpEmailTool.py
│   ├── agents/         # 🤖 Agentes inteligentes
│   │   └── mcpEmailAgent.py
│   ├── routers/        # 🛣️ Endpoints da API
│   │   ├── emails.py
│   │   └── mcp.py
│   ├── database.py     # 💾 Configuração do banco
│   ├── config.py       # ⚙️ Configurações
│   └── main.py         # 🚀 Aplicação principal
├── .env                # 🔐 Variáveis secretas
├── requirements.txt    # 📦 Dependências
└── README.md          # 📖 Documentação
```

## 🚀 Passo a Passo

### Passo 1: Configurar o Ambiente

#### 1.1 Instalar Python e Dependências

```bash
# Criar pasta do projeto
mkdir mcp-gmail-simple
cd mcp-gmail-simple

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Mac/Linux)
source venv/bin/activate

# Instalar dependências
# Instalar dependências principais da API
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlmodel==0.0.14

# Upload de arquivos e validação de e-mail
pip install python-multipart==0.0.6 email-validator==2.1.0

# Langchain e variáveis de ambiente
pip install langchain==0.2.17 langchain-core==0.2.43 langchain-community==0.2.19 langsmith==0.1.147
pip install python-dotenv==1.0.0

```

### Como gerar o requirements.txt

Rode o seguinte comando no terminal (com seu ambiente virtual ativado):

pip freeze > requirements.txt

#### 1.2 Configurar Gmailphython

1. **Ativar 2FA na sua conta Gmail:**

    - Vá em [myaccount.google.com](https://myaccount.google.com)
    - Clique em "Segurança"
    - Ative "Verificação em duas etapas"

2. **Gerar senha de aplicativo:**
    - Na página de segurança, procure "Senhas de app"
    - Selecione "Email" e "Outro (nome personalizado)"
    - Digite "MCP Gmail" como nome
    - **IMPORTANTE:** Copie a senha de 16 caracteres gerada

#### 1.3 Criar arquivo .env

```env
# Configurações do Gmail
GMAIL_EMAIL=seu_email@gmail.com
GMAIL_APP_PASSWORD=sua_senha_de_16_caracteres

# ⚠️ NUNCA compartilhe essas informações!
```

### Passo 2: Entender as Camadas

#### 2.1 Models (Modelos de Dados)

```python
# O que faz: Define como os dados são salvos no banco
# Localização: app/models/emailModel.py

class Email(EmailBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    to_email: str
    subject: str
    body: str
    status: EmailStatus = "pending"
    created_at: datetime
```

**Por que usar?** Os models definem a estrutura dos dados de forma consistente.

#### 2.2 Schemas (Validação)

```python
# O que faz: Valida dados que entram e saem da API
# Localização: app/schemas/email.py

class EmailCreate(BaseModel):
    to_email: EmailStr  # Valida se é um email válido
    subject: str
    body: str

    @validator('subject')
    def validate_subject(cls, v):
        if len(v) > 200:
            raise ValueError('Assunto muito longo')
        return v
```

**Por que usar?** Os schemas garantem que apenas dados válidos entrem no sistema.

#### 2.3 Repositories (Acesso aos Dados)

```python
# O que faz: Gerencia operações com o banco de dados
# Localização: app/repositories/emailRepository.py

class EmailRepository:
    def create_email(self, email_data: EmailCreate) -> Email:
        # Salva email no banco

    def get_email_by_id(self, email_id: int) -> Email:
        # Busca email por ID
```

**Por que usar?** Separa a lógica de banco de dados da lógica de negócio.

#### 2.4 Services (Lógica de Negócio)

```python
# O que faz: Contém as regras de negócio da aplicação
# Localização: app/services/emailService.py

class EmailService:
    def send_email(self, email: Email) -> bool:
        # Conecta ao Gmail
        # Envia o email
        # Atualiza status no banco
```

**Por que usar?** Centraliza toda a lógica complexa em um lugar.

#### 2.5 Tools (Ferramentas LangChain)

```python
# O que faz: Integra funcionalidades com LangChain
# Localização: app/tools/mcpEmailTool.py

class MCPEmailTool(BaseTool):
    def _run(self, query: str) -> str:
        # Processa comando JSON
        # Envia email
        # Retorna resultado
```

**Por que usar?** Permite que agentes de IA usem nossas funcionalidades.

#### 2.6 Agents (Agentes Inteligentes)

```python
# O que faz: Orquestra o uso de ferramentas
# Localização: app/agents/mcpEmailAgent.py

class MCPEmailAgent:
    def process_command(self, message: str):
        # Entende linguagem natural
        # Chama ferramentas apropriadas
        # Retorna resposta amigável
```

**Por que usar?** Permite interação em linguagem natural.

#### 2.7 Routers (Endpoints da API)

```python
# O que faz: Define as rotas da API
# Localização: app/routers/emails.py

@router.post("/send")
async def send_email(email_data: EmailCreate):
    # Valida dados
    # Chama serviço
    # Retorna resposta
```

**Por que usar?** Organiza os endpoints de forma clara.

### Passo 3: Implementar o Código

#### 3.1 Criar estrutura de pastas

```bash
mkdir -p app/models app/schemas app/repositories app/services app/tools app/agents app/routers
```

#### 3.2 Copiar o código

Copie cada arquivo do código fornecido para sua respectiva pasta. Vou explicar os arquivos principais:

**app/main.py** - Arquivo principal

```python
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import emails, mcp

app = FastAPI(title="MCP Gmail Sender - Simples")

# Incluir rotas
app.include_router(emails.router)
app.include_router(mcp.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()  # Cria banco SQLite
    print("🚀 Sistema iniciado!")
```

**app/database.py** - Configuração do banco

```python
from sqlmodel import create_engine, Session

# SQLite é um banco simples em arquivo
DATABASE_URL = "sqlite:///./emails.db"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session  # Fornece sessão para as rotas
```

### Passo 4: Testar o Sistema

#### 4.1 Iniciar o servidor

```bash
# Na pasta do projeto
uvicorn app.main:app --reload

# Você verá:
# INFO: Uvicorn running on http://127.0.0.1:8000
```

#### 4.2 Acessar a documentação

Abra no navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Você verá uma interface automática para testar a API!

#### 4.3 Primeiro teste - Criar email

Na documentação, clique em `POST /emails` e teste:

```json
{
    "to_email": "teste@exemplo.com",
    "subject": "Meu primeiro email MCP",
    "body": "Esta é uma mensagem de teste!",
    "priority": "normal"
}
```

#### 4.4 Segundo teste - Enviar email

Clique em `POST /emails/send` e use os mesmos dados. O email será enviado via Gmail!

### Passo 5: Exemplos Práticos

#### 5.1 Teste via Python

Crie um arquivo `teste.py`:

```python
import requests

# Criar email
data = {
    "to_email": "destinatario@exemplo.com",
    "subject": "Teste programático",
    "body": "Email enviado via código Python!"
}

response = requests.post("http://127.0.0.1:8000/emails/send", json=data)
print(response.json())
```

#### 5.2 Teste MCP com comando natural

```python
import requests

command = "Envie um email para joao@empresa.com com assunto 'Reunião' e mensagem 'Reunião marcada para amanhã às 14h'"

response = requests.post(
    "http://127.0.0.1:8000/mcp/command",
    params={"command": command}
)
print(response.json())
```

#### 5.3 Teste direto via MCP

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/mcp/send",
    params={
        "to": "teste@exemplo.com",
        "subject": "Via MCP",
        "body": "Mensagem enviada através do protocolo MCP",
        "priority": "high"
    }
)
print(response.json())
```

### Passo 6: Entender o Fluxo

#### 6.1 Fluxo de Criação de Email

```
1. Cliente faz POST /emails
2. Router valida dados com Schema
3. Router chama EmailService
4. Service chama Repository
5. Repository salva no banco SQLite
6. Dados retornam pela mesma cadeia
```

#### 6.2 Fluxo de Envio de Email

```
1. Cliente faz POST /emails/send
2. EmailService cria email (fluxo acima)
3. EmailService.send_email():
   - Conecta ao Gmail SMTP
   - Envia mensagem
   - Atualiza status no banco
4. Retorna sucesso/erro
```

#### 6.3 Fluxo MCP com LangChain

```
1. Cliente faz POST /mcp/command
2. MCPEmailAgent recebe comando
3. LangChain processa linguagem natural
4. Agent decide usar MCPEmailTool
5. Tool converte para JSON
6. Tool chama EmailService
7. Email é enviado
8. Resposta em linguagem natural
```

### Passo 7: Personalizar e Expandir

#### 7.1 Adicionar novos campos

Em `app/models/emailModel.py`:

```python
class Email(EmailBase, table=True):
    # ... campos existentes ...
    cc_email: Optional[str] = Field(default=None)  # Novo campo
    is_urgent: bool = Field(default=False)         # Novo campo
```

#### 7.2 Criar nova funcionalidade

Em `app/services/emailService.py`:

```python
def send_urgent_emails(self):
    """Enviar apenas emails urgentes"""
    urgent_emails = self.session.exec(
        select(Email).where(
            Email.is_urgent == True,
            Email.status == EmailStatus.PENDING
        )
    ).all()

    for email in urgent_emails:
        self.send_email(email)
```

#### 7.3 Adicionar nova rota

Em `app/routers/emails.py`:

```python
@router.post("/send-urgent")
async def send_urgent_emails(session: Session = Depends(get_session)):
    """Enviar emails urgentes"""
    email_service = EmailService(session)
    email_service.send_urgent_emails()
    return {"message": "Emails urgentes processados"}
```

### Passo 8: Solução de Problemas

#### 8.1 Erro de autenticação Gmail

```
SMTPAuthenticationError: Username and Password not accepted
```

**Soluções:**

1. Verificar se o 2FA está ativado
2. Gerar nova senha de aplicativo
3. Verificar arquivo `.env`
4. Testar credenciais manualmente

#### 8.2 Banco de dados não encontrado

```
sqlite3.OperationalError: no such table: emails
```

**Solução:**

```python
# Reiniciar o servidor para criar tabelas
# Ou executar manualmente:
from app.database import create_db_and_tables
create_db_and_tables()
```

#### 8.3 Erro de importação

```
ModuleNotFoundError: No module named 'app'
```

**Solução:**

```bash
# Executar do diretório correto:
cd mcp-gmail-simple
uvicorn app.main:app --reload
```

#### 8.4 Debug com logs

Adicione logs para entender o que está acontecendo:

```python
# Em qualquer arquivo
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usar nos métodos
logger.info(f"Processando email para: {email.to_email}")
logger.error(f"Erro ao enviar: {str(e)}")
```

### Passo 9: Próximos Passos

#### 9.1 Melhorias simples

1. **Adicionar validações:**

    - Verificar se email existe
    - Limitar tamanho da mensagem
    - Validar prioridade

2. **Melhorar interface:**

    - Adicionar descrições nas rotas
    - Criar exemplos na documentação
    - Adicionar códigos de erro específicos

3. **Funcionalidades extras:**
    - Agendar emails
    - Templates de mensagem
    - Lista de contatos

#### 9.2 Conceitos para estudar depois

-   **Autenticação**: Como proteger as rotas
-   **Testes**: Como criar testes automáticos
-   **Deploy**: Como colocar em produção
-   **Monitoramento**: Como acompanhar o sistema
-   **Cache**: Como melhorar a performance

#### 9.3 Tecnologias para o futuro

-   **PostgreSQL**: Banco mais robusto
-   **Redis**: Cache e filas
-   **Docker**: Containerização
-   **AWS**: Deploy na nuvem

### 📊 Resumo dos Conceitos

| Camada         | Responsabilidade            | Exemplo                        |
| -------------- | --------------------------- | ------------------------------ |
| **Models**     | Definir estrutura dos dados | `class Email(SQLModel)`        |
| **Schemas**    | Validar entrada/saída       | `class EmailCreate(BaseModel)` |
| **Repository** | Acessar banco de dados      | `def create_email()`           |
| **Service**    | Lógica de negócio           | `def send_email()`             |
| **Tool**       | Integração LangChain        | `class MCPEmailTool`           |
| **Agent**      | Orquestração inteligente    | `class MCPEmailAgent`          |
| **Router**     | Endpoints da API            | `@router.post("/send")`        |

### 🎯 Checklist de Conclusão

-   [ ] ✅ Ambiente configurado
-   [ ] ✅ Gmail configurado com senha de app
-   [ ] ✅ Código implementado
-   [ ] ✅ Servidor rodando
-   [ ] ✅ Primeiro email enviado
-   [ ] ✅ Teste MCP funcionando
-   [ ] ✅ Entendi as camadas
-   [ ] ✅ Fiz personalização
-   [ ] ✅ Testei resolução de problemas

### 🏆 Parabéns!

Você acabou de criar seu primeiro sistema MCP Gmail Sender! Agora você entende:

-   ✅ Como estruturar uma aplicação em camadas
-   ✅ Como integrar com serviços externos (Gmail)
-   ✅ Como usar LangChain de forma prática
-   ✅ Como criar APIs com FastAPI
-   ✅ Os conceitos básicos de MCP

**Próximo passo:** Quando se sentir confortável, volte ao tutorial avançado com PostgreSQL, Redis e funcionalidades completas!

### 📚 Recursos Extras

-   [Documentação FastAPI](https://fastapi.tiangolo.com/)
-   [Documentação SQLModel](https://sqlmodel.tiangolo.com/)
-   [Documentação LangChain](https://python.langchain.com/)
-   [Tutorial Gmail API](https://developers.google.com/gmail/api)

### 💡 Dicas Finais

1. **Sempre teste pequenas partes primeiro**
2. **Use os logs para entender o que está acontecendo**
3. **Não tenha medo de experimentar e quebrar**
4. **Peça ajuda quando precisar**
5. **Celebre as pequenas vitórias!** 🎉
