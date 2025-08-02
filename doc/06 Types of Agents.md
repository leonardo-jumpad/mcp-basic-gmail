Aqui está um exemplo simples em Python para ilustrar **cada tipo de agente** de forma didática. O contexto usado é de um agente que decide como responder a uma temperatura ambiente:

---

### 🌡️ Cenário comum para todos:

```python
temperatura = 30  # Temperatura ambiente em graus Celsius
```

---

### 1. 🤖 **Simple Reflex Agent**

-   **Simple Reflex Agents**: Tomam decisões baseadas **exclusivamente no momento atual** (regra condicional "se isso, faça aquilo"). Não têm memória e são baseados em regras fixas.

> Regra fixa: se estiver quente, ligue o ventilador.

```python
def simple_reflex_agent(temperatura):
    if temperatura > 25:
        return "Ligar o ventilador"
    else:
        return "Nada a fazer"

print(simple_reflex_agent(temperatura))
```

---

### 2. 🧠 **Model Based Reflex Agent**

-   **Model Based Reflex Agents**: Possuem **memória de estado interno**, o que os permite perceber o ambiente, preencher informações ausentes e tomar decisões com base na compreensão do contexto.

> Usa **memória de estado interno** (ex: se já ligou o ventilador ou não).

```python
estado_interno = {"ventilador_ligado": False}

def model_based_agent(temperatura):
    if temperatura > 25 and not estado_interno["ventilador_ligado"]:
        estado_interno["ventilador_ligado"] = True
        return "Ligar o ventilador"
    elif temperatura <= 25 and estado_interno["ventilador_ligado"]:
        estado_interno["ventilador_ligado"] = False
        return "Desligar o ventilador"
    else:
        return "Manter estado atual"

print(model_based_agent(temperatura))
```

---

### 3. 🎯 **Utility Based Agent**

-   **Utility Based Agents**: Usam uma **função de utilidade** para tomar decisões, ideal quando há diversas soluções e o agente precisa escolher a melhor considerando benefício, satisfação, conforto, etc..

> Escolhe a ação com **maior benefício** (ex: conforto térmico).

```python
def utility_based_agent(temperatura):
    utilidade = {
        "ventilador": -abs(temperatura - 23),
        "ar_condicionado": -abs(temperatura - 22),
        "nada": -abs(temperatura - 25)
    }
    melhor_acao = max(utilidade, key=utilidade.get)
    return f"Ação ideal: {melhor_acao}"

print(utility_based_agent(temperatura))
```

---

### 4. 🥅 **Goal Based Agent**

-   **Goal Based Agents**: Tomam **decisões orientadas por metas**, considerando as consequências de suas ações para atingir seus objetivos, lidando com cenários mais complexos.

> Tem uma **meta explícita**: manter a temperatura ideal.

```python
def goal_based_agent(temperatura, meta=24):
    if temperatura > meta + 1:
        return "Ligar ar-condicionado"
    elif temperatura < meta - 1:
        return "Ligar aquecedor"
    else:
        return "Temperatura dentro da meta"

print(goal_based_agent(temperatura))
```

---

### 5. 📈 **Learning Agent**

-   **Learning Agents**: Se aprimoram ao longo do tempo por meio de **aprendizado por reforço (reinforcement learning)**, ótimos para funções que precisam se adaptar a novos contextos.

> Aprende com o feedback do ambiente. Aqui um **exemplo simplificado**.

```python
historico = []

def learning_agent(temperatura):
    acao = "ventilador" if temperatura > 25 else "nada"
    recompensa = 1 if 22 <= temperatura <= 25 else -1
    historico.append((temperatura, acao, recompensa))
    return f"Ação: {acao}, Recompensa: {recompensa}"

print(learning_agent(temperatura))
```

---

### 6. 🏗️ **Hierarchical Agent**

-   **Hierarchical Agents**: Organizados em camadas, onde um agente de nível superior quebra uma tarefa complexa em tarefas menores e as passa para agentes de nível inferior. O agente superior coleta os resultados e coordena os subordinados para garantir o resultado final.

> Divide tarefas em subtarefas (decide temperatura → decide ação → executa).

```python
def agente_superior(temperatura):
    meta = definir_meta()
    acao = escolher_acao(temperatura, meta)
    return executar_acao(acao)

def definir_meta():
    return 24  # meta de conforto

def escolher_acao(temp, meta):
    if temp > meta:
        return "Ligar ar-condicionado"
    elif temp < meta:
        return "Ligar aquecedor"
    else:
        return "Nada a fazer"

def executar_acao(acao):
    return f"Executando: {acao}"

print(agente_superior(temperatura))
```

---

Se quiser, posso juntar tudo num único script com menu para os alunos testarem interativamente. Deseja isso?
