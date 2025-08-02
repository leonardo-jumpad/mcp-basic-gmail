from setup_llm import llm

problema = "Quais são as maneiras de economizar dinheiro em um supermercado?"

prompt = f"""
Considere três ideias diferentes para resolver este problema:

{problema}

Para cada ideia, pense nos prós e contras. Ao final, escolha a melhor delas.
"""

resposta = llm.invoke(prompt)
print("Resposta:\n", resposta.content)


# 3. Tree of Thoughts (Árvore de Pensamentos)
# Simulamos isso manualmente (LangGraph faria melhor). A ideia é gerar várias soluções possíveis, comparar e escolher a melhor.

# 1. Fazer uma lista de compras e segui-la.
#    Prós: Evita compras por impulso.
#    Contras: Pode esquecer itens necessários.

# 2. Comprar marcas próprias.
#    Prós: Mais barato.
#    Contras: Pode ter qualidade inferior.

# 3. Usar cupons e promoções.
#    Prós: Reduz muito o custo.
#    Contras: Exige tempo e planejamento.

# Melhor opção: Combinar a lista com cupons para máxima economia.
