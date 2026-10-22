---
name: dimensionamento-ntec
description: Dimensiona propostas de software do NTec (Poli Júnior) — sites, webapps, PWAs, apps e painéis — e devolve uma faixa de semanas (otimista, provável, conservador) com os riscos para a área de projetos, no template "Proposta Técnica" do NTec (PDF com 14 seções, cronograma por sprint e memória do dimensionamento). Feita para CNs sem formação técnica; a entrada padrão são as transcrições na íntegra do Fathom da AT Diagnóstico e da AT Aprofundamento, e a skill dimensiona pelo que foi discutido nas duas calls. Use quando pedirem para dimensionar, estimar prazo, validar ou "ver quantas sprints dá" um projeto do NTec; quando colarem a transcrição da AT Diag, da AT Aprof ou de qualquer call com o cliente; quando pedirem a proposta técnica para validação; quando mandarem formulário, ficha ou briefing (estimativa preliminar); ou quando perguntarem "cabe em X semanas?" ou "isso é viável?", mesmo que pareça só uma estimativa rápida.
---

# Skill de Dimensionamento — NTec

Transforma as **transcrições da AT Diagnóstico e da AT Aprofundamento** (Fathom, na íntegra) numa **faixa de semanas** defensável, calibrada nos projetos reais do NTec. O público principal são **CNs sem formação técnica**: a skill lê a conversa com o cliente, traduz para fatores técnicos e devolve números que a área de projetos reconhece.

**Onde fica no processo:** AT Diag → AT Aprof (protótipo e escopo) → **esta skill dimensiona a partir das duas transcrições** → área de projetos revisa → proposta. Com uma call só, ou sem transcrição, a skill ainda dimensiona, mas o resultado é preliminar.

A área de projetos sempre revisa o resultado antes de virar proposta. A skill evita que chegue à equipe um prazo "nada a ver". Ela não substitui a validação.

## Arquivos desta pasta (ler sob demanda)

| Arquivo | Quando ler |
|---|---|
| `fatores/README.md` e `fatores/glossario.md` | **Sempre.** Índice dos fatores, decisões em aberto (D1 a D5) e a definição única de cada termo (o glossário vence qualquer outro arquivo) |
| `fatores/F0-viabilidade.md` | **Sempre, antes de tudo.** Critérios que rejeitam o projeto (🚫) ou param para a área de projetos (🚩) |
| `fatores/F1-*.md` a `fatores/F6-*.md` | Sempre: pergunta, onde ler e o que fazer sem resposta para cada fator, com os pesos de cada fase |
| `leitura-transcricoes.md` | **Sempre que houver transcrição.** Como preparar a transcrição, o que conta como escopo, como montar o inventário de jornadas, onde está cada campo do JSON nas calls e o que vira lacuna |
| `insumos-e-perguntas.md` | Quando **não** houver transcrição (formulário, ficha, briefing, texto do CN), e para o vocabulário de negócio → técnico |
| `regua-dimensionamento.md` | Sempre: regras de uso, faixa final, quando parar, calibração e histórico das mudanças (os pesos estão em `fatores/`) |
| `regra-fronteira-e-faixa.md` | Quando um fator encaixar em duas linhas da régua, e para a tabela de cortes de "O que cortar" |
| `exemplos/*.md` | Para achar um **precedente** parecido (mesmo formato, mesmo porte) e comparar o resultado. `exemplos/projeto-h.md` é o caso completo a partir de duas transcrições |
| `scripts/calcular_faixa.py` | Sempre, para fazer a conta (não somar de cabeça) |
| `proposta-tecnica.md` | Sempre, no fim: como preencher cada uma das 14 seções da **Proposta Técnica** (o entregável) a partir das calls e da conta |
| `scripts/gerar_proposta.py` | Sempre, no fim: gera o PDF "[Proposta Técnica] {projeto}" no template do NTec |
| `exemplos/ficticio-petagenda-proposta.md` | Modelo do JSON da proposta, para copiar a estrutura |

## Procedimento

