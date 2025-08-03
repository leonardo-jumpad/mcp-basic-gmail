# Simulação educativa completa de Context Engineering

class ShortTermMemory:
    """
    Memória de curto prazo: armazena o histórico da conversa atual.
    """
    def __init__(self):
        self.history = []

    def store(self, message):
        self.history.append(message)

    def get_context(self):
        return " ".join(self.history[-5:])  # últimos 5 itens (exemplo)

class LongTermMemory:
    """
    Memória de longo prazo (simulação RAG + knowledge base).
    """
    def __init__(self):
        self.knowledge = {
            "openai": "OpenAI é uma empresa de pesquisa em IA.",
            "python": "Python é uma linguagem de programação popular.",
            "claude": "Claude é um modelo de linguagem da Anthropic."
        }

    def search(self, query):
        for key, value in self.knowledge.items():
            if key in query.lower():
                return value
        return None

    def add(self, fact):
        key = fact.lower().split()[0]
        self.knowledge[key] = fact

class ActionTools:
    """
    Ferramentas externas (simples exemplo de ferramenta de cálculo).
    """
    def execute(self, query):
        if "2 + 2" in query:
            return "A resposta de 2 + 2 é 4."
        return None

class Prompt:
    """
    Monta o prompt (contexto) para o agente decidir o próximo passo.
    """
    def __init__(self, user_input, context):
        self.content = f"{context}\nUsuário: {user_input}"

    def get(self):
        return self.content

class Agent:
    """
    Agente principal: coordena RAG, ferramentas e raciocínio.
    """
    def __init__(self, long_term_memory, tools):
        self.memory = long_term_memory
        self.tools = tools

    def decide(self, prompt_text):
        # Tenta ferramenta primeiro
        tool_result = self.tools.execute(prompt_text)
        if tool_result:
            return tool_result
        
        # Depois tenta RAG
        rag_result = self.memory.search(prompt_text)
        if rag_result:
            return rag_result

        # Se nada encontrado, dá resposta genérica
        return "Desculpe, não tenho essa informação."

class User:
    """
    Representa o usuário que envia inputs.
    """
    def __init__(self, name):
        self.name = name

    def send_input(self):
        return input(f"{self.name}: ")

def main():
    """
    Fluxo completo simulando o diagrama Context Engineering.
    """
    print("\nSimulação Context Engineering (digite 'sair' para encerrar)\n")

    # Inicializa os componentes
    user = User("Você")
    short_term_memory = ShortTermMemory()
    long_term_memory = LongTermMemory()
    tools = ActionTools()
    agent = Agent(long_term_memory, tools)

    while True:
        user_input = user.send_input()
        if user_input.lower() == "sair":
            break

        # Etapa 1: guarda entrada na memória de curto prazo
        short_term_memory.store(user_input)

        # Etapa 2: monta prompt com histórico recente
        prompt = Prompt(user_input, short_term_memory.get_context())

        # Etapa 3: agente decide resposta
        answer = agent.decide(prompt.get())

        # Etapa 4: mostra resposta
        print(f"Agente: {answer}\n")

        # Etapa 5: adiciona resposta na memória de curto prazo
        short_term_memory.store(answer)

        # Etapa 6: opção de adicionar manualmente à memória de longo prazo
        if "adicionar memória:" in user_input.lower():
            new_fact = user_input.split(":", 1)[1].strip()
            long_term_memory.add(new_fact)
            print("📥 Fato adicionado à memória de longo prazo.\n")

if __name__ == "__main__":
    main()



# O que essa versão ilustra:
# User → envia input.
# Short-Term Memory → armazena histórico da conversa.
# Prompt → monta o contexto atual.
# Agent → decide se usa ferramenta, RAG ou responde genérico.
# RAG (Long-Term Memory) → busca conhecimentos salvos.
# Action Tools → executa ações simples (ex.: cálculo).
# Answer → entregue ao usuário.
# Add to Memory → permite simular atualização da memória de longo prazo.


