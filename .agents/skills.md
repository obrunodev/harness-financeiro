# 🛠️ Skills — Procedimentos Passo a Passo

Procedimentos operacionais para as tarefas mais comuns neste repositório. Sempre que uma tarefa do usuário se encaixar em um desses padrões, siga o passo a passo — ele já incorpora lições de erros passados (ver `rules.md` para o "porquê" de cada regra).

---

## Registrar um pagamento (Rápido e Direto)

1. Localizar a linha da conta no checklist de `contas_mensais.md`.
2. Marcar `[x]` e anotar a data: `*(Pago em DD/MM/AAAA)*`. (Uma única edição pontual; NÃO duplicar texto redundante no rodapé nem em planejamento.md).
3. Apenas se for parcela com a tag 🛒 (Loja Shopee): lançar o custo em `shopee.md` (tabela de custos do mês + recalcular resultado).
4. Apenas se for amortização de dívida pessoal (Mãe/Vando): registrar a saída em `emprestimos.md` e atualizar o saldo consolidado no topo e no `README.md`.
5. Apenas se era a **última parcela** (N/N): aplicar `rules.md#2` (marcar [FIM], remover do checklist ativo e recalcular Total Contas Mensais).
6. Se o valor pago era estimado (`[Confirmar]`): atualizar o valor definitivo e remover a tag.
7. Executar `python3 scripts/audit.py` para validar se as fontes continuam consistentes.

## Registrar uma conta atrasada (venceu sem confirmação de pagamento)

1. Adicionar linha em `contas_atrasadas.md` → tabela "Painel de Pendências Ativas", com Conta, Data de Vencimento, Valor (usar `[Confirmar]` se estimado) e Status.
2. Recalcular o total da tabela.
3. Atualizar `README.md` → indicador "Contas em Atraso".
4. Se `contas_mensais.md` ainda tiver essa conta no checklist do mês, marcar como *"movida para contas_atrasadas.md"* em vez de deixar duas fontes conflitantes.
5. Atualizar `planejamento.md`: atualizar o backlog no Diagnóstico de Caixa, total necessário para zerar e, caso envolva risco crítico (corte de serviço essencial como água/luz, promessa com prazo ou quebra de acordo), registrar ou ajustar no painel "Alertas Críticos & Foco Imediato". (NÃO recriar tabelas espelho de 20 linhas).

## Adicionar uma nova conta recorrente (ex: Internet, Guardinha)

1. Perguntar ao usuário: valor, dia de vencimento, se é fixa ou variável.
2. Adicionar ao checklist de `contas_mensais.md` (seção 1, Despesas Fixas).
3. Recalcular Total Contas Mensais (regra 1 de `rules.md`) e propagar para `casa.md` e `README.md`.
4. Se havia parcelas atrasadas dessa conta específica (ex: meses anteriores não cadastrados), adicionar cada uma individualmente em `contas_atrasadas.md` com sua própria data de vencimento — nunca como "N parcelas" genérico, sempre discriminado por mês.

## Adicionar uma nova conta parcelada / acordo

1. Coletar metadados completos (regra 3 de `rules.md`): valor da parcela, dia de vencimento, mês/ano da 1ª parcela, número total de parcelas.
2. Adicionar ao checklist de `contas_mensais.md` (seção 2) com o número da parcela correspondente ao mês atual (calcular a partir do início, não assumir).
3. Adicionar à tabela de "Projeção de Parcelas" se ela também acompanha esse acordo.
4. Registrar os metadados completos em "Histórico ou Notas Adicionais" para nunca mais perder essa informação.

## Virar o mês {#virar-o-mes}

Ver `rules.md#6` para a visão geral. Agora o procedimento conta com apoio mecânico via script:

1. **Simulação e verificação prévia:**
   Execute no terminal para listar contas pendentes e alertar parcelas em reta final:
   ```bash
   python3 scripts/virar_mes.py --dry-run
   ```
2. **Conferir pendências com o usuário:** para cada item não pago listado na simulação, confirmar se foi pago ou transferir para `contas_atrasadas.md`.
3. **Executar a rolagem mecânica:**
   ```bash
   python3 scripts/virar_mes.py
   ```
   Isso rolará parcelas `(N/M) -> (N+1/M)`, resetará os checkboxes de pagamento e atualizará os cabeçalhos de data automaticamente.
4. **Conferir contas variáveis:** perguntar explicitamente sobre Água, CPFL e qualquer outra `[Variável]` — não deixar passar em branco.
5. **Atualizar tabela de custos da Shopee e Projeção de Parcelas:** se necessário, ajustar a nova linha do mês em `contas_mensais.md` e arquivar o mês anterior em `shopee.md`.
6. **Reescrever `planejamento.md`** para o novo mês: diagnóstico, cenários, tabela de prioridades e plano de ação — não é só editar números, o texto narrativo precisa refletir a realidade atual.
7. **Rodar auditoria mecânica obrigatória:**
   ```bash
   python3 scripts/audit.py
   ```
   Certifique-se de que o script finaliza com sucesso antes de entregar a tarefa.

## Auditoria de divergências {#auditoria}

A auditoria principal é realizada de forma determinística pelo script:
```bash
python3 scripts/audit.py
```
O script verifica automaticamente:
1. Recálculo das fontes e comparação com todos os espelhos do SSOT (`rules.md#1`).
2. Consistência interna de somas em `contas_mensais.md`, `casa.md`, `contas_atrasadas.md`, `emprestimos.md` e `shopee.md`.
3. Alinhamento dos cabeçalhos de Mês/Ano entre todos os arquivos.
4. Varredura completa de tags de incerteza (`[preencher]` e `[Confirmar]`).

Se o script apontar qualquer divergência:
- Identifique a causa raiz e corrija os arquivos correspondentes.
- Reexecute `python3 scripts/audit.py` até obter `STATUS: SUCESSO INTEGRAL`.


## Registrar um empréstimo/dívida pessoal nova (Mãe, Vando, etc.)

1. Adicionar linha na tabela de detalhamento do credor em `emprestimos.md` (Data, Descrição, Tipo, Valor, Saldo Acumulado).
2. Atualizar o "Resumo de Dívidas Ativas" no topo do arquivo (saldo do credor + total geral).
3. Atualizar `README.md` → indicador "Dívidas Consolidadas".
4. Se o usuário mencionar um prazo/promessa de pagamento, adicionar como item de prioridade em `planejamento.md` (mesmo sem vencimento formal de "conta").
