---
name: dimensionamento-ntec
description: Dimensiona propostas de software do Núcleo de Tecnologia (NTec) da Poli Júnior — sites, webapps, PWAs, apps mobile e painéis — e devolve uma faixa de semanas (otimista, provável e conservador) com os riscos que a área de projetos precisa ver. Feita para coordenadores de negócios (CNs) sem formação técnica. A entrada padrão é a PRD (Documento de Requisitos "[Requisitos] {projeto}" gerado pela skill documento-requisitos-ntec), e esta skill roda logo depois dela. Use quando alguém pedir para dimensionar, estimar prazo, validar ou "ver quantas sprints dá" um projeto do NTec; quando mandarem a PRD, o PDF de requisitos ou o bloco "Inventário para dimensionamento"; quando colarem o formulário Dimensionamento Tec, uma ficha de qualificação, um briefing ou a transcrição de uma call (nesses casos a estimativa sai como preliminar); ou quando perguntarem "cabe em X semanas?" ou "isso é viável?" — inclusive quando parecer só uma estimativa rápida, porque é aí que o número sai errado.
---

# Skill de Dimensionamento — NTec

Transforma a **PRD** do projeto (o documento de requisitos que vira anexo de contrato) numa **faixa de semanas** defensável, calibrada nos projetos reais do NTec. O público principal são **CNs sem formação técnica**: a skill pergunta em linguagem de negócio, traduz para fatores técnicos e devolve números que a área de projetos reconhece.

**Onde fica no processo:** reuniões com o cliente → skill `documento-requisitos-ntec` gera a PRD → **esta skill dimensiona a partir da PRD** → área de projetos revisa → proposta. Sem PRD a skill ainda dimensiona, mas o resultado é preliminar.

A área de projetos sempre revisa o resultado antes de virar proposta. A skill evita que chegue à equipe um prazo "nada a ver". Ela não substitui a validação.

## Arquivos desta pasta (ler sob demanda)

| Arquivo | Quando ler |
|---|---|
| `leitura-prd.md` | **Sempre primeiro quando houver PRD.** Onde está cada fator na PRD, como traduzir os fatores de complexidade dela e como tirar do Fathom o que a PRD não responde (o resto vira lacuna para o CN) |
| `insumos-e-perguntas.md` | Quando **não** houver PRD (formulário, ficha, briefing, transcrição), e para o vocabulário de negócio → técnico |
| `regua-dimensionamento.md` | Sempre: pesos de cada fase (F1 a F6), faixa final, quando parar |
| `regra-fronteira-e-faixa.md` | Quando um fator encaixar em duas linhas da régua, e para a tabela de cortes de "O que cortar" |
| `exemplos/*.md` | Para achar um **precedente** parecido (mesmo formato, mesmo porte) e comparar o resultado |
| `scripts/calcular_faixa.py` | Sempre, para fazer a conta (não somar de cabeça) |

## Procedimento

1. **Ler a entrada.**
   - **Com PRD** (PDF ou markdown "[Requisitos] {projeto}", com ou sem o bloco "Inventário para dimensionamento"): seguir `leitura-prd.md`. Se o inventário não veio, montar a partir do PDF.
   - **Sem PRD** (formulário Dimensionamento Tec, ficha, briefing ou transcrição): seguir `insumos-e-perguntas.md` e marcar a resposta como ⚠️ *Estimativa preliminar, sem PRD*.
2. **Preencher os fatores** da régua. Com PRD, o que ela não responde (disponibilidade do cliente, stack e infra, benchmark, data de início) é **procurado na transcrição do Fathom** (`leitura-prd.md`, Passo 4). O que não estiver lá vira **lacuna**: entra na conta com o valor mais pesado e volta para o CN na seção 5 da resposta, com a pergunta pronta. **Integrações não geram pergunta:** recebem peso fixo pela regra de `regua-dimensionamento.md` (serviço de mercado = com documentação; sistema do cliente = sem documentação, com cláusula de contrato e plano B). No máximo 5 perguntas por rodada, as que mais mexem no prazo primeiro. Se o CN não souber, usar o valor mais pesado plausível e registrar em *Suposições*.
3. **Montar o JSON** de entrada (formato dos `exemplos/*.json`) e rodar:
   ```bash
   python scripts/calcular_faixa.py entrada.json
   ```
   Sem Python disponível, fazer a conta pela tabela de `regua-dimensionamento.md` e dizer isso em *Observações*.
