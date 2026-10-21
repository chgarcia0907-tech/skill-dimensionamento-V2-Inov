# F0 — Viabilidade (critérios de exclusão)

✅ **Reunião 20/10:** antes de dimensionar, a skill confere se o projeto é viável. Projeto que cai em um critério de exclusão **não é dimensionado**: a skill para, não gasta tokens com F1 a F6 e devolve ao CN o motivo.

**Não soma semanas.** O F0 só tem dois resultados:

| Resultado | O que a skill faz |
|---|---|
| 🚫 **Rejeitado** | Para. Responde ao CN com o critério, a citação e o que precisaria mudar para o projeto voltar a ser viável |
| 🚩 **Parar e consultar** | Para. Encaminha para a área de projetos decidir. Só dimensiona depois da resposta |

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
| Hospedagem | Vercel, AWS, Supabase, ou a infra do cliente (ver F5) |

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| O cliente **exige** alguma tecnologia fora da tabela acima? | PRD 3.1; Fathom ("tem que ser em…", "nossa TI só aceita…") | Segue para o F1. Registrar em *Suposições* que a stack será a do template, como premissa a validar na Sprint de Refino |

Exemplos de **rejeição** (✅ Reunião 20/10): .NET, Angular, COBOL, Delphi. Também: Java/Spring, PHP/Laravel, Vue, Flutter, Django, Ruby on Rails (🔎 Proposta: estão fora da lista, confirmar).

**Troca aceita** (✅ Reunião 20/10): trocar MongoDB por Supabase ou Postgres **não** rejeita. Segue para o F1 (ver `F1-imersao-setup.md`, item 1.3).

**"Exigir" é diferente de "sugerir".** "A gente usa .NET lá, mas vocês decidem" não é exigência. Só conta se o cliente disse que **tem que ser** naquela tecnologia.

## 0.2 Offline com sincronização + MongoDB

✅ **Reunião 20/10:** offline com sincronização **não** se vende com MongoDB (problemas em projetos passados). Recomendar Postgres.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O app **grava** dados sem internet para subir depois **e** o cliente exige MongoDB? | PRD (termo "offline"); 3.1; Fathom | 🚫 Rejeitado, até o cliente aceitar Postgres |
| O app grava sem internet e o cliente **não** exige banco | — | Segue. A proposta registra "Postgres" como premissa (ver ⏳ **D5**) |

> ⏳ **D5 — em aberto:** quando a troca para Postgres é obrigatória por causa do offline, isso soma como "stack fora do template" no F1? **Provisório:** não soma, vira só premissa da Sprint de Refino.

## 0.3 Condições de contrato

✅ **Reunião 20/10** pediu critério de contrato; a lista é 🔎 Proposta.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O cliente exige um prazo **menor que o cenário otimista** da skill? | Fathom; briefing do CN | 🚩 Parar e consultar (a skill dimensiona, mas o status fica 🚩) |
| O contrato prevê **multa por atraso**? | Fathom; minuta | 🚩 Parar e consultar |
| O cliente exige **suporte 24/7, SLA ou sustentação** além da garantia de 30 dias? | Fathom; PRD 3 | 🚫 Rejeitado (o NTec não oferece) |
| O sistema vai rodar na infra do cliente **sem acesso do time do NTec** para publicar e corrigir? | PRD 3.1; Fathom | 🚫 Rejeitado |
| **Ninguém do cliente** foi nomeado para testar e aprovar as entregas? | Fathom | 🚩 Parar e consultar |

## 0.4 Restrições técnicas que antes eram 🚩 nas fases

Estes casos estavam espalhados em F2 e F3. Agora são conferidos aqui, antes de qualquer conta.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| Algum tenant tem **código ou regra de negócio diferente** dos outros? (ver *Instâncias* no glossário) | Visão Geral, 2.1, RNs, 3.4 | 🚩 Parar e consultar |
| Alguma integração é com sistema que, segundo a PRD ou o Fathom, **não tem API**? (unidirecional **ou** bidirecional) | Itens SID "integrar com…"; Fathom | 🚩 Parar e consultar. Alternativa a sugerir: importação/exportação de planilha |
| Alguma feature não tem **nenhuma** referência citada **e** não tem documentação técnica pública? | PRD fatores de complexidade; Fathom | 🚩 Parar e consultar. Pode exigir prova de conceito paga antes da proposta |
| O produto depende de **hardware** (Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal)? | PRD; Fathom | 🚩 Parar e consultar (🔎 Proposta) |

## 0.5 Demanda pouco detalhada

Não rejeita. Ver o alerta de discovery em `F1-imersao-setup.md`, item 1.2.

---

## Formato da resposta quando o F0 para

```
🚫 Projeto rejeitado no F0 — {critério}
Motivo: {citação da PRD ou do Fathom}
O que precisaria mudar: {ex.: cliente aceitar Next.js em vez de Angular}
```

```
🚩 Parado no F0 — {critério}
Motivo: {citação}
Encaminhar para: área de projetos
Pergunta para a área de projetos: {pergunta objetiva}
```
