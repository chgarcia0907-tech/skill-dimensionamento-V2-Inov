# Leitura da PRD — do documento de requisitos para os fatores da régua

A **PRD** (Documento de Requisitos de produto do NTec) é a entrada padrão desta skill. Ela é gerada pela skill `documento-requisitos-ntec` ([repositório](https://github.com/rivasaugustus/documento-requisitos-ntec)) a partir das reuniões com o cliente e vira anexo de contrato. Esta skill roda **depois** dela.

Este arquivo diz onde, na PRD, está cada fator da régua e como traduzi-lo para o JSON do `scripts/calcular_faixa.py`.

---

## Passo 1 — O que o CN manda

| Peça | De onde vem | Como usar |
|---|---|---|
| **PDF "[Requisitos] {projeto}"** (ou o `.md` que gerou o PDF) | Saída da skill da PRD | **Fonte principal.** Seções 1 (Visão Geral), 2 (Requisitos Funcionais por módulo), 3 (Não Funcionais) e 4 (Exclusões) |
| **Bloco "Inventário para dimensionamento"** | Chat da skill da PRD, logo depois do PDF | Atalho: uma linha por módulo, com `Módulo \| Superfície \| Itens A(cli)D \| Itens SID \| Integrações \| Fluxos de dados \| Fatores de complexidade`. Se o CN não colar, **montar o inventário a partir do PDF** com as mesmas colunas |
| **Bloco "Pontos para a imersão"** | Chat da skill da PRD | Detalhes que não mudam o tamanho. Não somam prazo: entram como atividades da imersão (F1) na resposta |
| Blocos "Perfis de acesso", "Funcionalidades" e "Integrações" | Chat da skill da PRD | Conferência. As fontes (`[Fathom · AT 12/03]`, `[chat]`…) mostram de onde veio cada item |

**Sem PRD** (só o formulário Dimensionamento Tec, uma transcrição ou um briefing): dimensionar mesmo assim pelo caminho de `insumos-e-perguntas.md`, mas o status nunca é ✅. Marcar ⚠️ **Estimativa preliminar, sem PRD** e dizer ao CN para rodar a skill da PRD antes de fechar a proposta.

**PDF e inventário divergem** (ex.: o inventário tem um módulo que o PDF não tem): vale o PDF, que é o anexo de contrato. Registrar a divergência em *Pontos de atenção*.

## Passo 2 — Onde está cada fator

| Fator da régua (campo do JSON) | Onde ler na PRD | Como traduzir |
|---|---|---|
| `formatos` | Linha `**Superfície:**` de cada módulo + 3.1 *Ambientes de entrega* | `app mobile` → `"app"`. `site` ou `painel web` → `"web"` (ou `"pwa"` se a PRD disser que instala pelo navegador). App mobile + painel web = dois formatos. Site + painel web no mesmo sistema = um formato só |
| `lojas` | Módulo *Disponibilização do Produto* + 3.1 | Publicação na App Store ou Play Store → `"normal"`. Se a 3.4 fala de dado de saúde, financeiro ou de menores → `"sensivel"`. Sem loja → `"nao"` |
| `niveis_acesso` | 2.1 *Autenticação e Perfis de Acesso* | Contar os perfis. Perfil com módulo ou superfície própria, ou com aprovação de cadastro → "grandes diferenças". Só ações a mais no mesmo módulo → "poucas diferenças". Sem 2.1 (sem login) → `"nenhum"` |
| `multitenancy` | Visão Geral, 2.1, RNs e 3.4 (termos: multiempresa, por unidade, por clínica, por filial) | Só o dado separado por empresa → `"separado"` ou `"isolado"` (perguntar qual, se a PRD não disser). Regras ou funções diferentes por empresa → `"instancias"` (🚩) |
| `fluxos_comuns` | Módulos da seção 2 | **1 módulo = 1 fluxo.** Não contam: 2.1 Autenticação (vai para F2) e *Disponibilização do Produto* (vai para F5 e F6) |
| `fluxos_rn_especifica` | Módulos com `### Regras de Negócio` + coluna *Fatores de complexidade* | O módulo sai de `fluxos_comuns` e entra aqui quando tem RN de cálculo, fórmula, regra clínica, legal ou de dinheiro, ou quando tem um dos fatores da tabela do Passo 3 que viram RN específica. Conta **uma vez por módulo**, mesmo com várias RNs |
| `features_atipicas` | Coluna *Fatores de complexidade* | Só pelos fatores da tabela do Passo 3 que viram feature atípica. O "produto sem benchmark" não está na PRD: perguntar ao CN (Passo 4) |
| `integracoes` | Itens `**SID** integrar com…` (Sentido, Dados, Meio) + coluna *Integrações* | **Peso fixo, sem perguntar ao CN** (regra em `regua-dimensionamento.md`, F3). Sentido `envia` ou `recebe` → unidirecional. `envia e recebe` → bidirecional. Serviço de mercado (pagamento, mapa, push, IA, WhatsApp Business, NF-e…) → `_doc`. Sistema do cliente (ERP, legado, sob medida), meio `arquivo` ou dúvida → `_sem_doc`, com cláusula de contrato e plano B. `"sem_api"` (🚩) só se a PRD disser que o sistema não tem API. Google, e-mail e upload de arquivo → `"template"` |
| `dependencia_dados` | Fluxos com `**Origem:**` / `**Processamento:**` / `**Destino:**` | Origem em planilha, base pública, CSV ou sistema antigo → `true` (e chamar o núcleo de Dados). Importação, seja carga única ou recorrente, também. Consulta automática a um serviço é integração, não dependência de dados |
| `offline` | Termo "offline" (a PRD sempre diz o mecanismo) | Só consulta sem internet → `"local"`. Registro com sincronização depois → `"sync"` |
| `volume_alto` | 3.3 *Performance* | Milhares de usuários simultâneos ou picos declarados → `true`. Sem 3.3 → `false` |
| `rn_critica` (F4) | RNs e 3.4 | RN de saúde, dinheiro, cálculo clínico ou legal → `true` |
| `demanda_pouco_detalhada` | — | **`false`.** A PRD é o documento de requisitos |
| `stack_fora_template` | 3.1 (serviços de terceiros definidos com o cliente) | A PRD não fixa stack de propósito. Só `true` se a 3.1 citar uma tecnologia exigida pelo cliente. Se não citar, perguntar (Passo 4) |
| `deploy_infra_cliente` | 3.1 | `true` se a 3.1 disser que roda nos servidores ou na nuvem do cliente. Se não disser, perguntar (Passo 4) |
| `atipico`, `cliente_pouca_disponibilidade` | — | Não estão na PRD. Perguntar (Passo 4) |

**Hardcoded** (decisão fixa do cliente) não muda nenhum peso. Ele só confirma que não há tela de configuração daquele item, e a skill não deve somar tela de configuração por conta própria.

**Exclusões Explícitas (seção 4)** não somam nada. Usar para duas coisas: conferir que nenhum item excluído foi contado e montar a seção "O que cortar" (um corte não pode ser algo que já está excluído).

## Passo 3 — Fatores de complexidade da PRD que a régua não tem

A PRD marca fatores que não têm linha própria na régua. Eles **encaixam nas linhas que já existem**, sem peso novo (não há dado de calibração para criar pesos).

| Fator na PRD | Linha da régua | Observação |
|---|---|---|
| Pagamento (gateway, Pix, cartão) | Integração `bi_doc` (cobra e recebe a confirmação) | Gateway é serviço de mercado. `bi_sem_doc` só se o pagamento passar pelo sistema próprio do cliente |
| IA (classificar, extrair, gerar, responder) | Integração `uni_doc` (API do modelo) | Se a PRD disser que a IA decide sem humano no fim, marcar também ⚠️ em *Pontos de atenção* |
| Notificação por push no app | Integração `uni_doc` | |
| Notificação por WhatsApp automático | Integração `uni_doc`, ou `bi_doc` se o sistema lê a resposta | Link para abrir o WhatsApp não é integração (0) |
| Notificação por e-mail | `template` | |
| Aviso dentro do sistema | 0 (faz parte do módulo) | |
| Tempo real por aviso do servidor (push) | +1 em `features_atipicas` | Atualização periódica (polling) = 0 |
| Relatório configurável pelo usuário (construtor) | +1 em `features_atipicas` | Tela fixa ou exportação para PDF ou Excel = 0 (faz parte do módulo) |
| Concorrência (ex.: aceite atômico, "o primeiro que aceitar leva") | O módulo vira `fluxos_rn_especifica` | |
| Imutabilidade ou versionamento (ex.: prontuário que não se edita) | O módulo vira `fluxos_rn_especifica` | |
| Rotina agendada (gatilho por horário, não por evento) | O módulo vira `fluxos_rn_especifica` | Gatilho por evento no sistema = 0 |
| Upload e armazenamento de arquivos | `template` (S3) | |
| Importação ou migração | `dependencia_dados: true` | |
| Multiempresa | `multitenancy` (ver Passo 2) | |
| Offline | `offline` (ver Passo 2) | |

**Não contar duas vezes.** O mesmo módulo vira RN específica uma vez só, mesmo que tenha concorrência **e** imutabilidade. Um fator que já virou integração não vira também feature atípica (a exceção é a IA que decide sozinha, que só ganha ⚠️, sem peso).

## Passo 4 — O que a PRD não responde: perguntar ao CN

A PRD descreve o produto, não o projeto. Depois de ler a PRD, fazer **uma rodada curta** só com o que falta, no máximo 5 perguntas, das que mais mexem no prazo para as que menos mexem:

| Fator | Pergunta para o CN |
|---|---|
| Disponibilidade do cliente (`cliente_pouca_disponibilidade`) | "Quem do cliente vai testar e aprovar as entregas? Essa pessoa tem umas 2 horas por semana para isso?" |
| Stack e infra (`stack_fora_template`, `deploy_infra_cliente`) | "O cliente exige alguma tecnologia, ou que o sistema fique nos servidores dele?" (pular se a 3.1 já responde) |
| Atípico (`atipico`, `features_atipicas`) | "Existe algum app ou site parecido que a gente possa usar de referência?" |
| Semanas off | "Qual é a data prevista de início? (para contar férias, provas e recesso)" |

Se o CN não souber, usar o valor mais pesado plausível e registrar em *Suposições*, com `(origem: suposição da skill)`.

**Não perguntar sobre a documentação das integrações.** O CN não tem como responder: a skill aplica o peso fixo do Passo 2 e registra a classificação em *Suposições* (ex.: `Integração ERP: bidirecional com sistema do cliente (origem: PRD 2.4 + regra de peso fixo)`).

**Lacuna dentro da PRD** (módulo sem superfície, integração sem meio, fluxo de dados sem uma das três partes, "tempo real" sem mecanismo): não deveria acontecer, porque a skill da PRD pergunta antes de gerar o PDF. Se aparecer, tratar como fator desconhecido (perguntar, ou usar o valor mais pesado) e registrar em *Pontos de atenção* que a PRD precisa de revisão antes de virar anexo de contrato.

## Passo 5 — Origem de cada fator

Com PRD, a origem cita a seção:

```
Níveis de acesso: 2 a 6 com grandes diferenças (origem: PRD 2.1 — 4 perfis, recepção e veterinário com módulos próprios)
Fluxos comuns: 4 (origem: PRD 2.2 a 2.5)
Integração Mercado Pago: bidirecional com serviço de mercado (origem: PRD 2.3 + regra de peso fixo)
Disponibilidade do cliente: pouca (origem: CN)
```
