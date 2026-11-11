#!/usr/bin/env python3
"""
scripts/audit.py - Auditoria e Linter Financeiro Automatizado

Valida a integridade, consistência e cálculos de todo o repositório financeiro,
garantindo conformidade estrita com o Single Source of Truth (SSOT) definido em .agents/rules.md.
"""

import sys
import re
from pathlib import Path
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Tuple, Optional, Any

# Cores ANSI para saída no terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).resolve().parent.parent

def parse_currency(val_str: str) -> Optional[Decimal]:
    """Converte strings no formato 'R$ 1.840,00', '- R$ 429,88' ou '1840,00' para Decimal."""
    if not val_str:
        return None
    # Procura explicitamente padrão de moeda: opcional '-', 'R$', número
    m = re.search(r"(-\s*)?R\$\s*([\d\.,]+)", val_str)
    if m:
        is_neg = bool(m.group(1))
        num_str = m.group(2).replace(".", "").replace(",", ".")
        try:
            val = Decimal(num_str)
            return -val if is_neg else val
        except InvalidOperation:
            return None

    # Se não tiver R$, tenta extrair número formatado em moeda brasileira
    m_num = re.search(r"(-\s*)?(\d+(?:\.\d{3})*,\d{2}|\d+,\d{2})", val_str)
    if m_num:
        is_neg = bool(m_num.group(1))
        num_str = m_num.group(2).replace(".", "").replace(",", ".")
        try:
            val = Decimal(num_str)
            return -val if is_neg else val
        except InvalidOperation:
            return None
    return None

def fmt_curr(val: Optional[Decimal]) -> str:
    """Formata Decimal de volta para string brasileira 'R$ X.XXX,XX'."""
    if val is None:
        return "R$ 0,00"
    sign = "- " if val < 0 else ""
    abs_val = abs(val)
    parts = f"{abs_val:.2f}".split(".")
    int_part = parts[0]
    dec_part = parts[1]
    # Inserir pontos de milhar
    formatted_int = ""
    for i, c in enumerate(reversed(int_part)):
        if i > 0 and i % 3 == 0:
            formatted_int = "." + formatted_int
        formatted_int = c + formatted_int
    return f"{sign}R$ {formatted_int},{dec_part}"