4. **Comparar com o precedente** mais parecido em `exemplos/`. Se o resultado ficar muito longe do precedente (mais de 30%), explicar o porquê ou rever os fatores.
5. **Aplicar fronteira** se necessário (`regra-fronteira-e-faixa.md`).
6. **Responder no formato abaixo.**

## Regras gerais

- **Nunca inventar número nem fator.** Fator desconhecido → procurar no Fathom. Não está lá → lacuna para o CN, com o valor mais pesado na conta + *Suposições*. No NTec, o erro histórico é vender para menos (Projeto C: vendido 11, levou ~14).
- **Sempre marcar a origem** do dado: `(origem: PRD 2.3)`, `(origem: Fathom · 12/03 — "trecho")`, `(origem: lacuna — não está no Fathom)`, `(origem: CN)`, `(origem: formulário)`, `(origem: transcrição da call)`, `(origem: palpite do CN)`, `(origem: suposição da skill)`.
- **Restrição técnica → parar, não aumentar prazo.** Multitenancy com instâncias isoladas, integração bidirecional que a PRD diz não ter API e feature sem benchmark nem documentação viram 🚩, não "+3 semanas".
- **Sempre trazer a seção "O que cortar".** Com PRD, cada corte é um módulo ou uma integração da seção 2, e nunca algo que já está nas Exclusões Explícitas.
- **A PRD é anexo de contrato.** Não acrescentar módulo, perfil ou integração que não estão nela. Se a skill achar que falta algo para o produto funcionar, isso vai para *Pontos de atenção* ("a PRD não cobre X"), e não para a conta.
- **Não prometer stack nem tecnologia.** Se o CN já falou "vai ser em X", registrar como premissa a validar.
- **Semanas off e garantia ficam fora da faixa**: somar as semanas off do calendário depois; a garantia de 30 dias é gratuita.

## Parar e sinalizar para a área de projetos

- Qualquer 🚩 de `regua-dimensionamento.md` (multitenancy por instâncias, integração sem API, feature atípica sem benchmark nem documentação).
- **Provável acima de 26 semanas**: a régua ainda não foi calibrada para projetos grandes (Projetos E e F, de 34 e 38 semanas, não têm ficha técnica). Dimensionar mesmo assim, marcar ⚠️ e sugerir quebrar em fases.
- Dependência de dados de bases soltas → chamar o núcleo de Dados.
- Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.
- Divergência entre o que o CN declarou e o que aparece na PRD, nos documentos ou na transcrição.
- Lacuna dentro da PRD (módulo sem superfície, integração sem meio, termo como "tempo real" sem mecanismo): a PRD precisa de revisão antes de virar anexo de contrato.
- Teto de fase atingido.

## Formato da resposta (sempre este, nesta ordem)

Público: um CN que talvez nunca tenha programado. Frases curtas. Todo termo técnico é explicado na primeira vez que aparece (ex.: "multitenancy (um mesmo sistema atendendo várias empresas com os dados separados)").

**Título:** `# Projeto [nome do cliente ou produto]`

**Status** (uma linha):
- ✅ Pronto para proposta
- ⚠️ Precisa de revisão da área de projetos (inclui toda estimativa sem PRD: "⚠️ Estimativa preliminar, sem PRD")
- 🚩 Parado (restrição técnica ou possível inviabilidade)

**1. Prazo em uma frase.** Ex.: *"Recomendado vender 18 semanas (9 sprints), mais as semanas off. Não vender abaixo de 13."*

**2. Faixa de semanas**

