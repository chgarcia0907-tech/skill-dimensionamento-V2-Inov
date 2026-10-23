# Dimensionamento NTec — Skill

_Guia explicativo · v5 (V2-Inov) · 22/10/2026. Se este guia e os arquivos da skill (raiz do repositório) divergirem, valem os arquivos da skill (e, para os pesos, `fatores/` e `scripts/calcular_faixa.py`)._

> **Para que serve este documento:** explicar o que tem na skill **dimensionamento-ntec**, como ela lê as **transcrições da AT Diagnóstico e da AT Aprofundamento** e chega a uma **faixa de semanas**, e como o coordenador de negócios (CN) usa no dia a dia.
> **Para quem:** CNs e área de projetos do Núcleo de Tecnologia. A skill não substitui a validação da área de projetos: ela evita que chegue à equipe um prazo "nada a ver".

1. O que é a skill
2. Onde ela entra no processo
3. Como acessar e usar
4. Arquitetura (o que tem dentro)
5. Procedimento
6. Das calls para a régua
7. F0 — Viabilidade
8. Régua de dimensionamento (F1 a F6)
9. Faixa final e cortes
10. O entregável: a Proposta Técnica
11. Lacunas: o que as calls não responderam
12. Calibração com projetos reais
13. Exemplo: PetAgenda sem e com as calls
14. Linha do tempo de exemplo (Projeto A)
15. Parar e sinalizar
16. Histórico, decisões em aberto e pendências

## 1. O que é a skill

Uma skill do Claude que transforma as **transcrições na íntegra do Fathom** da AT Diag e da AT Aprof numa faixa de semanas calibrada nos projetos reais do NTec. Ela dimensiona **pelo que o cliente confirmou nas duas calls**, sem documento de requisitos (PRD) no meio. Com uma call só, só o resumo do Fathom, ou sem transcrição (formulário *Dimensionamento Tec*, ficha, briefing), ela dimensiona mesmo assim, mas o resultado sai como **estimativa preliminar**. A arquitetura segue a skill de dimensionamento do NCiv (Gabrielle Lobo); a estrutura de fases segue o formulário Dimensionamento Tec.

- **Entrega três números:** otimista (piso), provável (recomendado) e conservador (teto de risco), em semanas e sprints de 2 semanas.
- **Começa pelo F0:** antes de contar semanas, confere se o projeto é viável (🚫 rejeita ou 🚩 para para a área de projetos).
- **Monta o inventário de jornadas** a partir das falas do cliente, com a citação (call e minuto) de cada uma.
- **Transforma o que as calls não responderam em lacuna:** entra na conta com o valor mais pesado, e o CN recebe a pergunta pronta para o cliente.
- **Mostra o que cortar:** cortes de escopo, com quantas semanas cada um economiza.
- **Entrega a Proposta Técnica em PDF**, no template oficial do NTec (Comercial → Validação de Projeto): as 15 seções, o cronograma sprint a sprint, a precificação, o checklist e a memória do dimensionamento.
- **Calcula o prazo e o preço do provável.** O preço sai do tipo de cada sprint: R$ 1.440 por analista por semana, 2 analistas em desenvolvimento e testes, 1 em imersão, deploy, gestão de mudança e publicação. O deploy é a primeira coisa depois da imersão. Os pesos supõem uma dupla com cerca de 20 horas por semana somadas e o template NTec, sem multiplicador por ferramenta e sem buffer percentual.

## 2. Onde ela entra no processo

```
AT Diag (dor e ideia) → AT Aprof (protótipo e escopo) → Dimensionamento (esta skill, pelas duas transcrições) → Proposta Técnica (PDF no template) → Área de projetos (valida) → Proposta (prazo vendido)
```

| Entrada | Status da resposta | Observação |
|---|---|---|
| Transcrição na íntegra da AT Diag **e** da AT Aprof (+ link do protótipo, se tiver) | **[OK]** | Entrada padrão. Cada fator aponta para a call e o minuto |
| Uma call só, ou só o resumo do Fathom | **[Revisar]** | "Estimativa preliminar". O resumo é texto do Fathom, não fala do cliente: não serve como citação |
| Formulário, ficha, briefing ou texto do CN, sem transcrição | **[Revisar]** | "Estimativa preliminar, sem transcrição das calls". Mandar as transcrições antes de fechar a proposta |

## 3. Como acessar e usar

