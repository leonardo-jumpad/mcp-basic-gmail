# guardrails_example.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from guardrails import Guard
from guardrails.hub import ValidJson

# Carrega chave da API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Definindo o "Guard" com restrições
guard = Guard.from_string(
    ValidJson(
        output_schema="""
        <rail version="0.1">
            <output>
                <object>
                    <string name="resposta" description="A resposta à pergunta, de forma educada e clara"/>
                </object>
            </output>
            <prompt>
                Você é um assistente educado e respeitoso. Responda sempre de forma educada e nunca use palavrões.
                Dê a resposta no formato JSON com campo 'resposta'.
            </prompt>
        </rail>
        """
    )
)

# Pergunta do usuário
user_input = "Por que a comida está uma merda hoje?"

# Chamada protegida
raw_llm_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_input}]
)

# Validação com o Guard
validated_output, validation_report = guard.parse(raw_llm_response.choices[0].message.content)

# Exibe o resultado
print("✅ Resposta validada:")
print(validated_output)


# O que esse exemplo faz?
# Força o formato de saída ser JSON com uma chave chamada resposta.
# Cria uma camada de verificação que proíbe palavrões ou linguagem inadequada.
# Usa o modelo da OpenAI via API, mas intercepta a resposta antes de entregá-la ao usuário.


# Possíveis extensões
# Impedir o compartilhamento de e-mails ou números de telefone.
# Limitar o tamanho da resposta.
# Garantir que a resposta esteja sempre em português.