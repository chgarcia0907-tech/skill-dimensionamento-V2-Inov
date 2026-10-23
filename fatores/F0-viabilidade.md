# F0 — Viabilidade (critérios de exclusão)

✅ **Reunião 20/10:** antes de dimensionar, a skill confere se o projeto é viável. Projeto que cai em um critério de rejeição **não é dimensionado**: a skill para, não gasta tokens com F1 a F6 e devolve ao CN o motivo.

**Não soma semanas.** O F0 tem dois resultados que param o projeto e uma condição de escopo:

| Resultado | Quando a skill confere | O que a skill faz |
|---|---|---|
| 🚫 **Rejeitado** | **Antes** do F1, com o que as calls dizem | Para. Não dimensiona. Responde ao CN com o critério, a citação e o que precisaria mudar para o projeto voltar a ser viável |
| 🚩 **Parar e consultar** | Antes do F1 (multa, feature sem referência, hardware, tenant com regra própria, integração sem API) ou **depois do cálculo** (prazo exigido abaixo do otimista, item 0.3) | Dimensiona, mas o status fica 🚩 e a proposta **não é concluída** nem vai para o cliente antes da resposta da área de projetos |
| **Condição de escopo** | Antes do F1 | Segue dimensionando, com a condição escrita na proposta (infra do cliente sem acesso do NTec, item 0.3) |

O critério de prazo é o único que **depende do dimensionamento**: só dá para comparar o prazo exigido com o cenário otimista depois que o F1 a F6 forem calculados. Os demais critérios continuam sendo conferidos antes de qualquer conta, e um 🚫 interrompe tudo ali.

Se nenhum critério bater, segue para o F1.

---

## 0.1 Stack e tecnologia

**Lista fechada de tecnologias aceitas** (🔎 Proposta: confirmar a lista com Augusto e Frank). Tudo que **não** está aqui e o cliente **exige** → 🚫 rejeitado.

| Camada | Aceito |
|---|---|
| Front-end web | Next.js / React |
| Mobile | Expo / React Native |
| Back-end | Node.js / TypeScript (API do template) |
| Banco | MongoDB (template), Postgres, Supabase |
| Hospedagem | Vercel, AWS, Supabase, ou a infra do cliente (ver F5 e o item 0.3) |

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| O cliente **exige** alguma tecnologia fora da tabela acima? | Calls ("tem que ser em…", "nossa TI só aceita…") | Segue para o F1. Registrar em *Suposições* que a stack será a do template, como premissa a validar na Sprint de Refino |

Exemplos de **rejeição** (✅ Reunião 20/10): .NET, Angular, COBOL, Delphi. Também: Java/Spring, PHP/Laravel, Vue, Flutter, Django, Ruby on Rails (🔎 Proposta: estão fora da lista, confirmar).

**Troca aceita** (✅ Reunião 20/10): trocar MongoDB por Supabase ou Postgres **não** rejeita. Segue para o F1 (ver `F1-imersao-setup.md`, item 1.3).

**"Exigir" é diferente de "sugerir".** "A gente usa .NET lá, mas vocês decidem" não é exigência. Só conta se o cliente disse que **tem que ser** naquela tecnologia.

## 0.2 Offline com sincronização

✅ **Revisão do consultor do NTec (posterior à reunião de 20/10):** offline com sincronização é uma **escolha técnica**, não um motivo de rejeição. O MongoDB é escolha do template do NTec, não do cliente; por isso não importa se o cliente pediu ou não um banco.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O app **grava** dados sem internet para sincronizar depois? | Calls ("sem internet", "no interior não pega", "quando a internet voltar, sobe") | Segue o dimensionamento normalmente. O banco é **Postgres**, não MongoDB (problemas em projetos passados). Registrar como premissa técnica na proposta (seção 12) e na Sprint de Refino. O peso do offline está no F3 (`F3-desenvolvimento.md`) |

> ⏳ **D5 — em aberto:** a revisão do consultor não resolve se a troca obrigatória para Postgres por causa do offline soma como "stack fora do template" no F1. **Provisório:** não soma, vira só premissa da Sprint de Refino.

## 0.3 Condições de contrato

✅ **Reunião 20/10** pediu critério de contrato; a lista é 🔎 Proposta. Os itens de prazo e de infra do cliente foram revistos pelo consultor do NTec depois da reunião.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O cliente exige um prazo **menor que o cenário otimista** da skill? | Calls (data exigida pelo **cliente**; o prazo que o CN falou não conta); briefing do CN | **Conferido depois do cálculo.** 🚩 Parar e consultar: a skill dimensiona, analisa a entrega parcial (abaixo) e não conclui a proposta antes da área de projetos |
| O contrato prevê **multa por atraso**? | Calls; minuta | 🚩 Parar e consultar |
| O cliente exige **suporte 24/7, SLA ou sustentação** além da garantia de 30 dias? | Calls ("suporte", "manutenção", "24h") | 🚫 Rejeitado (o NTec não oferece) |
| O sistema vai rodar na infra do cliente **sem acesso do time do NTec** para publicar e corrigir? | Calls ("nossos servidores", "a nossa TI publica") | **Condição de escopo** (abaixo). Segue o dimensionamento |

