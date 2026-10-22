# F3 — Desenvolvimento: fluxos, formato e extras

**Baseline do formulário:** 1 a X semanas. É a fase que mais varia. Sem teto.

✅ **Reunião 20/10:** integrações e fluxos são **tópicos separados**. As integrações estão em `F3-integracoes.md`.

✅ **Reunião 20/10:** o fator Claude Code (×0,6 / ×0,75 / ×0,9 no núcleo) foi **removido**.

**Conta do F3:**

```
F3 = Σ (fluxos de cada código × fator daquele código) + integrações + extras [+ margem, ver D3]
fluxos = fluxos comuns + fluxos com RN específica + features atípicas
```

---

## 3.1 Núcleo — contar os fluxos

### Passo 1: quantos fluxos

A unidade é a **jornada**, não a numeração da PRD. A mesma PRD numerada em dois ou em três níveis tem de dar o mesmo número de fluxos (no Projeto G, contar por seção dava 26 semanas e contar por subseção dava 40). A regra completa está no glossário (*Fluxo*); o resumo:

| # | Passo | Onde ler |
|---|---|---|
| 1 | Listar as **folhas** da seção 2: a subseção mais funda que tem itens A(cli)D (2.2.1, 2.2.2… se existirem; senão 2.2, 2.3…). Fora: 2.1 Autenticação (F2) e Disponibilização do Produto (F5 e F6) | PRD seção 2 |
| 2 | Tirar as folhas de **offline e sincronização** quando `offline` for `sync` ou `local`: o custo delas está no extra de offline (3.3), não em fluxo | PRD (termo "offline") |
| 3 | **Juntar** folhas que são a mesma jornada: mesma entidade principal, mesmo código e uma é a continuação da outra (lista + detalhe da mesma coisa; criar + gerenciar a mesma coisa). Folha com **até 2 itens A(cli)D** que só existe para servir outra jornada (ex.: cadastrar pessoa durante a anotação) entra nela | PRD seção 2 |
| 4 | Jornada com **mais de 8 itens A(cli)D** conta como **2 fluxos** | PRD seção 2 |
| 5 | Registrar cada junção em *Suposições*, com as folhas juntadas (ex.: "2.2.1 + 2.2.2 = Auditorias") | — |

**Sem PRD:** perguntar ao CN as jornadas completas (`insumos-e-perguntas.md`). Sem fluxos, **não dimensionar**.

> 🔎 **Proposta:** o limite de 8 itens por fluxo e o "até 2 itens se junta" precisam ser calibrados quando o primeiro projeto com PRD terminar.

### Passo 2: cada fluxo é comum ou tem RN específica?

| Pergunta | Onde ler | Se sim |
|---|---|---|
| O cliente precisa entregar uma **fórmula, tabela, norma ou protocolo escrito** para esse fluxo funcionar? | RNs do módulo; Fathom | RN específica |
| O fluxo tem **concorrência** ("o primeiro que aceitar leva") ou **imutabilidade** (registro que não se edita, versionamento)? | Coluna *Fatores de complexidade* | RN específica |
| Nenhuma das duas | — | Fluxo comum |

**Sem resposta:** fluxo comum, desde que a PRD não marque fator de complexidade no módulo. Se marca e não explica → RN específica + alerta de discovery (F1, item 1.2).

**Não é RN específica:** validação padrão de mercado (CPF, CNPJ, CEP, e-mail), "cálculo que não pode errar" sem documento, só envolver dinheiro, ou **gerar um documento num template fixo** (relatório, contrato, certificado), inclusive em mais de um formato (PDF, Word, Excel). Template fixo e exportação fazem parte do módulo: o fluxo é comum (`leitura-prd.md`, Passo 3). Template que o usuário monta ou edita é *relatório configurável* (feature atípica).

**Não usar a fronteira aqui.** "Na dúvida, linha mais pesada" (`regra-fronteira-e-faixa.md`) só vale quando as perguntas acima não decidem. Se a resposta das perguntas é "não", o fluxo é comum, mesmo que o módulo pareça trabalhoso.

