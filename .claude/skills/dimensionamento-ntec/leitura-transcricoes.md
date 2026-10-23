# Leitura das transcrições — AT Diagnóstico e AT Aprofundamento

A entrada padrão desta skill são as **transcrições na íntegra do Fathom** das duas calls com o cliente:

- **AT Diagnóstico (AT Diag):** a primeira call. O cliente conta a dor, o contexto e a ideia do produto.
- **AT Aprofundamento (AT Aprof):** a segunda call. Normalmente o CN mostra um protótipo, o cliente valida o fluxo, e se fecham escopo, perfis, lojas e às vezes prazo e preço.

A skill dimensiona **pelo que foi discutido nas duas calls**. Não há documento de requisitos (PRD) no meio: esta skill monta, a partir das falas, o inventário que antes vinha da PRD.

Este arquivo diz onde, nas calls, está cada campo do JSON do `scripts/calcular_faixa.py`. O critério completo de cada fator (pergunta, o que fazer sem resposta) está no arquivo da fase em `fatores/`; se este arquivo e `fatores/` divergirem, vale `fatores/`. **Todo campo é obrigatório:** o script não tem valor padrão e para se faltar algum.

---

## Passo 1 — O que o CN manda

| Peça | Obrigatória? | Como usar |
|---|---|---|
| **Transcrição da AT Diag** (Fathom, modo transcrição, na íntegra) | Sim | Dor, público, jornadas que o cliente descreve, formato ("aplicativo", "site"), offline, quem vai usar |
| **Transcrição da AT Aprof** (Fathom, modo transcrição, na íntegra) | Sim | Validação do protótipo, funcionalidades confirmadas ou descartadas, login, lojas, prazo e condições |
| Link do protótipo (Lovable, Figma…) | Não | Seção 14 da proposta e conferência das telas que o cliente aprovou na AT Aprof |
| Documentos que o cliente mandou (planilha, tabela, norma, protocolo) | Não | É o documento da **RN específica**. Sem ele, a regra conta do mesmo jeito, e o pedido do documento vai para *Pontos em aberto* |
| Calls a mais (segunda AT Aprof, call de proposta) | Não | Valem como as outras. Se divergirem, vale a mais recente |

**Só o resumo do Fathom** (Summary, Action Items, Highlights): pedir uma vez a transcrição na íntegra. O resumo é texto gerado pelo Fathom, não fala do cliente, e não serve como citação. Se o CN não tiver a íntegra, dimensionar pelo resumo e marcar ⚠️ *Estimativa preliminar*.

**Só uma das duas calls:** dimensionar mesmo assim, marcar ⚠️ *Estimativa preliminar* e dizer qual call falta. Com só a AT Diag, `demanda_pouco_detalhada` é `true` (`fatores/F1-imersao-setup.md`, 1.2).

**Sem nenhuma transcrição** (só formulário, ficha, briefing ou texto do CN): caminho de `insumos-e-perguntas.md`, sempre ⚠️ *Estimativa preliminar*.

## Passo 2 — Preparar a transcrição antes de ler

O Fathom entrega a transcrição neste formato:

```
{Cliente} & Poli Júnior - {data}
VIEW RECORDING - {n} mins

0:00 - {Nome} ({Empresa})
  {fala}
  ACTION ITEM: {tarefa} - WATCH: {link}
```

1. **Qual call é qual.** Pela data do cabeçalho: a mais antiga é a AT Diag. Se o CN disser outra coisa, vale o CN.
2. **Quem é quem.** Do NTec é quem se apresenta como da Poli Júnior. O Fathom nem sempre põe "(Poli Júnior)" no nome: no exemplo do Projeto H, uma CN aparece com o sufixo e a outra sem. Cliente é quem sobra. Anotar no começo da memória quem é cliente e quem é do NTec.
3. **Descartar o que não é conversa com o cliente:** a conversa interna antes de o cliente entrar e depois que ele sai, a apresentação institucional da Poli Júnior e o papo social. Nada disso é escopo.
4. **`ACTION ITEM` não é fala.** É texto gerado pelo Fathom. Serve só como pista de pendência (ex.: "mandar a planilha"); a citação tem de vir da fala.
5. **Erros de transcrição.** O Fathom erra termos e nomes (no Projeto H, "EES" no lugar de Play Store). Interpretar só quando o contexto deixa **uma leitura só** ("tanto para a EES quanto para a App Store" = Play Store e App Store) e registrar a leitura em *Suposições*. Se couber mais de uma leitura e ela mexe no prazo, é lacuna.