### Prazo exigido abaixo do otimista: analisar uma entrega parcial

✅ **Revisão do consultor do NTec.** O status continua 🚩. Antes de consultar a área de projetos, a skill verifica se dá para **disponibilizar antes um módulo utilizável** do sistema, por meio de um deploy parcial, enquanto o resto do projeto continua em desenvolvimento. Responder com o inventário de jornadas e o cronograma:

| Pergunta | Onde ler |
|---|---|
| Qual módulo (jornada ou conjunto de funcionalidades) atende à necessidade **prioritária** do cliente na data pedida? | Calls (o que o cliente disse que precisa primeiro, e por quê); inventário de jornadas |
| Esse módulo **funciona sozinho**, de forma utilizável? Ele depende de login, cadastros, integrações ou dados que ficariam para depois? | Inventário; F2 e integrações do F3 |
| Pelo dimensionamento, dá para entregar esse módulo até a data pedida? | Cronograma: somar as semanas centrais de F1, do deploy (F5), do login (F2) e das jornadas do módulo, na ordem das sprints, e comparar com o prazo exigido |

- A alternativa vai para a **área de projetos avaliar**. Não prometer a entrega antecipada ao cliente.
- **O prazo total não muda.** Não reduzir semanas nem tirar fase para caber na data do cliente: a faixa continua a da conta.
- Se **não** houver entrega parcial viável (o módulo prioritário depende do resto, ou não cabe na data), escrever isso na consulta.

### Infra do cliente sem acesso do NTec: condição de responsabilidade e escopo

✅ **Revisão do consultor do NTec.** Não rejeita mais. Quando o sistema vai rodar na infra do cliente e o time do NTec não tem acesso:

- O **deploy é responsabilidade do cliente**.
- O deploy nessa infra **sai do escopo e do dimensionamento** do NTec: o F5 fica zerado (`F5-deploy.md`), e o cronograma não tem a etapa de deploy.
- A **garantia de 30 dias não se aplica** nesse cenário. A proposta diz isso expressamente (o `gerar_proposta.py` escreve a condição na seção 15).
- Continuam com o NTec as atividades de preparação e entrega: as versões parciais para o cliente revisar, na infra do NTec, durante o desenvolvimento e os testes (`F4-testes.md`), e a entrega do código e do pacote para o cliente publicar.

No JSON: `f0.infra_cliente_sem_acesso: true`.

## 0.4 Restrições técnicas que antes eram 🚩 nas fases

Estes casos estavam espalhados em F2 e F3. Agora são conferidos aqui, antes de qualquer conta.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| Algum tenant tem **código ou regra de negócio diferente** dos outros? (ver *Instâncias* no glossário) | Calls ("cada unidade tem a sua regra") | 🚩 Parar e consultar |
| Alguma integração é com sistema que, segundo o cliente, **não tem API**? (unidirecional **ou** bidirecional) | Calls (sistemas citados) | 🚩 Parar e consultar. Alternativa a sugerir: importação/exportação de planilha |
| Alguma feature não tem **nenhuma** referência citada **e** não tem documentação técnica pública? | Calls | 🚩 Parar e consultar. Pode exigir prova de conceito paga antes da proposta |
| O produto depende de **hardware** (Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal)? | Calls | 🚩 Parar e consultar (🔎 Proposta) |

## 0.5 Demanda pouco detalhada

Não rejeita. Ver o alerta de discovery em `F1-imersao-setup.md`, item 1.2.

---

## Formato da resposta quando o F0 para

```
🚫 Projeto rejeitado no F0 — {critério}
Motivo: {citação da call, com o minuto}
O que precisaria mudar: {ex.: cliente aceitar Next.js em vez de Angular}
```

```
🚩 Parado no F0 — {critério}
Motivo: {citação}
Encaminhar para: área de projetos
Pergunta para a área de projetos: {pergunta objetiva}
```

Quando o critério é o prazo exigido abaixo do otimista, acrescentar:

```
Prazo exigido: {N} semanas · Faixa da skill: {otimista} / {provável} / {conservador}
Entrega parcial: {módulo, o que ele resolve, de que depende, em que sprint fica pronto pelo cronograma}
                 ou "Sem entrega parcial viável: {motivo}"
```
