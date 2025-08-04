# servidor mcp
import asyncio
# Usa a biblioteca oficial mcp da Anthropic
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from github import Github

# Servidor MCP
# Cria uma instância do servidor MCP oficial
server = Server("github-server")

# Usa os decorators oficiais do protocolo MCP
#Tool(...)           # Tipo oficial para definir ferramentas
#TextContent(...)    # Tipo oficial para resposta de conteúdo
# inputSchema Define schema JSON Schema válido para validação de entrada. Segue o padrão esperado pelo protocolo MCP
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="criar_issue",
            description="Cria uma nova issue no GitHub",
            inputSchema={
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"},
                    "corpo": {"type": "string"}
                },
                "required": ["titulo", "corpo"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "criar_issue":
        # Lógica para criar issue
        return [TextContent(type="text", text="Issue criada com sucesso")]

async def main():
    # Implementa comunicação via stdin/stdout (padrão MCP)
    # Permite que clientes MCP se conectem via JSON-RPC
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1])

if __name__ == "__main__":
    asyncio.run(main())