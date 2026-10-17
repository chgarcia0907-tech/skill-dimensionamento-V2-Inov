# Régua de Dimensionamento — NTec

Pesos usados para transformar o que o coordenador de negócios (CN) levantou em uma faixa de semanas. A estrutura de fases vem do **Baseline de Projeto** do formulário *Dimensionamento Tec* (seção 7). Os fatores vêm do **Perfil da demanda** (seção 6). Os pesos foram calibrados contra os projetos reais do NTec (ver `exemplos/`).

**Fonte da verdade dos números:** `scripts/calcular_faixa.py`. Esta tabela e o script precisam bater. Se mudar um, mude o outro e registre no fim deste arquivo.

**Índice:** Regras de uso · Regras transversais · F1 a F6 · Faixa final · Parar e sinalizar · Calibração · Lacunas · Registro das fontes

---

## Regras de uso (ler antes de dimensionar)

1. **Não inventar fator.** Se o CN não sabe responder, a skill pergunta (ver `insumos-e-perguntas.md`). Se mesmo assim não houver resposta, usar o valor **mais pesado** plausível e registrar em *Suposições*. Uma empresa júnior erra muito mais para menos do que para mais.
2. **Toda linha tem três valores: mínimo / central / máximo.** O mínimo é o cenário "tudo dá certo", o central é o que costuma acontecer no NTec e o máximo é "os riscos aparecem".
3. **Somar fase a fase, na ordem F1 a F6.** As fases são sequenciais na régua, mesmo quando na prática se sobrepõem um pouco. A sobreposição é a folga natural do time.
4. **Rodar o script para fechar a conta.** Não somar de cabeça.
5. **Casos de fronteira** (o projeto encaixa em duas linhas): `regra-fronteira-e-faixa.md`.

---

## Regras transversais

### Os pesos já assumem o time típico do NTec
Uma dupla de empresa júnior com **cerca de 20 horas por semana somadas**, codando com **Claude Code**, sprints de 2 semanas e o template do monorepo NTec (Next.js + Expo + MongoDB/Prisma + Better Auth).

### Fator Claude Code (desde 17/10/2026)
Todos os projetos do NTec agora são codados com Claude Code. O ganho aparece no código que o time escreve, e não no que depende de gente de fora:

| O que muda | Mín | Central | Máx |
|---|---|---|---|
| Núcleo do F3 (fluxos comuns, fluxos com RN específica, features atípicas, já com o fator de formato) | x0,6 | x0,75 | x0,9 |
| F2 (níveis de acesso, multitenancy, login) | x0,7 | x0,85 | x1 |
| F1, extras do F3 (integrações, offline com sincronização, dependência de dados, volume alto), F4, F5 e F6 | x1 | x1 | x1 |

- **Por que só esses:** imersão e validação dependem do cliente; integração depende da documentação de terceiros; offline com sincronização e dados são decisão de modelagem; testes dependem da agenda do cliente; deploy e lojas dependem de revisão externa.
- **De onde vem o número: meio-termo entre dois projetos.** No Projeto B, o motor das 3 faixas e a tela completa saíram em cerca de 1 semana de código (30/09 a 06/10/2026), contra 5,1 semanas de F3 da régua antiga; a área de projetos espera fechar abaixo de 12 semanas. Num app + painel web de 8 fluxos com offline com sincronização, a área de projetos espera ~12 sprints (24 semanas). Um x0,5 (tentado primeiro) acertava o projeto pequeno mas dava 20 semanas no grande. O x0,75 acerta os dois: o ganho da ferramenta é parcialmente comido pelas ~20 h/semana da dupla (antes a régua supunha 3 a 4 h/dia por pessoa) e pela coordenação, revisão e integração entre módulos, que crescem com o tamanho do projeto.
- **No JSON:** `"claude_code": true` é o padrão. Os projetos antigos da calibração usam `"claude_code": false`, porque foram feitos sem a ferramenta.
- **Ainda não calibrado:** dois projetos, ambos sem o realizado final (um em execução, outro pela expectativa da área de projetos). O F2 com fator não foi medido (o Projeto B não tem login). Conferir no primeiro projeto com login e no fim do Projeto B.
 **Não há buffer percentual:** o risco já está no intervalo mínimo / central / máximo de cada linha.

