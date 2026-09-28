import os
from enum import Enum

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, Field, field_validator

load_dotenv()
MODEL = "gemini-3.5-flash-lite"


class Severidade(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"


class ItemAuditoria(BaseModel):
    tabela: str
    coluna: str
    anomalia_detectada: str
    registros_afetados: int
    severidade: Severidade

    @field_validator("registros_afetados")
    @classmethod
    def nao_negativo(cls, valor: int) -> int:
        if valor < 0:
            raise ValueError("registros_afetados não pode ser negativo")
        return valor

    @field_validator("tabela", "coluna", "anomalia_detectada")
    @classmethod
    def nao_vazio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("o campo não pode estar vazio")
        return valor


class RelatorioAuditoria(BaseModel):
    base_analisada: str
    itens: list[ItemAuditoria]
    resumo: str = Field(description="Resumo executivo em até 2 frases")
    requer_acao_imediata: bool


RELATORIO_TEXTO = """
Auditoria da base de vendas (vendas.db). Na tabela clientes, a coluna email esta nula
em 37 registros, o que impede o envio de notas fiscais. Na tabela pedidos, a coluna
valor_total tem 4 pedidos com valores negativos, provavel erro de estorno. Na tabela
produtos, a coluna descricao tem 120 registros com texto duplicado, sem impacto operacional.
"""


if __name__ == "__main__":
    # Teste local: não chama o Gemini.
    try:
        ItemAuditoria(
            tabela="clientes",
            coluna="email",
            anomalia_detectada="Valor nulo",
            registros_afetados=-5,
            severidade=Severidade.ALTA,
        )
    except ValueError as erro:
        print("Validador funcionando: valor negativo rejeitado.")
        print(erro)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY no arquivo .env")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"Estruture o relatório de auditoria abaixo.\n{RELATORIO_TEXTO}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RelatorioAuditoria,
            ),
        )
    except errors.ServerError as erro:
        print(f"Falha no serviço do Gemini: {erro}")
        raise SystemExit(1) from None

    relatorio = response.parsed
    if not isinstance(relatorio, RelatorioAuditoria):
        raise ValueError("O Gemini não retornou um RelatorioAuditoria válido.")

    print(f"\nBase analisada: {relatorio.base_analisada}")
    for item in relatorio.itens:
        print(
            f"[{item.severidade.value}] "
            f"{item.tabela}.{item.coluna}: "
            f"{item.registros_afetados} registros"
        )
    print(f"Resumo: {relatorio.resumo}")
    print(f"Requer ação imediata: {relatorio.requer_acao_imediata}")