- **Pelo nome:** em qualquer conversa do Claude Code, digitar `/dimensionamento-ntec` e colar as duas transcrições (Fathom, modo transcrição, na íntegra), mais o link do protótipo.
- **Pedindo direto:** "dimensiona esse projeto", "cabe em 12 semanas?", "isso é viável?". A skill é acionada sozinha.
- **Onde está instalada:** `~\.claude\skills\dimensionamento-ntec\` (pasta pessoal; vale para qualquer projeto).
- **Cópia de trabalho (para editar e versionar):** este repositório. A cópia instalada **não se atualiza sozinha**: depois de editar aqui, copiar de novo para lá.
- **No claude.ai:** compactar a pasta `dimensionamento-ntec` em .zip e enviar em Settings → Capabilities → Skills.
- **No GitHub:** `github.com/chgarcia0907-tech/skill-dimensionamento-V2-Inov`. A raiz do repositório é a pasta da skill: para o claude.ai, baixar o .zip (*Code → Download ZIP*) e enviar; para o Claude Code, extrair em `~/.claude/skills/dimensionamento-ntec/`.

## 4. Arquitetura (o que tem dentro)

Igual à skill do NCiv: um arquivo curto que coordena, e arquivos de conhecimento lidos só quando precisa.

| Arquivo | O que faz | Quando é lido |
|---|---|---|
| `SKILL.md` | Orquestrador: procedimento, regras gerais, quando parar, o entregável e a resposta curta no chat | Sempre |
| `fatores/README.md` e `fatores/glossario.md` | Índice dos fatores, decisões em aberto (D1 a D5) e a definição única de cada termo | Sempre |
| `fatores/F0-viabilidade.md` | Critérios que rejeitam (🚫) ou param (🚩) o projeto | Sempre, antes de tudo |
| `fatores/F1-*.md` a `fatores/F6-*.md` | Pergunta, onde ler, o que fazer sem resposta e os pesos de cada fase | Sempre |
| `leitura-transcricoes.md` | Como preparar a transcrição, o que conta como escopo, o inventário de jornadas, onde está cada campo do JSON nas calls e as lacunas | Sempre que houver transcrição |
| `insumos-e-perguntas.md` | Caminho sem transcrição (formulário, ficha, briefing) e vocabulário negócio → técnico | Quando não há transcrição |
| `regua-dimensionamento.md` | Regras de uso, faixa final, quando parar, calibração e registro das fontes | Sempre |
| `regra-fronteira-e-faixa.md` | Desempate quando um fator cabe em duas linhas; tabela de cortes | Em caso de dúvida e para "O que cortar" |
| `scripts/calcular_faixa.py` | Faz a conta (fonte da verdade dos pesos), para o número não sair de cabeça | Sempre |
| `proposta-tecnica.md` | Como preencher cada uma das 15 seções da Proposta Técnica a partir das calls e da conta | Sempre, no fim |
| `template-proposta-tecnica.md` | O template original do NTec, como o comercial recebe | Só para consulta |
| `scripts/gerar_proposta.py` | Gera o PDF "[Proposta Técnica] {projeto}", recalcula a faixa, calcula o preço e confere o checklist do template | Sempre, no fim |
| `exemplos/` | Precedentes reais anonimizados (Projetos A a D, Projeto H), Projetos E e F pendentes e o caso fictício PetAgenda. Cada ficha traz no fim o JSON de entrada da régua | Para comparar com projeto parecido |

## 5. Procedimento

1. **Ler a entrada.** Com as duas transcrições, seguir `leitura-transcricoes.md`: preparar a transcrição (quem é cliente, o que descartar), separar o que o cliente confirmou do que é ideia solta e montar o **inventário de jornadas**. Com uma call só, ou sem transcrição, marcar como preliminar.
2. **F0 — Viabilidade.** Responder cada critério com citação da call. 🚫 → parar aqui, sem PDF. 🚩 → seguir dimensionando, mas a proposta não vai ao cliente antes da área de projetos.
3. **Preencher F1 a F6**, cada fator pelo seu arquivo em `fatores/`. A linha mais leve só entra com o trecho da call que a justifica; sem citação, vai a mais pesada. O que as calls não respondem vira **lacuna** (seção 11). Integrações não geram pergunta: peso fixo.
4. **Montar o JSON e rodar o script.** Nenhum campo tem padrão: se faltar um, o script para e diz qual.
5. **Comparar com o precedente** mais parecido. Diferença acima de 30% precisa de explicação. Comparar também com o prazo que o CN já falou na AT Aprof, se falou.
6. **Aplicar a regra de fronteira** se precisar (no máximo 3 ajustes por projeto).
7. **Montar a Proposta Técnica** (um JSON com as 15 seções e a memória do dimensionamento) e gerar o PDF com `gerar_proposta.py`.
8. **Responder no chat, curto:** status, prazo em uma frase, faixa, inventário de jornadas, caminho do PDF, lacunas para o CN, itens pendentes do checklist e os 2 ou 3 pontos de atenção mais graves.

## 6. Das calls para a régua

As duas calls têm papéis diferentes. A **AT Diag** traz a dor, o contexto, as jornadas que o cliente descreve e o formato. A **AT Aprof** traz a validação do protótipo, o que foi confirmado ou descartado, login, lojas e, às vezes, prazo e preço.

### O que conta como escopo

**Só entra na conta o que o cliente confirmou.**

| O que aparece na call | Entra na conta? | Para onde vai |
|---|---|---|
| O cliente descreve uma funcionalidade como parte do produto | Sim | Inventário |
| O CN propõe e o cliente confirma **aquela** proposta | Sim | Inventário |
| Telas do protótipo que o cliente aprovou na AT Aprof | Sim | Inventário e seção 14 |
| O CN propõe e o cliente não responde ou muda de assunto | Não | Lacuna, se mexe no prazo |
| O cliente hesita ("não sei se precisa", "talvez") | Não | Lacuna, se mexe no prazo; senão roadmap *A confirmar* |
| O cliente descarta ("não precisa") | Não | Exclusão. Não pode virar corte |
| Ajuste visual, textos, nomes | Não soma | Pontos para a imersão |
| "Depois a gente vê", "numa segunda versão" | Não | Roadmap *Futuro* |
| Prazo ou preço que o **CN** já falou ao cliente | **Nunca** | *Observações*, comparado com a faixa |
| Data que o **cliente** exige | Sim, no F0 | `prazo_exigido_semanas` |

A skill **não acrescenta escopo**: se achar que falta algo e ninguém falou disso, vai para *Pontos de atenção* ("as calls não cobrem X").

### Inventário de jornadas

Uma linha por **jornada** (o que alguém faz do começo ao fim no sistema, como o cliente descreveu), com quem faz, onde (app, web, painel), regra ou cálculo, integrações, dados de fora e a citação. Login e perfis (F2), lojas (F5 e F6) e offline (extra do F3) ficam fora da contagem. Variações da mesma jornada contam uma vez; jornada com mais de 8 ações diferentes conta 2.

### Funcionalidades que a régua não tem como linha

Encaixam nas linhas que já existem, sem peso novo:

| O cliente fala de… | Linha da régua |
|---|---|
| Pagamento (gateway, Pix, assinatura no app) | Integração bidirecional com serviço de mercado (`bi_doc`). App pago na loja = 0 |
| IA (classificar, extrair, gerar, responder) | Integração unidirecional com serviço de mercado (+ alerta se decide sem humano) |
| Notificação push · WhatsApp automático | Integração unidirecional (bidirecional se o sistema lê a resposta) |
| E-mail · upload de arquivo | Template (0) |
| Concorrência · imutabilidade · rotina agendada | A jornada vira fluxo com RN específica (uma vez por jornada) |
| Tempo real por push · relatório configurável pelo usuário | Feature atípica (atualização periódica, tela fixa ou exportação = 0) |
| Migração ou carga de base existente | Dependência de dados |

### Integrações: peso fixo, sem perguntar ao CN

O CN não tem como avaliar a API de outro sistema. A linha sai de perguntas que as calls respondem: a troca é automática? É login, e-mail ou upload (template)? O cliente diz que não tem API (F0)? Envia e recebe (bi) ou só um dos dois (uni)? O outro lado é **serviço de mercado** (documentação pública e sandbox que o NTec acessa sozinho)?

| Sistema do outro lado | Linha | O que mais sai na resposta |
|---|---|---|
| **Serviço de mercado** (Mercado Pago, Stripe, Google Maps, Expo Push, OpenAI, WhatsApp Business, NF-e) | Com documentação (`_doc`) | Nada |
| **Sistema do cliente** (ERP, legado, sob medida, SaaS que depende da TI do cliente) ou dúvida | Sem documentação (`_sem_doc`) | Cláusula de contrato + plano B (planilha) em "O que cortar" |
| O cliente diz que o sistema não tem API | F0, parado | Área de projetos avalia |

## 7. F0 — Viabilidade

O F0 não soma semanas: decide se a skill dimensiona.

| Resultado | Critérios | O que a skill faz |
|---|---|---|
| 🚫 **Rejeitado** | Stack exigida fora da lista aceita (Next.js/React, Expo/React Native, Node/TypeScript, MongoDB, Postgres, Supabase, Vercel, AWS); SLA ou sustentação além da garantia de 30 dias | Não dimensiona e não gera PDF. Responde ao CN com o critério, o motivo e o que precisaria mudar |
| 🚩 **Parado** | Multa por atraso; feature sem referência **e** sem documentação; hardware; multitenancy com regra diferente por cliente; integração com sistema sem API; prazo exigido abaixo do otimista (conferido depois da conta, com análise de entrega parcial) | Dimensiona, mas a proposta não vai ao cliente sem a área de projetos |
| **Condição de escopo** | Infra do cliente sem acesso do NTec | Dimensiona sem o deploy (F5 zerado). O deploy é do cliente, e a proposta diz que a garantia de 30 dias não se aplica |

Trocar MongoDB por Postgres ou Supabase **não** rejeita: soma como troca de stack no F1. Offline com sincronização também não rejeita: o banco é Postgres, como premissa técnica (D5, em aberto, decide se isso soma no F1).

## 8. Régua de dimensionamento (F1 a F6)

Cada linha tem **mínimo / central / máximo** em semanas. Os pesos já consideram o time típico do NTec (uma dupla com cerca de 20 horas por semana somadas, sprints de 2 semanas, template Next.js + Expo + MongoDB/Prisma + Better Auth). Login por e-mail e Google, recuperação de senha, e-mail (Resend), upload para S3 e painel admin básico já vêm no template e não somam prazo.

### F1 — Imersão, refinamento e setup (teto 4)

| Fator | Mín | Central | Máx |
|---|---|---|---|
| Base (sempre) | 1,5 | 2 | 2,5 |
| Demanda pouco detalhada (falta a AT Aprof, jornadas não listáveis, formato não decidido, regra que o cliente não sabe descrever) | +0,5 | +1 | +1 |
| Troca de stack aceita no F0 (ex.: MongoDB → Supabase) | +1 | +1,5 | +2 |
| Produto atípico (sem referência) | +0,5 | +0,5 | +1 |

### F2 — Infra, níveis de acesso e login (teto 4)

| Níveis de acesso / multitenancy | Mín | Central | Máx |
|---|---|---|---|
| Nenhum (sem login) | 0 | 0 | 0 |
| 1 nível | 0,5 | 0,5 | 1 |
| 2 a 5, poucas diferenças | 0,5 | 1 | 1,5 |
| 2 a 5, grandes diferenças (telas e regras próprias, aprovação de cadastro) | 1,5 | 2 | 2,5 |
| 6 ou mais | 2,5 | 3 | 4 |
| Multitenancy: dados separados | +0,5 | +0,5 | +1 |
| Multitenancy: isolamento de dados | +1 | +1,5 | +2 |
| Multitenancy: regras diferentes por cliente | F0, parado | — | — |

### F3 — Desenvolvimento

**Fluxo** = jornada completa que o cliente descreveu. Cada fluxo é multiplicado pelo fator do **código em que existe**: **Web x1,0 · PWA x1,1 · App nativo x1,2**. Fluxo com tela em dois códigos (`compartilhado`) recebe o fator do mais pesado **+0,2 por formato extra** (app + painel web = x1,4). Integrações e extras somam depois do fator.

| Item | Mín | Central | Máx |
|---|---|---|---|
| Cada fluxo comum (CRUD, listagem, mapa com filtros, agenda) | 1 | 1,25 | 1,5 |
| Cada fluxo com regra de negócio específica (fórmula, tabela, norma, concorrência, rotina agendada) | 2 | 3 | 4 |
| Cada feature atípica (sem referência) | 1 | 1,5 | 2 |
| Integração unidirecional com serviço de mercado | +0,5 | +0,5 | +1 |
| Integração bidirecional com serviço de mercado | +0,5 | +1 | +1,5 |
| Integração unidirecional com sistema do cliente | +1 | +1,5 | +2 |
| Integração bidirecional com sistema do cliente | +4 | +4 | +5 |
| Dependência de dados (migrar, limpar ou cruzar bases que já existem) — chamar o núcleo de Dados | +1 | +1,5 | +2 |
| Offline com sincronização (offline só local = 0) — exige Postgres | +1,5 | +2 | +3 |
| Volume de uso alto (milhares simultâneos) | +1 | +1,5 | +2 |

### F4, F5 e F6 — Testes, deploy e lojas

| Fase / fator | Mín | Central | Máx |
|---|---|---|---|
| F4 Testes com cliente — base (teto 4) | 1 | 1,5 | 2 |
| F4 + regra de negócio crítica (o código do NTec calcula saúde, dinheiro ou prazo legal) | +0,5 | +0,5 | +1 |
| F5 Deploy web | 0,5 | 0,5 | 1 |
| F5 Deploy de app sem web / app junto com web | 0,5 / +0 | 0,5 / +0,5 | 1 / +0,5 |
| F5 + infra ou regras de deploy do cliente | +1 | +1 | +2 |
| F6 Lojas — app comum | 2 | 2,5 | 4 |
| F6 Lojas — app sensível (saúde, finanças, crianças, pagamento no app) | 2,5 | 3 | 6 |

_Desde 20/10/2026 a régua não tem fator Claude Code nem o fator "cliente com pouca disponibilidade". Tetos de fase não cortam a soma: a fase acima do teto sai com alerta. Semanas off (férias, provas, recessos) e a garantia gratuita de 30 dias ficam fora da régua: as semanas off são somadas depois, pelo calendário._

## 9. Faixa final e cortes

| Cenário | Conta | Para que serve |
|---|---|---|
| **Otimista (piso)** | Soma dos mínimos | Nunca vender abaixo disto |
| **Provável (recomendado)** | Soma dos centrais | O valor para a proposta |
| **Conservador (teto)** | Soma dos máximos | O que acontece se os riscos se confirmarem |

Semanas são sempre arredondadas para cima. A **recomendação de venda** é o provável fechado em sprints inteiras (número par de semanas), mais as semanas off. Com lacunas, a venda mostra com "+" quanto depende delas (seção 11). Sem buffer percentual: o risco está no intervalo de cada linha.

### Cortes que mais economizam

| Corte | Economia típica (central) |
|---|---|
| Publicar como PWA em vez de app nas lojas | F6 inteira (2,5 a 3) + fator de formato |
| Tirar o segundo formato do MVP (só app ou só web) | Fluxos compartilhados de x1,4 para x1,2; os fluxos que só existem no código cortado saem junto; parte do deploy |
| Juntar perfis de usuário | 0,5 a 1 em F2 |
| Mover jornadas não essenciais para uma fase 2 | 1,25 por fluxo comum e 3 por fluxo com RN específica, vezes o fator do código |
| Trocar integração automática por importação manual no MVP (plano B de toda integração com sistema do cliente) | 0,5 a 4 |

_Na dúvida entre duas linhas da régua, a skill vai sempre para a mais pesada, com um comentário de duas linhas explicando o ajuste (máximo de 3 ajustes por projeto). O histórico do NTec é vender para menos. Todo corte é recalculado com o script e nunca é algo que o cliente já descartou na call._

## 10. O entregável: a Proposta Técnica

O dimensionamento final sai no **template "Proposta Técnica" do NTec** (Comercial → Validação de Projeto). O PDF "[Proposta Técnica] {projeto}" é gerado pelo `scripts/gerar_proposta.py`, que recalcula a faixa a partir dos fatores, para a proposta nunca divergir da régua. O template original pede PRD + protótipo; na V2-Inov, o cabeçalho e o checklist pedem as **duas transcrições** + protótipo.

| Parte da proposta | O que leva |
|---|---|
| Caixa de status (topo) | Status, prazo recomendado (com "+" das lacunas) e a faixa otimista / provável / conservador |
| 1 a 3. Problema, visão geral, entidades | A dor e as jornadas contadas na AT Diag; formato e público confirmados nas calls |
| 4. Perfis · 6. Regras · 8. Segurança (obrigatórias) | Tipos de pessoa citados, toda regra dita nas calls, dados, login e logs. O que ninguém discutiu sai como "não discutido nas calls" |
| 5. Fluxo · 7. Arquitetura · 9. Módulos críticos | A jornada principal etapa por etapa (com as decisões futuras marcadas), componentes, integrações e automações |
| 10. Roadmap (obrigatória) | Tudo que está na conta é Prioritário; A confirmar e Futuro nunca entram no cronograma |
| 11. Pontos em aberto (obrigatória) | Lacunas das calls, documentos que o cliente precisa mandar, divergências e dependências externas. Nunca vazio |
| 12. Stack | Template NTec, sempre como premissa a validar na Sprint de Refino |
| 13. Cronograma sprint a sprint | As fases F1 a F6 (centrais) em sprints de 2 semanas, somando a recomendação; sprint que depende da seção 11 vem marcada |
| 14. Protótipo × regras (obrigatória) | Só com protótipo recebido; sem ele, a seção sai com aviso para o comercial |
| Checklist final | O script marca OK ou PENDENTE em cada item do template |
| Anexo — Memória do dimensionamento | Faixa, F1 a F6 com critério e citação, inventário de jornadas, alertas, pontos de atenção, lacunas, precedente, O que cortar, suposições, fronteira, imersão e observações (prazo ou preço que o CN já falou) |

_Nada interno no corpo da proposta: as origens e citações ficam no anexo e no chat. O antigo bloco para colar no formulário Dimensionamento Tec saiu: o template de Proposta Técnica o substitui._

## 11. Lacunas: o que as calls não responderam

O que as duas calls não respondem vira **lacuna**. A skill dimensiona mesmo assim, com o valor mais pesado plausível, e:

1. **Mostra quanto da venda depende das lacunas:** *"Recomendado vender 14 semanas (7 sprints) = 12 + 2 que dependem de confirmar com o cliente (login e perfis, integrações)"*.
2. **Devolve ao CN as Lacunas para o CN** (no chat, na seção 11 e no anexo): o fator, o que foi procurado e não achado, a pergunta pronta e o valor provisório.
3. **Status:** lacuna que mexe na faixa → **[Revisar]** até o CN responder. Lacuna só na data de início não rebaixa o status.

No máximo 5 perguntas por rodada, as que mais mexem no prazo primeiro. O CN repassa ao cliente (WhatsApp serve), a skill troca o valor e roda de novo.

| Fator | Pergunta para o cliente |
|---|---|
| Login | A pessoa precisa criar conta e entrar com login, ou abre o app e já usa? |
| Pagamento | Como você quer cobrar: o app é pago na loja, tem assinatura dentro do app, ou é gratuito? |
| Lojas | O app vai para a App Store e a Play Store, ou só para uso interno? |
| Referência | Existe algum app ou site parecido que a gente possa usar de referência? |
| Stack e infra | Vocês exigem alguma tecnologia, ou que o sistema fique nos servidores de vocês? |
| Documento da regra | Você consegue mandar a planilha (ou a tabela, a norma) com as fórmulas que o sistema vai seguir? |
| Data de início | Qual é a data prevista de início? (para contar férias, provas e recesso) |

Sem transcrição nenhuma, a skill usa as perguntas de `insumos-e-perguntas.md` (fluxos, regra de negócio, formato, níveis de acesso, integrações, offline, multitenancy, condições de contrato).

## 12. Calibração com projetos reais

A régua atual (revisão de 20/10/2026) rodada sobre os projetos do NTec. Os projetos aparecem anonimizados. Faixa = otimista / provável / conservador, em semanas.

| Projeto | Formato | Vendido | Faixa da régua | Situação | Leitura |
|---|---|---|---|---|---|
| Projeto A | PWA | 12 (+1 off) | 9 / **12** / 16 | No prazo, finalizando | **[OK]** Provável = vendido |
| Projeto D | App + web | 18 (+3 off) | 13 / **18** / 23 | Execução, sem atraso | **[OK]** Recomendação = vendido |
| Projeto C | Web + app | 11 (+2 off) | 13 / **18** / 24 | Entregue com atraso (~14 sem) | **[Revisar]** Vendido abaixo do piso → atrasou |
| Projeto B | App nativo | 12 (+1 off) | 10 / **13 → vender 14** / 20 | Execução, 45% | **[Revisar]** Vendido entre o piso e o provável; conferir em 23/11/2026 |
| Projeto H | App nativo | Em negociação | 10 / **13 → vender 14** / 20 | Primeiro pelas transcrições | **[Revisar]** A CN falou "2 a 3 meses"; "2 meses" fica abaixo do piso |
| Projetos E e F | ? | 34 e 38 | não calibrado | Execução | — |

- **Projetos A e D:** a recomendação da régua bate com o vendido, e os dois estão no prazo.
- **Projeto C:** vendido abaixo do piso (11 contra 13) e atrasou. A régua ficou ~3 semanas acima do real, porque o time juntou setup e login em 2 semanas: viés conhecido, não corrigido com um único projeto.
- **Projeto B:** codado com Claude Code, o motor e a tela andaram mais rápido que a régua. O fator Claude Code saiu em 20/10/2026: se o ganho for real, ele aparece nos realizados e entra pelos pesos, com dado medido.
- **Projetos E e F:** sem ficha técnica. Por isso, todo provável acima de **26 semanas** sai com alerta de "fora da faixa calibrada".

> **Os Projetos A a D são anteriores à leitura das calls.** Os fluxos foram contados a partir das tasks do Notion. O Projeto H é o primeiro dimensionado pelas transcrições ("fluxo = jornada descrita pelo cliente"); quando ele terminar, vira o precedente para conferir essa leitura.

## 13. Exemplo: PetAgenda sem e com as calls

Caso fictício: app para tutores de pets (lojas) e painel web para uma rede de 3 clínicas. 4 perfis (tutor, recepção, veterinário, admin da rede), pagamento pelo Mercado Pago e lembrete de vacina por push.

| Fator | Valor | Origem nas calls |
|---|---|---|
| Formatos | app + web, com fator por fluxo | Onde cada jornada acontece |
| Níveis de acesso | 2 a 5, grandes diferenças | AT Aprof: recepção e veterinário com telas próprias |
| Multitenancy | dados separados | Cada clínica vê só os próprios dados, com as mesmas regras |
| Fluxos | 3 comuns + 1 com RN específica | O lembrete é uma rotina agendada (data da próxima dose) |
| Integrações | Mercado Pago (bi, mercado); push (uni, mercado) | Peso fixo |
| Demanda pouco detalhada | não | As duas calls existem |

|  | Sem transcrição (só o relato do CN) | Com as duas calls |
|---|---|---|
| Imersão (F1, central) | 3 semanas (demanda sem documento) | 2 semanas |
| Desenvolvimento | 4 fluxos comuns | 3 comuns + 1 com RN (lembrete agendado) |
| Faixa (otim. / prov. / cons.) | 14 / 18 / 24 | 14 / 19 / 26 |
| Recomendação de venda | 18 semanas (9 sprints) | 20 semanas (10 sprints) |

_As calls tiraram a semana extra de imersão, mas revelaram o lembrete por rotina agendada, que o relato não deixava claro e pesa mais que um fluxo comum. Arquivos: `exemplos/ficticio-petagenda.md` (sem transcrição) e `exemplos/ficticio-petagenda-proposta.md` (proposta completa)._

## 14. Linha do tempo de exemplo (Projeto A)

As fases no valor central da régua, encaixadas no calendário real do projeto: início em 20/07/2026, 12 semanas de trabalho + 1 semana off entre a S4 e a S5, fim previsto em 19/10/2026.

| Fase | Semanas (a partir de 20/07/2026) | Duração |
|---|---|---|
| F1 Imersão e setup | 0 → 2 | 2 sem |
| F2 Acesso e login | 2 → 3 | 1 sem |
| F3 Desenvolvimento | 3 → 8 | 5 sem |
| Semana off | 8 → 9 | 1 sem |
| F3 Desenvolvimento (cont.) | 9 → 10,5 | 1,5 sem |
| F4 Testes com cliente | 10,5 → 12 | 1,5 sem |
| F5 Deploy + arredondamento | 12 → 13 | 1 sem |

_Total: 13 semanas (12 de trabalho + 1 off), de 20/07/2026 a 19/10/2026. A linha de deploy inclui o arredondamento de 11,5 para 12 semanas._

## 15. Parar e sinalizar

A skill não decide sozinha nestes casos. Ela marca e devolve para a área de projetos:

- **[Rejeitado]** Critério de rejeição do F0 (seção 7): não dimensiona.
- **[Parado]** Critério de parada do F0 (seção 7), inclusive multitenancy com regra por cliente, integração sem API e prazo exigido abaixo do otimista.
- **[Revisar]** Demanda pouco detalhada → recomendar discovery antes da proposta. O status nunca é OK.
- **[Revisar]** Prazo que o CN já falou ao cliente abaixo do otimista: a expectativa do cliente está errada e o CN precisa corrigir antes da proposta.
- **[Revisar]** Dependência de dados de bases soltas → chamar o núcleo de Dados.
- **[Revisar]** Provável acima de 26 semanas (fora da faixa calibrada) → considerar quebrar em fases.
- **[Revisar]** Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.
- **[Revisar]** Divergência entre as duas calls, ou entre o que o CN declarou e o que aparece na transcrição.
- **[Revisar]** Lacuna que mexe na faixa, até o CN responder.
- **[Revisar]** Estimativa sem as duas transcrições: sempre preliminar.
- **[Revisar]** Teto de fase passado (F1, F2 ou F4 acima de 4 semanas): a soma é mantida, não cortada.

## 16. Histórico, decisões em aberto e pendências

| Data | O que aconteceu |
|---|---|
| 13/04/2026 | Início do Projeto C (primeiro projeto da base de calibração) |
| 10/07/2026 | Deploy do Projeto C, com atraso: 11 semanas vendidas, ~14 realizadas |
| 20/07/2026 | Início do Projeto A e do Projeto E |
| 01/09/2026 | Início do Projeto B |
| 16/10/2026 | v1: criação e calibração da skill a partir da skill do NCiv, do formulário Dimensionamento Tec e do levantamento no Notion. v2: a PRD vira a entrada padrão; projetos anonimizados; publicação no GitHub |
| 17/10/2026 | v3: integrações com peso fixo, sem perguntar ao CN; buffer de risco e negociação de prazo removidos; o que a PRD não responde vem do Fathom, e o que faltar volta ao CN como lacuna |
| 17/10/2026 | v4: o entregável passa a ser a Proposta Técnica no template do NTec (PDF gerado pela skill); fator Claude Code na régua |
| 19/10/2026 | Fim previsto do Projeto A — confirmar se a calibração continua valendo |
| 20/10/2026 | Reunião "Validação Skill NTec" (aplicada em 21/10): F0 de viabilidade, um arquivo por fator em `fatores/`, JSON sem padrões, tetos que não cortam, fator Claude Code e "cliente com pouca disponibilidade" removidos, F2 em 2 a 5 / 6+, formato extra +0,2, `bi_sem_doc` com mínimo 4 |
| 22/10/2026 | Projeto G: fator de formato por fluxo (`fluxos_por_formato`) |
| 22/10/2026 | **V2-Inov:** a entrada padrão passa a ser a transcrição na íntegra da AT Diag e da AT Aprof; primeiro caso pelas transcrições: Projeto H. Insumos em Markdown e exemplos refeitos com a régua atual. Guia v5 |
| 23/11/2026 | Fim previsto do Projeto B e do Projeto D — atualizar a calibração com o realizado |

### Decisões em aberto (valores provisórios no script)

| Código | Decisão | Provisório |
|---|---|---|
| D1 | "Formato extra pelo menos 1,2": +0,2 por formato extra ou x1,2 sobre o fator? | +0,2 (app + web = x1,4) |
| D2 | Pesos que a reunião mandou aumentar (2 a 5 com grandes diferenças, isolamento, RN crítica, central e máximo de `bi_sem_doc`) | Valores atuais; `bi_sem_doc` 4 / 4 / 5 |
| D3 | Margem de segurança explícita sobre o F3 ou o total? | Sem margem extra, com aviso |
| D4 | Fase acima do teto: manter a soma ou parar? | Manter a soma e marcar |
| D5 | Postgres obrigatório por causa do offline soma como troca de stack no F1? | Não soma; vira premissa da Sprint de Refino |

### Pendências

- Fechar as decisões D1 a D5 com a área técnica e fazer o teste de concordância (2 CNs + Claude nos Projetos A a D).
- Fichas técnicas de Projetos E e F, para calibrar projetos grandes (o levantamento recebido veio cortado).
- Conteúdo da subpágina "Régua de Dimensionamento" do Notion, citada no formulário mas não recebida. Se tiver números, eles valem mais que os da skill.
- Conferir no hand-off do Projeto D os fatores marcados como palpite (perfis, fluxos, offline, onde cada jornada vive).
- Preencher as retrospectivas: hoje quase todas estão vazias, e sem elas não se sabe a causa dos atrasos.
- Conferir a leitura das transcrições ("fluxo = jornada descrita pelo cliente", "só conta o que o cliente confirmou") quando o Projeto H terminar.
- Conferir com o realizado do Projeto B (23/11/2026) se a régua sem fator de ferramenta ficou acima do real.

> **Manutenção:** pesos mudam no `scripts/calcular_faixa.py` **e** no arquivo da fase em `fatores/`, com uma linha no Registro das fontes de `regua-dimensionamento.md`. Quando um projeto termina, ele entra em `exemplos/` com vendido × realizado, anonimizado; o nome real fica só na pasta `privado/`, fora do GitHub.
