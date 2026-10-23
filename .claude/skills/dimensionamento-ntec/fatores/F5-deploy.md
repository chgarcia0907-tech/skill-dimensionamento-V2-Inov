# F5 — Deploy

**Baseline do formulário:** 1 a 4 semanas. **Sem teto definido** (🔎 Proposta: usar 4, como F1, F2 e F4).

| Item | Mín | Central | Máx |
|---|---|---|---|
| 5.1 Tem web ou PWA (infra do NTec, ex.: Vercel) | 0,5 | 0,5 | 1 |
| 5.2 Tem app nativo, sem web | 0,5 | 0,5 | 1 |
| 5.3 Tem app nativo junto com web | +0 | +0,5 | +0,5 |
| 5.4 Infra do cliente | +1 | +1 | +2 |

Os itens 5.1 a 5.3 saem direto do formato (`F3-desenvolvimento.md`, item 3.2). Não há pergunta.

**Deploy primeiro** (23/10/2026): o deploy é **a primeira coisa depois da imersão**, no começo da sprint seguinte, para cobrir cedo uma etapa complexa. Não ocupa uma sprint dedicada: o resto da sprint já é desenvolvimento. Na precificação, só as semanas centrais do F5 são cobradas com 1 analista (`proposta-tecnica.md`, *Precificação*). Os **testes de deploy** ficam no F4 e são cobrados com 2 analistas.

**Deploys parciais** (✅ Reunião 20/10): depois do deploy inicial, o time publica versões parciais a cada sprint. Por isso o F5 é curto: ele cobre o deploy inicial, domínio e ajustes de produção.

**Publicação nas lojas não é F5:** é F6.

---

## 5.4 Infra do cliente

É `true` se **qualquer** pergunta for sim:

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| A conta de nuvem ou o servidor onde o sistema vai rodar é **do cliente**? | Calls ("nossos servidores", "a nossa TI hospeda") | `false` se o cliente é pessoa física ou não tem TI própria. Empresa com TI e ninguém falou → lacuna: "O sistema vai ficar nos servidores ou na nuvem do cliente?" |
| A TI do cliente precisa **aprovar cada publicação**, ou exige um pipeline de deploy próprio? | Calls | Idem |

Infra do cliente **sem acesso do time do NTec** para publicar e corrigir → **F0** (rejeitado).

**Alerta:** pedir os acessos e as regras de deploy do cliente **já na imersão**.
