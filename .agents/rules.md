# ⚙️ Regras Gerais para a IA

Este arquivo complementa (não substitui) as seções "Regras de Operação" que já existem no final de cada arquivo `.md` do repositório. Ele existe porque, na prática, várias inconsistências já ocorreram por falta de um checklist único de propagação. Leia isto antes de fazer qualquer edição financeira.

---

## 1. Fonte única de verdade (evitar números divergentes)

| Métrica | Onde é calculada (fonte) | Onde é espelhada (deve bater sempre) |
|---|---|---|
| Total Contas Mensais | Soma dos itens **não-variáveis e não-quitados** em `contas_mensais.md` | `casa.md` (Fluxo de Caixa) e `README.md` (Resumo Geral) |
| Saldo Mensal Estimado | Ganhos Totais − Total Contas Mensais | `casa.md` e `README.md` |
| Contas em Atraso | Soma da tabela "Painel de Pendências Ativas" em `contas_atrasadas.md` | `README.md` e `planejamento.md` |
| Dívidas Consolidadas | Soma dos saldos acumulados por credor em `emprestimos.md` | `README.md` |
| Resultado da Loja Shopee | Saques − Custos − Equipamentos em `shopee.md` | Nenhum outro arquivo replica o valor, mas custos com tag 🛒 devem existir também em `contas_mensais.md` |

**Regra prática de eficiência:**
- **Pagamento normal do mês:** Apenas marque `[x] *(Pago DD/MM)*` no checklist de `contas_mensais.md`. NÃO reescrever tabelas em `planejamento.md` nem duplicar texto em histórico.
- **Propagação obrigatória:** Apenas quando envolver amortização de credor (`emprestimos.md` → `README.md`), alteração no painel de atrasos (`contas_atrasadas.md` → `README.md`), custos da Shopee (`contas_mensais.md` → `shopee.md`), ou na virada de mês.

---

## 2. Contas totalmente quitadas saem do cálculo na hora

Quando uma parcela atinge `(N/N)` (última parcela) e é paga:
1. Marcar como `[FIM]` / "Totalmente Quitado".
2. Remover a linha do checklist ativo de `contas_mensais.md` (mover o registro para "Histórico ou Notas Adicionais").
3. **Recalcular o Total Contas Mensais na mesma hora** — não deixar a conta quitada inflando o total (já aconteceu com o Carlos Empréstimo 1).

## 3. Toda conta parcelada precisa de metadados completos

Nunca cadastre uma parcela sem: **valor**, **dia de vencimento**, **data de início (mês/ano da 1ª parcela)** e **número total de parcelas**. Sem isso é impossível saber qual parcela está ativa em cada mês (já aconteceu com Acordo Lis Itaú e Acordo Cartão Ariadne — a IA presumiu incorretamente qual parcela estava ativa).

Sempre que possível, mantenha a contagem de parcela **em sincronia real** com a linha do tempo (mês de início + número da parcela), e não apenas com o que está marcado `[x]` no checklist — o checklist pode ficar desatualizado se ninguém "virar o mês" nele.

## 3.1. Cuidado ao interpretar "pagamento duplo" no mesmo dia

Quando duas parcelas do mesmo acordo são pagas na mesma data, **não presuma automaticamente que a segunda é um adiantamento** ("antecipada"). Investigue: pode ser que a primeira estava simplesmente **em atraso** (não registrada como tal) e a segunda é a parcela normal do mês corrente. Já aconteceu com Carlos 2, Carlos 3, Notebook Ari e Impressora Eliana — a IA rotulou incorretamente como "antecipação" quando na verdade eram atrasos de Agosto/2026 quitados junto com a parcela normal de Setembro/2026. Pergunte ao usuário se não tiver certeza — a diferença muda completamente o diagnóstico (atraso = problema de rastreio; antecipação = decisão proativa do usuário).

## 4. Contas variáveis (Água, CPFL, etc.) precisam de conferência TODO mês, sem exceção

Esse foi o erro mais recorrente: contas variáveis (sem valor fixo) ficaram sem ser rastreadas em meses seguidos porque não há um lembrete automático. Regra:
- Toda conta marcada `[Variável]` deve aparecer no checklist do mês corrente **mesmo que o valor ainda não seja conhecido** (use `R$ [preencher]` ou uma estimativa com `[Confirmar]`).
- Se o usuário não confirmar status de pagamento até a virada do mês, ela **deve** ser movida para `contas_atrasadas.md` — nunca deve simplesmente desaparecer do controle.
- No início de cada nova sessão que envolva "virar o mês", pergunte explicitamente: "as contas variáveis do mês passado (Água, CPFL, etc.) foram pagas?"

## 5. Nunca invente dado crítico — sinalize

Valores ou datas desconhecidos usam `[preencher]` (dado ausente) ou `[Confirmar]` (estimativa a validar). Nunca escreva um valor definitivo sem essas tags quando ele foi estimado por você, e sempre liste esses itens ao final da interação (regra já existente no `README.md`, reforçada aqui).

## 6. Rotina de virada de mês (checklist obrigatório)

Ao perceber que o mês virou (ou que o usuário está tratando o mês seguinte como corrente), execute nesta ordem — ver detalhes em `skills.md#virar-o-mes`:
1. Conferir quais contas fixas/parceladas do mês anterior ficaram sem pagamento confirmado → mover para `contas_atrasadas.md`.
2. Avançar o número de todas as parcelas ativas (usando os metadados da regra 3, não só o checklist).
3. Atualizar o cabeçalho de mês em `contas_mensais.md`, `casa.md` e `README.md` para o novo mês.
4. Recalcular Total Contas Mensais, Saldo Mensal Estimado, Contas em Atraso.
5. Reescrever o diagnóstico de `planejamento.md` para o novo mês (não é só trocar números, é um resumo textual — ver `skills.md`).
6. Rodar uma auditoria de divergências (ver `skills.md#auditoria`) antes de finalizar.

## 7. Custos da Loja Shopee (🛒) são lançados em dois lugares

Qualquer item marcado 🛒 em `contas_mensais.md` (parcela de equipamento, insumo, etc.) deve **também** virar uma linha na tabela de custos de `shopee.md` do mês correspondente, com o resultado do mês recalculado.

## 8. Empréstimos informais (Mãe/Vando) e outras dívidas pessoais

- Toda movimentação em `emprestimos.md` atualiza a tabela de detalhamento **e** o resumo de saldo no topo do arquivo **e** o total em `README.md`.
- Se o usuário mencionar uma promessa de pagamento com prazo (ex: "prometi pagar até o fim de semana"), registre isso como prioridade alta em `planejamento.md`, mesmo que o valor não tenha vencimento fixo formal no sentido de "conta".

## 9. Ao fazer uma auditoria de divergências

Releia TODOS os arquivos do zero (não confie em memória de conversas antigas) e cruze os valores usando a tabela da Regra 1. Ver processo detalhado em `skills.md#auditoria`.

## 10. Validação Mecânica Obrigatória (`scripts/audit.py`)

Após qualquer alteração financeira no repositório (pagamento, inclusão de despesa, alteração de dívida ou virada de mês), **SEMPRE execute no terminal:**
```bash
python3 scripts/audit.py
```
Essa ferramenta determinística valida os cálculos e garante que a tabela de SSOT da Regra 1 está 100% íntegra. Não finalize uma edição sem que o retorno do script seja `STATUS: SUCESSO INTEGRAL`.