**Conta uma vez por módulo**, mesmo com várias RNs.

**Rotina agendada** (roda sozinha por horário): hoje transforma o fluxo em RN específica (+1,75 no central).
> 🔎 **Proposta:** é desproporcional para um agendamento simples. Sugestão: +0,5 no fluxo em vez de trocar de linha. **Até validar:** continua virando RN específica.

### Passo 3: features atípicas

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Quantas features da PRD estão nesta lista: tempo real por aviso do servidor (push), relatório configurável pelo usuário (construtor)? | Coluna *Fatores de complexidade* | — |
| Quantas outras features não têm **nenhuma** referência citada no Fathom? | Fathom | Lacuna: "Existe algum app que já faça {feature}?" |

É uma **contagem** de features, não semanas. Feature sem referência **e** sem documentação técnica pública vai para o **F0**.

### Tabela do núcleo

| Item (por unidade) | Mín | Central | Máx |
|---|---|---|---|
| Fluxo comum | 1 | 1,25 | 1,5 |
| Fluxo com RN específica | 2 | 3 | 4 |
| Feature atípica | 1 | 1,5 | 2 |

---

## 3.2 Fator de formato

| Pergunta | Onde ler | Resultado |
|---|---|---|
| Precisa estar na App Store ou Play Store, **ou** usa Bluetooth, GPS em segundo plano, NFC, notificação com o app fechado em iOS ou sensores? | PRD linha **Superfície**, 3.1, Disponibilização do Produto | App nativo |
| Instala pelo navegador (ícone na tela), sem loja? | PRD 3.1 | PWA |
| Só abre no navegador | PRD 3.1 | Web |
| Quantos **códigos separados** vão para o ar? | PRD Superfície | Cada código além do primeiro é um formato extra |

**Sem resposta entre PWA e app:** app.

| Formato | Fator |
|---|---|
| Web | ×1,0 |
| PWA | ×1,1 |
| App nativo | ×1,2 |
| Fluxo que existe em mais de um código (`compartilhado`) | fator do formato mais pesado + ⏳ **D1** por formato extra |

O `webapp` do script deixa de existir: vira PWA se instala, web se não instala.

### Fator por fluxo (revisão de 22/10/2026)

**Cada fluxo recebe o fator do código em que existe.** Com mais de um formato, o JSON leva `fluxos_por_formato`, dizendo quantos fluxos estão em cada código:

| Pergunta (para cada fluxo) | Onde ler | Chave |
|---|---|---|
| O fluxo só existe no app (ou só no painel)? | Linha **Superfície** do módulo, ou o título da seção-mãe ("Fluxo do Consultor (Aplicativo Mobile)") | O formato daquele código (`app`, `pwa`, `web`) |
| O fluxo tem tela nos dois códigos (ex.: o tutor agenda no app e a recepção gerencia a mesma agenda no painel)? | Superfície "app mobile e painel web" | `compartilhado` |
| Não dá para saber | — | `compartilhado` (linha mais pesada) |

```json
"formatos": ["app", "pwa"],
"fluxos_por_formato": {
  "app":           {"comuns": 3, "rn_especifica": 0, "atipicas": 0},
  "pwa":           {"comuns": 5, "rn_especifica": 1, "atipicas": 0},
  "compartilhado": {"comuns": 0, "rn_especifica": 0, "atipicas": 0}
}
```

A soma de cada coluna tem de bater com `fluxos_comuns`, `fluxos_rn_especifica` e `features_atipicas` (o script confere). Com um formato só, o campo não entra.

**Por quê:** antes, o fator de app + painel (×1,4) multiplicava **todos** os fluxos. Quando cada jornada vive num código só (consultor só no app, admin só no painel), o segundo código já está pago pelos fluxos dele, e o ×1,4 cobrava de novo. No Projeto G isso somava ~4 semanas. O custo de ter dois códigos que não está nos fluxos (setup e deploy do segundo código) já está no F1 e no F5.