## Passo 3 — O que conta como escopo

**Só entra na conta o que o cliente confirmou.** A transcrição tem ideias soltas, propostas do CN e hesitações; a skill separa o que é escopo do que não é.

| O que aparece na call | Entra na conta? | Para onde vai |
|---|---|---|
| O cliente descreve uma funcionalidade como parte do produto ("a pessoa jogaria o peso… ele me daria o volume") | Sim | Inventário (Passo 4) |
| O CN propõe e o cliente confirma **aquela** proposta ("Sim, perfeito", "é isso mesmo") | Sim | Inventário |
| Telas do protótipo que o cliente aprovou na AT Aprof | Sim | Inventário e seção 14 |
| O CN propõe e o cliente não responde, muda de assunto ou responde a outra coisa | Não | Lacuna, se mexe no prazo |
| O cliente hesita ("não sei se precisa", "talvez", "seria legal ter") | Não | Lacuna, se mexe no prazo (Passo 6); senão roadmap *A confirmar* |
| O cliente descarta ("acho que não precisaria", "não precisa") | Não | Exclusão. Não pode virar corte em *O que cortar* |
| Ajuste visual (cor, nomes, ordem dos campos, textos explicativos) | Não soma | *Pontos para a imersão* |
| "Os ajustes a gente faz no decorrer do projeto" | Não soma | Ajuste dentro do escopo, não funcionalidade nova |
| "Depois a gente vê", "numa segunda versão" | Não | Roadmap *Futuro* |
| As calls dizem coisas diferentes | Vale a mais recente | A divergência vai para *Pontos de atenção* |
| **Prazo ou preço que o CN já falou para o cliente** ("dois a três meses", "uns 30 mil") | **Nunca** | *Observações*: comparar com a faixa da skill. Se o prazo falado está abaixo do otimista, vira o ponto de atenção mais grave, porque o cliente já tem essa expectativa |
| Data ou prazo que o **cliente** exige ("precisa estar pronto até março") | Sim, no F0 | `f0.prazo_exigido_semanas` |

**A skill não acrescenta escopo.** Se achar que falta algo para o produto funcionar e ninguém falou disso nas calls, vai para *Pontos de atenção* ("as calls não cobrem X"), não para a conta.

## Passo 4 — Montar o inventário a partir das calls

Sem PRD, a skill monta o inventário que a área de projetos revisa. Uma linha por **jornada** (glossário, *Fluxo*):

| Jornada | Quem faz | Onde (app, web, painel) | Regra, cálculo ou documento | Integrações | Dados de fora | Citação |
|---|---|---|---|---|---|---|
| Calcular o soro | Médico | App | Fórmula da planilha da cliente, por faixa de peso e tipo de soro; aviso de concentração máxima | — | — | AT Diag · 7:46 — "a pessoa jogaria o peso do paciente…" |

Como contar:
1. **Listar o que alguém faz do começo ao fim** no sistema, como o cliente descreveu ("o médico entra, coloca o peso e o tipo de soro, e sai com o volume e a velocidade de infusão").
2. **Fora da contagem:** login e perfis (F2), publicação nas lojas (F5 e F6) e offline (extra do F3).
3. **Juntar variações da mesma jornada.** Três tipos de soro na mesma tela de cálculo são uma jornada, não três. Escolher uma unidade (cálcio em mg ou em mEq) é um campo da jornada, não uma jornada.
4. **Jornada com muitas ações diferentes** (cadastrar, listar, editar, aprovar, exportar… mais de 8) conta 2 fluxos.
5. **Registrar cada junção** em *Suposições*.

O inventário vai para o anexo da proposta (campo `criterios`, F3) e para a resposta no chat, para a área de projetos conferir.

## Passo 5 — Onde está cada fator

**Primeiro o F0** (`fatores/F0-viabilidade.md`). Preencher o bloco `"f0"` antes do resto:

