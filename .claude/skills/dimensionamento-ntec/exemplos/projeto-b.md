# Projeto B — app clínico offline

**Situação:** em execução (45% do prazo em 16/10/2026). **Vendido:** 12 semanas (+1 off), 6 sprints.

## O que era
Calculadora clínica pediátrica que substitui a planilha usada hoje pela cliente. App nativo iOS e Android, publicado nas 2 lojas. Sem login, sem backend, sem banco: 100% offline com cálculo local. Cliente: profissional de saúde com plantões e pouca disponibilidade para validar.

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | App nativo | hand-off |
| Níveis de acesso | nenhum | hand-off |
| Fluxos | 1 com RN específica (motor de cálculo com várias faixas, soluções e alertas) + 1 comum (interface e preferências) | hand-off |
| Offline | local, sem sincronizar → 0 | hand-off |
| RN crítica | sim: erro de cálculo é risco clínico | hand-off |
| Cliente com pouca disponibilidade | sim | hand-off |
| Lojas | app sensível (saúde): revisão mais rigorosa | hand-off |
| Buffer | +10%: time com menos de 6 meses de prática | hand-off |

## Resultado da régua

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0 | 0 | 0 |
| F3 Desenvolvimento (x1,2) | 3,6 | 5,1 | 6,6 |
| F4 Testes com cliente | 2 | 2,5 | 4 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| F6 Lojas (sensível) | 2,5 | 3 | 6 |
| **Faixa (buffer 10%)** | **11** | **15 → vender 16** | **23** |

## Vendido × planejado
Plano do hand-off: imersão (sem. 1–2), motor de cálculo em três etapas (3–6), interface e preferências (7–8), testes, deploy e lojas (9–12).

- O vendido (12) fica **entre o piso (11) e o provável (15)**. Pela regra de fronteira, isso só se sustenta com escopo congelado e cliente disponível. Nenhuma das duas condições vale aqui (uma regra de cálculo ainda estava em aberto e a cliente tem pouca agenda).
- O próprio hand-off registrou os riscos: escopo real maior que o da ficha, prazo encolhido de 4 para 2–3 meses e "não se sustenta com só 1 dev".
- **Resultado final: a confirmar** quando o projeto terminar.

## Lição para a régua
1. **A ficha de qualificação subestimou o escopo** (variáveis clínicas e unidades que só apareceram depois). Por isso o "fluxo com RN específica" exige o documento da regra antes da proposta.
2. **A stack (Expo) foi sugestão comercial, sem validação do time** → regra "o CN não promete stack".
3. Testes, deploy e lojas de um app de saúde em 4 semanas está no limite inferior da régua (F4 + F5 + F6 no mínimo = 5).