✅ **Reunião 20/10:** o antigo "+0,1 por formato extra" é pouco. Deve ser **pelo menos 1,2**. Agora ele vale só para os fluxos `compartilhado`.

> ⏳ **D1 — em aberto:** "pelo menos 1,2" quer dizer:
> - (a) **+0,2 por formato extra**: app + painel web = 1,2 + 0,2 = **×1,4**; ou
> - (b) **×1,2 sobre o fator**: app + painel web = 1,2 × 1,2 = **×1,44**.
>
> **Provisório:** (a), +0,2 por formato extra.

Os prazos de desenvolvimento **não** incluem a publicação nas lojas (que é F6).

---

## 3.3 Extras (somam depois do fator de formato)

| Item | Mín | Central | Máx | Alerta |
|---|---|---|---|---|
| Dependência de dados | +1 | +1,5 | +2 | ⚠️ Chamar o núcleo de Dados |
| Offline local | 0 | 0 | 0 | |
| Offline com sincronização | +1,5 | +2 | +3 | ⚠️ Postgres, não MongoDB (ver F0, item 0.2) |
| Volume alto | +1 | +1,5 | +2 | ⚠️ Requisitos de performance por escrito |

### Dependência de dados

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| O projeto depende de dados que **já existem fora do sistema** (planilha legada, base pública, sistema antigo) e precisam ser **migrados, limpos ou convertidos** para o produto funcionar? | Fluxos com **Origem** / **Processamento** / **Destino**; Exclusões | `true` se a PRD citar migração ou carga de base existente sem dizer o formato |

**Não é dependência de dados** (é parte do módulo, 0 a mais): um **upload simples feito pelo usuário dentro do produto**, com formato definido na PRD, que vira registros na hora (ex.: planilha de uma coluna em que cada linha vira uma pergunta). Sinais: a PRD fixa o formato do arquivo, não pede conversão de unidades nem cruzamento com outra base, e a importação é uma tela do produto, não uma tarefa do projeto.

É dependência de dados quando há pelo menos um destes: migração do histórico do cliente; base pública ou externa a tratar; conversão de unidades ou de formatos; cruzamento entre bases; dado sujo que precisa de limpeza. Nesses casos chamar o núcleo de Dados.

Se a importação roda **sozinha**, sem ninguém disparar, é integração (`F3-integracoes.md`), não dependência de dados.

### Offline

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O app **grava** algo sem internet para subir depois? | PRD (termo "offline") | Offline com sincronização |
| O app só **lê** sem internet o que já está no aparelho? | PRD | Offline local |
| A PRD não fala de offline | — | Nenhum (0) |

> 🔎 **Proposta:** baixar dados do servidor para consultar offline já é uma sincronização de mão única e tem custo. Sugestão: offline local com leitura de dados do servidor = +0,5 / +0,5 / +1. **Até validar:** 0.

✅ **Reunião 20/10:** offline com sincronização **não** se vende com MongoDB. A proposta registra Postgres como premissa (ver ⏳ **D5** no F0).

### Volume alto

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| A seção 3.3 declara **1.000 ou mais usuários simultâneos**, ou um pico com data (evento, lançamento)? | PRD 3.3 | `false` (sem 3.3, não há requisito de volume) |

> 🔎 **Proposta:** o limite de 1.000 precisa ser validado pela área técnica.

---

## 3.4 Margem de segurança ("gordura")

✅ **Reunião 20/10:** o dimensionamento deve ter uma **margem de segurança explícita** contra imprevistos, em vez de prazo justo. Se o time entregar antes, o tempo vira over delivery para o cliente.

Isso contradiz a regra atual da régua ("não há buffer percentual", desde 17/10/2026). A regra antiga sai.

> ⏳ **D3 — em aberto:** onde e quanto?
> - (a) percentual sobre o F3 (🔎 sugestão: +10% a +15% no central);
> - (b) percentual sobre o total;
> - (c) embutida nos centrais de cada linha.
>
> **Provisório:** sem margem extra na conta. A resposta ao CN avisa: "Margem de segurança ainda não definida pelo NTec (D3)."