| Campo do bloco `"f0"` | O que procurar nas calls | Como traduzir | Sem resposta |
|---|---|---|---|
| `stack_exigida_fora_da_lista` | "Tem que ser em…", "a nossa TI só aceita…" | `true` só se o cliente **exige** tecnologia fora da lista do F0. "Vocês decidem" → `false`. 🚫 rejeita | `false` + stack do template em *Suposições* |
| `sla_ou_sustentacao` | Suporte 24/7, SLA, "vocês mantêm depois" | `true` se for além da garantia de 30 dias. 🚫 rejeita | `false` + *Suposições* |
| `infra_cliente_sem_acesso` | "Fica nos nossos servidores" sem acesso do NTec | Não rejeita: o deploy fica com o cliente, o F5 zera e a proposta diz que a garantia de 30 dias não se aplica (F0, item 0.3) | `false` |
| `multa_por_atraso` | Multa, penalidade | 🚩 | `false` + *Suposições* |
| `feature_sem_referencia_nem_doc` | Feature que ninguém sabe se existe em algum lugar e não tem documentação técnica pública | 🚩 | `false`, se toda feature tem referência ou é comum |
| `hardware` | Leitor, impressora, sensor, Bluetooth com aparelho próprio | 🚩 | `false` |
| `prazo_exigido_semanas` | Data limite **exigida pelo cliente** | Comparado com o otimista **depois da conta**: abaixo dele = 🚩, com análise de entrega parcial (F0, item 0.3). Converter para semanas a partir do início previsto. "Seria para esse ano, mas não tem pressa" **não é** exigência → `null` + *Suposições* | `null` |

**Depois F1 a F6:**

| Campo do JSON | O que procurar nas calls | Como traduzir | Sem resposta |
|---|---|---|---|
| `formatos` | "Aplicativo", "baixar", "App Store", "Play Store" → app. "Site", "página na internet", "no computador" → web. "Ícone na tela, sem loja" → PWA | O cliente diz "aplicativo" para qualquer coisa: só é app nativo com loja confirmada ou recurso nativo (glossário). Cada código entra uma vez | App + `"lojas"` como lacuna |
| `fluxos_por_formato` | Onde cada jornada acontece | **Só com mais de um formato.** Mesma regra de `fatores/F3-desenvolvimento.md`, 3.2 | `compartilhado` |
| `lojas` | "Vai para a App Store e a Play Store", "disponibilizar para outros médicos", "vender" | Loja aberta ao público → teste de `fatores/F6-lojas.md` (saúde, finanças, crianças ou pagamento no app → `"sensivel"`). Só uso interno → `"nao"` | Publica + `"lojas"` em `lacunas_fathom` |
| `niveis_acesso` | "Precisa de login?", "cada um vê os seus", tipos de pessoa que entram no sistema | Contar os tipos de pessoa que fazem login (admin conta). Teste de grandes diferenças de `fatores/F2-acesso-multitenancy.md`. "Não precisa de cadastro" confirmado → `"nenhum"` | Hesitação ("não sei se seria interessante um login") → `"1"` + `niveis_acesso` em `lacunas_fathom` com o valor leve `"nenhum"` |
| `multitenancy` | "Várias clínicas", "cada unidade", "por filial" | Teste em ordem de `fatores/F2-acesso-multitenancy.md` | `"isolado"` + lacuna, se há mais de uma empresa; `"nao"` se só o cliente usa ou se cada usuário é independente |
| `fluxos_comuns` | Inventário (Passo 4) | Jornadas sem RN específica | — (sem jornadas, não dimensionar) |
| `fluxos_rn_especifica` | "Tem um cálculo", "uma fórmula", "a minha planilha", "uma tabela", "segue a norma", "o primeiro que aceitar leva" | A jornada sai de `fluxos_comuns` e entra aqui quando depende de fórmula, tabela, norma ou protocolo que o cliente tem de entregar, ou tem concorrência ou imutabilidade. Conta **uma vez por jornada** | Fluxo comum, se ninguém falou de regra |
| `features_atipicas` | Tabela do Passo 7 | Só as linhas que viram feature atípica | `0` |
| `integracoes` | Outros sistemas citados: pagamento, ERP, planilha automática, mapa, WhatsApp, IA | **Peso fixo, sem perguntar ao CN** (`fatores/F3-integracoes.md`). Tabela do Passo 7 | Funcionalidade que **pode** precisar de integração e o cliente não decidiu (ex.: "é para venda", sem dizer como cobra) → a integração mais provável na conta + `integracoes` em `lacunas_fathom` com o valor leve (Passo 6) |
| `dependencia_dados` | "Os dados estão numa planilha", "base do governo", "sistema antigo" | `true` se registros que já existem fora precisam ser migrados, limpos ou cruzados. **A planilha que contém a fórmula ou a tabela da regra não é dependência de dados:** é o documento da RN específica | `false` |
| `offline` | "Sem internet", "no interior não pega sinal" | Só calcula ou consulta sem internet, nada sobe depois → `"local"`. Grava sem internet e sobe depois → `"sync"` | `"nao"` se ninguém falou de internet |
| `volume_alto` | "Milhares ao mesmo tempo", evento, lançamento com data | `true` só com o número ou o pico dito | `false` |
| `rn_critica` (F4) | O sistema calcula dinheiro, dose, dado clínico, prazo legal ou fiscal | `true` se **o código do NTec calcula** e o erro causa dano (`fatores/F4-testes.md`) | `true` se há cálculo de saúde, dinheiro ou legal e não se sabe quem calcula |
| `demanda_pouco_detalhada` | As duas calls inteiras | `true` se **qualquer** item de `fatores/F1-imersao-setup.md`, 1.2, for sim (falta a AT Aprof; não dá para listar as jornadas do começo ao fim; formato não decidido; regra que o cliente ainda não sabe descrever) | — |
| `stack_fora_template` | Tecnologia da lista do F0 exigida e diferente do template (ex.: Supabase) | `true` só com exigência dita | `false`, ou `true` + lacuna se houve indício sem resposta |
| `deploy_infra_cliente` | "Nossos servidores", "a nossa TI publica" | `true` se dito | `false` (cliente pessoa física ou sem TI própria); lacuna se é empresa com TI e ninguém falou |
| `atipico` | "Igual ao…", "tipo o…", "as que eu já vi" (referência ao produto inteiro) | Referência citada → `false`. "Não existe nada parecido" → `true` | `true` + lacuna |

