# F1 — Imersão, refinamento, setup e acessos

**Baseline do formulário:** 1 a 4 semanas. **Teto de referência:** 4 (ver ⏳ **D4**).

| Item | Mín | Central | Máx |
|---|---|---|---|
| 1.1 Base (sempre) | 1,5 | 2 | 2,5 |
| 1.2 Demanda pouco detalhada | +0,5 | +1 | +1 |
| 1.3 Troca de stack aceita no F0 | +1 | +1,5 | +2 |
| 1.4 Produto atípico | +0,5 | +0,5 | +1 |

> **Inconsistência a corrigir:** o formulário diz que o F1 vai de 1 a 4 semanas, mas a base mínima é 1,5. Ou o formulário passa a dizer 1,5 a 4, ou a base mínima vira 1. (🔎 Proposta: ajustar o texto do formulário para 1,5.)

---

## 1.1 Base

Sempre entra. Cobre imersão, Sprint de Refino, setup do monorepo e pedido de acessos.

## 1.2 Demanda pouco detalhada → alerta de discovery

✅ **Reunião 20/10:** quando a demanda estiver pouco detalhada, a skill emite um **alerta para o CN recomendando discovery** antes de seguir.

É `true` se **qualquer** pergunta abaixo for sim:

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Falta a transcrição da AT Aprof (só a AT Diag, só o resumo do Fathom, ou nenhuma call)? | Entrada da skill | — |
| Depois das duas calls, não dá para listar as jornadas do começo ao fim (quem entra, o que faz, com o que sai)? | Inventário (`leitura-transcricoes.md`, Passo 4) | Sim |
| O formato (app, web, PWA) não foi decidido? ("ainda não sei se é app ou site") | Calls | Sim |
| Alguma integração citada não tem o outro sistema identificado ou o sentido (envia, recebe, os dois)? | Calls | Sim |
| Alguma jornada depende de uma regra que o cliente **ainda não sabe descrever** ("vou pensar como seria o cálculo")? Documento que existe e só não foi enviado não conta: vai para *Pontos em aberto* | Calls | Sim |

**Quando for `true`:**
1. Soma a linha 1.2 na conta.
2. A resposta abre com:
   ```
   ⚠️ Demanda pouco detalhada — recomendamos uma fase de discovery antes da proposta.
   Faltam: {lista do que faltou acima}
   ```
3. O status nunca é ✅.

🔎 **Proposta:** oferecer a discovery como serviço pago (2 a 4 semanas), em vez de dimensionar com escopo vago.

## 1.3 Troca de stack aceita no F0

Stack que o cliente exige e está **fora** da lista do F0 já foi rejeitada. Aqui entra só a troca **aceita** que muda o template.

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| O cliente exige uma tecnologia da lista aceita do F0 que **não é a do template** (ex.: Supabase ou Postgres no lugar de MongoDB)? | Calls | `false`. Registrar a stack do template como premissa a validar na Sprint de Refino |

> ⏳ **D5 — em aberto:** a troca para Postgres obrigatória por causa do offline com sincronização conta aqui? **Provisório:** não conta.

**O CN não promete stack.** Se o cliente ouviu "vamos fazer em X", tratar como premissa a validar (aconteceu no Projeto B: Expo foi sugestão comercial).

## 1.4 Produto atípico

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Nenhum app ou site foi citado como referência para o **produto inteiro**? | Calls ("tipo o…", "igual ao…", "vi um que…", "as que eu já vi") | `true` + lacuna: "Existe algum app ou site parecido que a gente possa usar de referência?" |

**Não confundir:**
- Setor incomum com produto comum (agenda para criadores de abelhas) → `false`.
- Uma **feature** sem referência é F3 (feature atípica), não F1.
- Fórmula científica ou clínica é RN específica (F3), não atípico. Não marcar os dois pelo mesmo motivo.

---

## Teto

> ⏳ **D4 — em aberto:** a soma pode passar do teto (2,5 + 1 + 2 + 1 = 6,5 no máximo). Hoje o script corta para 4, e com isso a troca de stack quase não pesa. **Provisório:** manter a soma e marcar ⚠️ "F1 acima do teto de 4 semanas: revisar com a área de projetos". Não cortar.