### O que o template já entrega (não soma prazo)
Login por e-mail e senha, recuperação de senha, login com Google, envio de e-mail (Resend), upload de arquivo para AWS S3, estrutura de API e painel admin básico. Quando uma "integração" é uma dessas, ela entra como `template` (0 semanas).

### Formato conta por código separado, não por tela
Um painel admin dentro do mesmo app web **não** é um formato a mais. Um app nativo + um painel web **são** dois formatos (dois códigos, duas publicações).

### Semanas off e garantia ficam fora da régua
- **Semanas off** (férias, provas, recesso de fim de ano, julho) entram por calendário, somadas depois da faixa. No histórico, de 1 a 3 por projeto.
- **Garantia de 30 dias** é gratuita e não entra no prazo (vale para o que está no documento de requisitos).

---

## F1 — Imersão, refinamento, setup e acessos
**Baseline do formulário:** 1 a 4 semanas. **Teto:** 4.

| Fator | Mín | Central | Máx |
|---|---|---|---|
| Base (sempre) | 1,5 | 2 | 2,5 |
| Demanda pouco detalhada (sem documento de requisitos nem protótipo) | +0,5 | +1 | +1 |
| Setor ou produto atípico (sem benchmark parecido) | +0,5 | +0,5 | +1 |
| Stack fora do template NTec (cliente exige outra tecnologia) | +1 | +1,5 | +2 |

- **Atípico ≠ regra de negócio específica.** Uma fórmula científica ou clínica é *fluxo com RN específica* (F3), não "setor atípico". Não marcar os dois pelo mesmo motivo (erro encontrado na calibração do Projeto C).
- **O CN não promete stack.** Se o cliente ouviu "vamos fazer em X", tratar como *premissa a validar* (aconteceu no Projeto B: Expo foi sugestão comercial, sem validação do time).

## F2 — Infra, níveis de acesso, cadastro e login
**Baseline do formulário:** 1 a 4 semanas. **Teto:** 4.

| Níveis de acesso (formulário, seção 6) | Mín | Central | Máx |
|---|---|---|---|
| Nenhum (sem login, sem backend) | 0 | 0 | 0 |
| 1 nível | 0,5 | 0,5 | 1 |
| 2 a 6, com poucas diferenças entre eles | 0,5 | 1 | 1,5 |
| 2 a 6, com grandes diferenças (telas e regras próprias por perfil, aprovação de cadastro) | 1,5 | 2 | 2,5 |
| 6 ou mais | 2,5 | 3 | 4 |

| Multitenancy | Mín | Central | Máx |
|---|---|---|---|
| Não | 0 | 0 | 0 |
| Dados separados, mas não isolados | +0,5 | +0,5 | +1 |
| Só para isolamento de dados | +1 | +1,5 | +2 |
| Instâncias com features e regras isoladas por cliente | 🚩 **parar** | — | — |

"Grandes diferenças" quer dizer que cada perfil tem telas próprias, regras próprias ou fluxo de aprovação (ex.: nutricionista com cadastro pendente ou rejeitado que bloqueia rotas). Só mudar o que aparece num menu é "poucas diferenças".

## F3 — Desenvolvimento
**Baseline do formulário:** 1 a X semanas. É a fase que mais varia.

### Núcleo (multiplicado pelo fator de formato)

| Item | Mín | Central | Máx |
|---|---|---|---|
| Cada fluxo crítico comum (CRUD, listagem, cadastro, mapa com filtros, agenda) | 1 | 1,25 | 1,5 |
| Cada fluxo com regra de negócio muito específica (fórmula, cálculo que não pode errar, regra regulatória) | 2 | 3 | 4 |
| Cada feature atípica (sem benchmark, sem saber se é possível) | 1 | 1,5 | 2 |

**Fluxo crítico** = uma jornada completa, do início ao fim, que se quebrar torna o produto inútil. Exemplo: "cidadão fotografa a espécie → o app pega a localização → o registro aparece no mapa". Uma tela solta não é um fluxo.

| Formato (fator sobre o núcleo) | Fator |
|---|---|
| Web | x1,0 |
| WebApp ou PWA | x1,1 |
| App mobile nativo | x1,2 |
| Cada formato adicional em código separado | +0,1 |