## Passo 6 — Lacunas: o que as calls não responderam

O que as duas calls não respondem vira **lacuna**:

1. **Dimensionar com o valor mais pesado plausível** (coluna *Sem resposta* do Passo 5).
2. **Mostrar quanto da venda depende das lacunas.** No JSON da régua, `"lacunas_fathom"` lista os fatores em lacuna, e `"fathom": true` diz que havia transcrição (o Fathom existe, mas não fala do assunto). Duas formas:
   - **Lista**, para os fatores com valor leve fixo: `["atipico", "lojas"]` (`atipico`, `stack_fora_template`, `deploy_infra_cliente`, `lojas`).
   - **Objeto**, quando o valor leve depende do projeto (`niveis_acesso`, `integracoes`): `{"niveis_acesso": "nenhum", "integracoes": ["template"], "lojas": "nao"}`. Para os quatro da lista, `null` usa o valor leve padrão.

   O script refaz a conta com o valor leve e mostra a diferença em sprints inteiras: *"Recomendado vender 12 semanas (6 sprints) = 10 + 2 que dependem de confirmar com o cliente (login e perfis, integrações), mais as semanas off."*
3. **Listar em *Lacunas para o CN*** (chat, seção 11 e anexo da proposta): o fator, o que foi procurado nas calls e não achado, a pergunta pronta e o valor provisório.
4. **Registrar o valor provisório em *Suposições***, com `(origem: lacuna — não está nas calls)`.
5. **Status:** lacuna que mexe na faixa → ⚠️ *Precisa de revisão* até o CN responder. Lacuna só na data de início não rebaixa o status.

**No máximo 5 perguntas por rodada**, as que mais mexem no prazo primeiro. O CN repassa ao cliente (WhatsApp serve) e manda a resposta; a skill troca o valor, tira o fator de `lacunas_fathom`, roda o script de novo e muda a origem para `(origem: CN)`.

**Perguntas prontas das lacunas mais comuns:**

| Fator | Pergunta para o cliente |
|---|---|
| Login (`niveis_acesso`) | "A pessoa precisa criar conta e entrar com login, ou abre o app e já usa?" |
| Pagamento (`integracoes`) | "Como você quer cobrar: o app é pago na loja, tem assinatura dentro do app, ou é gratuito?" |
| Lojas (`lojas`) | "O app vai para a App Store e a Play Store, ou só para uso interno?" |
| Referência (`atipico`) | "Existe algum app ou site parecido que a gente possa usar de referência?" |
| Stack e infra (`stack_fora_template`, `deploy_infra_cliente`) | "Vocês exigem alguma tecnologia, ou que o sistema fique nos servidores de vocês?" |
| Documento da regra | "Você consegue mandar a planilha (ou a tabela, a norma) com as fórmulas que o sistema vai seguir?" |
| Data de início | "Qual é a data prevista de início? (para contar férias, provas e recesso)" |

