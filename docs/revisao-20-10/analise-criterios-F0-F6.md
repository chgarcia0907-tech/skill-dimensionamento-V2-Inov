# Análise dos critérios F0–F6: skill de dimensionamento NTec

Data: 21/10/2026. Insumos:
- repositório `skill-dimensionamento-ntec` (régua, leitura-prd, regra de fronteira, `calcular_faixa.py`);
- anotações da reunião "Validação Skill NTec" (20/10/2026);
- LLM Council (5 conselheiros, revisão cruzada anônima e síntese).

---

## 1. Como a skill dimensiona hoje (resumo)

A skill lê a PRD, preenche um JSON de fatores e roda o `calcular_faixa.py`. O script soma F1 a F6, cada linha com mín, central e máx. O resultado é: otimista = soma dos mínimos, provável = soma dos centrais (vendido arredondado para sprints inteiras) e conservador = soma dos máximos.

| Fase | O que mede | Teto |
|---|---|---|
| F1 | Imersão e setup: base, mais demanda pouco detalhada, setor atípico e stack fora do template | 4 |
| F2 | Níveis de acesso (5 linhas) **e** multitenancy (4 linhas) na mesma fase, × fator Claude Code | 4 |
| F3 | Fluxos (comum, com RN específica ou atípico) × formato × Claude Code, somados aos extras (integrações, dados, offline, volume) | — |
| F4 | Testes: base, mais RN crítica e cliente com pouca disponibilidade | 4 |
| F5 | Deploy: web, app e infra do cliente | — |
| F6 | Lojas: não, comum ou sensível | — |
| **F0** | **Não existe.** Os 🚩 estão espalhados: `instancias`, `sem_api`, feature sem benchmark | — |

---

## 2. Veredito do Conselho

### Onde todos concordam (sinal forte)
1. **Toda ambiguidade cai na linha mais leve.** A régua diz "na dúvida, o mais pesado", mas o mecanismo faz o contrário, por três caminhos:
   - **Defaults do script.** Campo ausente vira o valor leve: `niveis_acesso="1"`, `multitenancy="nao"`, `offline="nao"`, `lojas="nao"`, `formatos=["web"]` (`calcular_faixa.py:124-125, 142, 165, 197`).
   - **Tetos que cortam.** Os tetos de F1, F2 e F4 reduzem a soma a 4, só com um alerta. No F1, 2,5 + 1 + 1 + 2 = 6,5 vira 4: a stack fora do template passa a custar ~0. No F2, "6+" com "isolado" dá 6 e vira 4. **Muito provavelmente é a "divergência nos tetos do F1" que o Ricardo viu.**
   - **Meio-termo de 0,5.** A regra de fronteira tem um "meio-termo de 0,5" que não existe no script, então o Claude teria de somar de cabeça.
2. **A régua classifica por adjetivos** ("poucas", "grandes", "muito específica", "milhares", "sensível", "regras de deploy dele"). Todo adjetivo precisa virar uma pergunta de sim ou não, respondida com citação da PRD. **Sem citação, vai para a linha pesada.**
3. **O F2 tem sobreposição numérica**: "2 a 6" e "6 ou mais" valem as duas para 6 perfis.
4. **Há definições divergentes entre arquivos**: régua × `leitura-prd.md` × `regra-fronteira-e-faixa.md` (ver a tabela da seção 3).
5. **O F0 precisa de lista fechada.** Uma lista negra (.NET, Angular, COBOL, Delphi) deixa Vue, Flutter, Java, PHP, Laravel e Django sem resposta.

### Onde há divergência
- **O que fazer quando bate no teto.** Uma corrente quer parar (🚩) e mandar para a área de projetos. Outra quer manter a soma e só alertar. *Recomendação: manter a soma e marcar ⚠️. Cortar esconde risco, e parar à toa trava o comercial.*
- **Multitenancy "instâncias" com 1 ou 2 regras por cliente.** Para uns, qualquer regra diferente por tenant já é 🚩. Para outros, uma feature ligada ou desligada a partir de uma lista fixa é "isolado", e 3 ou mais regras divergentes vão para F0. *Recomendação: a segunda.*
- **Peso por entidade nas integrações.** Uma resposta pede peso por entidade sincronizada. As outras mantêm peso fixo. *Recomendação: manter fixo agora (sem dado para calibrar) e reavaliar depois.*

