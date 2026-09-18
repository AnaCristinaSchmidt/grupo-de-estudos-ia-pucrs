import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from configuracao import criar_cliente

client = criar_cliente()

MODELO_FLASH = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# --- Parte 1: Few-Shot Prompting ---
# Ensinamos o padrao de resposta fornecendo 3 exemplos antes da classificacao real.
prompt_few_shot = """
Classifique a urgencia do chamado de suporte como BAIXA, MEDIA ou ALTA.

Chamado: "O botao de exportar CSV esta com a cor errada."
Urgencia: BAIXA

Chamado: "Nao conseguimos processar pagamentos ha 10 minutos, clientes reclamando."
Urgencia: ALTA

Chamado: "O relatorio mensal demora 5 segundos a mais que o normal para carregar."
Urgencia: MEDIA

Chamado: "O sistema de login caiu para todos os usuarios da empresa."
Urgencia:
"""

response_few_shot = client.models.generate_content(
    model=MODELO_FLASH,
    contents=prompt_few_shot,
)
print("=" * 60)
print("1. FEW-SHOT PROMPTING")
print("=" * 60)
print(f"Resposta do modelo: {(response_few_shot.text or "[Sem resposta textual]").strip()}")

# --- Parte 2: Chain-of-Thought (CoT) Classico via Prompt ---
# Nao requer flag na API: a instrucao "Pense passo a passo" guia o raciocinio.
# O texto intermediario vem misturado diretamente em response.text.
prompt_cot = """
Um trio tem 45 tarefas para dividir igualmente entre si na Sprint.
No meio da sprint, 2 integrantes saem de ferias e sobra so 1 pessoa para terminar
o restante das tarefas do trio inteiro. Quantas tarefas essa pessoa vai assumir sozinha?

Forneça uma justificativa breve e a resposta final. Explicite informações ausentes e não suponha quantas tarefas já foram concluídas.
"""

response_cot = client.models.generate_content(
    model=MODELO_FLASH,
    contents=prompt_cot,
)
print("\n" + "=" * 60)
print("2. CHAIN-OF-THOUGHT CLASSICO VIA PROMPT (Sem flags)")
print("=" * 60)
print((response_cot.text or "[Sem resposta textual]").strip())

# --- Parte 3: Raciocinio Nativo com ThinkingConfig (Recurso do SDK) ---
# Em modelos com suporte nativo a Thinking, o SDK isola o raciocinio interno!
# response.text contera apenas a resposta limpa e assertiva.
config_thinking = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True
    ),
    temperature=0.7
)

response_thinking = client.models.generate_content(
    model=MODELO_FLASH,
    contents=prompt_cot,
    config=config_thinking
)

print("\n" + "=" * 60)
print("3. RACIOCINIO NATIVO DA LLM (ThinkingConfig no SDK)")
print("=" * 60)
print(f"Resposta Final Limpa (response.text):\n{(response_thinking.text or "[Sem resposta textual]").strip()}")

# Inspecionar blocos de pensamento interno estruturados
print("\nResumos de pensamento disponíveis (candidates[0].content.parts):")
parts = []
if response_thinking.candidates and response_thinking.candidates[0].content:
    parts = response_thinking.candidates[0].content.parts or []
for i, part in enumerate(parts, 1):
    if getattr(part, "thought", False) and part.text:
        trecho = part.text.strip().replace("\n", " ")[:160]
        print(f"  [Resumo de pensamento #{i}]: {trecho}...")

if response_thinking.usage_metadata:
    tokens_pensamento = getattr(response_thinking.usage_metadata, "thoughts_token_count", 0)
    print(f"\nTokens de Pensamento dedicados: {tokens_pensamento}")
