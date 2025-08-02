from setup_llm import llm

prompt = """
Resolva o seguinte problema passo a passo:

Se João tem 3 maçãs e ganha mais 2 de Maria, quantas maçãs ele tem agora?
"""

resposta = llm.invoke(prompt)
print("Resposta:\n", resposta.content)


# Chain of Thought (Cadeia de Pensamento)
# Essa técnica encoraja o modelo a pensar em etapas antes de responder.