class AuditReport:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.successes: List[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def ok(self, msg: str):
        self.successes.append(msg)

    def print_summary(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}📑 RELATÓRIO DA AUDITORIA FINANCEIRA{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")

        if self.successes:
            print(f"{GREEN}{BOLD}✅ CHECAGENS APROVADAS ({len(self.successes)}):{RESET}")
            for s in self.successes:
                print(f"  {GREEN}✓{RESET} {s}")
            print()

        if self.warnings:
            print(f"{YELLOW}{BOLD}⚠️  ALERTAS E PENDÊNCIAS ({len(self.warnings)}):{RESET}")
            for w in self.warnings:
                print(f"  {YELLOW}⚠{RESET} {w}")
            print()

        if self.errors:
            print(f"{RED}{BOLD}❌ ERROS E DIVERGÊNCIAS ({len(self.errors)}):{RESET}")
            for e in self.errors:
                print(f"  {RED}✗{RESET} {e}")
            print()
            print(f"{RED}{BOLD}STATUS: FALHA NA AUDITORIA (Corrija os erros acima){RESET}\n")
            return False
        else:
            print(f"{GREEN}{BOLD}STATUS: SUCESSO INTEGRAL (Todos os números e regras batem perfeitamente!){RESET}\n")
            return True


# ==============================================================================
# PARSERS INDIVIDUAIS
# ==============================================================================

def audit_contas_mensais(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "contas_mensais.md"
    data = {
        "nao_variaveis": Decimal("0.00"),
        "variaveis": Decimal("0.00"),
        "total_geral": Decimal("0.00"),
        "total_pago": Decimal("0.00"),
        "total_pendente": Decimal("0.00"),
        "itens_shopee": [],
        "mes_ano": None
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")

    m_header = re.search(r"## 📈 Contas de ([A-Za-zçÇ]+/\d{4})", text)
    if m_header:
        data["mes_ano"] = m_header.group(1)

    lines = text.splitlines()
    in_checklist = False

    for line in lines:
        if line.startswith("## 📈 Contas de"):
            in_checklist = True
            continue
        if line.startswith("## 📅 Projeção"):
            in_checklist = False

        if in_checklist and (line.strip().startswith("- [ ]") or line.strip().startswith("- [x]")):
            is_checked = line.strip().startswith("- [x]")
            is_variavel = "[Variável]" in line
            is_shopee = "🛒" in line or "[Loja Shopee]" in line

            name_match = re.search(r"\*\*(.*?)\*\*", line)
            name = name_match.group(1) if name_match else line

            val = parse_currency(line)
            if val is None:
                report.error(f"contas_mensais.md: Não foi possível ler o valor na linha: {line.strip()}")
                continue

            data["total_geral"] += val
            if is_variavel:
                data["variaveis"] += val
            else:
                data["nao_variaveis"] += val

            if is_checked:
                data["total_pago"] += val
            else:
                data["total_pendente"] += val

            if is_shopee:
                data["itens_shopee"].append({"nome": name, "valor": val, "linha": line.strip()})

    report.ok(
        f"contas_mensais.md: Não-variáveis = {fmt_curr(data['nao_variaveis'])}, "
        f"Variáveis = {fmt_curr(data['variaveis'])}, Total Previsto = {fmt_curr(data['total_geral'])} "
        f"(Pago: {fmt_curr(data['total_pago'])}, Pendente: {fmt_curr(data['total_pendente'])})"
    )
    return data


def audit_casa(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "casa.md"
    data = {
        "ganhos_total": Decimal("0.00"),
        "ganhos_declarado": None,
        "contas_mensais_declarado": None,
        "saldo_disponivel_declarado": None,
        "mes_ano": None
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")
    m_header = re.search(r"## 💰 Ganhos Mensais \(([A-Za-zçÇ]+/\d{4})\)", text)
    if m_header:
        data["mes_ano"] = m_header.group(1)

    # 1. Tabela de ganhos
    in_ganhos = False
    ganhos_sum = Decimal("0.00")
    for line in text.splitlines():
        if "## 💰 Ganhos Mensais" in line:
            in_ganhos = True
            continue
        if in_ganhos and line.startswith("## "):
            in_ganhos = False

        if in_ganhos and line.strip().startswith("|") and not line.strip().startswith("| Membro") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 3:
                membro = cols[0]
                val = parse_currency(cols[2])
                if "TOTAL DE GANHOS" in membro:
                    data["ganhos_declarado"] = val
                elif val is not None:
                    ganhos_sum += val

    data["ganhos_total"] = ganhos_sum

    # 2. Fluxo de Caixa Mensal Consolidado
    in_fluxo = False
    for line in text.splitlines():
        if "## 📊 Fluxo de Caixa Mensal Consolidado" in line:
            in_fluxo = True
            continue
        if in_fluxo and line.startswith("## "):
            in_fluxo = False

        if in_fluxo and line.strip().startswith("|") and not line.strip().startswith("| Categoria") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                cat = cols[0].replace("*", "").strip()
                val = parse_currency(cols[1])
                if "Contas Mensais" in cat:
                    data["contas_mensais_declarado"] = val
                elif "Saldo Disponível" in cat:
                    data["saldo_disponivel_declarado"] = val

    if data["ganhos_declarado"] != data["ganhos_total"]:
        report.error(
            f"casa.md: Soma dos ganhos na tabela ({fmt_curr(data['ganhos_total'])}) "
            f"diverge do TOTAL DE GANHOS declarado ({fmt_curr(data['ganhos_declarado'])})"
        )
    else:
        report.ok(f"casa.md: Ganhos totais somam perfeitamente {fmt_curr(data['ganhos_total'])}")

    if data["ganhos_total"] is not None and data["contas_mensais_declarado"] is not None and data["saldo_disponivel_declarado"] is not None:
        calc_saldo = data["ganhos_total"] - data["contas_mensais_declarado"]
        if calc_saldo != data["saldo_disponivel_declarado"]:
            report.error(
                f"casa.md: Cálculo do Saldo Disponível incorreto: "
                f"{fmt_curr(data['ganhos_total'])} - {fmt_curr(data['contas_mensais_declarado'])} "
                f"= {fmt_curr(calc_saldo)}, mas está declarado {fmt_curr(data['saldo_disponivel_declarado'])}"
            )
        else:
            report.ok(f"casa.md: Fluxo de caixa interno consistente ({fmt_curr(calc_saldo)})")

    return data


def audit_contas_atrasadas(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "contas_atrasadas.md"
    data = {
        "total_calculado": Decimal("0.00"),
        "total_declarado": None,
        "itens": []
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")
    in_painel = False

    for line in text.splitlines():
        if "## 📊 Painel de Pendências Ativas" in line:
            in_painel = True
            continue
        if in_painel and line.startswith("## "):
            in_painel = False

        if in_painel and line.strip().startswith("|") and not line.strip().startswith("| Conta") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 3:
                conta = cols[0]
                val = parse_currency(cols[2])
                if "TOTAL EM ATRASO" in conta:
                    data["total_declarado"] = val
                elif val is not None:
                    data["total_calculado"] += val
                    data["itens"].append({"conta": conta, "valor": val})

    if data["total_declarado"] != data["total_calculado"]:
        report.error(
            f"contas_atrasadas.md: Soma das pendências ativas ({fmt_curr(data['total_calculado'])}) "
            f"diverge do TOTAL EM ATRASO declarado ({fmt_curr(data['total_declarado'])})"
        )
    else:
        report.ok(f"contas_atrasadas.md: Total em atraso soma perfeitamente {fmt_curr(data['total_calculado'])}")

    return data


def audit_emprestimos(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "emprestimos.md"
    data = {
        "credores_resumo": {},
        "total_geral_declarado": None,
        "total_geral_calculado": Decimal("0.00")
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")

    # 1. Resumo no topo
    in_resumo = False
    for line in text.splitlines():
        if "## 📊 Resumo de Dívidas Ativas" in line:
            in_resumo = True
            continue
        if in_resumo and line.startswith("## "):
            in_resumo = False

        if in_resumo and line.strip().startswith("|") and not line.strip().startswith("| Credor") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                credor = cols[0].replace("*", "").strip()
                val = parse_currency(cols[1])
                if "TOTAL GERAL" in credor:
                    data["total_geral_declarado"] = val
                elif val is not None:
                    data["credores_resumo"][credor] = val
                    data["total_geral_calculado"] += val

    if data["total_geral_declarado"] != data["total_geral_calculado"]:
        report.error(
            f"emprestimos.md: Soma dos credores no topo ({fmt_curr(data['total_geral_calculado'])}) "
            f"diverge do TOTAL GERAL declarado ({fmt_curr(data['total_geral_declarado'])})"
        )
    else:
        report.ok(f"emprestimos.md: Total geral no topo consistente ({fmt_curr(data['total_geral_calculado'])})")

    # 2. Verificar detalhamento de cada credor (saldo acumulado final)
    for credor, saldo_resumo in data["credores_resumo"].items():
        pattern = rf"##\s*.*?{credor}"
        m_section = re.search(pattern, text)
        if m_section:
            section_start = m_section.start()
            section_text = text[section_start:]
            next_sec = re.search(r"\n## ", section_text[1:])
            if next_sec:
                section_text = section_text[:next_sec.start()+1]

            last_balance = None
            for s_line in section_text.splitlines():
                if s_line.strip().startswith("|") and not s_line.strip().startswith("| Data") and not s_line.strip().startswith("| :---"):
                    cols = [c.strip() for c in s_line.split("|")[1:-1]]
                    if len(cols) >= 5:
                        bal_val = parse_currency(cols[4])
                        if bal_val is not None:
                            last_balance = bal_val

            if last_balance is not None and last_balance != saldo_resumo:
                report.error(
                    f"emprestimos.md: Saldo final na tabela do credor '{credor}' ({fmt_curr(last_balance)}) "
                    f"diverge do saldo no resumo do topo ({fmt_curr(saldo_resumo)})"
                )
            elif last_balance is not None:
                report.ok(f"emprestimos.md: Detalhamento do credor '{credor}' bate com o resumo ({fmt_curr(last_balance)})")

    return data


def audit_shopee(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "shopee.md"
    data = {
        "resultado_real_declarado": None,
        "resultado_real_calculado": None,
        "custos_previstos_declarado": None,
        "custos_previstos_calculado": Decimal("0.00"),
        "saques_declarado": None,
        "itens_custo": []
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")

    # 1. Indicadores do topo
    in_resultado = False
    saques = Decimal("0.00")
    custos_op = Decimal("0.00")
    equip = Decimal("0.00")
    acordos = Decimal("0.00")

    for line in text.splitlines():
        if "## 📊 Resultado Financeiro do Mês" in line:
            in_resultado = True
            continue
        if in_resultado and line.startswith("## "):
            in_resultado = False

        if in_resultado and line.strip().startswith("|") and not line.strip().startswith("| Indicador") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                ind = cols[0].replace("*", "").strip()
                val = parse_currency(cols[1])
                if val is not None:
                    if "Saques Depositados" in ind:
                        saques = val
                    elif "Custos Operacionais Aportados" in ind:
                        custos_op = val
                    elif "Parcelas de Equipamentos" in ind:
                        equip = val
                    elif "Acordos" in ind:
                        acordos = val
                    elif "Resultado Real Atual" in ind:
                        data["resultado_real_declarado"] = val

    # Resultado = Saques - Custos - Equipamentos - Acordos
    calc_res = saques - custos_op - equip - acordos
    data["resultado_real_calculado"] = calc_res

    if data["resultado_real_declarado"] is not None and data["resultado_real_declarado"] != calc_res:
        report.error(
            f"shopee.md: Cálculo do Resultado Real Atual ({fmt_curr(calc_res)}) "
            f"diverge do declarado no painel ({fmt_curr(data['resultado_real_declarado'])})"
        )
    else:
        report.ok(f"shopee.md: Resultado Real Atual consistente ({fmt_curr(calc_res)})")

    # 2. Tabela de Custos e Despesas
    in_custos = False
    for line in text.splitlines():
        if "## 💸 Tabela de Custos e Despesas da Loja" in line:
            in_custos = True
            continue
        if in_custos and line.startswith("## "):
            in_custos = False

        if in_custos and line.strip().startswith("|") and not line.strip().startswith("| Data") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 4:
                item_desc = cols[2]
                val = parse_currency(cols[3])
                if "TOTAL CUSTOS PREVISTOS" in cols[0] or "TOTAL CUSTOS" in cols[0]:
                    data["custos_previstos_declarado"] = val
                elif val is not None:
                    data["custos_previstos_calculado"] += val
                    data["itens_custo"].append({"desc": item_desc, "valor": val})

    if data["custos_previstos_declarado"] is not None:
        if data["custos_previstos_declarado"] != data["custos_previstos_calculado"]:
            report.error(
                f"shopee.md: Soma da tabela de custos ({fmt_curr(data['custos_previstos_calculado'])}) "
                f"diverge do TOTAL CUSTOS PREVISTOS ({fmt_curr(data['custos_previstos_declarado'])})"
            )
        else:
            report.ok(f"shopee.md: Soma da tabela de custos bate com o total ({fmt_curr(data['custos_previstos_calculado'])})")

    return data


def audit_readme(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "README.md"
    data = {
        "ganhos": None,
        "contas_mensais": None,
        "saldo_mensal": None,
        "contas_atraso": None,
        "dividas_consolidadas": None,
        "mes_ano": None
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")
    m_header = re.search(r"## 📈 Resumo Geral \(([A-Za-zçÇ]+/\d{4})\)", text)
    if m_header:
        data["mes_ano"] = m_header.group(1)

    for line in text.splitlines():
        if line.strip().startswith("|") and not line.strip().startswith("| Indicador") and not line.strip().startswith("| :---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                indicador = cols[0].replace("*", "").strip()
                val = parse_currency(cols[1])
                if "Ganhos Mensais" in indicador:
                    data["ganhos"] = val
                elif "Total Contas Mensais" in indicador:
                    data["contas_mensais"] = val
                elif "Saldo Mensal Estimado" in indicador:
                    data["saldo_mensal"] = val
                elif "Contas em Atraso" in indicador:
                    data["contas_atraso"] = val
                elif "Dívidas Consolidadas" in indicador:
                    data["dividas_consolidadas"] = val

    report.ok("README.md: Indicadores do painel lidos com sucesso")
    return data


def audit_planejamento(report: AuditReport) -> Dict[str, Any]:
    path = REPO_ROOT / "planejamento.md"
    data = {
        "contas_atrasadas": None,
        "contas_nao_variaveis": None,
        "mes_ano": None
    }
    if not path.exists():
        report.error(f"Arquivo não encontrado: {path}")
        return data

    text = path.read_text(encoding="utf-8")
    m_header = re.search(r"## 🔍 Diagnóstico de Caixa Atual \(([A-Za-zçÇ]+/\d{4})\)", text)
    if m_header:
        data["mes_ano"] = m_header.group(1)

    m_atraso = re.search(r"1\.\s*\*\*Contas Atrasadas.*?\*\*:\s*`([^`]+)`", text)
    if m_atraso:
        data["contas_atrasadas"] = parse_currency(m_atraso.group(1))

    m_fixas = re.search(r"Despesas Fixas e Parceladas não-variáveis:\s*`([^`]+)`", text)
    if m_fixas:
        data["contas_nao_variaveis"] = parse_currency(m_fixas.group(1))

    report.ok("planejamento.md: Diagnóstico e obrigações lidos com sucesso")
    return data


# ==============================================================================
# AUDITORIA CRUZADA (SSOT - REGRA 1)
# ==============================================================================

def cross_audit_ssot(
    report: AuditReport,
    mensais: Dict[str, Any],
    casa: Dict[str, Any],
    atrasadas: Dict[str, Any],
    emprestimos: Dict[str, Any],
    shopee: Dict[str, Any],
    readme: Dict[str, Any],
    planejamento: Dict[str, Any]
):
    print(f"\n{CYAN}{BOLD}--- AUDITORIA DE CRUZA DE DADOS (SSOT - Regra 1) ---{RESET}")

    # 1. Total Contas Mensais (Não-variáveis e não-quitadas)
    fonte_cm = mensais["nao_variaveis"]
    if casa["contas_mensais_declarado"] != fonte_cm:
        report.error(
            f"DIVERGÊNCIA em 'Total Contas Mensais': contas_mensais.md fonte ({fmt_curr(fonte_cm)}) "
            f"!= casa.md ({fmt_curr(casa['contas_mensais_declarado'])})"
        )
    else:
        report.ok(f"SSOT: Total Contas Mensais bate entre contas_mensais.md e casa.md ({fmt_curr(fonte_cm)})")

    if readme["contas_mensais"] != fonte_cm:
        report.error(
            f"DIVERGÊNCIA em 'Total Contas Mensais': contas_mensais.md fonte ({fmt_curr(fonte_cm)}) "
            f"!= README.md ({fmt_curr(readme['contas_mensais'])})"
        )
    else:
        report.ok(f"SSOT: Total Contas Mensais bate entre contas_mensais.md e README.md ({fmt_curr(fonte_cm)})")

    if planejamento["contas_nao_variaveis"] is not None and planejamento["contas_nao_variaveis"] != fonte_cm:
        report.error(
            f"DIVERGÊNCIA em 'Total Contas Mensais': contas_mensais.md fonte ({fmt_curr(fonte_cm)}) "
            f"!= planejamento.md ({fmt_curr(planejamento['contas_nao_variaveis'])})"
        )
    elif planejamento["contas_nao_variaveis"] is not None:
        report.ok(f"SSOT: Total Contas Mensais bate com planejamento.md ({fmt_curr(fonte_cm)})")

    # 2. Ganhos Mensais
    fonte_ganhos = casa["ganhos_total"]
    if readme["ganhos"] != fonte_ganhos:
        report.error(
            f"DIVERGÊNCIA em 'Ganhos Mensais': casa.md fonte ({fmt_curr(fonte_ganhos)}) "
            f"!= README.md ({fmt_curr(readme['ganhos'])})"
        )
    else:
        report.ok(f"SSOT: Ganhos Mensais bate entre casa.md e README.md ({fmt_curr(fonte_ganhos)})")

    # 3. Saldo Mensal Estimado
    saldo_esperado = fonte_ganhos - fonte_cm
    if readme["saldo_mensal"] != saldo_esperado:
        report.error(
            f"DIVERGÊNCIA em 'Saldo Mensal Estimado': calculado ({fmt_curr(saldo_esperado)}) "
            f"!= README.md ({fmt_curr(readme['saldo_mensal'])})"
        )
    else:
        report.ok(f"SSOT: Saldo Mensal Estimado bate em README.md ({fmt_curr(saldo_esperado)})")

    # 4. Contas em Atraso
    fonte_atraso = atrasadas["total_calculado"]
    if readme["contas_atraso"] != fonte_atraso:
        report.error(
            f"DIVERGÊNCIA em 'Contas em Atraso': contas_atrasadas.md fonte ({fmt_curr(fonte_atraso)}) "
            f"!= README.md ({fmt_curr(readme['contas_atraso'])})"
        )
    else:
        report.ok(f"SSOT: Contas em Atraso bate entre contas_atrasadas.md e README.md ({fmt_curr(fonte_atraso)})")

    if planejamento["contas_atrasadas"] is not None and planejamento["contas_atrasadas"] != fonte_atraso:
        report.error(
            f"DIVERGÊNCIA em 'Contas em Atraso': contas_atrasadas.md fonte ({fmt_curr(fonte_atraso)}) "
            f"!= planejamento.md ({fmt_curr(planejamento['contas_atrasadas'])})"
        )
    elif planejamento["contas_atrasadas"] is not None:
        report.ok(f"SSOT: Contas em Atraso bate com planejamento.md ({fmt_curr(fonte_atraso)})")

    # 5. Dívidas Consolidadas
    fonte_dividas = emprestimos["total_geral_calculado"]
    if readme["dividas_consolidadas"] != fonte_dividas:
        report.error(
            f"DIVERGÊNCIA em 'Dívidas Consolidadas': emprestimos.md fonte ({fmt_curr(fonte_dividas)}) "
            f"!= README.md ({fmt_curr(readme['dividas_consolidadas'])})"
        )
    else:
        report.ok(f"SSOT: Dívidas Consolidadas bate entre emprestimos.md e README.md ({fmt_curr(fonte_dividas)})")

    # 6. Alinhamento de cabeçalhos de Mês/Ano
    meses = {
        "contas_mensais.md": mensais["mes_ano"],
        "casa.md": casa["mes_ano"],
        "README.md": readme["mes_ano"],
        "planejamento.md": planejamento["mes_ano"]
    }
    referencia_mes = mensais["mes_ano"]
    for arquivo, mes in meses.items():
        if mes and referencia_mes and mes != referencia_mes:
            report.error(f"DIVERGÊNCIA DE MÊS: {arquivo} tem '{mes}', enquanto contas_mensais.md tem '{referencia_mes}'")
        elif mes:
            report.ok(f"Cabeçalho de mês sincronizado em {arquivo}: {mes}")


# ==============================================================================
# AUDITORIA DE TAGS PENDENTES ([preencher] e [Confirmar])
# ==============================================================================

def check_pending_tags(report: AuditReport):
    print(f"\n{CYAN}{BOLD}--- VERIFICAÇÃO DE DADOS AUSENTES E ESTIMATIVAS ---{RESET}")
    md_files = sorted(REPO_ROOT.glob("*.md"))
    total_preencher = 0
    total_confirmar = 0

    for path in md_files:
        # Ignora arquivos puramente documentais de regras/índice
        if path.name in ("README.md", "AGENTS.md"):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, 1):
            if "[preencher]" in line:
                total_preencher += 1
                report.warn(f"{path.name}:{idx} possui campo ausente [preencher]: {line.strip()[:80]}")
            if "[Confirmar]" in line:
                total_confirmar += 1
                report.warn(f"{path.name}:{idx} possui estimativa a [Confirmar]: {line.strip()[:80]}")

    if total_preencher == 0 and total_confirmar == 0:
        report.ok("Nenhum campo com [preencher] ou [Confirmar] pendente no repositório.")
    else:
        report.ok(f"Varredura concluída: {total_preencher} [preencher] e {total_confirmar} [Confirmar] encontrados.")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    report = AuditReport()

    print(f"{BOLD}{CYAN}🔍 Executando auditoria financeira em {REPO_ROOT}...{RESET}\n")

    mensais = audit_contas_mensais(report)
    casa = audit_casa(report)
    atrasadas = audit_contas_atrasadas(report)
    emprestimos = audit_emprestimos(report)
    shopee = audit_shopee(report)
    readme = audit_readme(report)
    planejamento = audit_planejamento(report)

    cross_audit_ssot(report, mensais, casa, atrasadas, emprestimos, shopee, readme, planejamento)
    check_pending_tags(report)

    success = report.print_summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
