# Simulação muito simples de Context Engineering em Python

# Memória de longo prazo simulada (ex.: bancos de dados, documentos, histórico)
long_term_memory = {
    "openai": "OpenAI é uma empresa de pesquisa em inteligência artificial.",
    "python": "Python é uma linguagem de programação de alto nível."
}

# Memória de curto prazo (histórico da conversa atual)
short_term_memory = []

def rag_search(query):
    """
    Simula o RAG: busca na memória de longo prazo.
    """
    for key, value in long_term_memory.items():
        if key in query.lower():
            return value
    return None

def action_tool(query):
    """
    Simula ferramentas externas (ex.: calculadora, API externa, etc).
    """
    if "2 + 2" in query:
        return "A resposta de 2 + 2 é 4."
    return None

def agent_reasoning(prompt):
    """
    O 'agente' decide se usa RAG, ferramenta ou responde direto.
    """
    # Primeiro tenta ferramenta
    tool_result = action_tool(prompt)
    if tool_result:
        return tool_result
    
    # Depois tenta RAG
    rag_result = rag_search(prompt)
    if rag_result:
        return rag_result

    # Se nada encontrou, responde genérico
    return "Desculpe, não sei a resposta para isso."

def add_to_long_term_memory(entry):
    """
    Simula adicionar informações importantes na memória de longo prazo.
    """
    key = entry.lower().split()[0]  # usa primeira palavra como chave simples
    long_term_memory[key] = entry

def main():
    """
    Fluxo principal: entrada do usuário → processamento → resposta
    """
    print("Simulação de Context Engineering (digite 'sair' para encerrar)\n")
    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            break
        
        # Etapa 1: entrada do usuário vai para short-term memory
        short_term_memory.append(user_input)
        
        # Etapa 2: agente processa o input
        answer = agent_reasoning(user_input)
        
        # Etapa 3: resposta enviada ao usuário
        print(f"Agente: {answer}\n")
        
        # Etapa 4: opcionalmente adicionar à long-term memory
        if "adicionar memória:" in user_input.lower():
            new_memory = user_input.split(":", 1)[1].strip()
            add_to_long_term_memory(new_memory)
            print("📝 Adicionado à memória de longo prazo.\n")
        
        # Etapa 5: salva tudo no short-term memory
        short_term_memory.append(answer)

if __name__ == "__main__":
    main()


# O que o código simula:
# User Input → você digita.
# Short-Term Memory → guarda o que foi dito na sessão.
# RAG → busca termos conhecidos na memória de longo prazo.
# Action Tools → se reconhecer uma operação, executa (ex.: 2 + 2).
# Agent → coordena tudo e dá a resposta.
# Adicionar memória → exemplo: adicionar memória: Claude é um modelo da Anthropic.

(User → Prompt → Agent → RAG → Tools → Answer → Memories).