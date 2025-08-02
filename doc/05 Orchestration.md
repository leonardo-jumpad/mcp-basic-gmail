Claro! Vamos construir um exemplo simples para **entender orquestração de agentes de IA** na prática, com explicação detalhada.

---

### ✅ **Exemplo de Orquestração: Planejamento de Viagem com 3 Agentes**

Suponha que você queira automatizar o **planejamento de uma viagem de férias** usando agentes de IA. Usaremos orquestração para coordenar esses agentes, cada um com uma função específica:

---

#### 🧠 **Agentes**

1. **Agente Planejador** → Cria um plano de viagem básico com destino, datas e duração.
2. **Agente de Pesquisa de Voos** → Busca voos com base no plano.
3. **Agente de Acomodações** → Sugere hotéis compatíveis com o orçamento e destino.

---

#### 🕹️ **Orquestrador**

É quem:

-   **Chama os agentes na ordem certa**
-   **Passa os dados entre eles**
-   **Inclui regras (guardrails)** para evitar destinos perigosos ou valores muito altos
-   **Permite revisão humana** antes da compra final

---

### 🔁 **Fluxo Orquestrado**

```text
[Entrada do Usuário]: "Quero viajar nas minhas férias em dezembro."

            ↓

[Agente Planejador]
-> Resposta: "Destino: Lisboa, 7 dias, de 10 a 17 de dezembro"

            ↓

[Agente de Pesquisa de Voos]
-> Entrada: Lisboa + Datas
-> Resposta: "Voo LATAM, R$ 3.200 ida e volta"

            ↓

[Agente de Acomodações]
-> Entrada: Lisboa + Datas + Orçamento
-> Resposta: "Hotel Solar do Castelo, R$ 1.900 / 7 dias"

            ↓

[Orquestrador]
→ Verifica se os valores são razoáveis
→ Checa se o destino é seguro (via API externa)
→ Mostra resumo final para o usuário

            ↓

[Usuário Aprova]

            ↓

[Orquestrador Finaliza e Envia por Email ou API]
```

---

### 📘 **Explicando com Analogia**

Imagine você como maestro:

-   Cada músico (agente) toca um instrumento específico (tarefas especializadas).
-   Você define a **ordem** das execuções, garante que **todos toquem juntos** no tempo certo.
-   Você **controla o volume**, **corrige erros**, e até para a música se algo sai errado (guardrails).
-   Pode até pedir ajuda a um **especialista humano** se algo estiver fora do normal.

---

### ⚙️ **Ferramentas de Orquestração Reais**

-   **LangGraph** (LangChain): coordena estados e fluxos entre agentes.
-   **CrewAI** / **Autogen Studio** (Microsoft): define papéis, memória e coordenação.
-   **Haystack Pipelines**: fluxo de agentes + buscas e validações.
-   **Flowise / SuperAgent / OpenDevin**: plataformas visuais e agentes autônomos.

---

### ✅ Benefícios da Orquestração

-   Coordenação eficiente de tarefas complexas.
-   Divisão de responsabilidades.
-   Capacidade de escalar e integrar APIs, bancos de dados e humanos no processo.
-   Aplicação de **guardrails** e lógica de negócios ao redor da IA.

---

Usa-se agentes usando `langchain` ou `CrewAI`.

Perfeito! Vamos montar um **exemplo prático com LangChain**, simulando a **orquestração de três agentes** como no exemplo da viagem:

---

## 🎯 Objetivo

Orquestrar 3 agentes usando **LangChain**:

1. **Planejador**: define destino e datas.
2. **Agente de Voos**: busca voos com base nas datas e destino.
3. **Agente de Hotéis**: sugere hotel baseado no orçamento.

---

## ⚙️ Pré-requisitos

Certifique-se de ter instalado:

```bash
pip install langchain langchain-openai openai
```

E configure a chave da OpenAI em `.env`:

```
OPENAI_API_KEY=sk-xxxx
```

---

## 🧠 Código com LangChain (Simples e Didático)