| Cenário | Semanas | Sprints | Quando acontece |
|---|---|---|---|
| Otimista (piso) | | | Escopo congelado, cliente responde rápido |
| **Provável (recomendado)** | | | O que costuma acontecer no NTec |
| Conservador (teto de risco) | | | Se os riscos da seção 4 se confirmarem |

**3. Resumo do projeto**, em 2 ou 3 linhas: o que é, formato(s), perfis de usuário, fluxos críticos (com PRD: os módulos) e o que tem de especial.

**4. Pontos de atenção**, do mais grave para o menos grave. Cada um com o que fazer. Toda integração com sistema do cliente traz aqui a **cláusula de contrato** pronta de `regua-dimensionamento.md` ("depende de o cliente fornecer acesso à API até a sprint {n}; sem acesso, vira planilha, sem alteração de prazo").

**5. Lacunas para o CN**: o que não estava na PRD nem na transcrição do Fathom. Uma linha por lacuna, nesta tabela:

| Fator | Procurado no Fathom e não achado | Pergunta para o cliente | Valor provisório na conta |
|---|---|---|---|

O que foi achado no Fathom **não** entra aqui: vai para o detalhamento com a origem (`Fathom · data — "trecho"`). Sem lacunas: `Sem lacunas: tudo veio da PRD e do Fathom.`

**6. Detalhamento por fase**: a tabela F1 a F6 (mín / central / máx) com o critério usado em cada linha (ex.: "F2: 3 perfis com poucas diferenças → 2 a 6 com poucas diferenças"). Com PRD, citar a seção (ex.: "F3: módulos 2.2 a 2.5 = 4 fluxos comuns; 2.4 tem concorrência → RN específica").

**7. Precedente**: o projeto do NTec mais parecido, com o prazo dele e por que é comparável (ou "sem precedente comparável").

**8. O que cortar**: 2 a 4 cortes concretos com a economia estimada em semanas (ex.: "publicar como PWA em vez de app nas lojas: −3 semanas"). Sempre presente, mesmo quando o prazo cabe. Se houver integração com sistema do cliente, um dos cortes é sempre o plano B: trocá-la por importação ou exportação de planilha.

**9. Bloco para colar no Dimensionamento Tec** (seção 7 do formulário; a seção 8, de buffer, fica em branco porque a régua não usa buffer):
```
7. Baseline: Imersão/setup X sem · Acesso/login X sem · Desenvolvimento X sem · Testes com cliente X sem · Deploy X sem · Lojas X sem
Faixa: otimista X · provável X · conservador X semanas (+ N semanas off)
```

**10. Observações**
- *Suposições:* tudo que a skill decidiu sem resposta explícita (inclui o valor provisório de cada lacuna). É o que a área de projetos mais precisa conferir.
- *Ajustes de fronteira:* os comentários de duas linhas de `regra-fronteira-e-faixa.md`, ou `Sem ajustes de fronteira.`
- *Pontos para a imersão:* os do bloco da PRD, um por linha. Não somam prazo: viram atividades da imersão (F1). Sem o bloco, `Não informados.`

## Status da skill

Versão inicial (16/10/2026). Entrada padrão passou a ser a PRD em 16/10/2026. Integrações com peso fixo, sem perguntar ao CN, desde 17/10/2026. Sem buffer percentual nem negociação de prazo desde 17/10/2026. O que a PRD não responde vem da transcrição do Fathom, e o que faltar volta ao CN como lacuna, desde 17/10/2026. Calibrada com Projeto A, Projeto D, Projeto C e Projeto B, que são anteriores ao formato de PRD: a contagem "1 módulo = 1 fluxo" ainda não foi conferida contra um projeto real com PRD. Pendente: (1) fichas técnicas de Projetos E e F para calibrar projetos grandes; (2) conteúdo da subpágina "Régua de Dimensionamento" do Notion, que não veio no PDF; (3) atualizar a calibração quando Projeto B e Projeto D terminarem.
