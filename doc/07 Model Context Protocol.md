# Guia do Model Context Protocol (MCP) - Versão Corrigida

## ✅ O que é **MCP** (Model Context Protocol)

**MCP (Model Context Protocol)** é um protocolo open-source criado pela **Anthropic** para **padronizar como grandes modelos de linguagem (LLMs)** se conectam com **ferramentas externas, APIs, bancos de dados e outros recursos**.

### ✨ Características principais:

-   **Protocolo baseado em JSON-RPC 2.0**: Comunicação padronizada entre cliente e servidor
-   **Transporte flexível**: Suporta stdio, HTTP e WebSocket
-   **Tipagem rigorosa**: Schemas JSON bem definidos para todas as mensagens
-   **Handshake de inicialização**: Negociação de capabilities entre cliente e servidor
-   **Gerenciamento de recursos**: Permite exposição de tools, resources e prompts

> 📦 **Importante**: MCP não é apenas uma "estrutura de mensagem", mas um protocolo completo com especificações rigorosas para comunicação entre sistemas.

---

## 🔍 MCP Real vs. Simulações Educativas

### ❌ **Simulação Educativa** (não é MCP real):

```python
# Exemplo didático - simula o conceito MCP
mensagem_simulada = {
    "tool": "calculadora",
    "input": {"numero": 5}
}
```

### ✅ **MCP Real**:

```python
# Implementação real usando biblioteca oficial MCP
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("meu-servidor")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="calculadora", description="...")]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Implementação da ferramenta
    pass
```

---

## 🚀 Tutorial: Implementação MCP Real

### ✅ Pré-requisitos:

-   Python 3.10+
-   Biblioteca oficial MCP: `pip install mcp`

---

### 📄 Exemplo: Servidor MCP com Calculadora

```python
# servidor_calculadora.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Criar servidor MCP
server = Server("calculadora-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista as ferramentas disponíveis"""
    return [
        Tool(
            name="calcular_porcentagem",
            description="Calcula porcentagem de um valor",
            inputSchema={
                "type": "object",
                "properties": {
                    "valor": {"type": "number", "description": "Valor base"},
                    "porcentagem": {"type": "number", "description": "Porcentagem a calcular"}
                },
                "required": ["valor", "porcentagem"]
            }
        ),
        Tool(
            name="dobrar_numero",
            description="Dobra um número",
            inputSchema={
                "type": "object",
                "properties": {
                    "numero": {"type": "number", "description": "Número para dobrar"}
                },
                "required": ["numero"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Executa a ferramenta solicitada"""

    if name == "calcular_porcentagem":
        valor = arguments["valor"]
        porcentagem = arguments["porcentagem"]
        resultado = (porcentagem / 100) * valor

        return [TextContent(
            type="text",
            text=f"{porcentagem}% de {valor} é {resultado}"
        )]

    elif name == "dobrar_numero":
        numero = arguments["numero"]
        resultado = numero * 2

        return [TextContent(
            type="text",
            text=f"O dobro de {numero} é {resultado}"
        )]

    else:
        return [TextContent(
            type="text",
            text=f"Ferramenta '{name}' não encontrada"
        )]

async def main():
    """Inicializa o servidor MCP via stdio"""
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1])

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 📄 Como usar o servidor MCP:

1. **Salve o código** como `servidor_calculadora.py`
2. **Execute o servidor**:

```bash
python servidor_calculadora.py
```

3. **Conecte um cliente MCP** (como Claude Desktop) que pode descobrir e usar suas ferramentas

---

### 📄 Exemplo: Cliente MCP Simples

```python
# cliente_mcp.py
import asyncio
import json
from mcp.client import Client
from mcp.client.stdio import stdio_client

async def usar_servidor_calculadora():
    """Exemplo de cliente que usa o servidor MCP"""

    # Conectar ao servidor via stdio
    async with stdio_client() as streams:
        client = Client("meu-cliente")

        # Inicializar conexão
        await client.initialize(streams[0], streams[1])

        # Listar ferramentas disponíveis
        tools = await client.list_tools()
        print("Ferramentas disponíveis:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # Usar ferramenta de porcentagem
        resultado = await client.call_tool(
            "calcular_porcentagem",
            {"valor": 150, "porcentagem": 20}
        )
        print(f"Resultado: {resultado[0].text}")

        # Usar ferramenta de dobrar número
        resultado = await client.call_tool(
            "dobrar_numero",
            {"numero": 7}
        )
        print(f"Resultado: {resultado[0].text}")

if __name__ == "__main__":
    asyncio.run(usar_servidor_calculadora())
```

---

## 🔄 Estrutura de Mensagens MCP Real

### Inicialização:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "clientInfo": {
            "name": "meu-cliente",
            "version": "1.0.0"
        }
    }
}
```

### Listar Ferramentas:

```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}
```

### Chamar Ferramenta:

```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "calcular_porcentagem",
        "arguments": {
            "valor": 150,
            "porcentagem": 20
        }
    }
}
```

---

## 📊 Comparação: Simulação vs. MCP Real

| Aspecto                | Simulação Educativa       | MCP Real                          |
| ---------------------- | ------------------------- | --------------------------------- |
| **Protocolo**          | Estrutura personalizada   | JSON-RPC 2.0 padrão               |
| **Transporte**         | Chamadas de função locais | stdio/HTTP/WebSocket              |
| **Tipagem**            | Informal                  | Schemas JSON rigorosos            |
| **Descoberta**         | Hard-coded                | `tools/list`, `resources/list`    |
| **Error Handling**     | Básico                    | Códigos de erro padronizados      |
| **Interoperabilidade** | Limitada ao código local  | Funciona com qualquer cliente MCP |

---

## 🎯 Quando Usar Cada Abordagem

### 📚 **Simulações Educativas** são úteis para:

-   Aprender o conceito de agentes com ferramentas
-   Prototipar rapidamente ideias
-   Ensinar arquiteturas de software
-   Demonstrações simples

### 🏗️ **MCP Real** é necessário para:

-   Integração com sistemas reais (Claude Desktop, etc.)
-   Aplicações em produção
-   Interoperabilidade entre diferentes ferramentas
-   Padrões de segurança e confiabilidade

---

## 🔗 Recursos Adicionais

-   **Documentação oficial**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
-   **Repositório GitHub**: [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
-   **Exemplos oficiais**: Verifique o repositório para servidores MCP de exemplo
-   **Claude Desktop**: Suporte nativo para servidores MCP

---

## 💡 Resumo Final

**MCP** é um protocolo completo e padronizado, não apenas uma "estrutura de mensagem". Para implementações reais, sempre use as bibliotecas oficiais e siga as especificações do protocolo.

Os exemplos "simulados" neste documento servem apenas para fins educativos e ajudam a entender os conceitos, mas não são implementações MCP válidas para uso em produção.
