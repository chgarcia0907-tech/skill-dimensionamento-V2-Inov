# Dimensionamento NTec — Skill

_Versão em Markdown do antigo PDF explicativo (v4 · 17/10/2026). É anterior à revisão de 20/10 e à V2-Inov: ainda fala da PRD como entrada padrão e do fator Claude Code. Para as regras em vigor, valem os arquivos de `.claude/skills/dimensionamento-ntec/`._

> **Para que serve este documento:** explicar o que tem na skill **dimensionamento-ntec**, como ela lê a **PRD** (o documento de requisitos do projeto) e chega a uma **faixa de semanas**, e como o coordenador de negócios (CN) usa no dia a dia.   
> **Para quem:** CNs e área de projetos do Núcleo de Tecnologia. A skill não substitui a validação da área de projetos: ela evita que chegue à equipe um prazo "nada a ver".

1. O que é a skill
2. Onde ela entra no processo
3. Como acessar e usar
4. Arquitetura (o que tem dentro)
5. Procedimento
6. Da PRD para a régua
7. Régua de dimensionamento (F1 a F6)
8. Faixa final e cortes
9. O entregável: a Proposta Técnica
10. Perguntas para o CN: Fathom e lacunas
11. Calibração com projetos reais
12. Exemplo: PetAgenda a partir da PRD
13. Linha do tempo de exemplo (Projeto A)
14. Parar e sinalizar
15. Histórico, datas e pendências

## 1. O que é a skill

Uma skill do Claude que transforma a **PRD** do projeto (o documento de requisitos "[Requisitos] {projeto}", que vira anexo de contrato) numa faixa de semanas calibrada nos projetos reais do NTec. Sem PRD, ela aceita o formulário *Dimensionamento Tec*, uma ficha, um briefing ou a transcrição de uma call, mas o resultado sai como **estimativa preliminar**. A arquitetura segue a skill de dimensionamento do NCiv (Gabrielle Lobo). A estrutura de fases segue o formulário Dimensionamento Tec.

- **Entrega três números:** otimista (piso), provável (recomendado) e conservador (teto de risco), em semanas e sprints de 2 semanas.
- **Pergunta em linguagem de negócio** o que falta, e traduz a resposta para os fatores técnicos.
- **Mostra o que cortar**: cortes de escopo, com quantas semanas cada um economiza.
- **Entrega a Proposta Técnica em PDF**, no template oficial do NTec (Comercial → Validação de Projeto): as 14 seções, o cronograma sprint a sprint, o checklist e a memória do dimensionamento (seção 9).
- **Considera Claude Code:** os pesos supõem uma dupla com cerca de 20 horas por semana somadas, codando com Claude Code (seção 7). A régua não usa buffer percentual.

## 2. Onde ela entra no processo

A skill roda **depois** da skill `documento-requisitos-ntec`, que transforma as reuniões com o cliente na PRD. Ela ocupa o lugar que a skill da PRD chama de *validacao-tecnica-ntec*, mas calcula só o prazo, sem preço.

```
Reuniões (com o cliente) → PRD (skill da PRD) → Dimensionamento (esta skill) → Proposta Técnica (PDF no template) → Área de projetos (valida) → Proposta (prazo vendido)
```

| Entrada | Status da resposta | Observação |
|---|---|---|
| PRD (PDF ou markdown), com ou sem o bloco "Inventário para dimensionamento" | **[OK]** | Entrada padrão. Cada fator aponta para uma seção da PRD |
| Formulário, ficha, briefing ou transcrição, sem PRD | **[Revisar]** | "Estimativa preliminar, sem PRD". Gerar a PRD antes de fechar a proposta |

## 3. Como acessar e usar

