# Projeto H — calculadora clínica (app nativo, offline)

**Primeiro projeto dimensionado pelas transcrições** da AT Diagnóstico (19 min) e da AT Aprofundamento (11 min), sem PRD. Serve de exemplo completo de `leitura-transcricoes.md`. Em negociação: ainda não há realizado.

Arquivos: a entrada da régua está no fim deste arquivo, e a Proposta Técnica completa em [projeto-h-proposta.md](projeto-h-proposta.md).

## O que é

App para médicos calcularem o soro de crianças: informa o peso, o tipo de soro e as quantidades desejadas de glicose e íons, e o app devolve o volume de cada componente, o volume total e a velocidade de infusão, com aviso quando a concentração passa do máximo. Funciona sem internet, não guarda dado de paciente e vai para a App Store e a Play Store. As fórmulas vêm de uma planilha da cliente.

## Como as calls viraram fatores

| Fator | Valor | De onde veio |
|---|---|---|
| Jornadas | 1 com RN específica: calcular o soro | AT Diag 7:46 (a cliente descreve a planilha e o cálculo); AT Aprof 1:35 ("é isso mesmo, é uma calculadora") |
| Junções | Três tipos de soro e a unidade do cálcio = a mesma jornada | AT Diag 11:53; AT Aprof 4:00 |
| Formato e lojas | App nativo, `sensivel` | AT Diag 15:04 ("EES" = Play Store, erro de transcrição) e 15:27 ("Perfeito"); dado clínico de crianças |
| Offline | `local`: o cálculo roda no aparelho, nada sobe | AT Diag 3:02 ("tem interior que nem sinal de internet tem") |
| Login | Lacuna: `"1"`, leve `"nenhum"` | AT Diag 13:32 ("não sei se seria interessante um login") |
| Cobrança | Lacuna: `bi_doc`, leve `[]` | AT Diag 14:37 ("é pra venda mesmo"), sem dizer como |
| Histórico | Fora (exclusão) | AT Diag 13:32 ("não é prontuário") |
| RN crítica | `true` | O app calcula volume e infusão de soro pediátrico |
| Atípico | `false` | AT Aprof 2:32 ("as [calculadoras] que eu já vi") |
| Quem valida | A própria cliente, pessoa física | AT Aprof 1:35 ("ajustes… a gente faria no decorrer do projeto") |
| Prazo exigido | `null` | AT Aprof 7:14 ("para esse ano, mas não tem pressa") |

**Descartado na leitura:** a conversa interna antes de a cliente entrar (AT Diag 0:00 a 1:31), a apresentação da Poli Júnior (16:11 a 17:57) e os *Action Items* do Fathom.

## Resultado da régua

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0,5 | 0,5 | 1 |
| F3 Desenvolvimento | 2,9 | 4,6 | 6,3 |
| F4 Testes | 1,5 | 2 | 3 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| F6 Lojas | 2,5 | 3 | 6 |
| **Total** | **9,4** | **12,6** | **19,8** |

**Otimista 10 · provável 13 · conservador 20 semanas. Vender 14 semanas (7 sprints) = 12 + 2 que dependem de confirmar com a cliente (login e cobrança).**

## Comparação com o que a CN falou

Na AT Aprof, a CN disse à cliente **"dois a três meses"** (~9 a 13 semanas), antes de a skill existir para este caso. Três meses bate com a venda sem as lacunas (12). Dois meses fica abaixo do otimista (10): a expectativa precisa ser alinhada antes da proposta.

O peso está em F4 e F6 (testes da regra crítica e loja sensível), não no desenvolvimento: um app de uma tela só não sai em 8 semanas se vai para as lojas na categoria de saúde.

## Pontos que a leitura levantou e as calls não cobrem

- Diretriz 1.4.2 da App Store para calculadoras de dose (pode recusar app publicado por pessoa física). A confirmar com a área de projetos.
- Termo de uso e responsabilidade pelo resultado do cálculo.

## A conferir quando terminar

- Se 1 jornada com RN específica + RN crítica (F3 + F4) acertou o tempo de construir e validar um cálculo clínico.
- Se o app sensível (F6 central 3) acertou o tempo de aprovação nas lojas.

## Entrada da régua

O JSON que o script lê (`python ../scripts/calcular_faixa.py projeto-h.md`). O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "Projeto H — calculadora clínica (app nativo, a partir da AT Diag e da AT Aprof)",
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
  "niveis_acesso": "1",
  "multitenancy": "nao",
  "fluxos_comuns": 0,
  "fluxos_rn_especifica": 1,
  "features_atipicas": 0,
  "formatos": ["app"],
  "integracoes": ["bi_doc"],
  "dependencia_dados": false,
  "offline": "local",
  "volume_alto": false,
  "rn_critica": true,
  "deploy_infra_cliente": false,
  "lojas": "sensivel",
  "fathom": true,
  "lacunas_fathom": {
    "niveis_acesso": "nenhum",
    "integracoes": []
  }
}
```
