# Exemplos — base de precedentes do NTec

Cada projeto tem uma ficha `.md`: o que era, como a régua classificou, comparação com o realizado e, no fim, a seção **Entrada da régua** com o JSON que o script lê (para rodar de novo quando a régua mudar). Os scripts aceitam o `.md` direto: usam o primeiro bloco ```json do arquivo.

| Projeto | Formato | Perfis | Fluxos (comuns + RN) | Faixa da régua (otim. / prov. / cons.) | Vendido | Situação |
|---|---|---|---|---|---|---|
| [Projeto A](projeto-a.md) | PWA | 3, poucas diferenças | 4 + 0 | 9 / 12 / 16 | 12 | No prazo |
| [Projeto B](projeto-b.md) | App nativo, offline | nenhum | 1 + 1 | 10 / 13 / 20 | 12 | Em execução |
| [Projeto C](projeto-c.md) | Web + app | 5, grandes diferenças | 3 + 1 | 13 / 18 / 24 | 11 | Atrasou (~14) |
| [Projeto D](projeto-d.md) | App + painel web | 2–3, poucas diferenças | 5 + 0 | 13 / 18 / 23 | 18 | Em execução, sem atraso |
| [Projetos E e F](projetos-e-f-pendente.md) | ? | ? | ? | não calibrado | 34 / 38 | Em execução |
| [Projeto H](projeto-h.md) | App nativo, offline | 1 (login em aberto) | 0 + 1 | 10 / 13 / 20 | — | Em negociação. **Primeiro dimensionado pelas transcrições** da AT Diag e da AT Aprof: exemplo completo de `leitura-transcricoes.md`, com a proposta em [projeto-h-proposta.md](projeto-h-proposta.md) |
| [PetAgenda (fictício)](ficticio-petagenda.md) | App + painel web | 4 | 4 + 0 | 14 / 18 / 24 | — | Resposta completa de exemplo (sem transcrição) |
| [PetAgenda proposta (fictício)](ficticio-petagenda-proposta.md) | App + painel web | 4 | 3 + 1 | 14 / 19 / 26 | — | JSON modelo da Proposta Técnica (`scripts/gerar_proposta.py`) |

**`fluxos_por_formato` (desde 22/10/2026):** com mais de um formato, o JSON diz em que código cada fluxo existe. Nos Projetos C e D, todos os fluxos estão como `compartilhado` (mesmo resultado de antes), porque as fichas não dizem onde cada jornada vive. É um palpite a conferir no hand-off: se as jornadas forem de um código só, a régua do C cai (o que aproxima do realizado) e a do D pode ficar abaixo do vendido. A proposta modelo da PetAgenda já distribui os fluxos por código.

Os Projetos A a D são **anteriores à leitura das calls**: os fluxos foram contados a partir das tasks do Notion. O Projeto H é o primeiro dimensionado pelas transcrições (fluxo = jornada descrita pelo cliente); quando ele terminar, vira o primeiro precedente para conferir essa leitura.

**Números da régua atual (22/10/2026):** as faixas da tabela e das fichas saem do script de hoje, sem o fator Claude Code (removido em 20/10/2026) e sem o fator de cliente com pouca disponibilidade. Quando a régua mudar, rodar de novo cada ficha e atualizar esta tabela.

## Como achar um precedente

1. Mesmo **formato** primeiro (app com lojas, PWA, web).
2. Depois o número de **fluxos** e o tipo de **níveis de acesso**.
3. Se nenhum bate, escrever "sem precedente comparável". Não forçar.

## Como adicionar um projeto novo

Quando um projeto terminar:
1. Criar `nome.md` no mesmo formato dos outros, com **vendido × realizado** e a causa dos desvios (puxar da retrospectiva).
2. No fim dele, a seção **Entrada da régua** com o JSON dos fatores, como a área de projetos classificaria hoje.
3. Rodar `python ../scripts/calcular_faixa.py nome.md`.
4. Atualizar a tabela acima e a tabela de Calibração em `regua-dimensionamento.md`.
5. Se 2 ou mais projetos errarem para o mesmo lado no mesmo fator, ajustar o peso no script **e** na régua, e registrar no "Registro das fontes".

Não copiar valores de contrato nem dados pessoais de clientes para estas fichas.
