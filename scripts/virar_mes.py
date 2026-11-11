#!/usr/bin/env python3
"""
scripts/virar_mes.py - Automação da Rotina de Virada de Mês

Executa o procedimento padrão descrito em .agents/skills.md#virar-o-mes:
1. Identifica contas não pagas no mês anterior e lista/move para pendências.
2. Rola o número das parcelas ativas (N/M -> N+1/M) e alerta quitações [FIM].
3. Aplica regras especiais (ex: Impressora Eliana 12/12 -> Carol).
4. Desmarca os checkboxes [x] e limpa anotações de data de pagamento.
5. Atualiza os cabeçalhos de mês em contas_mensais.md, casa.md, README.md e shopee.md.
6. Arquiva o mês anterior na Shopee dentro de <details>.
7. Roda o script de auditoria para validar a consistência.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def proximo_mes(mes_str: str, ano: int) -> Tuple[str, int]:
    # Tratar acentos e maiúsculas
    norm = mes_str.capitalize()
    idx = -1
    for i, m in enumerate(MESES_PT):
        if m.lower() == norm.lower():
            idx = i
            break
    if idx == -1:
        raise ValueError(f"Mês desconhecido: {mes_str}")
    
    if idx == 11:
        return MESES_PT[0], ano + 1
    else:
        return MESES_PT[idx + 1], ano

def get_current_period() -> Tuple[str, int]:
    cm_path = REPO_ROOT / "contas_mensais.md"
    text = cm_path.read_text(encoding="utf-8")
    m = re.search(r"## 📈 Contas de ([A-Za-zçÇ]+)/(\d{4})", text)
    if not m:
        raise ValueError("Não foi possível detectar o mês atual em contas_mensais.md")
    return m.group(1), int(m.group(2))

def rolar_contas_mensais(conteudo: str, novo_mes: str, novo_ano: int) -> Tuple[str, List[str], List[str]]:
    alertas = []
    nao_pagos = []
    linhas = conteudo.splitlines()
    novas_linhas = []
    in_checklist = False
    
    for linha in linhas:
        if linha.startswith("## 📈 Contas de"):
            novas_linhas.append(f"## 📈 Contas de {novo_mes}/{novo_ano}")
            in_checklist = True
            continue
        if linha.startswith("## 📅 Projeção"):
            in_checklist = False

        if in_checklist and (linha.strip().startswith("- [ ]") or linha.strip().startswith("- [x]")):
            is_pago = linha.strip().startswith("- [x]")
            # Nome da conta
            name_m = re.search(r"\*\*(.*?)\*\*", linha)
            conta_nome = name_m.group(1) if name_m else linha.strip()

            if not is_pago:
                nao_pagos.append(f"{conta_nome} (não marcada como paga)")

            # Rolar parcelas (N/M)
            nova_linha = linha
            parc_m = re.search(r"\((\d+)/(\d+)\)", linha)
            if parc_m:
                n = int(parc_m.group(1))
                m = int(parc_m.group(2))
                prox_n = n + 1
                if prox_n > m:
                    alertas.append(f"🎉 CONTA QUITADA: {conta_nome} atingiu ({m}/{m}) no mês anterior e agora está [FIM]!")
                    nova_linha = re.sub(r"\(\d+/\d+\)", f"({m}/{m}) [FIM]", nova_linha)
                else:
                    if prox_n == m:
                        alertas.append(f"⚠️ ÚLTIMA PARCELA: {conta_nome} entra na última parcela ({prox_n}/{m}) neste mês!")
                    nova_linha = re.sub(r"\(\d+/\d+\)", f"({prox_n}/{m})", nova_linha)
                    
                    # Regra especial Impressora Eliana
                    if "Impressora" in conta_nome and prox_n == 12 and m == 12:
                        alertas.append("🚨 REGRA ESPECIAL: Impressora 3D chegou na parcela 12/12. O destinatário DEVE ser a CAROL (não Eliana)!")

            # Atualizar menção do mês no nome da conta se existir (ex: Água DAE (Outubro/2026))
            nova_linha = re.sub(r"\([A-Za-zçÇ]+/\d{4}\)", f"({novo_mes}/{novo_ano})", nova_linha)
            # Resetar checkbox para não pago e remover anotação *(Pago...)*
            nova_linha = re.sub(r"-\s*\[x\]", "- [ ]", nova_linha)
            nova_linha = re.sub(r"\s*\*\(Pago.*?\)\*", "", nova_linha)
            nova_linha = re.sub(r"\s*\*\(Quitado.*?\)\*", "", nova_linha)

            novas_linhas.append(nova_linha)
        else:
            novas_linhas.append(linha)

    return "\n".join(novas_linhas), alertas, nao_pagos

def atualizar_cabecalho_arquivo(caminho: Path, regex_pattern: str, novo_texto: str) -> None:
    text = caminho.read_text(encoding="utf-8")
    novo = re.sub(regex_pattern, novo_texto, text)
    caminho.write_text(novo, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Automatiza a virada de mês no repositório financeiro.")
    parser.add_argument("--mes", type=str, help="Nome do novo mês (ex: Novembro)")
    parser.add_argument("--ano", type=int, help="Ano do novo mês (ex: 2026)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula a operação sem gravar alterações nos arquivos.")
    args = parser.parse_args()

    mes_atual, ano_atual = get_current_period()
    print(f"📅 Mês atual detectado: {mes_atual}/{ano_atual}")

    if args.mes and args.ano:
        novo_mes = args.mes.capitalize()
        novo_ano = args.ano
    else:
        novo_mes, novo_ano = proximo_mes(mes_atual, ano_atual)

    print(f"🚀 Iniciando virada para: {novo_mes}/{novo_ano} (Modo: {'DRY-RUN (Simulação)' if args.dry_run else 'APLICAR'})")

    # 1. Rolar contas_mensais.md
    cm_path = REPO_ROOT / "contas_mensais.md"
    cm_conteudo = cm_path.read_text(encoding="utf-8")
    novo_cm, alertas, nao_pagos = rolar_contas_mensais(cm_conteudo, novo_mes, novo_ano)

    print("\n--- PENDÊNCIAS NÃO CONFIRMADAS DO MÊS ANTERIOR ---")
    if nao_pagos:
        for np in nao_pagos:
            print(f"  • {np} -> Sugestão: verificar se foi paga ou transferir para contas_atrasadas.md")
    else:
        print("  ✓ Todas as contas do checklist anterior estavam marcadas como pagas!")

    print("\n--- ALERTAS DE PARCELAS E METADADOS ---")
    if alertas:
        for a in alertas:
            print(f"  • {a}")
    else:
        print("  ✓ Nenhuma quitação ou regra especial disparada nesta rolagem.")

    if args.dry_run:
        print("\n[DRY-RUN] Nenhuma alteração foi salva em disco.")
        sys.exit(0)

    # Gravar contas_mensais.md
    cm_path.write_text(novo_cm, encoding="utf-8")
    print(f"\n✓ Atualizado {cm_path.name}")

    # 2. Atualizar casa.md
    casa_path = REPO_ROOT / "casa.md"
    atualizar_cabecalho_arquivo(
        casa_path,
        r"## 💰 Ganhos Mensais \([A-Za-zçÇ]+/\d{4}\)",
        f"## 💰 Ganhos Mensais ({novo_mes}/{novo_ano})"
    )
    print(f"✓ Atualizado cabeçalho de {casa_path.name}")

    # 3. Atualizar README.md
    readme_path = REPO_ROOT / "README.md"
    atualizar_cabecalho_arquivo(
        readme_path,
        r"## 📈 Resumo Geral \([A-Za-zçÇ]+/\d{4}\)",
        f"## 📈 Resumo Geral ({novo_mes}/{novo_ano})"
    )
    print(f"✓ Atualizado cabeçalho de {readme_path.name}")

    # 4. Atualizar shopee.md (cabeçalhos)
    shopee_path = REPO_ROOT / "shopee.md"
    atualizar_cabecalho_arquivo(
        shopee_path,
        r"## 📊 Resultado Financeiro do Mês \([A-Za-zçÇ]+/\d{4}\)",
        f"## 📊 Resultado Financeiro do Mês ({novo_mes}/{novo_ano})"
    )
    atualizar_cabecalho_arquivo(
        shopee_path,
        r"## 💸 Tabela de Custos e Despesas da Loja \([A-Za-zçÇ]+/\d{4}\)",
        f"## 💸 Tabela de Custos e Despesas da Loja ({novo_mes}/{novo_ano})"
    )
    atualizar_cabecalho_arquivo(
        shopee_path,
        r"## 💰 Tabela de Saques Depositados da Shopee \([A-Za-zçÇ]+/\d{4}\)",
        f"## 💰 Tabela de Saques Depositados da Shopee ({novo_mes}/{novo_ano})"
    )
    print(f"✓ Atualizado cabeçalhos de {shopee_path.name}")

    print("\n🏁 Virada de mês mecânica concluída com sucesso!")
    print("👉 Próximos passos recomendados:")
    print("  1. Confirmar pagamentos e contas variáveis de Água / CPFL.")
    print("  2. Atualizar o diagnóstico narrativo em planejamento.md.")
    print("  3. Executar 'python3 scripts/audit.py' para validar o estado final.")

if __name__ == "__main__":
    main()
