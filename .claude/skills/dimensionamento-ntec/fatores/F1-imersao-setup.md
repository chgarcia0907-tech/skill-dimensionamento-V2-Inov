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

Antes, com PRD, este fator era sempre `false` e o alerta nunca disparava. Agora é `true` se **qualquer** pergunta abaixo for sim:

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Não há PRD gerada pela skill `documento-requisitos-ntec`? | Entrada da skill | — |
| Algum módulo da PRD não tem a linha **Superfície**, nem no próprio módulo nem no título da seção-mãe (ex.: "2.2 Fluxo do Consultor (Aplicativo Mobile)" vale para 2.2.1 a 2.2.5)? | Seção 2 | Sim |
| Alguma integração da PRD não tem **Sentido**, **Dados** ou **Meio**? | Itens SID | Sim |
| Algum fluxo de dados não tem **Origem**, **Processamento** ou **Destino**? | Seção 2 | Sim |
| Algum módulo marcado com fator de complexidade não tem a seção **Regras de Negócio**? | Seção 2 | Sim |

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
| O cliente exige uma tecnologia da lista aceita do F0 que **não é a do template** (ex.: Supabase ou Postgres no lugar de MongoDB)? | PRD 3.1; Fathom | `false`. Registrar a stack do template como premissa a validar na Sprint de Refino |

> ⏳ **D5 — em aberto:** a troca para Postgres obrigatória por causa do offline com sincronização conta aqui? **Provisório:** não conta.

**O CN não promete stack.** Se o cliente ouviu "vamos fazer em X", tratar como premissa a validar (aconteceu no Projeto B: Expo foi sugestão comercial).

## 1.4 Produto atípico

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Nenhum app ou site foi citado como referência para o **produto inteiro**? | Fathom ("tipo o…", "igual ao…", "vi um que…") | `true` + lacuna: "Existe algum app ou site parecido que a gente possa usar de referência?" |

**Não confundir:**
- Setor incomum com produto comum (agenda para criadores de abelhas) → `false`.
- Uma **feature** sem referência é F3 (feature atípica), não F1.
- Fórmula científica ou clínica é RN específica (F3), não atípico. Não marcar os dois pelo mesmo motivo.

---

## Teto

> ⏳ **D4 — em aberto:** a soma pode passar do teto (2,5 + 1 + 2 + 1 = 6,5 no máximo). Hoje o script corta para 4, e com isso a troca de stack quase não pesa. **Provisório:** manter a soma e marcar ⚠️ "F1 acima do teto de 4 semanas: revisar com a área de projetos". Não cortar.