1. **Ler a entrada.**
   - **Com as duas transcrições** (AT Diag e AT Aprof, na íntegra): seguir `leitura-transcricoes.md`. Preparar a transcrição (quem é cliente, o que descartar), separar o que o cliente confirmou do que é ideia solta e montar o **inventário de jornadas** (Passos 2 a 4).
   - **Com uma call só, ou só o resumo do Fathom:** seguir `leitura-transcricoes.md` do mesmo jeito, marcar ⚠️ *Estimativa preliminar* e dizer o que falta.
   - **Sem transcrição** (formulário Dimensionamento Tec, ficha, briefing, texto do CN): seguir `insumos-e-perguntas.md` e marcar ⚠️ *Estimativa preliminar, sem transcrição das calls*.
2. **F0 — Viabilidade** (`fatores/F0-viabilidade.md`). Responder cada critério com citação da call. Critério de 🚫 rejeição → **parar aqui**: não preencher F1 a F6, não gerar PDF e responder ao CN no formato do fim do F0 (critério, motivo, o que precisaria mudar). Critério de 🚩 parada → seguir dimensionando, mas o status fica 🚩 e a proposta não vai para o cliente antes da área de projetos responder.
3. **Preencher os fatores de F1 a F6**, cada um pelo seu arquivo em `fatores/`, com a tabela do Passo 5 de `leitura-transcricoes.md`. **Regra de citação:** a linha mais leve só entra com o trecho da call que a justifica (call, minuto e fala); sem citação, vai a mais pesada. O que as calls não respondem vira **lacuna**: entra na conta com o valor mais pesado, vai para `lacunas_fathom` no JSON (o script mostra quantas semanas da venda dependem dela) e volta para o CN em *Lacunas para o CN* (no chat, na seção 11 e no anexo da proposta), com a pergunta pronta. **Integrações não geram pergunta sobre documentação:** recebem peso fixo pelo teste de `fatores/F3-integracoes.md`. No máximo 5 perguntas por rodada, as que mais mexem no prazo primeiro.
4. **Montar o JSON** de entrada no formato da seção *Entrada da régua* dos `exemplos/*.md`: o bloco `"f0"` e **todos** os campos de F1 a F6. Nenhum campo tem padrão: se faltar um, o script para e diz qual. Rodar:
   ```bash
   python scripts/calcular_faixa.py entrada.json
   ```
   Sem Python disponível, fazer a conta pelas tabelas de `fatores/` e dizer isso em *Observações*.
5. **Comparar com o precedente** mais parecido em `exemplos/`. Se o resultado ficar muito longe do precedente (mais de 30%), explicar o porquê ou rever os fatores. **Comparar também com o prazo que o CN já falou para o cliente** na AT Aprof, se falou: a diferença vai para *Observações* e, se o prazo falado estiver abaixo do otimista, para o topo de *Pontos de atenção*.
6. **Aplicar fronteira** se necessário (`regra-fronteira-e-faixa.md`).
7. **Montar a Proposta Técnica** (`proposta-tecnica.md`): um JSON com as 14 seções do template e o bloco `dimensionamento` (a mesma entrada do passo 4, mais critérios, inventário, lacunas, precedente, cortes e observações). Gerar o PDF:
   ```bash
   python scripts/gerar_proposta.py proposta.json --saida <pasta-que-o-CN-vê>
   ```
   O script recalcula a faixa a partir de `dimensionamento.entrada` (nunca digitar as semanas no JSON) e confere o checklist final do template. Projeto rejeitado no F0 não gera PDF. Os avisos internos (decisões D1 a D5 em aberto) saem só no terminal. Sem `reportlab`: `pip install reportlab`. Se não der para instalar, entregar o JSON e dizer isso.
8. **Responder no chat** no formato curto abaixo: o detalhe está no PDF.

## Regras gerais

