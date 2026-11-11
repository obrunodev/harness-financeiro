# 🤖 Instruções para Agentes de IA (Agent Harness)

Este repositório é um sistema de controle financeiro pessoal gerenciado com assistência de Inteligência Artificial. Para garantir precisão matemática, consistência de dados e prevenir erros históricos do modelo, este ambiente possui um **Agent Harness** composto por regras declarativas e validações mecânicas.

---

## ⚡ Regras Fundamentais de Operação

1. **Consulte o Harness antes de editar:**
   * [`rules.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/rules.md) — Regras de negócio, guardrails e a tabela de **Fonte Única de Verdade (SSOT)**.
   * [`skills.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/skills.md) — Procedimentos operacionais passo a passo para pagamentos, novos acordos e virada de mês.
   * [`specs.md`](file:///home/bruno/dev/pessoal/financeiro/.agents/specs.md) — Convenções de tags (`[Variável]`, `[preencher]`, `[Confirmar]`, 🛒, etc.).

2. **Validação Mecânica Obrigatória:**
   Sempre que alterar qualquer arquivo financeiro (`contas_mensais.md`, `casa.md`, `contas_atrasadas.md`, `emprestimos.md`, `shopee.md`, `planejamento.md` ou `README.md`), você **DEVE executar a ferramenta de auditoria mecânica**:
   ```bash
   python3 scripts/audit.py
   ```
   * Se o script retornar código `0` (`STATUS: SUCESSO INTEGRAL`), a edição foi consistente e validada.
   * Se o script reportar divergências ou código `1`, você deve corrigir a divergência nos arquivos antes de finalizar a resposta ao usuário.

3. **Automação da Virada de Mês:**
   Para virar o ciclo mensal, utilize o script automatizado:
   ```bash
   # Simular a virada e ver alertas de parcelas/atrasos:
   python3 scripts/virar_mes.py --dry-run

   # Executar a rolagem mecânica de parcelas e datas:
   python3 scripts/virar_mes.py
   ```
   Após a virada mecânica, revise contas variáveis (Água, CPFL), atualize o diagnóstico narrativo em `planejamento.md` e rode `python3 scripts/audit.py`.

4. **Tags de Incerteza (Anti-Alucinação):**
   * Nunca invente datas ou valores ausentes. Use `[preencher]` para campos vazios e `[Confirmar]` para estimativas.
   * Ao final de cada resposta, sempre liste itens que ainda precisam de confirmação do usuário.