Exemplo: app nativo + painel web = 1,2 + 0,1 = **x1,3**.

### Extras (somam depois do fator)

| Item | Mín | Central | Máx | Observação |
|---|---|---|---|---|
| Integração que o template já tem (Google, S3, e-mail) | 0 | 0 | 0 | |
| Integração unidirecional com serviço de mercado (ex: Mapbox, push) — `uni_doc` | +0,5 | +0,5 | +1 | |
| Integração bidirecional com serviço de mercado (ex: Mercado Pago) — `bi_doc` | +0,5 | +1 | +1,5 | |
| Integração unidirecional com sistema do cliente — `uni_sem_doc` | +1 | +1,5 | +2 | ⚠️ Cláusula de contrato + plano B (planilha) |
| Integração bidirecional com sistema do cliente — `bi_sem_doc` | +1,5 | +2,5 | +3,5 | ⚠️ Cláusula de contrato + plano B (planilha) |
| Integração bidirecional que a PRD diz não ter API — `sem_api` | 🚩 | — | — | Avaliar alternativa; potencial inviabilidade |
| Dependência de dados (bases soltas, planilhas, CSV, tabelas externas) | +1 | +1,5 | +2 | ⚠️ Chamar o núcleo de Dados |
| Offline só local (cálculo no aparelho, sem sincronizar) | 0 | 0 | 0 | |
| Offline com sincronização | +1,5 | +2 | +3 | ⚠️ Revisar a estrutura do banco |
| Volume de uso alto (milhares de usuários simultâneos, picos) | +1 | +1,5 | +2 | ⚠️ Requisitos de performance por escrito |

#### Integrações: peso fixo, sem perguntar ao CN

O CN não tem como avaliar a API de outro sistema, e não há técnico para validar antes da proposta. Por isso a skill **não pergunta** sobre documentação e **não pesquisa** o fornecedor: cada integração recebe um peso fixo a partir de duas informações que a PRD já traz.

1. **Sentido.** `envia` ou `recebe` → unidirecional. `envia e recebe` → bidirecional.
2. **De quem é o sistema do outro lado.**
   - **Serviço de mercado** → linha "com documentação" (`uni_doc` / `bi_doc`). É um produto vendido para qualquer empresa, com API pública: gateways de pagamento e Pix, mapas, push (Expo/FCM), modelos de IA, WhatsApp Business, emissores de NF-e, Google Calendar, envio de SMS etc.
   - **Sistema do cliente** → linha "sem documentação" (`uni_sem_doc` / `bi_sem_doc`). É um ERP, sistema legado, sistema feito sob medida ou qualquer sistema que só o cliente usa. Também entram aqui o meio `arquivo` (o layout ainda vai ser combinado) e **qualquer caso em dúvida** (fronteira para o lado mais pesado).

Bidirecional com sistema do cliente **não vira 🚩 por suposição**. Só vira `sem_api` quando a PRD diz explicitamente que o sistema não tem API. Sem essa informação, entra como `bi_sem_doc`, e a cláusula abaixo cobre o risco.

**Toda integração com sistema do cliente leva, na resposta:**
- **Cláusula de contrato sugerida** (em *Pontos de atenção*): "A integração com {sistema} depende de o cliente fornecer acesso à API e à documentação dela até o início da sprint {n}. Sem esse acesso, a integração será substituída por importação e exportação de planilha, sem alteração de prazo."
- **Plano B em "O que cortar":** trocar a integração por importação ou exportação manual de planilha, com a economia em semanas recalculada pelo script.

Os pesos são os que já existiam. A regra só fixa **qual linha usar**, para não depender de uma resposta que o CN não tem.

## F4 — Testes com o cliente
**Baseline do formulário:** 1 a 4 semanas. **Teto:** 4.

| Fator | Mín | Central | Máx |
|---|---|---|---|
| Base | 1 | 1,5 | 2 |
| Regra de negócio crítica (saúde, dinheiro, cálculo clínico ou legal) | +0,5 | +0,5 | +1 |
| Cliente com pouca disponibilidade para validar (plantões, agenda cheia) | +0,5 | +0,5 | +1 |

## F5 — Deploy
**Baseline do formulário:** 1 a 4 semanas.

