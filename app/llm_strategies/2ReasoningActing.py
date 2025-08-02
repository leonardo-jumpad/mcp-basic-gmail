from setup_llm import llm
from leitor_txt_tool import leitor_tool
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=[leitor_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

resposta = agent.invoke("O que é LangChain?")
print("Resposta:\n", resposta)


# ReAct (Reasoning + Acting)
# Usamos ferramentas externas e o modelo alterna entre pensar e agir.