- **Nunca inventar número nem fator.** Fator que as calls não respondem → lacuna para o CN, com o valor mais pesado na conta + *Suposições*. No NTec, o erro histórico é vender para menos (Projeto C: vendido 11, levou ~14).
- **Sempre marcar a origem** do dado: `(origem: AT Diag · 14/07 7:46 — "trecho")`, `(origem: AT Aprof · 21/07 1:35 — "trecho")`, `(origem: lacuna — não está nas calls)`, `(origem: CN)`, `(origem: formulário)`, `(origem: palpite do CN)`, `(origem: suposição da skill)`.
- **Só os fatores contam.** O prazo sai do F0 ao F6 e dos multiplicadores de `fatores/`, nada além disso: nem faixa de portfólio, nem prazo pedido pelo cliente, nem **o prazo ou o preço que o CN já falou na call**.
- **Restrição técnica → F0, não aumentar prazo.** Multitenancy com regra diferente por tenant, integração com sistema sem API, feature sem referência nem documentação e dependência de hardware viram 🚩 no F0, não "+3 semanas".
- **Sempre trazer a seção "O que cortar".** Cada corte é uma jornada ou uma integração do inventário, nunca algo que o cliente já descartou na call.
- **Escopo é o que o cliente confirmou nas calls.** Não acrescentar jornada, perfil ou integração que ninguém confirmou (`leitura-transcricoes.md`, Passo 3). Ideia solta ou hesitação não entra na conta: vira lacuna, se mexe no prazo, ou roadmap *A confirmar*. Se a skill achar que falta algo para o produto funcionar, isso vai para *Pontos de atenção* ("as calls não cobrem X"), e não para a conta.
- **Não prometer stack nem tecnologia.** A seção 12 da proposta sugere a stack do template NTec sempre como *premissa a validar na Sprint de Refino*. Se o CN já falou "vai ser em X", registrar também como premissa a validar.
- **Semanas off e garantia ficam fora da faixa**: somar as semanas off do calendário depois; a garantia de 30 dias é gratuita.
- **Dado pessoal fica fora do repositório.** Transcrição, nome do cliente e valores de contrato não vão para `exemplos/` (`leitura-transcricoes.md`, Passo 9).

## Parar e sinalizar para a área de projetos

- 🚫 **Rejeitado no F0** (stack exigida fora da lista, offline com sincronização em MongoDB exigido, SLA ou sustentação, infra do cliente sem acesso do NTec): não dimensionar.
- 🚩 **Parado no F0** (multa por atraso, ninguém nomeado para validar, feature sem referência nem documentação, hardware, multitenancy com regra diferente por tenant, integração sem API, prazo exigido abaixo do otimista): dimensionar, mas não vender sem a área de projetos.
- **Demanda pouco detalhada** (`fatores/F1-imersao-setup.md`, 1.2): abrir a resposta com o alerta de discovery. O status nunca é ✅.
- **Prazo já falado ao cliente abaixo do otimista** da skill: a expectativa do cliente está errada; o CN precisa corrigir antes da proposta.
- **Provável acima de 26 semanas**: a régua ainda não foi calibrada para projetos grandes (Projetos E e F, de 34 e 38 semanas, não têm ficha técnica). Dimensionar mesmo assim, marcar ⚠️ e sugerir quebrar em fases.
- Dependência de dados de bases soltas → chamar o núcleo de Dados.
- Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.
- Divergência entre as duas calls, ou entre o que o CN declarou e o que aparece na transcrição.
- Teto de fase passado (F1, F2 ou F4 acima de 4 semanas): a soma é mantida, não cortada, e a área de projetos revisa (D4, provisório).

## Entregável: a Proposta Técnica (template do NTec)

O dimensionamento final sai **no template "Proposta Técnica" do NTec** (Comercial → Validação de Projeto), o documento que o comercial envia para a validação técnica. São 14 seções, seis delas OBRIGATÓRIAS (4 Perfis, 6 Regras, 8 Segurança, 10 Roadmap, 11 Pontos em aberto, 14 Protótipo), o checklist final e, no fim, o **Anexo — Memória do dimensionamento**, com o que a área de projetos precisa revisar: faixa, F1 a F6 com critério, o inventário de jornadas, alertas, lacunas, precedente, O que cortar, suposições, ajustes de fronteira e pontos para a imersão.

Onde o dimensionamento aparece no corpo do template:
- **Caixa de status** (topo da página 1): status, prazo recomendado e a faixa.
- **10. Roadmap:** tudo que está na conta é *Prioritário*. *A confirmar* e *Futuro* nunca entram no cronograma (o script confere).
- **11. Pontos em aberto:** as lacunas das calls, os documentos que o cliente ainda precisa mandar e toda dependência externa. Nunca vazio.
- **13. Cronograma sprint a sprint:** as fases F1 a F6 (valores centrais) distribuídas em sprints de 2 semanas, somando a recomendação de venda. Sprint que depende de um ponto da seção 11 vem marcada.