### O que só apareceu na revisão cruzada
- **Contradição F0 × template.** O template NTec usa **MongoDB**, e a reunião proibiu offline com sync em MongoDB. Então, todo projeto com sync vira "stack fora do template"? É preciso decidir isso explicitamente.
- **Teste de concordância.** Antes de fixar os discriminantes, aplicar a nova régua a 3 ou 4 projetos antigos (A, B, C, D) com 2 CNs e o Claude, às cegas, e medir onde a classificação diverge.
- **Glossário único.** "Um .md por fator" pode **multiplicar** a divergência entre arquivos. Os termos (fluxo, perfil, tenant, RN específica, RN crítica, sensível) devem ficar num `glossario.md` só, citado pelos outros arquivos.
- **Dono do desempate.** Quem decide quando o discriminante não resolve, e onde isso fica registrado.
- **Contagem dupla F3 × F4.** A mesma RN soma em "RN específica" (F3) e em "RN crítica" (F4). Hoje isso é permitido, mas falta dizer quando.

### Recomendação
Reescrever cada critério como **pergunta de sim ou não + onde ler na PRD + o que fazer sem resposta**. Fazer o script **recusar campo ausente** e **parar de cortar no teto**. Criar o F0 como lista fechada de stacks **aceitas**, mais as condições de contrato.

### Primeira ação
Corrigir o script (default leve → erro, teto → mantém a soma + ⚠️) **antes** de reescrever os .md. Sem isso, qualquer critério bem escrito continua sendo anulado pela conta.

---

## 3. Critérios mal definidos, fator a fator

Legenda da coluna "Reunião": ✅ a reunião já decidiu; ➕ ponto novo levantado pelo Conselho.

### F0 — Viabilidade (novo)

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| Stack incompatível | Só há exemplos (.NET, Angular, COBOL, Delphi). Vue, Flutter, Java e PHP ficam sem resposta | **Lista de stacks aceitas**: Next.js/React, Expo/React Native, Node/TS, Postgres/Supabase, MongoDB. Trocas aceitas: Mongo↔Supabase/Postgres. Fora da lista → rejeita | ✅ |
| "Condições de contrato incompatíveis" | Não tem definição | Lista fechada: (a) prazo exigido abaixo do otimista; (b) multa por atraso; (c) SLA 24/7 ou sustentação além da garantia de 30 dias; (d) hospedagem no cliente sem acesso do NTec; (e) nenhum validador do cliente nomeado | ✅ (sem lista) |
| 🚩 espalhados | `instancias`, `sem_api` e feature sem benchmark **e** sem doc ficam em F2 e F3 | Passam para o F0 | ➕ |
| Hardware, IoT, Bluetooth | Nenhuma linha cobre | Entra no F0 como "parar e consultar" | ➕ |
| Provável > 26 semanas | Hoje é só ⚠️ | Decidir se vira F0 (sugestão: continua ⚠️ e recomenda quebrar em fases) | ➕ |
| Offline com sync + MongoDB | O template é Mongo | Sync → Postgres obrigatório. **Decidir** se isso conta como stack fora do template (+F1) ou é só premissa | ✅ (sem regra) |

### F1 — Imersão e setup

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| Teto 4 | A soma chega a 6,5 e o `limita()` corta. O risco some | Manter a soma e emitir ⚠️ "bateu no teto" | ✅ (divergência apontada) |
| Baseline | O formulário diz 1–4, mas o mínimo da base é 1,5 | Alinhar texto e número | ➕ |
| Demanda pouco detalhada | Com PRD é **sempre false**, então o alerta de discovery nunca dispara | Alerta de discovery se: não há PRD, **ou** algum módulo sem superfície, **ou** integração sem sentido/dados/meio, **ou** módulo sem RN escrita | ✅ |
| Setor atípico × feature atípica | O mesmo teste ("sem benchmark") vale para F1 e F3 | F1 = o **produto inteiro** não tem referência citada no Fathom. F3 = uma **feature** específica não tem | ➕ |
| Stack em lacuna | Só vira true "se houver indício", o que contraria a regra 1 | Some da régua se o F0 rejeitar a stack. Se a troca for aceita (Mongo → Supabase), o peso continua | ➕ |

### F2 — Acesso e multitenancy (separar em duas tabelas ✅)