```python
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# Modelo base
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# ---------- FERRAMENTAS (AGENTES FUNCIONAIS) ----------

def planejar_viagem(_):
    return "Destino: Lisboa, Datas: 10 a 17 de dezembro, Orçamento: R$5000"

def buscar_voos(_):
    return "Voo LATAM, ida e volta por R$3200"

def buscar_hotel(_):
    return "Hotel Solar do Castelo, 7 diárias por R$1700"

# Criar ferramentas como agentes
tools = [
    Tool(
        name="PlanejadorDeViagem",
        func=planejar_viagem,
        description="Cria um plano de viagem com destino, datas e orçamento"
    ),
    Tool(
        name="BuscaVoos",
        func=buscar_voos,
        description="Busca voos baseados no plano de viagem"
    ),
    Tool(
        name="BuscaHotel",
        func=buscar_hotel,
        description="Sugere hotel baseado no plano e orçamento"
    ),
]

# ---------- AGENTE ORQUESTRADOR ----------

orquestrador = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Execução orquestrada
resposta = orquestrador.run("Quero planejar uma viagem em dezembro")
print("\n🧳 Plano de viagem final:\n", resposta)
```

---

## 🔍 O que está acontecendo?

-   Cada **função simples representa um agente funcional**.
-   O `initialize_agent` cria um **agente orquestrador** que decide **qual ferramenta (agente) chamar** em que ordem.
-   O `AgentType.ZERO_SHOT_REACT_DESCRIPTION` permite que o orquestrador **raciocine passo a passo**.

---

## 🧠 Expansões possíveis:

-   Substituir `planejar_viagem`, `buscar_voos`, `buscar_hotel` por agentes com lógica interna ou chamadas de API reais.
-   Usar **LangGraph** para fazer fluxos com mais controle de estado e memória.
-   Incluir validações: por exemplo, rejeitar hotéis acima de R\$2000.
-   Incluir humano no loop com `input()` no fim para aprovar o plano.

---

Póximos passos:

Deseja que eu adapte esse código para LangGraph (fluxo com estados e memória) ou adicionar chamadas reais (como API de voos e hotéis)

Excelente! 🎉 Seu exemplo de agente orquestrador com ferramentas (`tools`) usando LangChain está funcionando perfeitamente — e com uma lógica clara, simples e didática. Agora, se quiser **acrescentar o conceito de Guardrails**, aqui vai um exemplo prático e adaptado ao seu código:

---

## 🛡️ Exemplo com Guardrails simples (manual, no LangChain)

Vamos adicionar uma **camada de verificação manual** que simula um guardrail antes de enviar a mensagem ao agente:

### ✅ Objetivo:

-   **Impedir** que o usuário compartilhe **dados pessoais sensíveis**.
-   Garantir que o input está dentro do escopo: "planejar uma viagem".

---

### 🧪 Adicionando um verificador simples:

```python
def verificar_input_usuario(input_usuario: str) -> bool:
    termos_proibidos = ["meu cpf", "meu cartão", "senha", "número do passaporte"]
    for termo in termos_proibidos:
        if termo.lower() in input_usuario.lower():
            return False
    if "viagem" not in input_usuario.lower():
        return False
    return True
```

### 🔧 Usando o verificador antes de orquestrar:

```python
entrada_usuario = "Quero planejar uma viagem em dezembro"

if verificar_input_usuario(entrada_usuario):
    resposta = orquestrador.run(entrada_usuario)
    print("\n🧳 Plano de viagem final:\n", resposta)
else:
    print("❌ Entrada não permitida: parece conter informações sensíveis ou fora do escopo.")
```

---

### 🧠 Explicação:

Esse guardrail manual:

-   **Verifica se há termos sensíveis** no input do usuário.
-   **Valida o contexto da tarefa** (neste caso, "viagem").
-   **Bloqueia a execução do agente**, caso não passe.

---

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI

# Carregar variáveis de ambiente

load_dotenv()

