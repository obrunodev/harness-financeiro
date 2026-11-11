# 📊 Painel Financeiro Pessoal

Bem-vindo ao seu sistema de controle financeiro simplificado em Markdown. Este repositório funciona como seu "banco de dados" financeiro, gerenciado de forma inteligente pela IA.

---

## 📌 Links Rápidos

* [📅 Contas Mensais](file:///home/bruno/dev/pessoal/financeiro/contas_mensais.md) — Controle de despesas recorrentes, parcelas e datas de vencimento.
* [🛒 Loja Shopee](file:///home/bruno/dev/pessoal/financeiro/shopee.md) — Controle de faturamento, saques, insumos e lucro líquido da loja.
* [💸 Empréstimos e Dívidas](file:///home/bruno/dev/pessoal/financeiro/emprestimos.md) — Histórico de valores emprestados por credores e saldo consolidado.
* [🚨 Contas em Atraso](file:///home/bruno/dev/pessoal/financeiro/contas_atrasadas.md) — Controle de contas vencidas e pendentes de pagamento.
* [🏠 Casa & Família](file:///home/bruno/dev/pessoal/financeiro/casa.md) — Informações gerais dos membros da família, pets e controle de ganhos mensais.
* [🧠 Planejamento & Conselho](file:///home/bruno/dev/pessoal/financeiro/planejamento.md) — Diagnóstico de fluxo de caixa, cenários e prioridades de pagamento.
* [🎯 Sonhos & Objetivos](file:///home/bruno/dev/pessoal/financeiro/sonhos_e_objetivos.md) — Planejamento e acompanhamento de metas financeiras de curto, médio e longo prazo.

---

## 📈 Resumo Geral (Novembro/2026)

> [!NOTE]
> Os valores abaixo são calculados com base nos lançamentos atuais dos arquivos correspondentes.

| Indicador | Valor Atual | Status / Observação |
| :--- | :---: | :--- |
| **Ganhos Mensais** | `R$ 12.215,00` | Renda familiar total cadastrada em [casa.md](file:///home/bruno/dev/pessoal/financeiro/casa.md) |
| **Total Contas Mensais** | `R$ 5.834,37` | Despesas fixas conhecidas (inclui parcelas e acordos) |
| **Saldo Mensal Estimado** | `R$ 6.380,63` | Saldo líquido estimado para o mês (Ganhos - Contas) |
| **Contas em Atraso** | `R$ 2.871,63` | Total acumulado de contas vencidas e pendentes de pagamento |
| **Dívidas Consolidadas** | `R$ 17.804,90` | Dívida total ativa acumulada (Mãe: `R$ 8.014,90` \| Vando: `R$ 9.790,00`) |

---

## 🤖 Regras Detalhadas para a IA

Além das regras resumidas abaixo, este repositório tem uma pasta [`.agents/`](file:///home/bruno/dev/pessoal/financeiro/.agents/) com o processo operacional completo:
* [`rules.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/rules.md) — regras gerais e tabela de "fonte única de verdade" para evitar números divergentes entre arquivos.
* [`skills.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/skills.md) — passo a passo para tarefas comuns (registrar pagamento, mover conta pra atraso, virar o mês, auditar divergências).
* [`specs.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/specs.md) — formato e tags (`[Variável]`, `[Confirmar]`, `[preencher]`, 🛒, etc.) usados em cada arquivo.
* [`scripts/audit.py`](file:///home/bruno/dev/pessoal/financeiro/scripts/audit.py) — auditoria mecânica e linter determinístico de consistência financeira.
* [`scripts/virar_mes.py`](file:///home/bruno/dev/pessoal/financeiro/scripts/virar_mes.py) — script de automação para rolagem segura de ciclos mensais.

A IA deve consultar essa pasta e rodar a auditoria antes de concluir qualquer edição financeira.

---

## ⚙️ Regras do Sistema (Instruções para a IA)

Sempre que a IA for ler, atualizar ou consolidar as informações deste repositório, ela deve seguir estritamente as seguintes regras:

### 1. Alertas de Dados Ausentes
* **Vencimentos ou Valores em Branco:** Identificar quaisquer itens que possuam `[preencher]`, `[Variável]` ou campos em branco/interrogação.
* **Ação:** Sempre listar esses itens ao final de cada interação para lembrar o usuário de preenchê-los assim que os valores/datas forem confirmados.

### 2. Controle de Parcelas
* Quando uma conta parcelada (ex: `(8/10)`) for paga e o mês virar, a IA deve atualizar a parcela para o próximo mês (ex: `(9/10)`).
* Quando a última parcela for atingida (ex: `(10/10)`), a IA deve alertar o usuário que a conta foi quitada e sugerir sua remoção ou arquivamento para o mês seguinte.
* **Exceção Impressora Eliana:** Na última parcela (`12/12`), o destinatário do pagamento muda de Eliana para **Carol**. A IA deve alertar isso explicitamente ao usuário quando esse vencimento ocorrer.

### 3. Consolidação de Empréstimos (Mãe)
* O saldo consolidado é a soma de todos os empréstimos recebidos menos as amortizações (pagamentos efetuados).
* Toda movimentação de empréstimo deve conter: **Data**, **Valor**, **Origem/Destino** (quem pagou o quê) e **Status**.

### 4. Priorização de Receitas (Reserva da Shopee)
* **Regra de Custeio:** O pagamento das despesas deve priorizar o salário do Bruno e os ganhos de projetos (marcenaria/interiores) da Ariadne.
* **Reserva da Loja:** O lucro da Loja Shopee deve ser protegido e considerado como reserva de segurança ou amortização de dívidas, evitando seu uso para o custeio fixo mensal, a menos que haja um déficit inevitável.
