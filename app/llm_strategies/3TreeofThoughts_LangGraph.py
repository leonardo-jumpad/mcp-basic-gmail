# langgraph_thought_tree.py
from setup_llm import llm
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, List

# 1. Define o esquema do estado (TypedDict é opcional, mas ajuda)
class ThoughtState(TypedDict):
    problema: str
    ideias: List[str]
    analise: str
    melhor_ideia: str

# Estado inicial
initial_state: ThoughtState = {
    "problema": "Quais são as maneiras de economizar dinheiro em um supermercado?",
    "ideias": [],
    "analise": "",
    "melhor_ideia": ""
}

# Nó 1: gerar três ideias
def gerar_ideias(state: ThoughtState) -> ThoughtState:
    prompt = f"""
Gere três ideias diferentes para resolver este problema:

{state['problema']}
"""
    resposta = llm.invoke(prompt)
    state["ideias"] = resposta.content.strip().split("\n")
    return state

# Nó 2: avaliar prós e contras de cada ideia
def analisar_ideias(state: ThoughtState) -> ThoughtState:
    ideias_formatadas = "\n".join(state["ideias"])
    prompt = f"""
Analise os prós e contras das ideias abaixo:

{ideias_formatadas}
"""
    resposta = llm.invoke(prompt)
    state["analise"] = resposta.content
    return state

# Nó 3: escolher a melhor ideia
def escolher_melhor_ideia(state: ThoughtState) -> ThoughtState:
    prompt = f"""
Com base nessa análise, escolha a melhor ideia entre as seguintes e justifique:

{state["analise"]}
"""
    resposta = llm.invoke(prompt)
    state["melhor_ideia"] = resposta.content
    return state

# Construir o grafo (passando o schema!)
graph = StateGraph(ThoughtState)

graph.add_node("gerar_ideias", RunnableLambda(gerar_ideias))
graph.add_node("analisar", RunnableLambda(analisar_ideias))
graph.add_node("escolher", RunnableLambda(escolher_melhor_ideia))

graph.set_entry_point("gerar_ideias")
graph.add_edge("gerar_ideias", "analisar")
graph.add_edge("analisar", "escolher")
graph.add_edge("escolher", END)

# Compilar e rodar
app = graph.compile()
final_state = app.invoke(initial_state)

# Exibir resultado final
print("\n🧠 Melhor ideia escolhida pelo LLM:")
print(final_state["melhor_ideia"])




# 3. Tree of Thoughts (Árvore de Pensamentos)
# Exemplo com LangGraph simulando o comportamento de Tree of Thoughts (ToT) de forma simples 

# StateGraph(ThoughtState): agora o grafo sabe o formato do estado que trafegará entre os nós.