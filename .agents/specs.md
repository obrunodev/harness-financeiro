# 📐 Specs — Formato dos Arquivos e Tags

Referência rápida de convenções usadas nos arquivos `.md` deste repositório. Mantenha esses formatos consistentes em qualquer edição.

---

## Tags usadas nos valores/itens

| Tag | Significado | Onde aparece |
|---|---|---|
| `[Variável]` | O valor muda todo mês (ex: água, luz) — precisa ser conferido mensalmente, nunca copiado do mês anterior sem checar | `contas_mensais.md` |
| `[preencher]` | Dado ausente (valor ou data) que o usuário ainda não informou | Qualquer arquivo |
| `[Confirmar]` | Valor estimado pela IA, ainda não validado pelo usuário | Qualquer arquivo |
| 🛒 [Loja Shopee] | O gasto/parcela pertence ao negócio da loja — deve ser espelhado em `shopee.md` | `contas_mensais.md` |
| `(N/M)` | Parcela N de um total de M parcelas | `contas_mensais.md` |
| `[FIM]` | Última parcela atingida / conta totalmente quitada | `contas_mensais.md` |
| `[PAGO]` / `[PAGO DD/MM]` | Marcação de status na tabela de projeção de parcelas (independente do checklist) | `contas_mensais.md` |
| `[x]` / `[ ]` | Checkbox de pago/pendente no checklist mensal | `contas_mensais.md` |

---

## `contas_mensais.md`

- **Cabeçalho de seção principal:** `## 📈 Contas de MÊS/AAAA` — deve sempre refletir o mês corrente.
- **Checklist (seção 1 e 2):** cada linha precisa ter: nome da conta, valor, dia de vencimento. Parcelas precisam do formato `(N/M)`. Ao pagar, apenas marcar `[x] *(Pago em DD/MM)*`.
- **Tabela de Projeção de Parcelas:** uma coluna por acordo parcelado ativo, uma linha por mês, até o mês de término (`[FIM]`).
- **Seção "Informações Gerais & Pendências":** lista concisa de itens com `[preencher]`.
- **Seção "Metadados dos Acordos e Regras Fixas":** guarda exclusivamente os metadados fixos dos acordos (início, total de parcelas, destinatários especiais). **PROIBIDO duplicar texto aqui ao pagar contas rotineiras** — o checklist já é a fonte do pagamento.

## `contas_atrasadas.md`

- Tabela "Painel de Pendências Ativas": uma linha por conta vencida, discriminada individualmente por mês de vencimento.
- Quando uma conta atrasada for quitada, mover para o histórico de quitadas.

## `casa.md`

- Ganhos: uma linha por membro/fonte de renda + linha de TOTAL.
- Fluxo de Caixa Mensal Consolidado: Ganhos Totais − Total Contas Mensais (fixas orçadas).
- Saldo Real em Conta: dinheiro disponível hoje.

## `shopee.md`

- Estrutura por mês: seção do mês ativa no topo + histórico de meses anteriores arquivados em `<details>`.
- Todo custo com tag 🛒 em `contas_mensais.md` deve ter linha correspondente aqui.

## `emprestimos.md`

- Uma tabela de detalhamento por credor com coluna de Saldo Acumulado.
- Resumo no topo reflete o saldo mais recente de cada credor + total geral.

## `planejamento.md`

- **Modelo Enxuto e Estratégico:** **PROIBIDO recriar tabela espelho de todas as contas normais** (o acompanhamento rotineiro pertence a `contas_mensais.md`).
- Estrutura:
  1. Diagnóstico de Caixa e Resumo de Obrigações (totais consolidados).
  2. Projeção de Cenários.
  3. Painel de **Alertas Críticos & Foco Imediato** (apenas contas com risco real de corte de serviço, quebra de renegociação ou promessas de prazo).
  4. Plano de Ação Estratégico.
- Pagamentos normais que não sejam alertas críticos **NÃO devem provocar edição neste arquivo**.

## `README.md`

- É o painel-índice — nunca deve ter números que não existam em outro arquivo-fonte. Se um valor aparece aqui, ele tem que vir de algum lugar rastreável.