Como preencher cada seção: `proposta-tecnica.md`. O PDF é lido pelo comercial e pela área de projetos: frases curtas e todo termo técnico explicado na primeira vez.

**O que a skill não inventa no template:** link e conteúdo do protótipo (sem protótipo, a seção 14 sai com o aviso "Protótipo não recebido" e o checklist fica PENDENTE), responsável comercial e data de envio (em branco, para o CN), e histórico, logs ou permissões que ninguém discutiu nas calls (escrever "não discutido nas calls").

## Resposta no chat (sempre esta, curta)

Público: um CN que talvez nunca tenha programado.

1. `# Projeto [nome do cliente ou produto]`
2. **Status**, uma linha: ✅ Pronto para proposta · ⚠️ Precisa de revisão da área de projetos (inclui "⚠️ Estimativa preliminar" e "⚠️ Demanda pouco detalhada") · 🚩 Parado · 🚫 Rejeitado no F0 (nesse caso, a resposta é só o bloco do fim de `fatores/F0-viabilidade.md`, sem os itens 3 a 9).
3. **Prazo em uma frase.** Ex.: *"Recomendado vender 18 semanas (9 sprints), mais as semanas off. Não vender abaixo de 13."* Com lacuna que mexe na venda, usar a frase do script, com "+": *"Recomendado vender 12 semanas (6 sprints) = 10 + 2 que dependem de confirmar com o cliente (login e perfis, integrações), mais as semanas off. Não vender abaixo de 9."*
4. **Faixa:** otimista · provável · conservador, em semanas e sprints. Se o CN já falou um prazo na call, uma linha comparando.
5. **Inventário de jornadas**, uma linha por jornada, com a call que a sustenta.
6. **Caminho do PDF** "[Proposta Técnica] {projeto}.pdf".
7. **Lacunas para o CN**, na tabela `Fator | Procurado nas calls e não achado | Pergunta para o cliente | Valor provisório na conta`, ou `Sem lacunas: tudo veio das calls.`
8. **Itens PENDENTES do checklist**, com o que o CN precisa fazer (ex.: anexar o protótipo e preencher a seção 14).
9. **Os 2 ou 3 pontos de atenção mais graves**, uma linha cada.

## Status da skill

Versão inicial (16/10/2026). Integrações com peso fixo, sem perguntar ao CN, desde 17/10/2026. Sem buffer percentual nem negociação de prazo desde 17/10/2026. Entregável no template "Proposta Técnica" do NTec, em PDF gerado por `scripts/gerar_proposta.py`, desde 17/10/2026. Revisão de 20/10/2026 (reunião de validação), aplicada em 21/10/2026: F0 de viabilidade antes de tudo, um arquivo por fator em `fatores/`, nenhum campo do JSON com padrão, tetos que não cortam a soma, e sem o fator Claude Code e o fator "cliente com pouca disponibilidade"; as decisões D1 a D5 usam valores provisórios até a área técnica validar. Revisão de 22/10/2026 (Projeto G): fluxo = jornada; fator de formato por fluxo (`fluxos_por_formato`); relatório em template fixo não é RN específica; upload simples do usuário não é dependência de dados; `lojas` pode ser lacuna. **V2-Inov (22/10/2026): a entrada padrão deixou de ser a PRD e passou a ser a transcrição na íntegra da AT Diag e da AT Aprof** (`leitura-transcricoes.md`); `lacunas_fathom` aceita também login (`niveis_acesso`) e `integracoes`, com o valor leve dito no JSON. Pesos inalterados. Primeiro caso pelas transcrições: Projeto H (`exemplos/projeto-h.md`). Calibrada com Projeto A, Projeto D, Projeto C e Projeto B, anteriores a este formato: a leitura das transcrições ainda não foi conferida contra um projeto terminado. Pendente: (1) fichas técnicas de Projetos E e F para calibrar projetos grandes; (2) conteúdo da subpágina "Régua de Dimensionamento" do Notion, que não veio no PDF; (3) atualizar a calibração quando Projeto B, Projeto D e Projeto H terminarem.