**Não perguntar sobre a documentação das integrações.** O CN não tem como responder: a skill aplica o peso fixo e registra a classificação em *Suposições*.

## Passo 7 — Funcionalidades que a régua não tem como linha

Algumas funcionalidades citadas nas calls não têm linha própria na régua. Elas **encaixam nas linhas que já existem**, sem peso novo:

| O cliente fala de… | Linha da régua | Observação |
|---|---|---|
| Pagamento (gateway, Pix, cartão, assinatura no app) | Integração `bi_doc` | Gateway e compra dentro do app são serviços de mercado. `bi_sem_doc` só se o pagamento passar pelo sistema próprio do cliente. App pago na loja (preço na Apple e no Google, sem cobrança no app) = 0 |
| IA (classificar, extrair, gerar, responder) | Integração `uni_doc` | Se a IA decide sem humano no fim, ⚠️ em *Pontos de atenção* |
| Notificação push no app | Integração `uni_doc` | |
| WhatsApp automático | Integração `uni_doc`, ou `bi_doc` se o sistema lê a resposta | Link para abrir o WhatsApp = 0 |
| E-mail | `template` | |
| Aviso dentro do sistema (ex.: "concentração acima do máximo") | 0 (faz parte da jornada) | |
| Tempo real por aviso do servidor (push) | +1 em `features_atipicas` | Atualização periódica = 0 |
| Relatório configurável pelo usuário (construtor) | +1 em `features_atipicas` | Tela fixa ou exportação PDF/Excel = 0 |
| Concorrência ("o primeiro que aceitar leva") | A jornada vira `fluxos_rn_especifica` | |
| Imutabilidade ou versionamento (prontuário que não se edita) | A jornada vira `fluxos_rn_especifica` | |
| Rotina agendada (todo dia às 8h) | A jornada vira `fluxos_rn_especifica` | Gatilho por ação do usuário = 0 |
| Upload e armazenamento de arquivos | `template` (S3) | |
| Migração ou carga de base existente | `dependencia_dados: true` | Upload simples do usuário dentro do produto = 0 |
| Relatório ou documento em template fixo | 0 (faz parte da jornada) | Não vira RN específica |
| Histórico ("ver os cálculos que eu já fiz") | Jornada a mais (fluxo comum) + login | Só se o cliente confirmou. "Não precisa de histórico" → exclusão |
| Várias empresas, unidades, clínicas | `multitenancy` (Passo 5) | |
| Sem internet | `offline` (Passo 5) | |

**Não contar duas vezes.** A mesma jornada vira RN específica uma vez só. Uma funcionalidade que já virou integração não vira também feature atípica.

## Passo 8 — Origem de cada fator

A origem cita a call, o minuto e um trecho curto da fala:

```
Formato: app nativo (origem: AT Diag · 14/07 15:04 — "tanto para a [Play Store] quanto para a App Store" / "Perfeito")
Fluxos com RN específica: 1, calcular o soro (origem: AT Diag · 14/07 7:46 — "a pessoa jogaria o peso do paciente")
Offline: local (origem: AT Diag · 14/07 3:02 — "tem interior que nem sinal de internet tem")
Login: lacuna (origem: lacuna — AT Diag · 14/07 13:32, "não sei se seria interessante um login")
Prazo falado ao cliente: 2 a 3 meses (origem: AT Aprof · 21/07 6:36, fala da CN — não entra na conta)
```

## Passo 9 — Cuidados com o conteúdo das calls

- **Não copiar dado pessoal** do cliente, de paciente ou de terceiro citado na call para os exemplos do repositório. Projeto real entra nos `exemplos/` só anonimizado (Projeto A, B, C…).
- **Links de protótipo com token de acesso** (ex.: `?magic_link=…` no Lovable) dão acesso a quem tiver o link. Na proposta, usar o link sem o token, ou só o nome do projeto, e avisar o CN.
- **Valores de contrato** falados na call ficam só em *Observações* da proposta, nunca nos exemplos.
