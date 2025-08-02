# Tutorial de Implementação - MCP Gmail Sender (Fusion Style)

## 📋 Índice

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Implementação Passo a Passo](#implementação-passo-a-passo)
5. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
6. [Integração com o Sistema](#integração-com-o-sistema)
7. [Testes e Validação](#testes-e-validação)
8. [Deploy e Monitoramento](#deploy-e-monitoramento)
9. [Exemplos de Uso](#exemplos-de-uso)
10. [Troubleshooting](#troubleshooting)

## 🏗️ Visão Geral da Arquitetura

### Camadas da Aplicação

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  /routers/emails.py  │  /routers/mcp.py  │  /api/mcpServer.py│
├─────────────────────────────────────────────────────────────┤
│                     APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  /services/emailService.py  │  /agents/mcpEmailAgent.py     │
├─────────────────────────────────────────────────────────────┤
│                     DOMAIN LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  /models/emailModel.py  │  /schemas/email.py               │
├─────────────────────────────────────────────────────────────┤
│                  INFRASTRUCTURE LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  /repositories/emailRepository.py  │  /tools/mcpEmailTool.py │
├─────────────────────────────────────────────────────────────┤
│                     BACKGROUND JOBS                         │
├─────────────────────────────────────────────────────────────┤
│  /tasks/emailTasks.py  │  /jobs/emailScheduler.py           │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

1. **API Request** → Router → Service
2. **Service** → Repository → Database
3. **MCP Agent** → Tool → Service
4. **Background Job** → Task → Service
5. **Scheduler** → Task Queue → Processing

## 🚀 Pré-requisitos

### Software Necessário

-   Python 3.8+
-   PostgreSQL 12+
-   Redis 6+
-   FastAPI
-   SQLModel
-   LangChain

### Configurações Gmail

-   Conta Gmail com 2FA ativado
-   Senha de aplicativo gerada
-   Acesso SMTP habilitado

### Dependências Python

```bash
pip install fastapi sqlmodel psycopg2-binary redis langchain
pip install email-validator python-multipart schedule
pip install httpx boto3 python-dotenv
```

## ⚙️ Configuração do Ambiente

### 1. Variáveis de Ambiente

Criar arquivo `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fusion_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Gmail Configuration
GMAIL_EMAIL=seu_email@gmail.com
GMAIL_APP_PASSWORD=sua_senha_de_16_caracteres

# Email Settings
EMAIL_MAX_RETRIES=3
EMAIL_BATCH_SIZE=50
EMAIL_RATE_LIMIT_PER_HOUR=100

# S3 Configuration (para anexos)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=us-east-1
```

### 2. Atualizar config/env.py

```python
# Adicionar ao arquivo de configuração existente
from pydantic import Field

class Settings(BaseSettings):
    # ... configurações existentes ...

    # Gmail Configuration
    GMAIL_EMAIL: str = Field(description="Email do remetente Gmail")
    GMAIL_APP_PASSWORD: str = Field(description="Senha de app do Gmail")

    # Email Configuration
    EMAIL_MAX_RETRIES: int = Field(default=3, description="Máximo de tentativas")
    EMAIL_BATCH_SIZE: int = Field(default=50, description="Tamanho do lote")
    EMAIL_RATE_LIMIT_PER_HOUR: int = Field(default=100, description="Limite por hora")
```

## 📝 Implementação Passo a Passo

### Etapa 1: Modelos de Dados

Implementar os modelos em `/app/models/emailModel.py` conforme mostrado no código.

**Pontos Importantes:**

-   Usar SQLModel para compatibilidade com FastAPI
-   Implementar enums para status e prioridade
-   Relacionamentos com User e Agent
-   Campos de auditoria (created_at, updated_at)

### Etapa 2: Schemas de Validação

Criar schemas em `/app/schemas/email.py` para:

-   Validação de entrada (EmailCreate)
-   Validação de saída (EmailPublic)
-   Requisições MCP (MCPEmailRequest)
-   Atualizações (EmailUpdate)

### Etapa 3: Repository Pattern

Implementar `/app/repositories/emailRepository.py`:

-   Interface abstrata para flexibilidade
-   Implementação concreta com SQLModel
-   Métodos para CRUD e consultas específicas
-   Separação clara de responsabilidades

### Etapa 4: Serviços de Negócio

Criar `/app/services/emailService.py`:

-   Lógica de envio via SMTP
-   Processamento de anexos
-   Gerenciamento de retry
-   Integração com repositório

### Etapa 5: Tools LangChain

Implementar `/app/tools/mcpEmailTool.py`:

-   Herança de BaseTool do LangChain
-   Validação de JSON de entrada
-   Integração com serviço de email
-   Tratamento de erros específicos

### Etapa 6: Agente MCP

Desenvolver `/app/agents/mcpEmailAgent.py`:

-   Wrapper para LangChain Agent
-   Processamento de linguagem natural
-   Métodos diretos e via prompt
-   Capacidades documentadas

### Etapa 7: API Endpoints

Criar routers em:

-   `/app/routers/emails.py` - CRUD de emails
-   `/app/routers/mcp.py` - Interface MCP
-   `/app/api/mcpServer.py` - Servidor MCP

### Etapa 8: Background Jobs

Implementar processamento assíncrono:

-   `/app/tasks/emailTasks.py` - Tasks individuais
-   `/app/jobs/emailScheduler.py` - Agendamento automático
-   Integração com sistema de filas existente

## 🗄️ Configuração do Banco de Dados

### 1. Migrations

Criar migration para as novas tabelas:

```sql
-- Migration: add_email_tables.sql
CREATE TABLE emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_user_id UUID NOT NULL REFERENCES users(id),
    agent_id UUID REFERENCES agents(id),
    to_email VARCHAR(255) NOT NULL,
    cc_emails TEXT,
    bcc_emails TEXT,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    html_body TEXT,
    priority VARCHAR(20) DEFAULT 'normal',
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    scheduled_at TIMESTAMPTZ,
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE email_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_id UUID NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_emails_sender_user_id ON emails(sender_user_id);
CREATE INDEX idx_emails_status ON emails(status);
CREATE INDEX idx_emails_scheduled_at ON emails(scheduled_at);
CREATE INDEX idx_emails_created_at ON emails(created_at);
```

### 2. Executar Migration

```bash
# Usando Alembic (se configurado)
alembic revision --autogenerate -m "add_email_tables"
alembic upgrade head

# Ou executar SQL diretamente
psql -d fusion_db -f migrations/add_email_tables.sql
```

## 🔗 Integração com o Sistema

### 1. Atualizar main.py

```python
# Adicionar imports
from app.routers import emails, mcp
from app.jobs.emailScheduler import email_scheduler
from app.middleware.emailMiddleware import EmailRateLimitMiddleware

# Incluir routers
app.include_router(emails.router)
app.include_router(mcp.router)

# Adicionar middleware
app.add_middleware(EmailRateLimitMiddleware, max_emails_per_hour=100)

# Eventos de startup/shutdown
@app.on_event("startup")
async def start_email_services():
    email_scheduler.start()
    logger.info("Email services started")

@app.on_event("shutdown")
async def stop_email_services():
    email_scheduler.stop()
    logger.info("Email services stopped")
```

### 2. Atualizar models/**init**.py

```python
# Adicionar imports dos novos modelos
from app.models.emailModel import Email, EmailAttachment

# Garantir que os modelos sejam incluídos no init_models()
```

### 3. Integração com Agentes Existentes

```python
# Em qualquer agent existente, adicionar capacidade de email
from app.tools.mcpEmailTool import MCPEmailTool

class ExistingAgent:
    def __init__(self, session, user_id, agent_id):
        # ... código existente ...

        # Adicionar ferramenta de email
        self.email_tool = MCPEmailTool(session, user_id, agent_id)

        # Adicionar à lista de ferramentas do agente
        self.tools.append(self.email_tool)

        # Reinicializar agente com nova ferramenta
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
```

## 🧪 Testes e Validação

### 1. Testes Unitários

Criar `/tests/test_email_service.py`:

```python
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from app.services.emailService import EmailService
from app.schemas.email import EmailCreate, MCPEmailRequest
from app.models.emailModel import Email, EmailStatus

class TestEmailService:

    @pytest.fixture
    def email_service(self, session_mock):
        return EmailService(session_mock)

    @pytest.fixture
    def email_data(self):
        return EmailCreate(
            to_email="test@example.com",
            subject="Teste",
            body="Mensagem de teste"
        )

    def test_create_email(self, email_service, email_data):
        user_id = uuid4()
        email = email_service.create_email(email_data, user_id)

        assert email.to_email == "test@example.com"
        assert email.sender_user_id == user_id
        assert email.status == EmailStatus.PENDING

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp, email_service):
        email = Email(
            id=uuid4(),
            to_email="test@example.com",
            subject="Teste",
            body="Teste",
            sender_user_id=uuid4()
        )

        result = email_service.send_email(email)
        assert result is True

    def test_process_mcp_request(self, email_service):
        request = MCPEmailRequest(
            to="test@example.com",
            subject="MCP Test",
            body="Teste MCP"
        )
        user_id = uuid4()

        email = email_service.process_mcp_request(request, user_id)
        assert email.to_email == "test@example.com"
```

### 2. Testes de Integração

Criar `/tests/test_email_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestEmailAPI:

    def test_create_email_endpoint(self, auth_headers):
        email_data = {
            "to_email": "test@example.com",
            "subject": "API Test",
            "body": "Teste via API"
        }

        response = client.post(
            "/emails",
            json=email_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        assert response.json()["to_email"] == "test@example.com"

    def test_mcp_send_email(self, auth_headers):
        mcp_data = {
            "to": "test@example.com",
            "subject": "MCP Test",
            "body": "Teste MCP"
        }

        response = client.post(
            "/emails/mcp",
            json=mcp_data,
            headers=auth_headers
        )

        assert response.status_code == 201

    def test_rate_limiting(self, auth_headers):
        # Simular muitas requisições
        for i in range(105):  # Acima do limite de 100
            response = client.post(
                "/emails/mcp",
                json={
                    "to": f"test{i}@example.com",
                    "subject": "Rate Test",
                    "body": "Teste"
                },
                headers=auth_headers
            )

            if i >= 100:
                assert response.status_code == 429
```

### 3. Testes de Carga

Criar `/tests/test_email_performance.py`:

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from app.agents.mcpEmailAgent import MCPEmailAgent

class TestEmailPerformance:

    def test_concurrent_email_sending(self, session, user_id):
        """Testa envio concorrente de emails"""
        agent = MCPEmailAgent(session, user_id)

        def send_email(index):
            return agent.send_email_direct(
                to=f"test{index}@example.com",
                subject=f"Teste {index}",
                body=f"Mensagem {index}"
            )

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_email, i) for i in range(50)]
            results = [future.result() for future in futures]

        end_time = time.time()
        duration = end_time - start_time

        assert len(results) == 50
        assert duration < 30  # Deve processar em menos de 30 segundos

    def test_memory_usage(self, session, user_id):
        """Testa uso de memória com muitos emails"""
        import psutil
        process = psutil.Process()

        initial_memory = process.memory_info().rss

        agent = MCPEmailAgent(session, user_id)

        # Criar muitos emails
        for i in range(1000):
            agent.send_email_direct(
                to=f"test{i}@example.com",
                subject=f"Memory Test {i}",
                body="Teste de memória"
            )

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Não deve usar mais que 100MB adicionais
        assert memory_increase < 100 * 1024 * 1024
```

## 🚀 Deploy e Monitoramento

### 1. Docker Configuration

Criar `docker/email-service.Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app/ ./app/

# Variáveis de ambiente
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando de inicialização
CMD ["python", "-m", "app.jobs.emailScheduler"]
```

### 2. Docker Compose

Adicionar ao `docker-compose.yml`:

```yaml
services:
    email-scheduler:
        build:
            context: .
            dockerfile: docker/email-service.Dockerfile
        environment:
            - DATABASE_URL=${DATABASE_URL}
            - REDIS_URL=${REDIS_URL}
            - GMAIL_EMAIL=${GMAIL_EMAIL}
            - GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}
        depends_on:
            - postgres
            - redis
        restart: unless-stopped

    email-worker:
        build:
            context: .
            dockerfile: docker/email-service.Dockerfile
        command: ["python", "-m", "app.tasks.emailTasks"]
        environment:
            - DATABASE_URL=${DATABASE_URL}
            - REDIS_URL=${REDIS_URL}
            - GMAIL_EMAIL=${GMAIL_EMAIL}
            - GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}
        depends_on:
            - postgres
            - redis
        restart: unless-stopped
        scale: 3
```

### 3. Monitoramento

Criar `/app/monitoring/emailMetrics.py`:

```python
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Métricas do Prometheus
emails_sent_total = Counter('emails_sent_total', 'Total de emails enviados')
emails_failed_total = Counter('emails_failed_total', 'Total de emails falhados')
email_send_duration = Histogram('email_send_duration_seconds', 'Tempo de envio')
emails_pending = Gauge('emails_pending', 'Emails pendentes na fila')

def track_email_metrics(func):
    """Decorator para rastrear métricas de email"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            emails_sent_total.inc()
            return result
        except Exception as e:
            emails_failed_total.inc()
            raise
        finally:
            duration = time.time() - start_time
            email_send_duration.observe(duration)
    return wrapper

class EmailMonitor:
    """Monitor para estatísticas de email"""

    def __init__(self, session):
        self.session = session

    def update_pending_count(self):
        """Atualiza contagem de emails pendentes"""
        from app.repositories.emailRepository import EmailRepository
        repo = EmailRepository(self.session)
        pending = len(repo.get_pending_emails())
        emails_pending.set(pending)

    def get_email_stats(self) -> dict:
        """Retorna estatísticas de email"""
        from app.models.emailModel import Email, EmailStatus
        from sqlmodel import select, func

        stats = {}

        # Total por status
        for status in EmailStatus:
            count = self.session.exec(
                select(func.count()).where(Email.status == status)
            ).one()
            stats[f"emails_{status.value}"] = count

        # Emails nas últimas 24h
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_count = self.session.exec(
            select(func.count()).where(Email.created_at >= yesterday)
        ).one()
        stats["emails_24h"] = recent_count

        return stats
```

### 4. Health Checks

Adicionar ao `/app/health/checks.py`:

```python
async def check_email_service_health():
    """Verifica saúde do serviço de email"""
    try:
        # Testar conexão SMTP
        import smtplib
        server = smtplib.SMTP(env.GMAIL_SMTP_SERVER, env.GMAIL_SMTP_PORT)
        server.starttls()
        server.login(env.GMAIL_EMAIL, env.GMAIL_APP_PASSWORD)
        server.quit()

        return HealthStatus(
            status="ok",
            message="Email service is healthy"
        )
    except Exception as e:
        return HealthStatus(
            status="error",
            message=f"Email service error: {str(e)}"
        )

async def check_email_queue_health():
    """Verifica saúde da fila de emails"""
    try:
        session = SessionLocal()
        repo = EmailRepository(session)
        pending_count = len(repo.get_pending_emails())

        if pending_count > 1000:
            return HealthStatus(
                status="warning",
                message=f"High pending email count: {pending_count}"
            )

        return HealthStatus(
            status="ok",
            message=f"Email queue healthy: {pending_count} pending"
        )
    except Exception as e:
        return HealthStatus(
            status="error",
            message=f"Email queue error: {str(e)}"
        )
    finally:
        session.close()
```

## 💡 Exemplos de Uso

### 1. Uso Básico via API

```python
import httpx

# Configurar cliente
client = httpx.Client(base_url="http://localhost:8000")
headers = {"Authorization": "Bearer your_token"}

# Enviar email simples
email_data = {
    "to_email": "destinatario@exemplo.com",
    "subject": "Teste de Integração",
    "body": "Esta é uma mensagem de teste do sistema MCP."
}

response = client.post("/emails", json=email_data, headers=headers)
print(f"Email criado: {response.json()}")

# Enviar via MCP
mcp_data = {
    "to": "destinatario@exemplo.com",
    "subject": "Via MCP",
    "body": "Mensagem enviada através do protocolo MCP",
    "priority": "high"
}

response = client.post("/emails/mcp", json=mcp_data, headers=headers)
print(f"Email MCP: {response.json()}")
```

### 2. Uso Programático

```python
from app.agents.mcpEmailAgent import MCPEmailAgent
from app.database import SessionLocal

# Criar sessão
session = SessionLocal()
user_id = "user-uuid-here"
agent_id = "agent-uuid-here"

# Criar agente
agent = MCPEmailAgent(session, user_id, agent_id)

# Envio direto
result = agent.send_email_direct(
    to="cliente@empresa.com",
    subject="Proposta Comercial",
    body="Prezado cliente, segue nossa proposta...",
    cc="supervisor@empresa.com",
    priority="high"
)
print(result)

# Comando em linguagem natural
command = """
Envie um email para equipe@empresa.com com assunto 'Reunião Semanal'
e mensagem 'Reunião marcada para segunda-feira às 9h na sala de conferências.
Favor confirmar presença.'
"""

response = agent.process_natural_language(command)
print(response)
```

### 3. Integração com Agente Existente

```python
# Em qualquer agente existente
from app.tools.mcpEmailTool import MCPEmailTool

class CustomerServiceAgent:
    def __init__(self, session, user_id, agent_id):
        self.session = session
        self.user_id = user_id
        self.agent_id = agent_id

        # Ferramentas existentes
        self.tools = [
            # suas ferramentas existentes...
        ]

        # Adicionar ferramenta de email
        self.email_tool = MCPEmailTool(session, user_id, agent_id)
        self.tools.append(self.email_tool)

        # Reinicializar agente
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

    def handle_customer_complaint(self, complaint_text: str, customer_email: str):
        """Processa reclamação e envia resposta automática"""
        prompt = f"""
        Analise a seguinte reclamação de cliente: {complaint_text}

        Depois envie um email de resposta para {customer_email} com:
        - Assunto apropriado
        - Resposta empática e profissional
        - Próximos passos para resolução
        """

        return self.agent.run(prompt)
```

### 4. Agendamento de Emails

```python
from datetime import datetime, timedelta
from app.schemas.email import EmailCreate

# Agendar email para amanhã
tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

email_data = EmailCreate(
    to_email="equipe@empresa.com",
    subject="Lembrete: Reunião Mensal",
    body="Lembrando da reunião mensal agendada para hoje às 14h.",
    scheduled_at=tomorrow,
    priority="normal"
)

email_service = EmailService(session)
email = email_service.create_email(email_data, user_id)
print(f"Email agendado para: {email.scheduled_at}")
```

### 5. Emails com Template HTML

```python
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .header { background-color: #f8f9fa; padding: 20px; }
        .content { padding: 20px; }
        .footer { background-color: #e9ecef; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{title}}</h1>
    </div>
    <div class="content">
        <p>{{message}}</p>
    </div>
    <div class="footer">
        <p>Enviado automaticamente pelo sistema MCP</p>
    </div>
</body>
</html>
"""

from jinja2 import Template

# Renderizar template
template = Template(html_template)
html_content = template.render(
    title="Relatório Mensal",
    message="Segue o relatório de atividades do mês."
)

# Enviar email com HTML
mcp_data = {
    "to": "gerencia@empresa.com",
    "subject": "Relatório Mensal - Automático",
    "body": "Versão texto do relatório...",
    "html": html_content,
    "priority": "normal"
}
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro de Autenticação Gmail

```
SMTPAuthenticationError: Username and Password not accepted
```

**Soluções:**

-   Verificar se 2FA está ativado
-   Gerar nova senha de aplicativo
-   Confirmar variáveis de ambiente
-   Testar credenciais manualmente

#### 2. Emails Não Enviados

```
Email stuck in PENDING status
```

**Diagnóstico:**

```python
# Verificar agendador
from app.jobs.emailScheduler import email_scheduler
print(f"Scheduler running: {email_scheduler.running}")

# Verificar fila
from app.repositories.emailRepository import EmailRepository
repo = EmailRepository(session)
pending = repo.get_pending_emails()
print(f"Pending emails: {len(pending)}")

# Verificar erros
failed = session.exec(
    select(Email).where(Email.status == EmailStatus.FAILED)
).all()
for email in failed:
    print(f"Failed: {email.error_message}")
```

#### 3. Rate Limiting

```
HTTP 429: Limite de emails por hora excedido
```

**Soluções:**

-   Aumentar limite no middleware
-   Implementar retry com backoff
-   Distribuir envios ao longo do tempo

#### 4. Performance Issues

**Otimizações:**

```python
# 1. Índices no banco
CREATE INDEX CONCURRENTLY idx_emails_status_created
ON emails(status, created_at) WHERE status = 'pending';

# 2. Batch processing
def process_emails_batch(batch_size=50):
    emails = repo.get_pending_emails(limit=batch_size)
    # processar em lote

# 3. Connection pooling
from sqlalchemy.pool import QueuePool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Monitoramento e Logs

#### Configurar Logs Detalhados

```python
import logging

# Logger específico para emails
email_logger = logging.getLogger('app.email')
email_logger.setLevel(logging.DEBUG)

# Handler para arquivo
handler = logging.FileHandler('logs/email.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
email_logger.addHandler(handler)
```

#### Alertas Críticos

```python
def setup_email_alerts():
    """Configurar alertas para problemas críticos"""

    # Alerta para muitos emails falhados
    failed_count = session.exec(
        select(func.count()).where(
            Email.status == EmailStatus.FAILED,
            Email.created_at >= datetime.now() - timedelta(hours=1)
        )
    ).one()

    if failed_count > 10:
        # Enviar alerta para administradores
        alert_email = {
            "to": "admin@empresa.com",
            "subject": "ALERTA: Muitos emails falharam",
            "body": f"Detectados {failed_count} emails falhados na última hora"
        }
        # Enviar via canal alternativo
```

## 📊 Métricas e KPIs

### Dashboard de Monitoramento

```python
class EmailDashboard:
    """Dashboard para métricas de email"""

    def get_daily_stats(self, date=None):
        if not date:
            date = datetime.now().date()

        return {
            "sent": self._count_by_status_and_date(EmailStatus.SENT, date),
            "failed": self._count_by_status_and_date(EmailStatus.FAILED, date),
            "pending": self._count_by_status_and_date(EmailStatus.PENDING, date),
            "success_rate": self._calculate_success_rate(date)
        }

    def get_performance_metrics(self):
        return {
            "avg_send_time": self._calculate_avg_send_time(),
            "queue_size": self._get_queue_size(),
            "retry_rate": self._calculate_retry_rate(),
            "peak_hours": self._get_peak_hours()
        }
```

Este tutorial fornece uma implementação completa e robusta do sistema MCP Gmail Sender seguindo os padrões de arquitetura do fusion-back, com separação clara de responsabilidades, testes abrangentes e monitoramento adequado.
