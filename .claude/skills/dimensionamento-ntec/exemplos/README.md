# Exemplos — base de precedentes do NTec

Cada projeto tem uma ficha `.md` (o que era, como a régua classificou, comparação com o realizado) e um `.json` (a entrada do script, para rodar de novo quando a régua mudar).

| Projeto | Formato | Perfis | Fluxos (comuns + RN) | Faixa da régua (otim. / prov. / cons.) | Vendido | Situação |
|---|---|---|---|---|---|---|
| [Projeto A](projeto-a.md) | PWA | 3, poucas diferenças | 4 + 0 | 9 / 12 / 16 | 12 | No prazo |
| [Projeto B](projeto-b.md) | App nativo, offline | nenhum | 1 + 1 | 11 / 14 / 21 | 12 | Em execução |
| [Projeto C](projeto-c.md) | Web + app | 5, grandes diferenças | 3 + 1 | 13 / 18 / 23 | 11 | Atrasou (~14) |
| [Projeto D](projeto-d.md) | App + painel web | 2–3, poucas diferenças | 5 + 0 | 13 / 17 / 23 | 18 | Em execução, sem atraso |
| [Projetos E e F](projetos-e-f-pendente.md) | ? | ? | ? | não calibrado | 34 / 38 | Em execução |
| [PetAgenda (fictício)](ficticio-petagenda.md) | App + painel web | 4 | 4 + 0 | 14 / 19 / 25 | — | Resposta completa de exemplo (sem PRD) |
| [PetAgenda via PRD (fictício)](ficticio-petagenda-prd.md) | App + painel web | 4 | 3 + 1 | 15 / 20 / 28 | — | Como ler a PRD e traduzir para a régua |
| [PetAgenda proposta (fictício)](ficticio-petagenda-proposta.json) | App + painel web | 4 | 3 + 1 | 15 / 20 / 28 | — | JSON modelo da Proposta Técnica (`scripts/gerar_proposta.py`) |

Os projetos reais desta tabela são **anteriores ao formato de PRD**: os fluxos foram contados a partir das tasks do Notion, e não pela regra "1 módulo = 1 fluxo". Quando um projeto com PRD terminar, ele vira o primeiro precedente para conferir essa regra.

## Como achar um precedente

1. Mesmo **formato** primeiro (app com lojas, PWA, web).
2. Depois o número de **fluxos** e o tipo de **níveis de acesso**.
3. Se nenhum bate, escrever "sem precedente comparável". Não forçar.

## Como adicionar um projeto novo

Quando um projeto terminar:
1. Criar `nome.json` com os fatores, como a área de projetos classificaria hoje.
2. Rodar `python ../scripts/calcular_faixa.py nome.json`.
3. Criar `nome.md` no mesmo formato dos outros, com **vendido × realizado** e a causa dos desvios (puxar da retrospectiva).
4. Atualizar a tabela acima e a tabela de Calibração em `regua-dimensionamento.md`.
5. Se 2 ou mais projetos errarem para o mesmo lado no mesmo fator, ajustar o peso no script **e** na régua, e registrar no "Registro das fontes".

Não copiar valores de contrato nem dados pessoais de clientes para estas fichas.
