# Resumo do dia 04

O encontro combina engenharia de prompt com segurança de aplicações que usam LLMs. A ideia é melhorar a qualidade das respostas e observar como entradas maliciosas podem desviar o comportamento de um assistente.

## Técnicas de prompting

**Zero-shot:** descreve a tarefa e os critérios sem exemplos resolvidos. No laboratório, classifica chamados em BAIXA, MEDIA ou ALTA conforme o impacto operacional.

**Few-shot:** acrescenta exemplos de entrada e saída para ensinar um padrão. Os exemplos devem representar situações relevantes sem entregar o gabarito dos casos de avaliação.

**CoT por prompting:** o roteiro demonstra instruções textuais para obter uma resolução explicada. O laboratório pede uma justificativa breve, com hipóteses explícitas. Isso é diferente do raciocínio nativo do modelo. `ThinkingConfig(include_thoughts=True)` solicita resumos de pensamento quando suportados; não expõe todo o processo interno nem garante que haverá resumos em cada resposta.

**Delimitadores:** tags XML ou blocos Markdown ajudam a distinguir instruções de dados. Não garantem que o modelo ignorará instruções maliciosas contidas nesses dados.

No problema das 45 tarefas, falta informar quantas já foram concluídas quando duas pessoas saem. Se foram concluídas C tarefas, a pessoa restante assume 45 − C. Só seriam 45 se nenhuma tivesse sido concluída. Dividir inicialmente por três não resolve essa ambiguidade.

## Campeonato de classificadores

Os dez chamados contrastam urgência emocional com impacto real: letras maiúsculas não tornam uma mudança de foto crítica; uma descrição calma de falha de pagamentos pode indicar alta prioridade. O script compara zero-shot com few-shot acompanhado de justificativa e apresenta o número de acertos.

Não é possível afirmar antecipadamente qual técnica vence. Após executar, observe os erros, especialmente nos casos 9 e 10, e compare o benefício com o aumento do prompt e da saída. Para estimar uso com 50.000 chamados/dia, multiplique a média observada de tokens de entrada e saída por 50.000 e aplique os preços vigentes do modelo. Dez casos são uma demonstração, não uma avaliação suficiente de produção.

## Segurança e mini-CTF

**Prompt injection direta:** o próprio usuário tenta sobrescrever instruções. **Indireta:** a instrução maliciosa chega em documentos, resultados de busca ou outros dados externos. **Prompt leaking:** vazamento das instruções internas. **Jailbreak:** tentativa de contornar restrições do assistente.

O CTF usa um segredo fictício conhecido pelo modelo. O Red Team tenta extraí-lo; o Blue Team combina três camadas: instruções defensivas, tratamento da entrada e inspeção da resposta antes de exibi-la. A rodada mantém dez tentativas, temperatura 0,7 e o modelo indicado no roteiro.

A implementação detecta assinaturas comuns, escapa delimitadores e bloqueia o segredo literal ou formas comuns de representação, como Base64, hexadecimal, inversão e códigos decimais. Isso reduz alguns vazamentos, mas não comprova proteção completa. Um filtro precisa continuar permitindo conversas legítimas; bloquear tudo descaracteriza o desafio.

## Estado da atividade

Código, quiz e material de apoio preparados. Os testes locais verificam comportamento determinístico dos filtros. Experimentos com Gemini, resultados do campeonato, desafios no Lakera, rodadas em grupo, quiz e autoavaliação dependem da execução posterior. Os formulários ficam para você preencher.
