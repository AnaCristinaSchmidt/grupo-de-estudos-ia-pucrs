"""Configuração comum, sem exibir credenciais."""
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


def criar_cliente():
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
    chave = os.getenv('GEMINI_API_KEY', '').strip()
    if not chave:
        raise SystemExit('Preencha GEMINI_API_KEY no arquivo .env da raiz antes de executar.')
    return genai.Client(api_key=chave)
