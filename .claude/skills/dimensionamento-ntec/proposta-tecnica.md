# Proposta Técnica — como preencher o template do NTec

O entregável da skill é a **Proposta Técnica** no template oficial do NTec ("Comercial → Validação de Projeto"). É o documento que o comercial manda para a validação técnica. A skill monta um JSON e roda `scripts/gerar_proposta.py`, que gera o PDF no visual do template: faixa azul-marinho no topo, selo laranja OBRIGATÓRIO, as 14 seções, o checklist final e um **Anexo — Memória do dimensionamento**.

Modelo completo do JSON: `exemplos/ficticio-petagenda-proposta.md` (bloco ```json). Template original, como o NTec o escreveu: `template-proposta-tecnica.md` (pede PRD; a skill usa as calls no lugar).

## Regras do preenchimento

- **Fonte de tudo são as calls** (transcrições da AT Diag e da AT Aprof), mais o que o CN responder às lacunas, como no resto da skill. A proposta não acrescenta jornada, perfil, integração, log ou permissão que o cliente não confirmou nas calls (`leitura-transcricoes.md`, Passo 3). Se o template pede algo que ninguém discutiu, escrever "não discutido nas calls". Se isso muda o prazo, vira ponto em aberto (seção 11).
- **As semanas não são digitadas.** O script recalcula a faixa a partir de `dimensionamento.entrada`, que é o mesmo JSON da régua (`calcular_faixa.py`). Caixa de status, cronograma e anexo saem do mesmo cálculo.
- **Lacunas do Fathom na caixa de status.** Com `lacunas_fathom` na entrada, a caixa de status mostra a venda com "+" ("14 semanas = 12 + 2 que dependem do Fathom") (`leitura-transcricoes.md`, Passo 6). O cronograma segue a venda com as lacunas.
- **Nada interno no corpo** (seções 1 a 14): sem `(origem: ...)` nem nome de arquivo da régua. As origens ficam no anexo (critérios, inventário, suposições) e no chat.
- **Nada que o CN falou de prazo ou preço no corpo.** Isso vai para `dimensionamento.observacoes`, comparado com a faixa.
- **Texto curto e sem adjetivo de venda.** Todo termo técnico é explicado na primeira vez que aparece.

## Cabeçalho (`cabecalho`)

| Campo | De onde vem |
|---|---|
| `cliente_projeto` | Nome do produto como o cliente chama nas calls + subtítulo ("PetAgenda · Agenda e carteirinha de vacina para rede de clínicas veterinárias") |
| `responsavel_comercial`, `data_envio` | Do CN. Sem resposta: deixar `""`, e o PDF sai com `______` para preencher à mão |
| `transcricoes` | Lista com uma linha por call: `{"call": "AT Diag", "data": "14/07", "link": "..."}` e `{"call": "AT Aprof", ...}`. O link é o da gravação no Fathom. O checklist só fica OK com as duas |
| `prototipo_link` | Do CN. **Sem token de acesso** (o script tira `?magic_link=` e parecidos). Sem link, fica `""` e o checklist sai PENDENTE |

`status`: `pronto`, `atencao`, `preliminar` (falta uma das duas calls, ou só há resumo) ou `parado`, com os mesmos critérios de antes.

## Seção por seção

| Seção | Campo no JSON | Como preencher a partir das calls |
|---|---|---|
| 1. Problema | `problema.dor`, `problema.problemas` (2 a 4) | O que o cliente contou na AT Diag (dor central e objetivo). Cada problema é uma dor concreta que uma jornada resolve |
| 2. Visão geral | `visao_geral.tipo`, `publico`, `proposta_valor`, `principios` | Formato e público confirmados nas calls; proposta de valor em 1 frase; princípios = o que o cliente pediu como regra do produto (funcionar sem internet, ser rápido de usar no plantão) |
| 3. Entidades | `entidades.centrais`, `entidades.apoio` | Substantivos que as jornadas criam ou consultam. Centrais = o que a jornada principal produz; apoio = cadastros, tabelas e registros auxiliares |
| 4. Perfis **(obrig.)** | `perfis.tabela` (`[perfil, o que faz, observações]`), `perfis.matriz_permissoes` | Os tipos de pessoa citados nas calls. Sem login confirmado, dizer isso e apontar o ponto em aberto. Matriz: dizer se existe ou se está em aberto |
| 5. Fluxo | `fluxo` (lista de etapas `etapa, quem, dados, validacoes, pendente`) | A jornada principal como o cliente descreveu e validou no protótipo, na ordem de uso. `pendente` marca a etapa que depende de decisão futura do cliente e precisa ter o mesmo assunto na seção 11 |
| 6. Regras **(obrig.)** | `regras` (`[regra, o que garante]`) | Toda regra dita nas calls (cálculo, faixa, limite, aviso) e a fonte dela (ex.: a planilha da cliente). Regra crítica (dose, limite, duplicidade, conflito) não pode faltar. Regra que depende de documento ainda não recebido: dizer isso |
| 7. Arquitetura | `arquitetura` (`[rótulo, texto]`) | Frontend por formato, backend (ou "sem backend", quando tudo roda no aparelho), banco, autenticação, integrações externas citadas. Sem stack aqui: stack é a seção 12 |
| 8. Segurança **(obrig.)** | `seguranca` (`[rótulo, texto]`) | Sempre cobrir: tipos de dado (pessoal? sensível? LGPD?), login e controle por perfil, histórico e logs, dados públicos (links sem login, formulários públicos). O que ninguém discutiu: "não discutido nas calls" |
| 9. Módulos críticos | `modulos_criticos` (`nome, detalhe, mvp, futuro`) | Pagamentos, cada integração externa, o cálculo com RN crítica e as automações (offline, rotina agendada, geração de documentos, importação). O que entra no MVP × o que o cliente descartou ou depende de terceiro. Sem nenhum: lista vazia |
| 10. Roadmap **(obrig.)** | `roadmap` (`[fase, entrega, natureza]`) | Cada jornada do inventário = uma entrega *Prioritário*. Item na conta que depende da seção 11 continua *Prioritário*, com "(depende do ponto em aberto N)". *A confirmar* = algo discutido em que o cliente hesitou e que não está na conta. *Futuro* = o que o cliente deixou para depois ou descartou. **Nada A confirmar ou Futuro pode aparecer no cronograma** (o script confere pelo texto da entrega) |
| 11. Pontos em aberto **(obrig.)** | `pontos_abertos` (lista de textos) | Nesta ordem: lacunas que mudam a faixa, documentos que o cliente ainda precisa mandar (planilha, tabela, norma), divergências entre as calls, dependências externas (API, fornecedor, conta de loja), e as lacunas que não mudam a faixa (data de início). Cada um diz o valor usado na conta, quando houver. **Nunca vazio** |
| 12. Stack | `stack.itens`, `stack.nao_validado` | O template NTec (Expo, Next.js, MongoDB + Prisma, Better Auth, S3, Vercel, Vitest e Playwright), só as peças que o projeto usa. O primeiro item de `nao_validado` é sempre "Toda a stack é premissa a validar na Sprint de Refino e Prototipação". Exigência do cliente (`stack_fora_template`) entra aqui também como não validada |
| 13. Cronograma | `cronograma.sprints` (`[sprint, entregas, depende_de]`), `cronograma.duracao_obs` | Ver abaixo |
| 14. Protótipo **(obrig.)** | `prototipo.recebido`, `prototipo.tabela` (`[tela, regra, adaptação, justificativa, vale p/ MVP]`), `prototipo.declaracao` | Só com protótipo recebido e validado pelo cliente. Sem adaptação: `declaracao` = "O protótipo segue integralmente as regras combinadas nas calls". Sem protótipo: `recebido: false`, tabela vazia; o PDF avisa o comercial |

`dependencia_externa_sem_confirmacao`: `true` se alguma integração ou fornecedor está sendo tratado como certo sem confirmação. Com a regra de peso fixo e a cláusula de contrato, o normal é `false`.

## Cronograma sprint a sprint (seção 13)

Usar os valores **centrais** de cada fase do `calcular_faixa.py` e encaixar em sprints de 2 semanas até fechar a recomendação de venda (provável arredondado para sprints inteiras).

1. **F1** (imersão e setup): Sprint 1, ou 1 e 2 se F1 passar de 2 semanas. Inclui validar o protótipo e, se houver app nas lojas, pedir as contas Apple e Google.
2. **F2** (acesso e login): a sprint seguinte. Se sobrar meia sprint, começar os cadastros.
3. **F3** (desenvolvimento): as jornadas do inventário na ordem de uso, de 1 a 2 por sprint conforme o peso. Jornada com RN específica ou offline com sincronização ocupa a sprint inteira ou mais. Integração com sistema do cliente vai depois da sprint em que vence o prazo da cláusula de acesso à API.
4. **F4** (testes com o cliente), **F5** (deploy) e **F6** (lojas) no fim, nessa ordem. Em F6, contar o tempo de aprovação das lojas.
5. Toda sprint cuja entrega depende de um ponto da seção 11 leva `depende_de` = "ponto N".
6. O número de sprints precisa bater com a recomendação. Se a soma dos centrais for quebrada, a folga fica na última sprint ("correções finais e entrega").

## Anexo — Memória do dimensionamento (`dimensionamento`)

É o que a área de projetos revisa. O PDF mostra a faixa e o detalhamento F1 a F6 calculados pelo script, os alertas da régua e os campos abaixo.

| Campo | Conteúdo (o mesmo de antes da proposta) |
|---|---|
| `entrada` | O JSON da régua, igual ao de `calcular_faixa.py` |
| `criterios` | `{"F1": "...", ..., "F6": "..."}`: o critério de cada fase, citando a call e o minuto (ex.: "F3: 1 jornada com RN específica, calcular o soro (AT Diag 7:46); app nativo (AT Diag 15:04)") |
| `inventario` | `[jornada, quem faz, onde, regra/cálculo/integração, citação]`: o inventário de `leitura-transcricoes.md`, Passo 4 |
| `atencao` | Pontos de atenção, do mais grave para o menos grave, cada um com o que fazer. Toda integração com sistema do cliente traz aqui a cláusula de contrato pronta de `regua-dimensionamento.md` |
| `lacunas` | `[fator, procurado e não achado, pergunta para o cliente, valor provisório]` |
| `precedente` | O projeto mais parecido em `exemplos/`, o prazo dele e por que é comparável (ou "sem precedente comparável"). Mais de 30% de distância: explicar |
| `cortes` | 2 a 4 cortes `[corte, economia]`, recalculados com o script. Nunca algo que o cliente já descartou. Com integração de sistema do cliente, um corte é sempre o plano B (planilha) |
| `suposicoes`, `fronteira`, `imersao` | Suposições (inclui o valor provisório de cada lacuna e as leituras de erro de transcrição), os comentários de duas linhas de `regra-fronteira-e-faixa.md` e os pontos para a imersão (ajustes visuais, unidades, textos explicativos que o cliente pediu) |
| `observacoes` | Prazo e preço que o CN já falou ao cliente na call, comparados com a faixa ("CN falou 2 a 3 meses na AT Aprof; a skill dá 10 a 15 semanas"). Divergência entre as calls |

## Onde foi parar cada parte da resposta antiga

| Antes (resposta no chat) | Agora |
|---|---|
| Status, prazo em uma frase, faixa | Caixa de status do PDF + chat |
| Resumo do projeto | Seções 1 e 2 |
| Pontos de atenção | Anexo `atencao` (os que dependem de decisão externa também na seção 11) |
| Lacunas para o CN | Seção 11 + anexo `lacunas` + chat |
| Detalhamento por fase | Anexo (calculado pelo script) + seção 13 (em sprints) |
| Precedente, O que cortar, Observações | Anexo |
| Bloco para colar no Dimensionamento Tec | Saiu: o template de Proposta Técnica substitui o formulário |

## Checklist final (o script confere)

| Item do template | Como o script decide |
|---|---|
| Transcrições da AT Diag e da AT Aprof e protótipo anexados | `transcricoes` com uma AT Diag e uma AT Aprof, e `prototipo_link` preenchido |
| Campos OBRIGATÓRIO preenchidos | Seções 4, 6, 8, 10, 11 e 14 não vazias |
| Protótipo segue as regras ou adaptações justificadas | `prototipo.recebido` e tabela ou declaração preenchidas |
| Roadmap e cronograma não se contradizem | Nenhuma entrega *A confirmar* ou *Futuro* aparece no texto do cronograma |
| Pontos em aberto listados | Seção 11 não vazia |
| Nenhuma dependência externa tratada como certa | `dependencia_externa_sem_confirmacao` é `false` |

Item PENDENTE não impede o PDF. Ele sai marcado e vai para o chat com o que o CN precisa fazer.
