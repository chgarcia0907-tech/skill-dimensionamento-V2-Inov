# Skill de Dimensionamento — NTec

Skill do Claude que ajuda coordenadores de negócios (CNs) do Núcleo de Tecnologia a chegar a uma **faixa de semanas** realista (otimista / provável / conservador) antes de mandar a proposta para a área de projetos. A arquitetura segue a skill de dimensionamento do NCiv (Gabrielle Lobo, [repositório](https://github.com/gabriellelobo-pj/skill-dimensionamento)). A régua segue o formulário *Dimensionamento Tec* e foi calibrada nos projetos reais do NTec.

**Entrada padrão: a PRD.** A skill roda logo depois da `documento-requisitos-ntec` ([repositório do Augustus](https://github.com/rivasaugustus/documento-requisitos-ntec)), que gera o documento de requisitos "[Requisitos] {projeto}". Esta skill ocupa o lugar que a skill da PRD chama de `validacao-tecnica-ntec`, mas calcula só o prazo, sem preço. Sem PRD, ela dimensiona mesmo assim, e o resultado sai como ⚠️ estimativa preliminar.

> **Retomando em outra conversa?** Leia a seção [Contexto para retomar](#contexto-para-retomar) no fim deste arquivo.

## Estrutura

```
skill-dimensionamento-ntec/
├── README.md                       ← este arquivo
├── docs/
│   ├── Dimensionamento-NTec-Skill.pdf   ← PDF explicativo (8 páginas, visual do Dimensionamento Tec)
│   └── gerar_pdf.py                     ← gera o PDF (reportlab + fontes Segoe UI do Windows)
└── .claude/skills/dimensionamento-ntec/
    ├── SKILL.md                    ← orquestrador: procedimento, guardrails, formato da resposta
    ├── leitura-prd.md              ← entrada padrão: onde está cada fator na PRD + o que perguntar ao CN
    ├── insumos-e-perguntas.md      ← caminho sem PRD (formulário, ficha, transcrição) + vocabulário
    ├── regua-dimensionamento.md    ← pesos por fase (F1 a F6), buffer, faixa final, calibração, fontes
    ├── regra-fronteira-e-faixa.md  ← desempate entre linhas + o que fazer quando o cliente quer menos prazo
    ├── scripts/calcular_faixa.py   ← faz a conta (fonte da verdade dos pesos)
    └── exemplos/                   ← precedentes (.md + .json): Projeto A, Projeto B, Projeto C, Projeto D,
                                      Projetos E e F (pendente), PetAgenda (fictício, resposta completa)
                                      e PetAgenda via PRD (fictício, leitura da PRD)
```

**Projetos anonimizados.** Os precedentes reais do NTec aparecem como Projeto A a F, só com o tipo de produto e os fatores da régua. Quem é cada um, as fichas originais e os links internos ficam numa pasta `privado/` que não vai para o repositório.

## Como usar

- **Instalada em:** `~\.claude\skills\dimensionamento-ntec\` (pasta pessoal; vale em qualquer projeto do Claude Code).
- **Chamar:** `/dimensionamento-ntec`, ou pedir "dimensiona esse projeto" mandando o PDF da PRD (e, se tiver, o bloco "Inventário para dimensionamento"). Sem PRD, aceita o formulário, a ficha ou a transcrição, mas a estimativa sai como preliminar.
- **claude.ai:** compactar a pasta `dimensionamento-ntec` em .zip e enviar em *Settings → Capabilities → Skills*.
- **Rodar a conta direto:**
  ```bash
  python .claude/skills/dimensionamento-ntec/scripts/calcular_faixa.py .claude/skills/dimensionamento-ntec/exemplos/projeto-a.json
  ```
- **Regerar o PDF:**
  ```bash
  python docs/gerar_pdf.py docs/Dimensionamento-NTec-Skill.pdf
  ```

**Instalar a partir do GitHub:** clonar o repositório e copiar a pasta `.claude/skills/dimensionamento-ntec` para `~/.claude/skills/`.

**Atenção:** esta pasta é a cópia de trabalho. A cópia instalada em `~/.claude/skills` **não se atualiza sozinha**: depois de editar aqui, copiar de novo para lá.

---

## Contexto para retomar

Resumo da conversa que criou a skill (16/10/2026), para continuar sem precisar do histórico.

### O que foi pedido
Criar, para o NTec, uma skill parecida com a do NCiv da Gabi Lobo, que leve em conta que somos uma **empresa júnior**, use os dados reais dos projetos e chegue a uma **faixa de semanas**. O uso deve ser **prático para CNs**, que em geral são fracos tecnicamente e mandam para a equipe de projetos prazos sem sentido.

### Insumos usados
1. **Skill do NCiv** (GitHub da Gabi): 4 arquivos Markdown. SKILL.md orquestra, os outros 3 trazem as regras (faixas por disciplina, regra de fronteira, leitura do Drive).
2. **Formulário "Dimensionamento Tec"** (`~\Downloads\dimensionamento.pdf`, 5 páginas): seções 1–10. O Baseline (seção 7) tem as fases de 1 a 4 semanas cada e lojas de 2 a 6. O perfil da demanda (seção 6) traz formato, níveis de acesso, multitenancy, integrações, dados e offline. A seção 8 é o buffer adaptável. A subpágina **"Régua de Dimensionamento"** do Notion é citada, mas **não veio no PDF**.
3. **Levantamento do Notion** (colado no chat, **cortado no meio do Projeto D**). Trouxe o inventário de 6 projetos e as fichas completas de Projeto C, Projeto A e Projeto B.

### Decisões tomadas
- **Modelo:** fases F1–F6 do formulário, cada fator com mínimo / central / máximo. Faixa: otimista = soma dos mínimos; provável = soma dos centrais × (1 + buffer); conservador = soma dos máximos × (1 + buffer). A venda recomendada é o provável arredondado para sprints inteiras (2 semanas), mais as semanas off.
- **Os pesos já embutem o "time júnior"** (3 a 4 h/dia, template NTec). O buffer é só para risco extra: time novato +10%, troca de membros +10 a 20%, terceiros +10%, 3 ou mais integrações +10%. Teto de 30%.
- **Fronteira: sempre para o lado mais pesado.** O histórico do NTec é vender para menos (Projeto C).
- **Atípico ≠ regra de negócio específica**, para não contar o mesmo motivo duas vezes (erro achado na calibração do Projeto C).
- **Cliente pede menos que o piso → negociar escopo, não prazo.** A resposta sempre traz a seção "O que cortar".
- **Template NTec** (Google login, e-mail, S3) não soma prazo. Painel admin no mesmo código web não conta como formato extra.
- **Script Python como fonte da verdade** dos pesos, para o Claude não somar de cabeça. Se mudar um peso, mudar no script **e** na régua.

### Calibração atual
| Projeto | Faixa da régua (otim. / prov. / cons.) | Vendido | Situação |
|---|---|---|---|
| Projeto A | 9 / 12 / 16 | 12 | No prazo ✅ |
| Projeto D | 13 / 17 → vender 18 / 23 | 18 | Sem atraso ✅ (fatores com palpite) |
| Projeto C | 13 / 18 / 23 | 11 | Atrasou (~14). Régua ~3 semanas acima do real (viés conhecido) |
| Projeto B | 11 / 15 → vender 16 / 23 | 12 | Em execução; fim previsto em 23/11/2026 |
| Projetos E e F | não calibrado | 34 / 38 | Sem ficha. Alerta automático acima de 26 semanas |

### PRD como entrada padrão (16/10/2026, segunda conversa)
- A PRD da skill `documento-requisitos-ntec` é a entrada padrão. A skill lê o PDF e, se o CN colar, o bloco "Inventário para dimensionamento". Se o bloco não vier, monta o inventário a partir do PDF.
- **Sem PRD:** dimensiona, mas marca ⚠️ "Estimativa preliminar, sem PRD".
- **O que a PRD não cobre** (documentação das APIs, disponibilidade do cliente, riscos do time, stack e infra, benchmark, data de início): uma rodada curta de perguntas ao CN.
- **1 módulo = 1 fluxo.** 2.1 Autenticação vai para F2, e Disponibilização vai para F5 e F6.
- **Fatores de complexidade da PRD encaixam nas linhas atuais**, sem peso novo. Pagamento, IA e push viram integração. Concorrência, imutabilidade e rotina agendada fazem o módulo virar RN específica. Tempo real por push e relatório configurável viram feature atípica. A tabela completa está em `leitura-prd.md`.
- **Calibração:** os projetos antigos não têm PRD, então essas regras ainda não foram conferidas contra um projeto real.
- **Pendente:** avisar o Augustus para trocar `validacao-tecnica-ntec` por `dimensionamento-ntec` na skill da PRD, e lembrar que a nossa não calcula preço.

### Pendências (próximos passos)
1. **Mandar o resto do levantamento** (Projeto D completo, Projetos E, F) para calibrar os projetos grandes e tirar os palpites do Projeto D.
2. **Conseguir a subpágina "Régua de Dimensionamento"** do Notion. Se tiver números, eles valem mais que os da skill.
3. **Atualizar a calibração** quando o Projeto A (19/10/2026) e o Projeto B e o Projeto D (23/11/2026) terminarem. O passo a passo está em `exemplos/README.md`.
4. **Conferir as regras de leitura da PRD** no primeiro projeto com PRD que terminar (principalmente "rotina agendada → RN específica").
5. Atualizar `docs/gerar_pdf.py` e o PDF explicativo para mostrar a PRD como entrada.
6. Opcional: subir esta pasta para o GitHub (como o repositório da Gabi) e testar a skill com um CN num lead real.

### Onde está cada coisa
| O quê | Caminho |
|---|---|
| Cópia de trabalho (esta pasta) | `~\OneDrive\Área de Trabalho\Projetos\skill-dimensionamento-ntec\` |
| Skill instalada | `~\.claude\skills\dimensionamento-ntec\` |
| PDF | `docs\Dimensionamento-NTec-Skill.pdf` (cópia também em `~\Downloads\`) |
| Formulário original | `~\Downloads\dimensionamento.pdf` |