# ---------- LLM ----------

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# ---------- FERRAMENTAS (FUNÇÕES DE SUPORTE) ----------

def planejar*viagem(*):
return "Destino: Lisboa, Datas: 10 a 17 de dezembro, Orçamento: R$5000"

def buscar*voos(*):
return "Voo LATAM, ida e volta por R$3200"

def buscar*hotel(*):
return "Hotel Solar do Castelo, 7 diárias por R$1700"

# Lista de ferramentas

tools = [
Tool(
name="PlanejadorDeViagem",
func=planejar_viagem,
description="Cria um plano de viagem com destino, datas e orçamento"
),
Tool(
name="BuscaVoos",
func=buscar_voos,
description="Busca voos baseados no plano de viagem"
),
Tool(
name="BuscaHotel",
func=buscar_hotel,
description="Sugere hotel baseado no plano e orçamento"
),
]

# ---------- GUARDRAIL MANUAL ----------

def verificar_input_usuario(input_usuario: str) -> bool:
termos_proibidos = ["cpf", "cartão", "senha", "passaporte", "rg", "pix", "número do", "número do cartão"]
for termo in termos_proibidos:
if termo.lower() in input_usuario.lower():
return False
if "viagem" not in input_usuario.lower():
return False
return True

# ---------- AGENTE ORQUESTRADOR ----------

orquestrador = initialize_agent(
tools=tools,
llm=llm,
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
verbose=True
)

# ---------- EXECUÇÃO ----------

entrada_usuario = input("✈️ O que deseja? ")

if verificar_input_usuario(entrada_usuario):
resposta = orquestrador.run(entrada_usuario)
print("\n🧳 Plano de viagem final:\n", resposta)
else:
print("❌ Entrada não permitida: parece conter informações sensíveis ou fora do escopo.")

Claro! Abaixo está o **código completo e funcional** com:

1. Orquestrador do LangChain usando ferramentas (Tools)
2. Um **guardrail manual** que:

    - Bloqueia entradas com dados sensíveis
    - Garante que a pergunta seja sobre **viagem**

---

### ✅ Código Completo com Guardrail Manual

```python
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI

# Carregar variáveis de ambiente
load_dotenv()

# ---------- LLM ----------
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# ---------- FERRAMENTAS (FUNÇÕES DE SUPORTE) ----------

def planejar_viagem(_):
    return "Destino: Lisboa, Datas: 10 a 17 de dezembro, Orçamento: R$5000"

def buscar_voos(_):
    return "Voo LATAM, ida e volta por R$3200"

def buscar_hotel(_):
    return "Hotel Solar do Castelo, 7 diárias por R$1700"

# Lista de ferramentas
tools = [
    Tool(
        name="PlanejadorDeViagem",
        func=planejar_viagem,
        description="Cria um plano de viagem com destino, datas e orçamento"
    ),
    Tool(
        name="BuscaVoos",
        func=buscar_voos,
        description="Busca voos baseados no plano de viagem"
    ),
    Tool(
        name="BuscaHotel",
        func=buscar_hotel,
        description="Sugere hotel baseado no plano e orçamento"
    ),
]

# ---------- GUARDRAIL MANUAL ----------

def verificar_input_usuario(input_usuario: str) -> bool:
    termos_proibidos = ["cpf", "cartão", "senha", "passaporte", "rg", "pix", "número do", "número do cartão"]
    for termo in termos_proibidos:
        if termo.lower() in input_usuario.lower():
            return False
    if "viagem" not in input_usuario.lower():
        return False
    return True

# ---------- AGENTE ORQUESTRADOR ----------

orquestrador = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ---------- EXECUÇÃO ----------

entrada_usuario = input("✈️ O que deseja? ")

if verificar_input_usuario(entrada_usuario):
    resposta = orquestrador.run(entrada_usuario)
    print("\n🧳 Plano de viagem final:\n", resposta)
else:
    print("❌ Entrada não permitida: parece conter informações sensíveis ou fora do escopo.")
```

---

