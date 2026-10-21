# F2 — Infra, níveis de acesso, cadastro e login

**Baseline do formulário:** 1 a 4 semanas. **Teto de referência:** 4 (ver ⏳ **D4**).

✅ **Reunião 20/10:** níveis de acesso (casos básicos) e multitenancy ficam em **tabelas separadas**, cada linha com um discriminante claro. O F2 é a soma de **F2a + F2b**.

✅ **Reunião 20/10:** o fator Claude Code (×0,7 / ×0,85 / ×1 no F2) foi **removido**. Os valores abaixo já são os finais, sem multiplicador.

**O que o template já entrega (0 semanas):** login por e-mail e senha, recuperação de senha, login com Google e painel admin básico.

---

## F2a — Níveis de acesso

### Passo 1: contar os perfis

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Quantos perfis a seção 2.1 da PRD lista? (admin conta) | PRD 2.1 | Lacuna. Usar a linha "2 a 5 com grandes diferenças" |

### Passo 2: o teste de "grandes diferenças" (só para 2 a 5 perfis)

É **grandes diferenças** se **qualquer** pergunta for sim. Se todas forem não, é **poucas diferenças**.

| # | Pergunta | Onde ler | Sem resposta |
|---|---|---|---|
| a | Algum perfil abre uma **tela exclusiva** (tela ou rota que pelo menos um outro perfil não abre)? O **painel admin básico** do template não conta (ver glossário) | PRD 2.1 e linha **Superfície** de cada módulo | Sim |
| b | Algum perfil tem **status de cadastro** (pendente, aprovado, rejeitado) que bloqueia o acesso até alguém aprovar? | PRD 2.1 e RNs | Sim |
| c | Algum perfil só vê os **próprios registros** (filtro por dono)? | PRD 2.1 e RNs dos módulos | Sim |

**Exemplos:**
- Admin e usuário, em que o admin só vê um item a mais no menu que leva a uma tela que o usuário também abre → poucas.
- Admin e usuário, em que o admin só gerencia usuários e edita os registros dos usuários (painel admin básico) → poucas.
- Admin e usuário, em que o admin abre um dashboard de relatórios que o usuário não abre → grandes (a).
- Nutricionista com cadastro pendente que bloqueia rotas → grandes (b).
- Paciente só vê o próprio diário → grandes (c).

### Tabela F2a

| Linha | Mín | Central | Máx |
|---|---|---|---|
| Nenhum (sem login, sem backend) | 0 | 0 | 0 |
| 1 perfil | 0,5 | 0,5 | 1 |
| 2 a 5, poucas diferenças | 0,5 | 1 | 1,5 |
| 2 a 5, grandes diferenças ⏳ **D2** | 1,5 | 2 | 2,5 |
| 6 ou mais | 2,5 | 3 | 4 |

> A faixa antiga era "2 a 6" e "6 ou mais", que valiam as duas para 6 perfis. Agora: **2 a 5** e **6 ou mais**.

> ⏳ **D2 — em aberto:** a reunião mandou **aumentar** o prazo de níveis de acesso complexos, sem dizer quanto. **Provisório:** valores atuais (1,5 / 2 / 2,5). 🔎 Sugestão: 2 / 2,5 / 3.

---

## F2b — Multitenancy

### O teste

Fazer as perguntas **na ordem**. A primeira que der sim decide a linha.

| # | Pergunta (pronta para o CN repassar ao cliente) | Onde ler | Se sim |
|---|---|---|---|
| 1 | "O sistema vai ser usado por mais de uma empresa, clínica, unidade ou filial, cada uma com os seus dados?" | Visão Geral, 2.1, RNs, 3.4 (termos: multiempresa, por unidade, por clínica, por filial) | Vai para a 2. Se **não**: linha "Não" |
| 2 | "Alguma empresa vai ter uma **regra** ou **funcionalidade** que funciona diferente das outras?" (Trocar logo ou cores, ou ligar e desligar features de uma lista fixa, **não** conta) | RNs, 3.4; Fathom | **F0** — parar e consultar |
| 3 | "Se a empresa A vir um dado da empresa B por causa de um erro, isso quebra o contrato ou a LGPD?" | 3.4; Fathom | **Isolado** |
| 4 | "Um administrador geral pode ver os dados de todas as empresas juntas?" | 2.1; Fathom | **Separado** |

**Sem resposta na 3 ou na 4:** **isolado** + lacuna para o CN com a pergunta 3.

### Tabela F2b

| Linha | O que significa | Mín | Central | Máx |
|---|---|---|---|---|
| Não | Uma empresa só | 0 | 0 | 0 |
| Separado | Um banco, filtro por tenant no código, admin geral vê tudo | +0,5 | +0,5 | +1 |
| Isolado ⏳ **D2** | Vazamento entre tenants quebra contrato ou LGPD; isolamento no banco (RLS, schema ou banco por tenant) | +1 | +1,5 | +2 |
| Instâncias | Código ou regra diferente por tenant | — vai para o **F0** — | | |

> ⏳ **D2 — em aberto:** a reunião mandou **aumentar** o prazo de isolamento de dados, sem dizer quanto. **Provisório:** valores atuais (1 / 1,5 / 2). 🔎 Sugestão: 1,5 / 2 / 3.

---

## Teto

> ⏳ **D4 — em aberto:** "6 ou mais" (4) + "isolado" (2) = 6 no máximo. Hoje o script corta para 4, e o isolamento some da conta. **Provisório:** manter a soma e marcar ⚠️ "F2 acima do teto de 4 semanas: revisar com a área de projetos". Não cortar.

## Origem na resposta

```
F2a: 4 perfis, grandes diferenças (origem: PRD 2.1 — veterinário abre "Prontuário", que a recepção não abre)
F2b: isolado (origem: Fathom · 12/03 — "cada clínica não pode nem sonhar em ver o dado da outra")
```
