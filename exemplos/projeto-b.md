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
| Cliente com pouca disponibilidade | sim (fator removido em 20/10/2026: não soma mais) | hand-off |
| Lojas | app sensível (saúde): revisão mais rigorosa | hand-off |

## Resultado da régua

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0 | 0 | 0 |
| F3 Desenvolvimento (x1,2) | 3,6 | 5,1 | 6,6 |
| F4 Testes com cliente (+ RN crítica) | 1,5 | 2 | 3 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| F6 Lojas (sensível) | 2,5 | 3 | 6 |
| **Faixa** | **10** | **13 → vender 14** | **20** |

## Vendido × planejado
Plano do hand-off: imersão (sem. 1–2), motor de cálculo em três etapas (3–6), interface e preferências (7–8), testes, deploy e lojas (9–12).

- O vendido (12) fica **entre o piso (10) e o provável (13)**, 2 semanas abaixo da recomendação de venda (14), com uma regra de cálculo ainda em aberto e a cliente com pouca agenda.
- O próprio hand-off registrou os riscos: escopo real maior que o da ficha, prazo encolhido de 4 para 2–3 meses e "não se sustenta com só 1 dev".
- **Resultado final: a confirmar** quando o projeto terminar.

## Lição para a régua
1. **A ficha de qualificação subestimou o escopo** (variáveis clínicas e unidades que só apareceram depois). Por isso o "fluxo com RN específica" exige o documento da regra antes da proposta.
2. **A stack (Expo) foi sugestão comercial, sem validação do time** → regra "o CN não promete stack".
3. Testes, deploy e lojas de um app de saúde em 4 semanas está no limite inferior da régua (F4 + F5 + F6 no mínimo = 4,5).

## Ritmo com Claude Code (17/10/2026)

O projeto está sendo codado com Claude Code por uma dupla com cerca de 20 horas por semana somadas. Pelo git, o código começou em 30/09/2026 e, até 06/10, já tinha o motor das 3 faixas, a composição do soro, a tela completa com o modal de alerta e o hook ligando a tela ao motor. É quase todo o F3, que a régua antiga estimava em 5,1 semanas no central.

Esse dado criou, em 17/10/2026, o **fator Claude Code** (x0,75 no núcleo do F3), que levava a faixa do Projeto B a 9 / 12 / 20 e a venda a 12, igual ao vendido. A reunião de validação de 20/10/2026 **removeu o fator**: a régua atual não tem multiplicador de ferramenta, e o JSON em *Entrada da régua* (fim deste arquivo) roda sem ele. O ritmo rápido fica registrado aqui para conferir com o realizado em 23/11/2026: se o projeto fechar em 12 semanas, a régua (13, venda 14) ficou acima do real.

## Entrada da régua

O JSON que o script lê (`python ../scripts/calcular_faixa.py projeto-b.md`). O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "Projeto B (app clínico offline)",
  "f0": {
    "stack_exigida_fora_da_lista": false,
    "sla_ou_sustentacao": false,
    "infra_cliente_sem_acesso": false,
    "multa_por_atraso": false,
    "feature_sem_referencia_nem_doc": false,
    "hardware": false,
    "prazo_exigido_semanas": null
  },
  "demanda_pouco_detalhada": false,
  "atipico": false,
  "stack_fora_template": false,
  "niveis_acesso": "nenhum",
  "multitenancy": "nao",
  "fluxos_comuns": 1,
  "fluxos_rn_especifica": 1,
  "features_atipicas": 0,
  "formatos": [
    "app"
  ],
  "integracoes": [],
  "dependencia_dados": false,
  "offline": "local",
  "volume_alto": false,
  "rn_critica": true,
  "deploy_infra_cliente": false,
  "lojas": "sensivel"
}
```
