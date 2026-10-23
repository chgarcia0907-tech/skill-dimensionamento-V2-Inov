# Glossário — dimensionamento NTec

Definição única de cada termo usado nos arquivos F0 a F6. Se outro arquivo da skill definir um termo de outro jeito, **vale este glossário**.

---

## Estrutura do produto

**Calls** — As transcrições na íntegra do Fathom da **AT Diagnóstico** (primeira call: dor, contexto, ideia do produto) e da **AT Aprofundamento** (segunda call: protótipo, escopo, condições). São a entrada padrão da skill desde a V2-Inov (`leitura-transcricoes.md`).

**Confirmado** — O que o cliente descreveu como parte do produto, ou o que o CN propôs e o cliente aceitou com uma resposta àquela proposta ("sim", "é isso mesmo"). Hesitação ("não sei se precisa", "talvez") e silêncio não são confirmação.

**Ação** — Cada coisa que o usuário faz dentro de uma jornada: cadastrar, consultar, listar, editar, desativar, aprovar, exportar.

**Fluxo** — Unidade de esforço do F3. Uma **jornada** completa, do início ao fim, que se quebrar torna o produto inútil. Nas calls:
1. Listar o que alguém faz do começo ao fim, como o cliente descreveu ("o médico entra, coloca o peso e o tipo de soro, e sai com o volume"). Fora: login e perfis (F2), publicação nas lojas (F5 e F6) e, quando `offline` for `sync` ou `local`, a parte de offline (vai para o extra de offline).
2. **Juntar** o que é a mesma jornada: mesma coisa principal, mesmo código, e uma parte é continuação da outra (lista + detalhe; criar + gerenciar). Variações dentro da mesma tela (três tipos de soro, a unidade do cálcio) são a mesma jornada. Uma parte pequena que só serve a outra jornada entra nela (ex.: cadastrar pessoa durante a anotação).
3. Jornada com **mais de 8 ações** conta 2 fluxos.
4. Cada junção vai para *Suposições*.

Uma tela solta não é fluxo. (🔎 Proposta: os limites 8 e "parte pequena" precisam ser calibrados.)

**Formato** — Cada **código separado** que vai para o ar. Painel admin dentro do mesmo app web é o mesmo formato. App nativo + painel web são dois formatos.

**Fluxo compartilhado** — Fluxo com tela em mais de um código (ex.: o tutor agenda no app e a recepção gerencia a mesma agenda no painel). Só ele recebe o formato extra (D1). Fluxo que vive num código só recebe só o fator daquele código (`F3-desenvolvimento.md`, 3.2).

**Web** — Abre no navegador, sem instalar.

**PWA** — Web que instala pelo navegador (ícone na tela do celular), sem passar por loja. Substitui o antigo `webapp`.

**App nativo** — Precisa estar na App Store ou Play Store, **ou** usa um recurso nativo desta lista: Bluetooth, GPS em segundo plano, NFC, notificação com o app fechado em iOS, leitura de sensores. Fora da lista → PWA.

## Perfis e acesso

**Perfil (nível de acesso)** — Cada tipo de pessoa que entra no sistema com login, citado nas calls. Admin conta como perfil.

**Tela exclusiva** — Tela ou rota que um perfil abre e pelo menos um outro perfil não abre. **Não contam:**
- um item a mais num menu que leva a uma tela que todos abrem;
- o **painel admin básico** (ver abaixo).

**Painel admin básico** — O que o template NTec já entrega para o admin, sem custo de prazo: gerenciar usuários (listar, criar, editar, desativar, trocar o perfil) e ver, editar ou remover os registros que os outros perfis criam, nas mesmas telas de listagem e detalhe dos módulos. Qualquer tela de admin **além disso** é tela exclusiva: dashboard ou relatório, aprovação de cadastro, configuração de regra de negócio, auditoria, financeiro. (🔎 Proposta: confirmar com a área técnica o que o painel admin do template cobre hoje.)

**Status de cadastro** — O cadastro de um perfil passa por estados (pendente, aprovado, rejeitado) que bloqueiam o acesso até alguém aprovar.

**Filtro por dono** — O perfil só vê os registros que ele mesmo criou ou que são dele (ex.: paciente só vê o próprio diário).

## Multitenancy

**Tenant** — Cada empresa, clínica, unidade ou filial que usa o mesmo sistema com seus próprios dados.