**F2a — Níveis de acesso**

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| "2 a 6" × "6 ou mais" | Ambas valem para 6 | 2–5 e 6+ | ➕ |
| Poucas × grandes diferenças | A régua fala em "telas/regras próprias", a leitura-prd em "módulo/superfície própria" e "ações a mais = poucas" | **Grande se algum destes for sim:** (1) algum perfil abre uma tela ou rota que outro não abre; (2) o cadastro tem status (pendente, aprovado, rejeitado); (3) o perfil só vê os **próprios** registros (filtro por dono). Se nenhum for sim, poucas | ✅ (pedir prazo maior) |
| "Regras próprias" | Termo sem definição | Sai da régua e é substituído pelo teste acima | ➕ |

**F2b — Multitenancy**

| Linha | Problema | Discriminante proposto (pergunta ao cliente) | Reunião |
|---|---|---|---|
| Separado | A leitura-prd diz "perguntar qual", mas não diz a quem nem como | "Um administrador geral pode ver os dados de todas as empresas juntas?" Sim → **separado** (um banco, `tenant_id` filtrado no código) | ✅ |
| Isolado | Idem | "Se a empresa A vir um dado da B por um bug, isso é quebra de contrato ou de LGPD?" Sim → **isolado** (RLS, ou schema/banco por tenant). Sem resposta → isolado | ✅ (aumentar prazo) |
| Instâncias 🚩 | Uma única feature diferente por cliente já dispara 🚩 | Ligar/desligar feature de uma lista fixa, ou logo e configuração, → isolado. **Código ou regra de negócio diferente** por cliente → F0 | ➕ |
| Teto F2 | 6+ (4) + isolado (2) = 6 → 4 | Separar os tetos das duas tabelas ou manter a soma com ⚠️ | ➕ |

### F3 — Desenvolvimento (integrações em seção separada ✅)

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| **Unidade de fluxo** | "1 módulo = 1 fluxo" (leitura-prd) × "jornada completa" (régua): um módulo de 15 itens pesa o mesmo que um de 2 | Fluxo = módulo com até N itens A(cli)D; acima de N, conta 2 (calibrar N nos exemplos; sugestão: 8) | ➕ |
| RN "muito específica" | Três critérios em três arquivos: "cálculo que não pode errar", "precisa de documento do cliente", "dinheiro" | Um só: **"O cliente precisa entregar fórmula, tabela ou norma escrita?"** | ➕ |
| Rotina agendada → RN específica | Um cron passa a pesar 3 semanas | Rotina agendada = +0,5 no fluxo, e não troca de linha | ➕ |
| Feature atípica | "Sem saber se é possível" exige julgamento técnico; "+1 em features_atipicas" parece semana, mas é unidade | Nenhuma referência citada no Fathom + item da lista do Passo 3. Deixar claro que é contagem | ➕ |
| `webapp` | Existe no script e nunca é definido | Remover, ou: web = abre no navegador sem instalar; PWA = manifest + instalação; app = loja **ou** API nativa de uma lista fechada (Bluetooth, GPS em segundo plano, NFC) | ➕ |
| Formato extra | "+0,1" é pouco, e a reunião disse "pelo menos 1,2" sem dizer se é +0,2 ou ×1,2 | **Escrever a fórmula.** Ex.: fator = max(formatos) × 1,2 por formato extra em código separado | ✅ (ambíguo) |
| `bi_sem_doc` | Central 2,5 | Mínimo ≥ 4 (ex.: 4 / 4,5 / 5,5) | ✅ |
| `uni_sem_doc` | Não foi revisto | Subir na mesma proporção (sugestão: 2 / 2,5 / 3) | ➕ |
| SaaS com instância do cliente (Totvs, Bling, RD Station) | Não cabe em "mercado" nem em "cliente" | Doc pública + sandbox que o NTec acessa sozinho → `_doc`; depende da TI do cliente → `_sem_doc` | ➕ |
| `sem_api` | Só cobre o caso bidirecional | Criar também a unidirecional sem API | ➕ |
| Dados × integração | Importação recorrente de arquivo cai nas duas linhas | Uma pessoa dispara → dependência de dados; roda sozinho → integração | ➕ |
| Offline "só local" = 0 | Baixar dado do servidor para consultar já é sync de mão única | O app **grava** sem internet → sync. Só lê cache → +0,5/+1 | ➕ |
| Volume alto | "Milhares" não é número | ≥ 1.000 usuários simultâneos declarados na 3.3 da PRD | ➕ |
| Margem ("gordura") | A régua diz "não há buffer", a reunião pediu margem explícita | Criar `F3_GORDURA` (ex.: +10–15% no central de F3) ou subir os centrais. Decidir qual | ✅ |
| Fator Claude Code | x0,75 no F3 e x0,85 no F2 | Remover das constantes, do `zip`, do print, da tabela e da calibração. Refazer a leitura do Projeto B | ✅ |

