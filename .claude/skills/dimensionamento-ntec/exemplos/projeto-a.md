# Projeto A — PWA de guia local

**Situação:** finalizando, no prazo. **Vendido:** 12 semanas (+1 off), 6 sprints.

## O que era
Guia de eventos, gastronomia e hospedagem de uma região, centrado num mapa. WebApp PWA mobile-first, mais o painel de gestão no mesmo sistema web. App nativo nas lojas ficou fora do escopo. Cliente pessoa física, sem conhecimento de tecnologia.

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | PWA (o painel está no mesmo código → não é formato extra) | hand-off |
| Níveis de acesso | visitante, cadastrado e admin → 2 a 5 com poucas diferenças | hand-off |
| Fluxos comuns | 4: mapa com filtros, agenda (hoje/amanhã), detalhe do local, cadastro de estabelecimentos e eventos | palpite, média confiança |
| Integrações | API de mapa (uni, doc), notificações (uni, doc); login Google e S3 = template; links para apps de navegação e WhatsApp = 0 | plannings S3–S5 |
| Demais fatores | nenhum | — |

## Resultado da régua

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0,5 | 1 | 1,5 |
| F3 Desenvolvimento (x1,1) | 5,4 | 6,5 | 8,6 |
| F4 Testes com cliente | 1 | 1,5 | 2 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| **Faixa** | **9** | **12** | **16** |

## Vendido × realizado
- **Provável da régua = vendido (12).** Projeto no prazo.
- Sprints: S1–S3 Delivery, S4–S5 Overdelivery.
- No real, imersão e setup ocuparam S1 e S2, e o login (Better Auth + Google + guarda de rotas + recuperar senha) ficou na S3, cerca de 2 semanas.

## Lição para a régua
A proposta original tinha **14 sprints** e foi cortada para um MVP de 6. Esse é o exemplo de "negociar escopo, não prazo": o corte foi no escopo, e o prazo do MVP foi cumprido.

## Entrada da régua

O JSON que o script lê (`python ../scripts/calcular_faixa.py projeto-a.md`). O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "Projeto A (PWA de guia local)",
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
  "fluxos_comuns": 4,
  "fluxos_rn_especifica": 0,
  "features_atipicas": 0,
  "formatos": [
    "pwa"
  ],
  "integracoes": [
    "uni_doc",
    "uni_doc",
    "template",
    "template"
  ],
  "dependencia_dados": false,
  "offline": "nao",
  "volume_alto": false,
  "rn_critica": false,
  "deploy_infra_cliente": false,
  "lojas": "nao"
}
```
