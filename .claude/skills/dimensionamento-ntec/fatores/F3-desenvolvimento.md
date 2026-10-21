# F3 — Desenvolvimento: fluxos, formato e extras

**Baseline do formulário:** 1 a X semanas. É a fase que mais varia. Sem teto.

✅ **Reunião 20/10:** integrações e fluxos são **tópicos separados**. As integrações estão em `F3-integracoes.md`.

✅ **Reunião 20/10:** o fator Claude Code (×0,6 / ×0,75 / ×0,9 no núcleo) foi **removido**.

**Conta do F3:**

```
F3 = (núcleo × fator de formato) + integrações + extras [+ margem, ver D3]
núcleo = fluxos comuns + fluxos com RN específica + features atípicas
```

---

## 3.1 Núcleo — contar os fluxos

### Passo 1: quantos fluxos

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Quantos módulos a seção 2 da PRD tem, fora 2.1 Autenticação e Disponibilização do Produto? | PRD seção 2 | Sem PRD: perguntar ao CN as jornadas completas (`insumos-e-perguntas.md`). Sem fluxos, **não dimensionar** |
| Algum módulo tem **mais de 8 itens A(cli)D**? Se sim, ele conta como **2 fluxos** | PRD seção 2 | — |

> 🔎 **Proposta:** o limite de 8 itens por fluxo resolve o "1 módulo = 1 fluxo", em que um módulo com 15 itens pesava o mesmo que um com 2. O número 8 precisa ser calibrado nos exemplos.

### Passo 2: cada fluxo é comum ou tem RN específica?

| Pergunta | Onde ler | Se sim |
|---|---|---|
| O cliente precisa entregar uma **fórmula, tabela, norma ou protocolo escrito** para esse fluxo funcionar? | RNs do módulo; Fathom | RN específica |
| O fluxo tem **concorrência** ("o primeiro que aceitar leva") ou **imutabilidade** (registro que não se edita, versionamento)? | Coluna *Fatores de complexidade* | RN específica |
| Nenhuma das duas | — | Fluxo comum |

**Sem resposta:** fluxo comum, desde que a PRD não marque fator de complexidade no módulo. Se marca e não explica → RN específica + alerta de discovery (F1, item 1.2).

**Não é RN específica:** validação padrão de mercado (CPF, CNPJ, CEP, e-mail), "cálculo que não pode errar" sem documento, ou só envolver dinheiro.

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

| Formato principal | Fator |
|---|---|
| Web | ×1,0 |
| PWA | ×1,1 |
| App nativo | ×1,2 |
| Cada formato extra em código separado | ⏳ **D1** |

O `webapp` do script deixa de existir: vira PWA se instala, web se não instala.

✅ **Reunião 20/10:** o antigo "+0,1 por formato extra" é pouco. Deve ser **pelo menos 1,2**.

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
| Algum dado vem de planilha, CSV, base pública ou sistema antigo e **uma pessoa dispara** a importação (uma vez ou de tempos em tempos)? | Fluxos com **Origem** / **Processamento** / **Destino** | `true` se a PRD citar importação ou migração |

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