### F4 — Testes com o cliente

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| RN crítica | "Dinheiro" faz qualquer app com gateway virar crítico | **O nosso código calcula** valor, dose, prazo legal ou nota? Sim → crítica. Só repassar para o gateway não conta | ✅ (aumentar prazo) |
| Base fixa | 2 fluxos e 12 fluxos testam no mesmo tempo | Base proporcional aos fluxos (ex.: +0,25 a cada 4 fluxos acima de 4) | ➕ |
| Pouca disponibilidade | — | **Remover** da tabela, das `LACUNAS_FATHOM` e do Passo 4 da leitura-prd | ✅ |

### F5 — Deploy

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| "Regras de deploy dele" | Vago | "A conta de nuvem ou o servidor é do cliente?" **ou** "A TI do cliente aprova cada publicação?" Sim → a linha vale | ➕ |
| Teto | O formulário diz 1–4, e não há teto | Definir | ➕ |
| Deploys parciais (Vercel) | A reunião validou a prática | Registrar como premissa, sem peso | ✅ |

### F6 — Lojas

| Critério | Problema | Discriminante proposto | Reunião |
|---|---|---|---|
| "Sensível" | Régua e leitura-prd usam critérios diferentes. Um app de academia conta como saúde? | Categoria Medical, Finance ou Kids na loja, **ou** dado sensível (LGPD art. 5º II), **ou** pagamento dentro do app, **ou** público < 13 anos | ➕ |
| "Só para testes" = 0 | O TestFlight também passa por revisão | Teste interno = 0; TestFlight externo = +0,5 | ➕ |

---

## 4. Checklist das mudanças da reunião (o que mexer em cada arquivo)

| # | Mudança decidida | Arquivos | Fica ambíguo? |
|---|---|---|---|
| 1 | Criar F0 (exclusão) | novo `F0-viabilidade.md`, `SKILL.md` (passo 0), script (`paradas`) | Lista fechada de stacks e de condições de contrato (seção 3) |
| 2 | Alerta de discovery | `F1.md`, `leitura-prd.md` (hoje é sempre false), script | Gatilho com PRD |
| 3 | Separar F2 em duas tabelas | `F2.md`, régua, script | Discriminantes da seção 3 + valores novos de "grandes diferenças" e "isolado" |
| 4 | Formato extra ≥ 1,2 | `F3.md`, script (`F3_FORMATO_EXTRA`), exemplo da regra de fronteira | **+0,2 ou ×1,2?** |
| 5 | `bi_sem_doc` ≥ 4 semanas | `F3.md`, script | Novos mín/máx; e o `uni_sem_doc`? |
| 6 | Margem explícita | régua ("Faixa final"), script | Onde aplica e quanto |
| 7 | Offline sync ≠ MongoDB | `F3.md` (flag), `F0` | Conta como stack fora? |
| 8 | Remover Claude Code | régua, script, `SKILL.md` (status), exemplos (`claude_code`), calibração | — |
| 9 | Remover efeito cloud da metodologia | `docs/` (PDF) | — |
| 10 | F4: subir RN crítica, tirar disponibilidade | `F4.md`, script, `leitura-prd.md`, `insumos-e-perguntas.md` | Novo valor de RN crítica |
| 11 | Um .md por fator (F0–F6) | novos arquivos + `README.md` + tabela de arquivos do `SKILL.md` | Criar também o `glossario.md` |
| 12 | Revisão por Augusto e Frank | — | — |

---

## 5. Decisões que dependem do time (não dá para tirar dos documentos)

1. **Formato extra ≥ 1,2.** Quer dizer +0,2 por formato extra (app + web = 1,4) ou ×1,2 sobre o fator (1,2 × 1,2 = 1,44)?
2. **Novos valores** de "2–5 com grandes diferenças", "isolado" e "RN crítica" (a reunião disse "aumentar" sem número).
3. **Margem ("gordura")**: percentual sobre o F3, sobre o total, ou embutida nos centrais?
4. **Teto atingido**: manter a soma + ⚠️ (recomendado) ou parar?
5. **Sync + Mongo**: ele soma como stack fora do template no F1?