| Fator | Mín | Central | Máx |
|---|---|---|---|
| Tem web (infra do NTec, ex: Vercel) | 0,5 | 0,5 | 1 |
| Tem app, sem web | 0,5 | 0,5 | 1 |
| Tem app, junto com web | +0 | +0,5 | +0,5 |
| Deploy na infra do cliente ou com regras de deploy dele | +1 | +1 | +2 |

## F6 — Publicação nas lojas (só app nativo)
**Baseline do formulário:** 2 a 6 semanas.

| Caso | Mín | Central | Máx |
|---|---|---|---|
| Não publica (PWA, web, ou app só para testes) | 0 | 0 | 0 |
| App comum | 2 | 2,5 | 4 |
| App sensível (saúde, finanças, público infantil): revisão mais rigorosa das lojas | 2,5 | 3 | 6 |

Dica que reduz o risco: pedir ao cliente que abra a conta de desenvolvedor (Apple e Google) **já na imersão**. Conta de empresa pode levar semanas para ser aprovada.

---

## Faixa final

Sem buffer percentual (removido em 17/10/2026: o efeito era desprezível e o risco já está no intervalo de cada linha).

| Cenário | Conta | Para que serve |
|---|---|---|
| **Otimista (piso)** | soma dos mínimos | Nunca vender abaixo disto. Só se chega nele com escopo congelado e cliente rápido |
| **Provável (recomendado)** | soma dos centrais | O valor para a proposta |
| **Conservador (teto de risco)** | soma dos máximos | O que acontece se os riscos listados se confirmarem |

- **Arredondamento:** semanas sempre para cima. A **recomendação de venda** é o provável arredondado para cima até fechar sprints inteiras (número par de semanas).
- **Depois somar as semanas off** do calendário.

---

## Parar e sinalizar (a skill não decide sozinha)

- 🚩 Multitenancy com instâncias e regras isoladas por cliente → "beira o inviável" (formulário).
- 🚩 Integração bidirecional que a PRD diz não ter API.
- 🚩 Feature atípica sem benchmark **e** sem documentação → pode exigir prova de conceito antes de vender.
- ⚠️ Dependência de dados → chamar o núcleo de Dados para avaliar se precisa de engenharia de dados.
- ⚠️ Provável acima de **26 semanas** → fora da faixa calibrada (ver Calibração). Validar com a área de projetos e considerar quebrar em fases ou contratos.
- ⚠️ Cliente Enterprise ou Grande com regras de deploy e restrição de stack → envolver a área de projetos antes da proposta.
- ⚠️ Qualquer teto de fase atingido (F1, F2 ou F4 em 4 semanas).

---

## Calibração (estado em 17/10/2026, sem buffer)

Rodando a régua sobre os projetos reais (detalhes em `exemplos/`):

| Projeto | Otimista | Provável | Conservador | Vendido | Realizado / situação | Leitura |
|---|---|---|---|---|---|---|
| Projeto A | 9 | 12 | 16 | 12 (+1 off) | No prazo, finalizando | ✅ Provável = vendido |
| Projeto D | 13 | 17 → **18** | 23 | 18 (+3 off) | Em execução, sem atraso (47,6% do prazo) | ✅ Recomendação = vendido |
| Projeto C | 13 | 18 | 23 | 11 (+2 off) | ~14 semanas, atrasou, testes não terminados | ⚠️ Vendido abaixo do piso → atrasou. Régua ~3 semanas acima do real |
| Projeto B | 11 | 14 | 21 | 12 (+1 off) | Em execução (45% do prazo), com Claude Code | ⚠️ Sem o fator, vendido entre piso e provável. **Com o fator Claude Code: 9 / 12 / 20, vender 12 = vendido.** O motor e a tela andaram bem mais rápido que a régua antiga |
| Projeto E | — | — | — | 34 | Em execução | Sem ficha técnica; não calibrado |
| Projeto F | — | — | — | 38 (+3 off) | Em execução | Sem ficha técnica; não calibrado |

