# Skill de Dimensionamento — NTec

Skill do Claude que ajuda coordenadores de negócios (CNs) do Núcleo de Tecnologia a chegar a uma **faixa de semanas** realista (otimista / provável / conservador) antes de mandar a proposta para a área de projetos. A arquitetura segue a skill de dimensionamento do NCiv (Gabrielle Lobo, [repositório](https://github.com/gabriellelobo-pj/skill-dimensionamento)). A régua segue o formulário *Dimensionamento Tec* e foi calibrada nos projetos reais do NTec.

**Entrada padrão: a PRD.** A skill roda logo depois da `documento-requisitos-ntec` ([repositório do Augustus](https://github.com/rivasaugustus/documento-requisitos-ntec)), que gera o documento de requisitos "[Requisitos] {projeto}". Esta skill ocupa o lugar que a skill da PRD chama de `validacao-tecnica-ntec`, mas calcula só o prazo, sem preço. Sem PRD, ela dimensiona mesmo assim, e o resultado sai como ⚠️ estimativa preliminar.

> **Retomando em outra conversa?** Leia a seção [Contexto para retomar](#contexto-para-retomar) no fim deste arquivo.

## Estrutura

```
skill-dimensionamento-ntec/
├── README.md                       ← este arquivo
├── docs/
│   ├── Dimensionamento-NTec-Skill.pdf   ← PDF explicativo (9 páginas, visual do Dimensionamento Tec)
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

Resumo das conversas que criaram e evoluíram a skill (16 e 17/10/2026), para continuar em outra conversa sem precisar do histórico. **Comece por "Onde paramos".**

### Onde paramos (17/10/2026)
- **Em discussão, nada implementado ainda:** como dimensionar integrações **sem** o CN informar a documentação das APIs. O CN não tem como saber isso, e **não há técnico disponível** para validar. Ver a proposta em [Integrações sem o CN informar a documentação](#integrações-sem-o-cn-informar-a-documentação-proposta-pendente).
- **Próximo passo:** o usuário decide se implementa a proposta. Se sim, a lista de arquivos a mexer está no fim da seção da proposta.
- **Como trabalhar com o usuário:** quando faltar informação ou houver decisão a tomar, **perguntar antes de assumir**, com uma opção recomendada.

### Linha do tempo
| Data | O que foi feito |
|---|---|
| 16/10/2026 | Criação da skill (v1) a partir da skill do NCiv, do formulário Dimensionamento Tec e do levantamento do Notion; calibração com 4 projetos |
| 16/10/2026 | A PRD da skill `documento-requisitos-ntec` virou a entrada padrão (`leitura-prd.md`) |
| 16/10/2026 | Projetos anonimizados (Projeto A a F) e repositório publicado (público) no GitHub |
| 16/10/2026 | PDF explicativo v2 (9 páginas), já com a PRD |
| 17/10/2026 | Explicação de onde vem o "Inventário para dimensionamento"; discussão sobre integrações sem documentação |

### O que foi pedido (origem)
Criar, para o NTec, uma skill parecida com a do NCiv da Gabi Lobo, que leve em conta que somos uma **empresa júnior**, use os dados reais dos projetos e chegue a uma **faixa de semanas**. O uso deve ser **prático para CNs**, que em geral são fracos tecnicamente e mandam para a equipe de projetos prazos sem sentido.

### Insumos usados
1. **Skill do NCiv** (GitHub da Gabi): 4 arquivos Markdown. SKILL.md orquestra, os outros 3 trazem as regras (faixas por disciplina, regra de fronteira, leitura do Drive).
2. **Formulário "Dimensionamento Tec"** (`~\Downloads\dimensionamento.pdf`, 5 páginas): seções 1–10. O Baseline (seção 7) tem as fases de 1 a 4 semanas cada e lojas de 2 a 6. O perfil da demanda (seção 6) traz formato, níveis de acesso, multitenancy, integrações, dados e offline. A seção 8 é o buffer adaptável. A subpágina **"Régua de Dimensionamento"** do Notion é citada, mas **não veio no PDF**.
3. **Levantamento do Notion** (colado no chat, **cortado no meio do Projeto D**). Trouxe o inventário de 6 projetos e as fichas completas de Projeto C, Projeto A e Projeto B.
4. **Skill da PRD** (`documento-requisitos-ntec`, [repositório do Augustus](https://github.com/rivasaugustus/documento-requisitos-ntec)): gera o documento de requisitos "[Requisitos] {projeto}" a partir das reuniões (Fathom, Granola, transcrições). Template: Visão Geral, Requisitos Funcionais por módulo (A(cli)D/SID, Superfície, integrações com sentido, dados e meio), Não Funcionais e Exclusões Explícitas.

### Decisões tomadas
**Régua (v1)**
- **Modelo:** fases F1–F6 do formulário, cada fator com mínimo / central / máximo. Faixa: otimista = soma dos mínimos; provável = soma dos centrais × (1 + buffer); conservador = soma dos máximos × (1 + buffer). A venda recomendada é o provável arredondado para sprints inteiras (2 semanas), mais as semanas off.
- **Os pesos já embutem o "time júnior"** (3 a 4 h/dia, template NTec). O buffer é só para risco extra: time novato +10%, troca de membros +10 a 20%, terceiros +10%, 3 ou mais integrações +10%. Teto de 30%.
- **Fronteira: sempre para o lado mais pesado.** O histórico do NTec é vender para menos (Projeto C).
- **Atípico ≠ regra de negócio específica**, para não contar o mesmo motivo duas vezes (erro achado na calibração do Projeto C).
- **Cliente pede menos que o piso → negociar escopo, não prazo.** A resposta sempre traz a seção "O que cortar".
- **Template NTec** (Google login, e-mail, S3) não soma prazo. Painel admin no mesmo código web não conta como formato extra.
- **Script Python como fonte da verdade** dos pesos, para o Claude não somar de cabeça. Se mudar um peso, mudar no script **e** na régua.

**PRD como entrada padrão**
- A skill lê o PDF da PRD e, se o CN colar, o bloco "Inventário para dimensionamento". Sem o bloco, monta o inventário a partir do PDF.
- **Sem PRD:** dimensiona, mas marca ⚠️ "Estimativa preliminar, sem PRD".
- **O que a PRD não cobre** (documentação das APIs, disponibilidade do cliente, riscos do time, stack e infra, benchmark, data de início): uma rodada curta de perguntas ao CN. *A parte das APIs está em revisão (ver "Onde paramos").*
- **1 módulo = 1 fluxo.** 2.1 Autenticação vai para F2, e Disponibilização vai para F5 e F6.
- **Fatores de complexidade da PRD encaixam nas linhas atuais**, sem peso novo. Pagamento, IA e push viram integração. Concorrência, imutabilidade e rotina agendada fazem o módulo virar RN específica. Tempo real por push e relatório configurável viram feature atípica. Tabela completa em `leitura-prd.md`.
- **Papel da skill:** ocupa o lugar que a skill da PRD chama de `validacao-tecnica-ntec`, mas calcula **só o prazo, sem preço**.

**Publicação**
- Repositório **público**: https://github.com/matheusrpgomes-sketch/skill-dimensionamento-ntec
- **Projetos reais anonimizados** como Projeto A a F. Nome real, fichas originais e links do Notion ficam em `privado/` (no `.gitignore`, só no computador local; o mapa está em `privado/mapa-projetos.md`). **Nunca** subir nome de cliente, link do Notion ou detalhe que identifique o projeto.

### De onde vem o "Inventário para dimensionamento"
É gerado pela skill da PRD, mas **não fica no PDF**: aparece só na resposta dela no chat (Passo 7), junto com Perfis, Funcionalidades, Integrações e Pontos para a imersão. Colunas fixas: `Módulo | Superfície | Itens A(cli)D | Itens SID | Integrações | Fluxos de dados | Fatores de complexidade`. O CN copia esse bloco e manda junto com o PDF; se esquecer, a nossa skill reconstrói o inventário a partir do PDF (só os "Pontos para a imersão" se perdem). Ideia para pedir ao Augustus: a skill da PRD salvar o inventário num arquivo ao lado do PDF.

### Integrações sem o CN informar a documentação (proposta pendente)
**Problema:** hoje `leitura-prd.md` (Passo 4) pede ao CN o link da documentação de cada API. O CN não sabe, e não há técnico para validar.

**Proposta (a skill faz a avaliação técnica sozinha):**
1. **Catálogo de integrações conhecidas** (`catalogo-integracoes.md`): Mercado Pago, Stripe, Pix, Google Maps, Mapbox, push (Expo/FCM), WhatsApp Business, OpenAI, Claude, emissores de NF-e, Google Calendar etc., já classificados (sentido típico, documentação pública, linha da régua). A PRD diz qual é o sistema, e a skill classifica sem perguntar.
2. **Pesquisa automática:** sistema fora do catálogo → a skill busca na web a documentação do fornecedor, lê e classifica (tem API pública? qual sentido? tem sandbox?), citando o link como evidência. Depende de a busca na web estar ligada (no Claude Code costuma estar; no claude.ai depende da conta da PJ).
3. **Sistema feito sob medida para o cliente:** a skill entrega ao CN uma **mensagem pronta para o cliente repassar ao TI ou ao fornecedor dele** ("tem API? tem documentação? exporta planilha?"). O CN só encaminha e cola a resposta; se vier link ou PDF, a skill lê sozinha.
4. **Sem resposta:** peso mais pesado (sem documentação) + **cláusula de contrato** sugerida ("a integração depende do acesso à API fornecido pelo cliente; sem acesso, vira importação por planilha") + o plano B (planilha) em "O que cortar", com a economia em semanas.
5. *Opcional, mexe no script:* categoria "a confirmar" = mínimo da linha com documentação + central e máximo da linha sem documentação (abre a faixa sem inflar o piso; os pesos já existem).

**Arquivos a mexer se aprovado:** novo `catalogo-integracoes.md`; `leitura-prd.md` (Passos 2 e 4); `insumos-e-perguntas.md` (pergunta de integrações); `SKILL.md` (procedimento e formato da resposta: mensagem para o cliente e cláusula); `regra-fronteira-e-faixa.md` (fronteira 4 "integração documentada ou não?"); `regua-dimensionamento.md` (registro das fontes); se fizer o item 5, `scripts/calcular_faixa.py` + régua; depois regerar o PDF, copiar para `~/.claude/skills/` e dar push.

### Calibração atual
| Projeto | Faixa da régua (otim. / prov. / cons.) | Vendido | Situação |
|---|---|---|---|
| Projeto A | 9 / 12 / 16 | 12 | No prazo ✅ |
| Projeto D | 13 / 17 → vender 18 / 23 | 18 | Sem atraso ✅ (fatores com palpite) |
| Projeto C | 13 / 18 / 23 | 11 | Atrasou (~14). Régua ~3 semanas acima do real (viés conhecido) |
| Projeto B | 11 / 15 → vender 16 / 23 | 12 | Em execução; fim previsto em 23/11/2026 |
| Projetos E e F | não calibrado | 34 / 38 | Sem ficha. Alerta automático acima de 26 semanas |

Todos são **anteriores à PRD**: as regras de leitura da PRD ainda não foram conferidas contra um projeto real.

### Pendências (próximos passos)
1. **Decidir e implementar a proposta de integrações** (seção acima).
2. **Avisar o Augustus:** trocar `validacao-tecnica-ntec` por `dimensionamento-ntec` na skill da PRD (a nossa não calcula preço) e, se possível, salvar o inventário num arquivo.
3. **Mandar o resto do levantamento** (Projeto D completo, Projetos E e F) para calibrar os projetos grandes e tirar os palpites do Projeto D.
4. **Conseguir a subpágina "Régua de Dimensionamento"** do Notion. Se tiver números, eles valem mais que os da skill.
5. **Atualizar a calibração** quando o Projeto A (19/10/2026) e os Projetos B e D (23/11/2026) terminarem. Passo a passo em `exemplos/README.md`; atualizar também a ficha original em `privado/`.
6. **Conferir as regras de leitura da PRD** no primeiro projeto com PRD que terminar (principalmente "rotina agendada → RN específica").
7. Testar a skill com um CN num lead real.

Feito: PDF v2 com a PRD; publicação no GitHub com projetos anonimizados.

### Onde está cada coisa
| O quê | Caminho |
|---|---|
| Cópia de trabalho (esta pasta, repositório git) | `~\OneDrive\Área de Trabalho\Projetos\skill-dimensionamento-ntec\` |
| Repositório no GitHub (público) | https://github.com/matheusrpgomes-sketch/skill-dimensionamento-ntec |
| Skill instalada (não sincroniza sozinha) | `~\.claude\skills\dimensionamento-ntec\` |
| Mapa dos projetos reais (fora do git) | `privado\mapa-projetos.md` e `privado\exemplos-originais\` |
| PDF | `docs\Dimensionamento-NTec-Skill.pdf` (cópia também em `~\Downloads\`) |
| Formulário original | `~\Downloads\dimensionamento.pdf` |
| Skill da PRD (Augustus) | https://github.com/rivasaugustus/documento-requisitos-ntec |

**Fluxo de atualização:** editar nesta pasta → rodar os exemplos com o script se mexeu em peso → copiar `.claude/skills/dimensionamento-ntec` para `~/.claude/skills/` → commit e push.
