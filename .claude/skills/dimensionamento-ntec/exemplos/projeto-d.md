# Projeto D — app de ciência cidadã

**Situação:** em execução, sem atraso (47,6% do prazo em 16/10/2026). **Vendido:** 18 semanas (+3 off), 9 sprints planejadas.

> ⚠️ **Ficha incompleta.** O levantamento recebido foi cortado no meio da ficha deste projeto. Os fatores abaixo marcados como *palpite* precisam ser conferidos no hand-off.

## O que era
O cidadão registra avistagens de espécies com foto e geolocalização. App nativo nas lojas + painel admin web + landing com mapa. Cliente do terceiro setor (ONG ou instituto).

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | App nativo + web (painel e landing, código separado); todos os fluxos como `compartilhado` (palpite) → x1,4 | hand-off |
| Níveis de acesso | cidadão, admin (talvez pesquisador) → 2 a 5 com poucas diferenças | **palpite** |
| Fluxos comuns | 5: registrar avistagem (foto + localização), mapa público, moderação pelo admin, catálogo de espécies, histórico do usuário | **palpite** |
| Integrações | mapa (uni, doc); upload de foto (S3) = template | **palpite** |
| Offline | não (**a conferir**: uso em campo pode precisar) | **palpite** |
| Lojas | app comum | hand-off |

## Resultado da régua

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0,5 | 1 | 1,5 |
| F3 Desenvolvimento (x1,4) | 7,5 | 9,25 | 11,5 |
| F4 Testes com cliente | 1 | 1,5 | 2 |
| F5 Deploy | 0,5 | 1 | 1,5 |
| F6 Lojas | 2 | 2,5 | 4 |
| **Faixa** | **13** | **18** | **23** |

## Vendido × realizado
- **Recomendação de venda da régua = vendido (18).** Sem atraso até agora: 6 de 9 sprints abertas.
- Resultado final: a confirmar.

## Lição para a régua
Se o hand-off mostrar que o app precisa funcionar **offline com sincronização** (comum em uso de campo), a régua soma +2 no central (faixa 15 / 20 / 26, recomendação de venda 20) e o banco tem de ser Postgres, não MongoDB (F0, item 0.2). Vale como alerta para futuros apps de campo: perguntar sempre.

## Entrada da régua

O JSON que o script lê (`python ../scripts/calcular_faixa.py projeto-d.md`). O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "Projeto D (app de ciência cidadã)",
  "f0": {
    "stack_exigida_fora_da_lista": false,
    "offline_sync_com_mongodb_exigido": false,
    "sla_ou_sustentacao": false,
    "infra_cliente_sem_acesso": false,
    "multa_por_atraso": false,
    "sem_validador_nomeado": false,
    "feature_sem_referencia_nem_doc": false,
    "hardware": false,
    "prazo_exigido_semanas": null
  },
  "demanda_pouco_detalhada": false,
  "atipico": false,
  "stack_fora_template": false,
  "niveis_acesso": "2-5-poucas",
  "multitenancy": "nao",
  "fluxos_comuns": 5,
  "fluxos_rn_especifica": 0,
  "features_atipicas": 0,
  "formatos": [
    "app",
    "web"
  ],
  "fluxos_por_formato": {
    "app": {
      "comuns": 0,
      "rn_especifica": 0,
      "atipicas": 0
    },
    "web": {
      "comuns": 0,
      "rn_especifica": 0,
      "atipicas": 0
    },
    "compartilhado": {
      "comuns": 5,
      "rn_especifica": 0,
      "atipicas": 0
    }
  },
  "integracoes": [
    "uni_doc",
    "template"
  ],
  "dependencia_dados": false,
  "offline": "nao",
  "volume_alto": false,
  "rn_critica": false,
  "deploy_infra_cliente": false,
  "lojas": "normal"
}
```