- **Pelo nome:** em qualquer conversa do Claude Code, digitar `/dimensionamento-ntec` e mandar o PDF da PRD (e, se tiver, o bloco "Inventário para dimensionamento" do chat da PRD).
- **Pedindo direto:** "dimensiona esse projeto", "cabe em 12 semanas?", "isso é viável?". A skill é acionada sozinha.
- **Onde está instalada:** `~\.claude\skills\dimensionamento-ntec\` (pasta pessoal; vale para qualquer projeto).
- **Cópia de trabalho (para editar e versionar):** `Projetos\skill-dimensionamento-ntec\`. As duas cópias não se sincronizam sozinhas.
- **No claude.ai:** compactar a pasta em .zip e enviar em Settings → Capabilities → Skills.
- **No GitHub:** `github.com/matheusrpgomes-sketch/skill-dimensionamento-ntec` (público). Para instalar, clonar e copiar `.claude/skills/dimensionamento-ntec` para `~/.claude/skills/`.

## 4. Arquitetura (o que tem dentro)

Igual à skill do NCiv: um arquivo curto que coordena, e arquivos de conhecimento lidos só quando precisa.

| Arquivo | O que faz | Quando é lido |
|---|---|---|
| SKILL.md | Orquestrador: procedimento, regras gerais, quando parar, o entregável e a resposta curta no chat | Sempre |
| leitura-prd.md | Onde está cada fator na PRD, tradução dos fatores de complexidade dela e o que perguntar ao CN | Sempre primeiro, quando há PRD |
| insumos-e-perguntas.md | Caminho sem PRD: como ler formulário, ficha ou transcrição; vocabulário negócio → técnico | Quando não há PRD |
| regua-dimensionamento.md | Pesos de cada fase (F1 a F6), faixa final, calibração e fontes | Sempre |
| regra-fronteira-e-faixa.md | Desempate quando um fator cabe em duas linhas; tabela de cortes | Em caso de dúvida e para O que cortar |
| scripts/calcular_faixa.py | Faz a conta (fonte da verdade dos pesos, incluindo o fator Claude Code), para o número não sair de cabeça | Sempre |
| proposta-tecnica.md | Como preencher cada uma das 14 seções da Proposta Técnica a partir da PRD e da conta | Sempre, no fim |
| scripts/gerar_proposta.py | Gera o PDF "[Proposta Técnica] {projeto}", recalcula a faixa e confere o checklist do template | Sempre, no fim |
| exemplos/ | Precedentes reais anonimizados (Projetos A a D), Projetos E e F pendentes e o caso fictício PetAgenda (sem PRD, via PRD e o JSON modelo da proposta) | Para comparar com projeto parecido |

## 5. Procedimento

1. **Ler a entrada.** Com PRD, seguir a leitura da seção 6 (se o inventário não veio, montar a partir do PDF). Sem PRD, ler o formulário, a ficha ou a transcrição e marcar a resposta como preliminar. Cada dado leva a origem, por exemplo *(origem: PRD 2.3)*.
2. **Preencher os fatores** da régua. Com PRD, a rodada de perguntas ao CN cobre só o que a PRD não responde (até 5 por rodada, as que mais mexem no prazo primeiro). Sem resposta, usar o valor mais pesado e registrar em Suposições.
3. **Rodar o script** com os fatores e obter as fases em mínimo, central e máximo.
4. **Comparar com o precedente** mais parecido. Diferença acima de 30% precisa de explicação.
5. **Aplicar a regra de fronteira** se precisar.
6. **Montar a Proposta Técnica** (um JSON com as 14 seções e a memória do dimensionamento) e gerar o PDF com `gerar_proposta.py`.
7. **Responder no chat, curto:** status, prazo em uma frase, faixa, caminho do PDF, lacunas para o CN, itens pendentes do checklist e os 2 ou 3 pontos de atenção mais graves.

## 6. Da PRD para a régua

A PRD descreve o **produto**: perfis, módulos, superfícies (app, site, painel), integrações, fluxos de dados e o que ficou fora. A régua precisa disso traduzido em fatores. A regra principal é simples: **1 módulo = 1 fluxo**.

| Na PRD | Vira na régua |
|---|---|
| Linha **Superfície** de cada módulo + 3.1 Ambientes de entrega | Formato: app mobile = app; site ou painel web = web. App + painel = dois formatos |
| Módulo **Disponibilização do Produto** | Lojas (F6) e deploy (F5). App de saúde, finanças ou menores = app sensível |
| **2.1 Autenticação e Perfis** | Níveis de acesso (F2). Perfil com módulo próprio ou aprovação de cadastro = grandes diferenças |
| Cada módulo da seção 2 (menos 2.1 e Disponibilização) | 1 fluxo comum. Com RN de cálculo, clínica, legal ou de dinheiro = fluxo com RN específica |
| **SID integrar com…** (sentido, dados, meio) | Integração: envia ou recebe = uni; os dois = bi. Serviço de mercado = com doc; sistema do cliente = sem doc (peso fixo, sem perguntar) |
| Fluxo de dados com origem em planilha, base externa ou importação | Dependência de dados (+ chamar o núcleo de Dados) |
| Multiempresa, offline, 3.3 Performance | Multitenancy, offline (local ou com sincronização), volume alto |
| **4. Exclusões Explícitas** | Não somam nada. Conferir que não foram contadas e não oferecer como corte |
| Pontos para a imersão (chat da PRD) | Não somam prazo: viram atividades da imersão (F1) |

### Fatores de complexidade da PRD

A PRD marca fatores que a régua não tem. Eles **encaixam nas linhas que já existem**, sem peso novo, porque ainda não há dado para calibrar pesos próprios.

| Fator na PRD | Linha da régua |
|---|---|
| Pagamento | Integração bidirecional documentada |
| IA (classificar, extrair, gerar, responder) | Integração unidirecional documentada (+ alerta se decide sem humano) |
| Notificação: push ou WhatsApp automático | Integração unidirecional (bidirecional se o sistema lê a resposta) |
| Notificação por e-mail · upload de arquivo | Template (0) |
| Concorrência · imutabilidade ou versionamento · rotina agendada | O módulo vira fluxo com RN específica (uma vez por módulo) |
| Tempo real por push · relatório configurável pelo usuário | Feature atípica (polling, tela fixa ou exportação = 0) |

### O que a PRD não responde

A PRD descreve o produto, não o projeto. Ficam de fora: disponibilidade do cliente para testar, stack ou infra exigida pelo cliente, app de referência (benchmark) e data de início (para contar as semanas off). A skill procura esses quatro na **transcrição do Fathom** das reuniões; o que não achar vira **lacuna** para o CN (seção 9).

### Integrações: peso fixo, sem perguntar ao CN

O CN não tem como avaliar a API de outro sistema, e não há técnico para validar antes da proposta. Por isso a skill não pergunta sobre documentação: usa o sentido (uni ou bi) e **de quem é o sistema**, que a PRD já traz.

| Sistema do outro lado | Linha da régua | O que mais sai na resposta |
|---|---|---|
| **Serviço de mercado** (pagamento, Pix, mapa, push, IA, WhatsApp Business, NF-e) | Com documentação | Nada |
| **Sistema do cliente** (ERP, legado, sob medida), arquivo ou dúvida | Sem documentação | Cláusula de contrato (acesso à API até a sprint n; sem acesso, vira planilha) + plano B em "O que cortar" |
| PRD diz explicitamente que o sistema não tem API (bidirecional) | Parado | Área de projetos avalia |

## 7. Régua de dimensionamento (F1 a F6)

Cada linha tem **mínimo / central / máximo** em semanas. Os pesos já consideram o time típico do NTec (uma dupla com cerca de 20 horas por semana somadas, codando com Claude Code, sprints de 2 semanas, template Next.js + Expo + MongoDB + Better Auth). Login com Google, e-mail e upload para S3 já vêm no template e não somam prazo.

### F1 — Imersão, refinamento, setup e acessos (teto 4)

| Fator | Mín | Central | Máx |
|---|---|---|---|
| Base (sempre) | 1,5 | 2 | 2,5 |
| Demanda pouco detalhada (sem requisitos nem protótipo) | +0,5 | +1 | +1 |
| Setor ou produto atípico (sem benchmark) | +0,5 | +0,5 | +1 |
| Stack fora do template NTec | +1 | +1,5 | +2 |

### F2 — Infra, níveis de acesso, cadastro e login (teto 4)

| Níveis de acesso / multitenancy | Mín | Central | Máx |
|---|---|---|---|
| Nenhum (sem login nem backend) | 0 | 0 | 0 |
| 1 nível | 0,5 | 0,5 | 1 |
| 2 a 6, poucas diferenças | 0,5 | 1 | 1,5 |
| 2 a 6, grandes diferenças (telas e regras próprias, aprovação de cadastro) | 1,5 | 2 | 2,5 |
| 6 ou mais | 2,5 | 3 | 4 |
| Multitenancy: dados separados, não isolados | +0,5 | +0,5 | +1 |
| Multitenancy: isolamento de dados | +1 | +1,5 | +2 |
| Multitenancy: instâncias com regras isoladas por cliente | Parado | — | — |

### F3 — Desenvolvimento

**Fluxo crítico** = jornada completa que, se quebrar, torna o produto inútil. Ex.: "o cidadão fotografa a espécie, o app pega a localização e o registro aparece no mapa". O núcleo é multiplicado pelo fator de formato: **Web x1,0 · WebApp/PWA x1,1 · App nativo x1,2 · +0,1 por formato extra em código separado**.

| Item | Mín | Central | Máx |
|---|---|---|---|
| Cada fluxo crítico comum (CRUD, listagem, mapa com filtros, agenda) | 1 | 1,25 | 1,5 |
| Cada fluxo com regra de negócio específica (fórmula, cálculo que não pode errar) | 2 | 3 | 4 |
| Cada feature atípica (sem benchmark) | 1 | 1,5 | 2 |
| Integração unidirecional com serviço de mercado | +0,5 | +0,5 | +1 |
| Integração bidirecional com serviço de mercado | +0,5 | +1 | +1,5 |
| Integração unidirecional com sistema do cliente | +1 | +1,5 | +2 |
| Integração bidirecional com sistema do cliente | +1,5 | +2,5 | +3,5 |
| Integração bidirecional que a PRD diz não ter API | Parado | — | — |
| Dependência de dados (planilhas, CSV, tabelas externas) — chamar núcleo de Dados | +1 | +1,5 | +2 |
| Offline com sincronização (offline só local = 0) | +1,5 | +2 | +3 |
| Volume de uso alto (milhares simultâneos) | +1 | +1,5 | +2 |

### Fator Claude Code (desde 17/10/2026)

Todos os projetos do NTec agora são codados com Claude Code. O ganho aparece no código que o time escreve, e não no que depende do cliente, de terceiros ou de revisão externa. Por isso o fator multiplica só duas partes:

| O que muda | Mín | Central | Máx |
|---|---|---|---|
| Núcleo do F3 (fluxos e features, já com o fator de formato) | x0,6 | x0,75 | x0,9 |
| F2 (níveis de acesso, multitenancy, login) | x0,7 | x0,85 | x1 |
| F1, extras do F3 (integrações, offline, dados, volume), F4, F5 e F6 | x1 | x1 | x1 |

> **De onde vem o x0,75:** meio-termo entre dois projetos. No Projeto B, motor de cálculo e tela completa saíram em ~1 semana de código, contra 5,1 semanas da régua antiga. Num app + painel de 8 fluxos com offline, a área de projetos espera ~12 sprints. Um x0,5 acertava o pequeno e errava o grande (20 semanas). O x0,75 acerta os dois: o ganho da ferramenta é parcialmente comido pelas ~20 h/semana da dupla e pela coordenação de projetos maiores. Ainda falta conferir com o realizado final. Projetos antigos rodam com `claude_code: false`.

### F4, F5 e F6 — Testes, deploy e lojas

| Fase / fator | Mín | Central | Máx |
|---|---|---|---|
| F4 Testes com cliente — base (teto 4) | 1 | 1,5 | 2 |
| F4 + regra de negócio crítica (saúde, dinheiro, legal) | +0,5 | +0,5 | +1 |
| F4 + cliente com pouca disponibilidade para validar | +0,5 | +0,5 | +1 |
| F5 Deploy web (infra NTec) | 0,5 | 0,5 | 1 |
| F5 Deploy de app sem web / app junto com web | 0,5 / +0 | 0,5 / +0,5 | 1 / +0,5 |
| F5 + infra ou regras de deploy do cliente | +1 | +1 | +2 |
| F6 Lojas — app comum | 2 | 2,5 | 4 |
| F6 Lojas — app sensível (saúde, finanças, infantil) | 2,5 | 3 | 6 |

_Semanas off (férias, provas, recessos) e a garantia gratuita de 30 dias ficam fora da régua: as semanas off são somadas depois, pelo calendário._

## 8. Faixa final e cortes

| Cenário | Conta | Para que serve |
|---|---|---|
| **Otimista (piso)** | Soma dos mínimos | Nunca vender abaixo disto |
| **Provável (recomendado)** | Soma dos centrais | O valor para a proposta |
| **Conservador (teto)** | Soma dos máximos | O que acontece se os riscos se confirmarem |

Semanas são sempre arredondadas para cima. A **recomendação de venda** é o provável fechado em sprints inteiras (número par de semanas), mais as semanas off.

### Cortes que mais economizam

| Corte | Economia típica (central) |
|---|---|
| Publicar como PWA em vez de app nas lojas | F6 inteira (2,5 a 3) + fator de formato |
| Tirar o segundo formato do MVP (só app ou só web) | ~10% do desenvolvimento + parte do deploy |
| Juntar perfis de usuário | 0,5 a 1 em F2 |
| Mover módulos não essenciais da PRD para uma fase 2 | 1,25 por fluxo comum; 3 por fluxo com regra específica |
| Trocar integração automática por importação manual no MVP (plano B de toda integração com sistema do cliente) | 0,5 a 2,5 |

_Na dúvida entre duas linhas da régua, a skill vai sempre para a mais pesada, com um comentário de duas linhas explicando o ajuste (máximo de 3 ajustes por projeto). O histórico do NTec é vender para menos._

## 9. O entregável: a Proposta Técnica

O dimensionamento final sai no **template "Proposta Técnica" do NTec** (Comercial → Validação de Projeto), o documento que o comercial manda para a validação técnica. O PDF "[Proposta Técnica] {projeto}" é gerado pelo `scripts/gerar_proposta.py`, que recalcula a faixa a partir dos fatores, para a proposta nunca divergir da régua.

| Parte da proposta | O que leva |
|---|---|
| Caixa de status (topo) | Status, prazo recomendado e a faixa otimista / provável / conservador |
| 1 a 3. Problema, visão geral, entidades | Tirados da Visão Geral e dos módulos da PRD |
| 4. Perfis · 6. Regras · 8. Segurança (obrigatórias) | PRD 2.1, as RNs e itens Hardcoded, PRD 3.4. O que a PRD não traz sai como "não previsto no PRD" |
| 5. Fluxo · 7. Arquitetura · 9. Módulos críticos | Jornada etapa por etapa (com as decisões futuras marcadas), componentes, integrações e automações |
| 10. Roadmap (obrigatória) | Tudo que está na conta é Prioritário; A confirmar e Futuro nunca entram no cronograma |
| 11. Pontos em aberto (obrigatória) | Lacunas do Fathom e da PRD e dependências externas. Nunca vazio |
| 12. Stack | Template NTec, sempre como premissa a validar na Sprint de Refino |
| 13. Cronograma sprint a sprint | As fases F1 a F6 (centrais) em sprints de 2 semanas, somando a recomendação; sprint que depende da seção 11 vem marcada |
| 14. Protótipo × regras (obrigatória) | Só com protótipo recebido; sem ele, a seção sai com aviso para o comercial |
| Checklist final | O script marca OK ou PENDENTE em cada item do template |
| Anexo — Memória do dimensionamento | Faixa, F1 a F6 com critério, alertas, pontos de atenção, lacunas, precedente, O que cortar, suposições, fronteira e imersão |

_O antigo bloco para colar na seção 7 do formulário Dimensionamento Tec saiu: o template de Proposta Técnica o substitui. No chat fica só o resumo curto._

## 10. Perguntas para o CN: Fathom primeiro, lacunas depois

Antes de perguntar qualquer coisa ao CN, a skill procura a resposta na **transcrição do Fathom** (ou no resumo) das reuniões com o cliente. Só conta o que foi **dito explicitamente**, e a resposta sai com a reunião e o trecho: *(origem: Fathom · 12/03 — "a Carla testa toda sexta")*. Dedução, silêncio ou fala vaga ("vamos ver") não contam.

| Fator (o que a PRD não responde) | O que a skill procura na transcrição |
|---|---|
| Disponibilidade do cliente | Quem testa e aprova, quantas horas, agenda ("sou plantonista", "valida toda sexta") |
| Stack e infra | Tecnologia exigida, "nossos servidores", "a nossa TI hospeda" |
| App de referência (benchmark) | "Tipo o…", "igual ao…", "vi um que…" |
| Data de início | Mês ou data de início, prazo de lançamento |

> **Não achou no Fathom = lacuna.** A skill dimensiona mesmo assim, com o valor mais pesado, e devolve ao CN as **Lacunas para o CN** (no chat, na seção 11 e no anexo da proposta): o fator, o que foi procurado, a pergunta pronta para o cliente e o valor provisório usado na conta. Lacuna que mexe na faixa (disponibilidade, stack ou benchmark) deixa o status em **Revisar** até o CN responder. Lacuna só na data de início não muda a faixa.

Sem PRD, a skill usa a lista inteira abaixo, também procurando cada resposta na transcrição antes de perguntar:

| Fator | Pergunta |
|---|---|
| Fluxos críticos | Quais são as 3 a 6 coisas principais que alguém faz no sistema, do começo ao fim? |
| Regra de negócio | Tem algum cálculo ou regra que, se errar, causa prejuízo, risco à saúde ou problema legal? Já existe escrito? |
| Formato | Vão usar pelo navegador, por um app da loja, ou os dois? Precisa estar na App Store / Play Store? |
| Níveis de acesso | Quantos tipos de pessoa usam? Cada tipo vê telas diferentes? Alguém aprova o cadastro de outro? |
| Integrações | Precisa conversar com outro sistema? Só puxa, só manda ou os dois? É um serviço conhecido ou um sistema próprio do cliente? |
| Offline | Precisa funcionar sem internet? Quando a internet volta, os dados precisam subir para algum lugar? |
| Multitenancy | Várias empresas vão usar? Cada uma tem regras próprias, ou só não pode ver os dados da outra? |
| Disponibilidade | Quem vai testar e aprovar as entregas? Tem umas 2 horas por semana para isso? |

## 11. Calibração com projetos reais

A régua foi rodada sobre os projetos do NTec com dados levantados no Notion (estado em 16/10/2026). Os projetos aparecem anonimizados (Projeto A a F). Faixa = otimista / provável / conservador, em semanas, **sem** o fator Claude Code (os projetos foram vendidos antes dele).

| Projeto | Formato | Início → fim previsto | Vendido | Faixa da régua | Situação | Leitura |
|---|---|---|---|---|---|---|
| Projeto A | PWA | 20/07/2026 → 19/10/2026 | 12 (+1 off) | 9 / **12** / 16 | Finalizando, no prazo | **[OK]** |
| Projeto D | App + web | 27/07/2026 → 23/11/2026 | 18 (+3 off) | 13 / **17→18** / 23 | Execução, 47,6%, sem atraso | **[OK]** |
| Projeto C | Web + app | 13/04/2026 → 10/07/2026 | 11 (+2 off) | 13 / **18** / 23 | Entregue com atraso (~14 sem) | **[Revisar]** |
| Projeto B | App nativo | 01/09/2026 → 23/11/2026 | 12 (+1 off) | 11 / **14** / 21 | Execução, 45,2% | **[Revisar]** |
| Projeto E | ? | 20/07/2026 → 15/01 ou 15/02/2027 | 34 | não calibrado | Execução, 37% | — |
| Projeto F | ? | 22/04/2026 → 06/01/2027 ou 25/10/2026 | 38 (+3 off) | não calibrado | Execução, 58,7% | — |

- **Projeto A e Projeto D:** a recomendação da régua bate com o vendido, e os dois estão no prazo.
- **Projeto C:** vendido abaixo do piso (11 contra 13) e atrasou. A régua ficou ~3 semanas acima do real, porque o time juntou setup e login em 2 semanas. É um viés conhecido, não corrigido com um único projeto.
- **Projeto B:** sem o fator, vendido entre o piso e o provável. É codado com Claude Code: motor e tela saíram em ~1 semana de código. **Com o fator, a régua dá 9 / 12 / 20 e a recomendação (12) bate com o vendido.** Resultado a confirmar em 23/11/2026.
- **Projetos E e F:** sem ficha técnica. Por isso, todo provável acima de **26 semanas** sai com alerta de "fora da faixa calibrada".

> **Todos esses projetos são anteriores à PRD.** Os fluxos foram contados a partir das tasks do Notion, e não pela regra "1 módulo = 1 fluxo". As regras de leitura da PRD ainda não foram conferidas contra um projeto real: o primeiro projeto com PRD que terminar vira o precedente para isso.

## 12. Exemplo: PetAgenda a partir da PRD

Caso fictício: app para tutores de pets (lojas) e painel web para uma rede de 3 clínicas. A PRD traz 4 perfis, os módulos 2.2 a 2.5, pagamento pelo Mercado Pago e lembrete de vacina por push, disparado na data da próxima dose.

| Fator | Valor | Origem |
|---|---|---|
| Formatos | app + web → x1,3 | Superfícies dos módulos e 2.6 |
| Níveis de acesso | 2 a 6, grandes diferenças | 2.1: recepção e veterinário com módulos próprios |
| Multitenancy | dados separados | Visão Geral: cada clínica vê só os próprios dados |
| Fluxos | 3 comuns + 1 com RN específica | 2.2, 2.4 e 2.5 comuns; 2.3 tem rotina agendada |
| Integrações | Mercado Pago (bi, doc); push (uni, doc) | 2.2 e 2.3 + peso fixo (serviços de mercado) |
| Demanda pouco detalhada | não | Tem PRD |

|  | Sem PRD (só a call) | Com PRD |
|---|---|---|
| Imersão (F1, central) | 3 semanas (demanda sem documento) | 2 semanas |
| Desenvolvimento | 4 fluxos comuns | 3 comuns + 1 com RN (lembrete agendado) |
| Faixa (otim. / prov. / cons.) | 14 / 19 / 25 | 15 / 20 / 28 |
| Recomendação de venda | 20 semanas | 20 semanas |
| Com o fator Claude Code | — | 12 / 18 / 26 (vender 18) |

_O número quase não mudou, mas agora cada fator aponta para uma seção do anexo de contrato. A PRD também revelou o lembrete por rotina agendada, que a call não deixava claro._

## 13. Linha do tempo de exemplo (Projeto A)

As fases no valor central da régua, encaixadas no calendário real do projeto: início em 20/07/2026, 12 semanas de trabalho + 1 semana off entre a S4 e a S5, fim previsto em 19/10/2026. Régua sem o fator Claude Code.

| Fase | Semanas (a partir de 20/07/2026) | Duração |
|---|---|---|
| F1 Imersão e setup | 0 → 2 | 2 sem |
| F2 Acesso e login | 2 → 3 | 1 sem |
| F3 Desenvolvimento | 3 → 8 | 5 sem |
| Semana off | 8 → 9 | 1 sem |
| F3 Desenvolvimento (cont.) | 9 → 10,5 | 1,5 sem |
| F4 Testes com cliente | 10,5 → 12 | 1,5 sem |
| F5 Deploy + arredondamento | 12 → 13 | 1 sem |

_Total: 13 semanas (12 de trabalho + 1 off), de 20/07/2026 a 19/10/2026._

_A linha de deploy inclui o arredondamento de 11,5 para 12 semanas._

## 14. Parar e sinalizar

A skill não decide sozinha nestes casos. Ela marca e devolve para a área de projetos:

- **[Parado]** Multitenancy com instâncias e regras isoladas por cliente ("beira o inviável").
- **[Parado]** Integração bidirecional que a PRD diz não ter API.
- **[Parado]** Feature atípica sem benchmark e sem documentação (pode exigir prova de conceito).
- **[Revisar]** Dependência de dados de bases soltas → chamar o núcleo de Dados.
- **[Revisar]** Provável acima de 26 semanas (fora da faixa calibrada) → considerar quebrar em fases.
- **[Revisar]** Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.
- **[Revisar]** Divergência entre o que o CN declarou e o que aparece na PRD, nos documentos ou na call.
- **[Revisar]** Lacuna dentro da PRD (módulo sem superfície, integração sem meio, "tempo real" sem mecanismo): a PRD precisa de revisão antes de virar anexo.
- **[Revisar]** Estimativa sem PRD: sempre preliminar.
- **[Revisar]** Teto de fase atingido.

## 15. Histórico, datas e pendências

| Data | O que aconteceu |
|---|---|
| 13/04/2026 | Início do Projeto C (primeiro projeto da base de calibração) |
| 10/07/2026 | Deploy do Projeto C, com atraso: 11 semanas vendidas, ~14 realizadas |
| 20/07/2026 | Início do Projeto A e do Projeto E |
| 01/09/2026 | Início do Projeto B |
| 16/10/2026 | Leitura da skill do NCiv, do formulário Dimensionamento Tec e do levantamento no Notion; criação e calibração da skill (v1); instalação em ~/.claude/skills |
| 16/10/2026 | v2: a PRD da skill documento-requisitos-ntec vira a entrada padrão; projetos anonimizados; publicação no GitHub |
| 17/10/2026 | v3: integrações com peso fixo, sem perguntar ao CN; buffer de risco e negociação de prazo removidos |
| 17/10/2026 | O que a PRD não responde vem da transcrição do Fathom; o que faltar volta ao CN como lacuna |
| 17/10/2026 | v4: o entregável passa a ser a Proposta Técnica no template do NTec (PDF gerado pela skill) |
| 17/10/2026 | Fator Claude Code na régua: núcleo do F3 x0,75 e F2 x0,85 (meio-termo entre o Projeto B e um projeto de ~12 sprints) |
| 19/10/2026 | Fim previsto do Projeto A — confirmar se a calibração continua valendo |
| 23/11/2026 | Fim previsto do Projeto B e do Projeto D — atualizar a calibração com o realizado |

### Pendências

- Fichas técnicas de Projetos E e F, para calibrar projetos grandes (o levantamento recebido veio cortado).
- Conteúdo da subpágina "Régua de Dimensionamento" do Notion, citada no formulário mas não incluída no PDF. Se tiver números, eles valem mais que os da skill.
- Conferir no hand-off do Projeto D os fatores marcados como palpite (perfis, fluxos, offline).
- Preencher as retrospectivas: hoje quase todas estão vazias, e sem elas não se sabe a causa dos atrasos.
- Avisar o autor da skill da PRD para trocar *validacao-tecnica-ntec* por *dimensionamento-ntec*.
- Conferir as regras de leitura da PRD ("1 módulo = 1 fluxo" e "rotina agendada → RN específica") no primeiro projeto com PRD que terminar.
- Conferir o fator Claude Code com o realizado do Projeto B (23/11/2026) e do primeiro projeto com login que terminar (o F2 com fator ainda não foi medido).

> **Manutenção:** pesos mudam no `scripts/calcular_faixa.py` **e** na `regua-dimensionamento.md`, com uma linha no Registro das fontes. Quando um projeto termina, ele entra em `exemplos/` com vendido × realizado, anonimizado; o nome real fica só na pasta `privado/`, fora do GitHub.
