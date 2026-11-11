# 🚨 Contas em Atraso

Este arquivo serve como um banco de dados e controle de fluxo para todas as despesas (fixas ou parceladas) que já passaram da data de vencimento e ainda não foram quitadas.

---

## 📊 Painel de Pendências Ativas

| Conta / Descrição | Data Vencimento | Valor original | Status / Observações |
| :--- | :---: | :---: | :--- |
| **DAS (MEI) - Atrasados (desde 08/2025)** | [Vários] | `R$ 1.100,00` | Estimado (11 parcelas de R$ 100,00 com juros/multas) |
| **DAS (MEI) - Julho/2026** | 20/07/2026 | `R$ 80,00` | Pendente de pagamento |
| **DAS (MEI) - Setembro/2026** | 20/09/2026 | `R$ 80,00` | Pendente de pagamento |
| **Academia Bruno (Setembro/2026)** | [Setembro] | `R$ 160,00` | Mensalidade de Setembro pendente |
| **Água DAE (Outubro/2026)** | 10/10/2026 | `R$ 150,00` [Confirmar] | Pendente de confirmação/pagamento |
| **DAS (MEI) - Outubro/2026** | 20/10/2026 | `R$ 80,00` | Pendente de pagamento |
| **Acordo Lis Itaú Ariadne (3/11)** | 22/10/2026 | `R$ 56,63` | Pendente de confirmação (débito aut.) |
| **Energia CPFL (Outubro/2026)** | 24/10/2026 | `R$ 400,00` [Confirmar] | Pendente de confirmação/pagamento |
| **Carlos Empréstimo 2 (9/10)** | 30/10/2026 | `R$ 765,00` | Parcela de Outubro pendente |
| **TOTAL EM ATRASO** | - | **`R$ 2.871,63`** | - |

---

## ✅ Histórico de Contas Quitadas (Atrasos)

| Conta / Descrição | Data Vencimento | Valor Pago | Data de Pagamento / Observações |
| :--- | :---: | :---: | :--- |
| **Energia CPFL (Setembro/2026)** | 24/09/2026 | `R$ 400,00` [Confirmar] | Pago em 20/10/2026 |
| **Acordo Lis Itaú Ariadne (2/11)** | 22/09/2026 | `R$ 58,20` | Débito automático "Crediario Autom 02/11" em 06/10/2026 (orig. R$ 56,63 + juros) |
| **Energia CPFL (Julho/2026)** | 24/07/2026 | `R$ 478,14` | Pago em 25/08/2026 |
| **DAE (Água) - Julho/2026** | 09/07/2026 | `R$ 144,91` | Pago em Setembro/2026 |
| **DAE (Água) - Agosto/2026** | 09/08/2026 | `R$ 150,00` | Pago em Setembro/2026 |
| **DAE (Água) - Setembro/2026** | 09/09/2026 | `R$ 150,00` | Pago em Setembro/2026 |
| **Guardinha - Agosto/2026** | 16/08/2026 | `R$ 40,00` | Pago em Setembro/2026 |
| **Guardinha - Setembro/2026** | 16/09/2026 | `R$ 40,00` | Pago em Setembro/2026 |

---

## ⚙️ Regras de Operação (Instruções para a IA)
1. **Lançamento de Atraso:** Quando um mês virar ou uma conta vencer no [contas_mensais.md](file:///home/bruno/dev/pessoal/financeiro/contas_mensais.md) e não estiver marcada como paga, ela deve ser transferida para este arquivo.
2. **Baixa de Pagamento:** Assim que uma conta em atraso for quitada, ela deve ser removida desta lista (ou movida para um histórico de pagamentos atrasados ao final deste arquivo) e o painel de **Resumo Geral** no [README.md](file:///home/bruno/dev/pessoal/financeiro/README.md) deve ser atualizado.