Leituras:
- **Projetos pequenos e médios (até ~20 semanas):** a régua acerta ou fica um pouco acima. É intencional que erre para cima.
- **Viés conhecido:** quando o time aproveita bem o template, setup e login andam juntos e mais rápido (Projeto C fez os dois em 2 semanas). A régua não desconta isso automaticamente.
- **Claude Code:** a calibração acima é sem o fator (projetos antigos). Com o fator, os mesmos projetos dariam: A 7 / 10 / 15, C 10 / 15 / 22, D 10 / 15 / 22. Não comparar esses números com o vendido deles, que foi feito sem a ferramenta.
- **Projetos grandes (Projetos E, F, 30+ semanas):** sem dados de ficha, a régua **não está calibrada** para eles. Por isso o alerta acima de 26 semanas.

---

## Lacunas

- **Amostra pequena:** 4 projetos com dados, 2 ainda em execução. Os pesos são um ponto de partida, não uma regressão.
- **Contagem de fluxos dos projetos antigos é estimada** a partir das tasks do Notion (marcada como palpite nos exemplos).
- **Regras de tradução da PRD ainda não calibradas:** "1 módulo = 1 fluxo" e "concorrência, imutabilidade ou rotina agendada → módulo com RN específica" (`leitura-prd.md`) não foram conferidas contra um projeto real, porque todos os projetos da calibração são anteriores à PRD.
- **A "Régua de Dimensionamento" citada no formulário é uma subpágina do Notion** que não veio no PDF. Se ela tiver números diferentes, ela vence e este arquivo precisa ser atualizado.
- **Retrospectivas quase sempre vazias:** as causas de atraso não estão registradas.

---

## Registro das fontes

| Data | Fonte | O que trouxe |
|---|---|---|
| 16/10/2026 | Formulário *Dimensionamento Tec* (PDF, 5 páginas) | Estrutura de fases (baseline 1–4 semanas por fase, lojas 2–6), fatores do perfil da demanda, níveis de multitenancy e integração, buffer adaptável, checklist da área de projetos |
| 16/10/2026 | Levantamento no Notion do NTec (base de projetos: Projeto C, Projeto A, Projeto B, Projeto D, Projetos E, F) | Semanas vendidas, sprints realizadas, fases por task, riscos dos hand-offs |
| 16/10/2026 | Calibração inicial (Matheus Padilha + Claude) | Pesos mín/central/máx; regra "atípico ≠ RN específica"; corte de calibração em 26 semanas |
| 16/10/2026 | Skill `documento-requisitos-ntec` ([repositório](https://github.com/rivasaugustus/documento-requisitos-ntec)) | PRD vira a entrada padrão. Mapeamento da PRD para os fatores, sem peso novo: 1 módulo = 1 fluxo; fatores de complexidade da PRD encaixados nas linhas existentes (`leitura-prd.md`) |
| 17/10/2026 | Decisão do NTec: CNs não avaliam API e não há técnico para validar antes da proposta | Integração com peso fixo, sem perguntar ao CN: serviço de mercado = linha "com documentação", sistema do cliente = linha "sem documentação", com cláusula de contrato e plano B (planilha). Pesos inalterados |
| 17/10/2026 | Decisão do NTec: buffer desprezível | Buffer de risco adaptável (seção 8 do formulário) removido: provável = soma dos centrais, conservador = soma dos máximos. Projeto B passa de 11 / 15 / 23 para 11 / 14 / 21. Também saiu a negociação "quando o cliente pede menos prazo" (a seção "O que cortar" continua) |
| 17/10/2026 | Template "Proposta Técnica" do NTec (PDF, 2 páginas, 14 seções) | Entregável da skill: a faixa entra na caixa de status, no roadmap (10), nos pontos em aberto (11) e no cronograma sprint a sprint (13); a memória do dimensionamento vai num anexo. Pesos inalterados |
| 17/10/2026 | Ritmo real do Projeto B no git (dupla, ~20 h/semana, Claude Code) | Fator Claude Code: núcleo do F3 x0,4 / 0,5 / 0,65 e F2 x0,5 / 0,65 / 0,8; demais fases iguais. Time típico passa a ser a dupla com ~20 h/semana somadas. Projetos antigos ficam com `claude_code: false` |
| 17/10/2026 | Revisão da área de projetos: app + painel de 8 fluxos com offline deve levar ~12 sprints | Fator Claude Code revisto para o meio-termo: núcleo do F3 x0,6 / 0,75 / 0,9 e F2 x0,7 / 0,85 / 1 (o x0,5 inicial dava 20 semanas para esse projeto). Projeto B continua em vender 12 |
