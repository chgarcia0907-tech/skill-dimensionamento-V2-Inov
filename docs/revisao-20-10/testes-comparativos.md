# Testes comparativos da régua: original × v1 × v2

Data: 21/10/2026.

**Versões comparadas**
- **Original**: a skill no commit `39875e8`.
  - Rodada com o fator Claude Code desligado, como nos exemplos.
  - Rodada também com o fator ligado, que é o padrão quando o campo falta.
- **v1**: o patch de 21/10 (`alteracoes-skill-v1.patch`).
- **v2**: o patch corrigido (`alteracoes-skill.patch`).
- **v2 + sugestões**: a v2 com os valores sugeridos para D2 e D3 (tabela no fim).

Como reproduzir:

```
python -I testes/comparar.py testes <caminho>/calcular_faixa.py
```

A pasta `testes/` tem os scripts da original e da v1 e a saída completa em `resultado.json`.

## Correções da v2 sobre a v1

| # | Problema na v1 | Correção na v2 |
|---|---|---|
| 1 | Projeto rejeitado no F0 gerava o PDF inteiro, com um bullet "PARADO" | `gerar_proposta.py` sai com erro, sem gerar PDF, e lista o motivo |
| 2 | Para saber da rejeição, o CN precisava preencher F1 a F6 | O F0 é validado e avaliado antes. Rejeição responde só com o bloco `f0` |
| 3 | O aviso da D3 entrava em todo PDF, e os alertas citavam "D4" e "D5" | Novo campo `avisos_internos`: aparece só no terminal, nunca no PDF. Os alertas não citam mais os códigos D |
| 4 | Rejeição ia para `paradas` com o prefixo "REJEITADO" | `paradas` e `rejeicoes` ficaram separadas |
| 5 | Tecnologia em lacuna do Fathom só somava no F1 | Alerta avisando que a tecnologia pode cair na rejeição do F0 |
| 6 | Formato repetido (`["app","app"]`) somava o extra | Erro de entrada |
| 7 | `prazo_exigido_semanas` aceitava 0 ou negativo | Erro de entrada |
| 8 | `projeto =d.get(` e mensagens de erro com acento quebrado no Windows | Corrigido; o stderr agora sai em UTF-8 |
| 9 | `calcular_faixa.py` saía com código 0 quando o projeto era rejeitado | Sai com código 1 (erro de entrada continua 2) |

Os 6 exemplos dão a mesma venda na v1 e na v2: A 12, B 14, C 18, D 18, PetAgenda 20, PetAgenda PRD 22.

## Casos hipotéticos

Cada célula mostra a **venda em semanas**, com o provável entre parênteses.

| Caso | Original | Original c/ Claude Code | v1 | v2 | v2 + sugestões |
|---|---|---|---|---|---|
| **H1** Marketplace B2B: 6+ perfis, isolado, ERP bidirecional sem doc, RN crítica | 24 (22,5) | 20 (19,6) | 26 (24,5) | 26 (24,5) | **28 (28,0)** ⚠️ >26 |
| **H2** App de campo: offline com sync, troca Mongo→Supabase, demanda vaga, atípico | 24 (22,1) | 20 (19,8) | 24 (23,1) | 24 (23,1) | **28 (26,2)** ⚠️ >26 |
| **H3** SaaS web + PWA + app em 3 bases de código | 20 (18,2) | 16 (15,8) | 20 (19,5) | 20 (19,5) | 22 (20,9) |
| **H4** Site simples com prazo exigido de 4 semanas | 8 | 8 | 8 🚩 | 8 🚩 | 8 🚩 |
| **H5** Cliente exige .NET; só o F0 foi preenchido | **6** (dimensiona um projeto vazio) | 6 | erro de entrada | 🚫 rejeitado | 🚫 rejeitado |
| **H6** = H1 sem `multitenancy`, `lojas` e `formatos` no JSON | **22** (leve, sem aviso) | 20 | erro de entrada | erro de entrada | erro de entrada |
| **H7** Tecnologia exigida em lacuna do Fathom | 12 | 10 | 12 | 12 + alerta F0 | 12 |
| **H8** Formato repetido por engano: `[app, app]` | 12 | 12 | 14 (soma o extra) | erro de entrada | erro de entrada |

### O que os casos mostram

1. **O teto da original escondia semanas.**
   - No H1, o F2 somava 3,5 / 4,5 / 6, e a original cortava para 3,5 / 4 / 4: foram 2 semanas a menos no conservador.
   - No H2, o F1 somava 3,5 / 5 / 6,5 e virava 3,5 / 4 / 4.
   - A v2 mantém a soma e alerta.
2. **A original dimensionava o que não devia.**
   - No H5, deu 6 semanas para um projeto sem nenhum fator preenchido.
   - No H6, esquecer três campos baixou a venda de 24 para 22, sem aviso.
   - A v1 e a v2 recusam os dois casos. A v2 ainda devolve a rejeição do H5 sem exigir o resto.
3. **O que mais move o número é o fator Claude Code.** Com ele ligado (o padrão da original), H1, H2 e H3 saíam 4 semanas mais baratos que na v2.
4. **As mudanças já decididas pesam pouco nos projetos simples.** O formato extra +0,2 e o `bi_sem_doc` com mínimo 4 pesam de verdade só no H1 (+2 semanas) e no H3 (+1,3 no provável, mesma venda).
5. **As sugestões de D2 e D3 são o que separa os projetos pesados.** Elas somam +2 a +4 semanas no H1, H2 e H3 e jogam o H1 e o H2 acima de 26 semanas, fora da faixa calibrada. Nos casos simples (H4, H7), mudam no máximo 0,5 semana.

### Achado novo: o teto do F1 é menor que as próprias linhas

Base (máx. 2,5) + troca de stack (máx. 2) = 4,5, acima do teto de 4. Então **toda troca de stack aceita** (por exemplo, Mongo → Supabase) já dispara o alerta de teto (H7), mesmo sem demanda vaga nem produto atípico. Ou o teto do F1 sobe para ~5, ou o alerta vira ruído. Vale levar junto com a D4.

## Valores usados em "v2 + sugestões"

| Decisão | Provisório (v2) | Sugestão testada |
|---|---|---|
| D2 · 2 a 5 perfis com grandes diferenças | 1,5 / 2 / 2,5 | 2 / 2,5 / 3 |
| D2 · Multitenancy isolado | 1 / 1,5 / 2 | 1,5 / 2 / 3 |
| D2 · RN crítica no F4 | 0,5 / 0,5 / 1 | 1 / 1 / 1,5 |
| D2 · `bi_sem_doc` | 4 / 4 / 5 | 4 / 4,5 / 5,5 |
| 🔎 · `uni_sem_doc` | 1 / 1,5 / 2 | 2 / 2,5 / 3 |
| D3 · Margem sobre o F3 | 0 | +12,5% |

A D1 ficou em +0,2 nas duas colunas.
