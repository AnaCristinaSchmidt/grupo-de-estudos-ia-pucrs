# Dia 04 — Engenharia de prompt e segurança

Implementação baseada no [roteiro oficial](https://github.com/eduardo-de-bastiani/grupo-de-estudos-ia/blob/main/sprint_1_fundamentos_rag/dia_04_prompt_engineering_gandalf.md). A cópia `roteiro_original.md` preserva o material de referência: suas caixas marcadas são do autor, não comprovam execução local.

## Executar

Na raiz do projeto, preencha `GEMINI_API_KEY` no `.env`. A chave está vazia e o arquivo é ignorado pelo Git. `.env.example` é apenas um modelo público.

```powershell
.\.venv\Scripts\python.exe -m pip install -r dia_04/requirements.txt
.\.venv\Scripts\python.exe dia_04/few_shot_cot_lab.py
.\.venv\Scripts\python.exe dia_04/campeonato_classificadores.py
.\.venv\Scripts\python.exe dia_04/ctf_guardian.py
```

O campeonato faz 20 chamadas; o laboratório faz 3; o CTF permite 10 tentativas, incluindo entradas bloqueadas. Essas execuções consomem a cota da API. O roteiro especifica `gemini-3.8-flash`: sua disponibilidade na conta não foi validada. Para os dois primeiros scripts, `GEMINI_MODEL` no `.env` permite selecionar outro modelo disponível. No CTF, o modelo permanece fixo conforme as regras; caso indisponível, alinhe a alteração com o responsável pela atividade.

Sem chave, os três scripts encerram com uma orientação curta. Erros de rede, cota ou modelo são reportados pelo SDK; não são resultados dos experimentos.

## Conteúdo preparado

- `few_shot_cot_lab.py`: few-shot, justificativa textual e resumos de pensamento via `ThinkingConfig`. Resumos não representam acesso integral ao raciocínio interno do modelo.
- `campeonato_classificadores.py`: os dez casos oficiais, dois classificadores e acurácia por correspondência exata; saídas fora do formato contam como erro.
- `ctf_guardian.py`: segredo fictício oficial, temperatura 0,7, modelo fixo e dez tentativas. Inclui instruções defensivas, detecção de padrões, escape XML e filtro de saída.
- `guardrails.py`: exercício bônus e filtro de vazamentos comuns. Rode diretamente para visualizar os exemplos.
- `test_guardrails.py`: testes locais sem API.
- `quiz_dia_04.html`: quiz oficial para abrir no navegador e responder individualmente.
- `RESUMO_DIA_04.md`: síntese dos conceitos e perguntas de discussão.

## Atividades pendentes

Executar os experimentos após cadastrar a chave; registrar acurácia e respostas reais; praticar no [Lakera Agent Breakers](https://gandalf.lakera.ai/agent-breaker); realizar as duas rodadas do CTF em grupo; responder ao quiz e preencher pessoalmente o formulário vinculado no roteiro. Nenhum formulário foi preenchido ou enviado.

Registro sugerido para cada rodada: prompt utilizado, técnica, tentativa, resposta exibida, bloqueio observado e resultado. Não atribua uma recusa ao system prompt com certeza apenas pela resposta; o filtro Python, quando acionado, possui mensagem explícita. Selecione dois ataques para a galeria após os testes.

## Verificação local

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s dia_04 -p "test_*.py"
```

Os filtros são heurísticos: podem bloquear perguntas legítimas e deixar passar ataques inéditos, fragmentados ou codificados de outras formas. XML organiza o conteúdo, mas não cria uma fronteira de segurança. Em produção, segredos devem ficar fora do contexto do modelo; neste CTF sua presença é obrigatória por regra.