### 🔎 Teste com diferentes entradas

-   ✅ `Quero planejar uma viagem em dezembro` → **Passa**
-   ❌ `Meu CPF é 123... quero viajar` → **Bloqueado**
-   ❌ `Quero comprar um carro` → **Bloqueado**
-   ✅ `Pode me ajudar com uma viagem para o Rio em janeiro?` → **Passa**

---

### 🔄 Evolução com `Guardrails AI` (biblioteca real)

Se quiser subir o nível depois, use a lib [**Guardrails AI**](https://github.com/ShreyaR/guardrails) que funciona com LangChain para estruturar entradas/saídas em JSON, definir regras com RAIL e até corrigir a resposta da IA.

Perfeito. Abaixo está a **versão com Guardrails AI oficial**, usando a biblioteca `guardrails-ai`. Essa abordagem usa um **esquema RAIL** para definir regras de segurança e validação da saída da LLM.

---

### ✅ 1. Instalar dependências

Se ainda não instalou:

```bash
pip install langchain openai guardrails-ai
```

---

### ✅ 2. Criar esquema RAIL

Crie um arquivo chamado `viagem_guardrails.rail`:

```xml
<guardrails>
  <output>
    <string name="resposta" description="Resposta do plano de viagem que o agente deve gerar." />
  </output>

  <prompt>
    Ajude o usuário a planejar uma viagem com destino, datas e orçamento.
    Garanta que a resposta não contenha dados sensíveis como CPF, RG, senhas ou informações bancárias.
  </prompt>

  <validators>
    <regex name="sem_dados_sensiveis" on="resposta" pattern="^(?!.*(cpf|rg|senha|pix|cart[aã]o|n[uú]mero)).*$">
      A resposta contém termos sensíveis. Remova informações como CPF, RG, senha ou dados bancários.
    </regex>
  </validators>
</guardrails>
```

---

### ✅ 3. Código Python com LangChain + Guardrails

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from guardrails.guard import Guard

# Carregar variáveis de ambiente
load_dotenv()

# LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Funções simuladas
def planejar_viagem(_):
    return "Destino: Paris, Datas: 15 a 22 de novembro, Orçamento: R$7000"

def buscar_voos(_):
    return "Voo AirFrance, ida e volta por R$3500"

def buscar_hotel(_):
    return "Hotel Ibis Paris, 7 noites por R$2000"

# Ferramentas
tools = [
    Tool(name="PlanejadorDeViagem", func=planejar_viagem, description="Planeja viagem com destino e orçamento"),
    Tool(name="BuscaVoos", func=buscar_voos, description="Busca voos com base no plano"),
    Tool(name="BuscaHotel", func=buscar_hotel, description="Sugere hotel dentro do orçamento")
]

# Agente LangChain
agente = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Guardrails
guard = Guard.from_rail("viagem_guardrails.rail")

# Entrada do usuário
entrada = input("✈️ O que deseja?\n")

# Rodar LangChain
resposta_raw = agente.run(entrada)

# Validar com Guardrails
resposta_validada, _, _ = guard(
    llm=llm,
    prompt_params={},
    output_params={"resposta": resposta_raw}
)

# Exibir resposta segura
print("\n🧳 Plano de viagem final:\n", resposta_validada["resposta"])
```

---

### 🧪 Resultado (com validação automática)

Se a LLM tentar colocar algo como:

```txt
"Destino: Lisboa. Meu CPF é 123.456.789-00"
```

A `guardrails-ai` vai rejeitar essa resposta e **regerar** automaticamente uma versão sem termos sensíveis.

---

### ✅ Benefícios

-   Garante que **nenhum dado proibido** vá para o output
-   Reduz o risco de **vazamento de dados pessoais**
-   Pode ser usado para **outros domínios**: financeiro, médico, jurídico, etc.

---

Próximos passos: logar as **respostas rejeitadas**, **usar múltiplas validações** (ex: verificação de JSON, data de viagem no futuro etc.), ou transformar isso num microserviço Flask.