**Separado** — Um banco só, cada registro marcado com o tenant, filtro no código. Um administrador geral vê os dados de todos os tenants.

**Isolado** — Vazamento de dado entre tenants é quebra de contrato ou de LGPD. Exige isolamento no banco (RLS, schema ou banco por tenant). Ligar ou desligar features de uma lista fixa, ou trocar logo e cores por tenant, continua sendo isolado.

**Instâncias** — Código ou regra de negócio **diferente** por tenant. Vai para o F0.

## Regras de negócio

**RN específica** (F3) — Regra que o cliente precisa entregar **escrita**: fórmula, tabela, norma, protocolo. Também: concorrência ("o primeiro que aceitar leva") e imutabilidade/versionamento. **Não são** RN específica: validação padrão de mercado (CPF, CNPJ, e-mail, CEP) e documento gerado num **template fixo** (relatório em PDF, Word ou Excel), mesmo em mais de um formato.

**RN crítica** (F4) — **O código do NTec calcula** valor em dinheiro, dose, dado clínico, prazo legal ou dado fiscal, e um erro causa dano ao usuário final. Só repassar um valor para o gateway de pagamento não é RN crítica.

**Rotina agendada** — Algo que roda sozinho por horário (todo dia às 8h), não por ação do usuário.

## Referência e risco

**Produto atípico** (F1) — Nenhum app ou site foi citado como referência para o **produto inteiro** em nenhuma das calls. Setor incomum com produto comum não é atípico.

**Feature atípica** (F3) — Uma **feature** específica está na lista do Passo 7 de `leitura-transcricoes.md` (tempo real por push, relatório configurável) ou não tem referência citada. É uma **contagem** (quantas features), não semanas.

**Lacuna** — Fator que as calls não respondem. Entra na conta com o valor mais pesado e volta para o CN como pergunta.

**Citação** — Trecho literal da transcrição, com a call (AT Diag ou AT Aprof), a data e o minuto, que justifica a linha escolhida. O resumo e os *Action Items* do Fathom não são citação.

## Integrações e dados

**Integração** — Troca **automática** de dados com outro sistema, sem uma pessoa disparar.

**Unidirecional** — O sistema só envia **ou** só recebe.

**Bidirecional** — O sistema envia **e** recebe.

**Serviço de mercado** — Produto vendido para qualquer empresa, com documentação pública **e** ambiente de teste (sandbox) que o NTec consegue acessar sozinho, sem depender da TI do cliente. Ex.: Mercado Pago, Google Maps, Expo Push, OpenAI, WhatsApp Business.

**Sistema do cliente** — ERP, sistema legado, sistema sob medida, ou SaaS em que o acesso depende da TI do cliente (ex.: Totvs, Bling ou RD Station sem sandbox liberado). Também: meio `arquivo` automático e qualquer caso em dúvida.

**Sem API** — O cliente diz explicitamente na call que o outro sistema não tem API.

**Dependência de dados** — Dados que **já existem fora do sistema** (planilha legada, base pública, sistema antigo) e precisam ser migrados, limpos, convertidos ou cruzados para o produto funcionar; **uma pessoa dispara** a importação (carga única ou recorrente). **Não é:** upload simples feito pelo usuário dentro do produto, com formato combinado na call, que vira registros na hora (ex.: planilha de uma coluna, uma pergunta por linha). Isso é parte do módulo.

**Offline local** — O app **só lê** sem internet o que já está no aparelho, sem gravar nada para subir depois.

**Offline com sincronização** — O app **grava** sem internet e sobe os dados quando a conexão volta.

**Volume alto** — Alguém diz na call que haverá **1.000 ou mais usuários simultâneos**, ou um pico com data (evento, lançamento). (🔎 Proposta: o limite 1.000 precisa ser validado.)

## Deploy e lojas

**Infra do cliente** — A conta de nuvem ou o servidor é do cliente, **ou** a TI do cliente aprova cada publicação.

**App sensível** — Categoria Medical, Finance ou Kids na loja, **ou** coleta de dado sensível (LGPD, art. 5º, II: saúde, biometria, origem racial, religião etc.), **ou** pagamento dentro do app, **ou** público com menos de 13 anos.

## Conta

**Linha pesada** — Entre duas linhas possíveis, a que tem o valor central maior.

**Teto** — Valor máximo de referência de uma fase. Ver D4 sobre o que acontece quando a soma passa dele.

**Piso** — O cenário otimista. Nunca vender abaixo dele.
