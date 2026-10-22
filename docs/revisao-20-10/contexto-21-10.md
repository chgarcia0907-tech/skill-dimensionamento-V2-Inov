# Contexto: revisão da skill de dimensionamento do NTec (Poli Júnior)

Atualizado em 21/10/2026. **Para o novo chat:** leia este arquivo inteiro antes de qualquer coisa. Depois leia os arquivos da seção "Acessos necessários".

---

## Acessos necessários

O novo chat precisa abrir a pasta **`C:\Users\chgar\Downloads\pastita`** como pasta de trabalho. Tudo o que foi produzido está nela.

| O quê | Onde | Para quê |
|---|---|---|
| Esta pasta | `C:\Users\chgar\Downloads\pastita` | Todo o trabalho feito (tabela abaixo) |
| Repositório da skill (público) | https://github.com/matheusrpgomes-sketch/skill-dimensionamento-ntec, commit `39875e8` | Versão original. Clonar num **caminho curto** (ex.: `C:\ntec\skill`), por causa do limite de 260 caracteres do Windows |
| Anotações da reunião de 20/10 | `C:\Users\chgar\Downloads\Validação Skill NTec - 2026_10_20 18_00 GMT-03_00 - Anotações do Gemini.md` | Fonte das decisões (resumo na seção 2) |
| Transcrição completa da reunião (opcional) | Google Docs, link dentro do arquivo de anotações. Exige o conector do Google Drive | Só se precisar de detalhe que não está nas anotações |
| Skill irmã da PRD (opcional) | https://github.com/rivasaugustus/documento-requisitos-ntec | Formato da PRD que alimenta esta skill |
| Python 3 + `pip install reportlab` | Na máquina | Rodar `calcular_faixa.py` e gerar o PDF da proposta (o reportlab ainda não está instalado) |

### Arquivos desta pasta

| Arquivo | O que é |
|---|---|
| `CONTEXTO.md` | Este arquivo |
| `analise-criterios-F0-F6.md` | Relatório do LLM Council: critérios mal definidos, fator a fator, e checklist das mudanças da reunião |
| `fatores/` | **Novos** arquivos da régua: `README.md` (índice, marcações, D1–D5), `glossario.md`, F0, F1, F2, F3 (desenvolvimento e integrações), F4, F5 e F6. Ainda não estão no repositório |
| `skill-alterada/scripts/` | `calcular_faixa.py` reescrito e `gerar_proposta.py` com um ajuste pequeno |
| `skill-alterada/exemplos/` | JSONs migrados para o formato novo. Os `.md` dos exemplos estão iguais ao original (desatualizados) |
| `alteracoes-skill.patch` | O mesmo que `skill-alterada/`, em formato de patch sobre o commit `39875e8` (versão v2, corrigida em 21/10). No clone: `git apply alteracoes-skill.patch` |
| `alteracoes-skill-v1.patch` | Primeira versão do patch, guardada só para comparação |
| `testes-comparativos.md` + `testes/` | Correções da v2 e casos hipotéticos H1–H8 rodados na original, na v1 e na v2 (script `testes/comparar.py`) |

**Repositório novo (público):** https://github.com/chgarcia0907-tech/skill-dimensionamento-ntec
- `main` = original (`39875e8`);
- `revisao-20-10` = commit `ed01191`, com o patch v2 e a pasta `fatores/` dentro da skill. PR aberto para revisão de Augusto e Frank: https://github.com/chgarcia0907-tech/skill-dimensionamento-ntec/pull/1

O `main` está protegido pelo ruleset "Proteger main": só muda via PR (0 aprovações por enquanto; subir para 1 quando Augusto e Frank forem colaboradores), sem force push e sem exclusão.

No clone `C:\ntec\skill`, `origin` aponta para o repo novo e `upstream` para o do Matheus.

---

## 1. O projeto

A skill fica em `.claude/skills/dimensionamento-ntec/` no repositório. Ela dimensiona projetos de software do NTec (sites, webapps, PWAs, apps) para coordenadores de negócios (CNs) sem formação técnica.
- **Entrada padrão:** a PRD (documento de requisitos).
- **Saída:** uma faixa de semanas e uma Proposta Técnica em PDF. A faixa tem três cenários:
  - otimista = soma dos mínimos;
  - provável = soma dos centrais (vende arredondado para sprints de 2 semanas);
  - conservador = soma dos máximos.

| Arquivo da skill | Função |
|---|---|
| `SKILL.md` | Procedimento |
| `regua-dimensionamento.md` | Pesos F1–F6 (versão antiga, a ser substituída por `fatores/`) |
| `leitura-prd.md` | Como a PRD vira cada fator |
| `regra-fronteira-e-faixa.md` | Desempate entre linhas |
| `insumos-e-perguntas.md` | Caminho sem PRD |
| `scripts/calcular_faixa.py` | A conta (fonte da verdade dos números) |
| `scripts/gerar_proposta.py` | Gera o PDF |
| `exemplos/` | Projetos A, B, C, D e PetAgenda (fictício), em `.md` + `.json` |

As fases são:
- **F1** imersão e setup;
- **F2** acesso, login e multitenancy;
- **F3** desenvolvimento: fluxos × fator de formato, mais integrações e extras;
- **F4** testes com o cliente;
- **F5** deploy;
- **F6** lojas.

O histórico do NTec é vender prazo para menos: o Projeto C foi vendido em 11 semanas e levou ~14.

## 2. Reunião de validação (20/10/2026)

Participantes: Augusto Cabral, Ricardo Rodrigues, Frank, Carlos Garcia e Matheus Padilha.

1. **F0.** Criar um F0 de exclusão:
   - stacks incompatíveis (.NET, Angular, COBOL, Delphi) são rejeitadas;
   - trocar MongoDB por Supabase é aceitável;
   - condições de contrato incompatíveis também rejeitam.
2. **F1.** Emitir um alerta ao comercial recomendando discovery quando a demanda for pouco detalhada. Ricardo apontou divergência nos tetos do F1.
3. **F2.** Separar níveis de acesso e multitenancy em tabelas distintas, com discriminantes claros. Aumentar os prazos de acesso complexo e de isolamento de dados.
4. **F3.**
   - Formato extra em código separado: "pelo menos 1,2" (antes era +0,1).
   - Integrações e fluxos viram tópicos separados.
   - Integração bidirecional com sistema do cliente: mínimo de 4 semanas.
   - Margem de segurança ("gordura") explícita.
   - Offline com sincronização não se vende com MongoDB; usar Postgres.
5. **Fator Claude Code.** Removido (era ×0,75 no núcleo do F3 e ×0,85 no F2).
6. **F4.** Aumentar o tempo de teste para RN crítica. Remover o fator "cliente com pouca disponibilidade".
7. **Arquivos e revisão.**
   - Um `.md` por fator (F0–F6), com revisão de Augusto e Frank.
   - Atualizar o README.
   - Remover o "efeito cloud" do PDF de metodologia.

Outros pontos da reunião: os deploys parciais na Vercel desde o início foram validados, e o prazo de desenvolvimento não inclui a publicação nas lojas.

## 3. O que foi feito

### A) Análise (`analise-criterios-F0-F6.md`)

Um LLM Council analisou a régua: 5 conselheiros, revisão cruzada anônima e síntese. A conclusão central é que toda ambiguidade caía na linha mais leve, por três caminhos:
1. o script usava valores padrão leves para campos ausentes;
2. os tetos de F1, F2 e F4 cortavam a soma (F1 6,5 → 4; F2 6 → 4), o que explica a divergência que o Ricardo viu;
3. o "meio-termo de 0,5" da regra de fronteira não existe no script.

Outros achados:
- no F2, as faixas "2 a 6" e "6+" se sobrepunham no 6;
- critérios definidos de forma diferente em arquivos diferentes;
- "1 módulo = 1 fluxo" ignora o tamanho do módulo;
- adjetivos vagos ("muito específica", "milhares", "sensível");
- o template usa MongoDB, mas offline com sync não pode usar MongoDB.

### B) Pasta `fatores/`

Cada critério segue o formato: **Pergunta (sim/não) · Onde ler na PRD · O que fazer sem resposta**. A linha mais leve só pode ser escolhida com citação da PRD ou do Fathom. O `glossario.md` prevalece sobre os outros arquivos.

Marcações:
- ✅ decidido na reunião;
- 🔎 proposta do council: se define um critério, já vale; se muda um peso, usa o valor atual até ser validada;
- ⏳ D1–D5: decisões em aberto.

Ajuste posterior: o **painel admin básico** do template não conta como tela exclusiva no F2. Esse painel cobre gerenciar usuários e ver ou editar os registros dos outros perfis. Dashboard, relatório, aprovação de cadastro e configuração de regra continuam contando.

### C) Script (`skill-alterada/scripts/calcular_faixa.py`)

**Entrada sem valor padrão.** Campo ausente, nome antigo ou campo removido geram `EntradaInvalida` e a conta sai com exit 2.

**F0, no bloco `"f0"` do JSON:**
- **rejeitam** (o projeto não é dimensionado): `stack_exigida_fora_da_lista`, `offline_sync_com_mongodb_exigido`, `sla_ou_sustentacao`, `infra_cliente_sem_acesso`;
- **param com 🚩** (o projeto é dimensionado, mas fica parado): `multa_por_atraso`, `sem_validador_nomeado`, `feature_sem_referencia_nem_doc`, `hardware` e `prazo_exigido_semanas` (número ou `null`) abaixo do otimista;
- multitenancy `instancias` e integração `sem_api` também viram 🚩.

**Mudanças na conta:**
- Teto: não corta mais a soma, só gera alerta (D4).
- Fator Claude Code e `cliente_pouca_disponibilidade`: removidos.
- `niveis_acesso`: `nenhum | 1 | 2-5-poucas | 2-5-grandes | 6+`.
- `formatos`: `web | pwa | app` (`webapp` removido).
- `F3_FORMATO_EXTRA = 0.2` (D1).
- `bi_sem_doc = (4, 4, 5)`.
- `F3_MARGEM = 0.0` (D3), com aviso na resposta.
- Novos alertas: discovery e Postgres para offline com sync.

**Em `gerar_proposta.py`:** mostra o erro de entrada de forma legível.

**Correções da v2 (21/10):**
- o F0 é avaliado antes do resto, então uma rejeição não exige preencher F1 a F6;
- projeto rejeitado não gera PDF;
- os avisos das decisões em aberto (D3, D5) foram para `avisos_internos`, que aparecem só no terminal;
- formato repetido e prazo ≤ 0 viram erro de entrada.

Detalhes em `testes-comparativos.md`. Clone de trabalho: `C:\ntec\skill`, branch `revisao-20-10`, sem commit.

**Venda recomendada (semanas), antes → depois:**

| Exemplo | Antes | Depois |
|---|---|---|
| Projeto A | 12 | 12 |
| Projeto B | 14 | 14 |
| Projeto C | 18 | 18 |
| Projeto D | 18 | 18 |
| PetAgenda | 20 | 20 |
| PetAgenda (PRD) | 20 | 22 |

A diferença vem do formato extra (agora ×1,4) e, no Projeto B, da saída do fator de disponibilidade. O "antes" já era sem Claude Code: os exemplos rodavam com `claude_code: false`.

Testes feitos, todos passaram:
- erro de entrada;
- rejeição no F0;
- 🚩 por prazo abaixo do otimista e por `sem_api`;
- teto de F1 e F2 mantido, com alerta;
- lacuna do Fathom.

## 4. Decisões em aberto (valor provisório em uso)

| # | Decisão | Provisório | Sugestão |
|---|---|---|---|
| D1 | Formato extra "pelo menos 1,2": +0,2 por formato (app+web = ×1,4) ou ×1,2 sobre o fator (×1,44)? | +0,2 | — |
| D2 | Números novos para: "2–5 grandes diferenças" (1,5/2/2,5), "isolado" (1/1,5/2), "RN crítica" no F4 (0,5/0,5/1), central/máx do `bi_sem_doc` (mínimo 4 já decidido) | Atuais; `bi_sem_doc` 4/4/5 | 2/2,5/3 · 1,5/2/3 · 1/1/1,5 · 4/4,5/5,5 |
| D3 | Margem de segurança: % sobre o F3, sobre o total, ou embutida? Quanto? | 0 + aviso | +10–15% no F3 |
| D4 | Teto atingido: manter a soma + ⚠️ ou parar? | Manter + ⚠️ | — |
| D5 | Sync que obriga Postgres soma como "stack fora do template" no F1? | Não soma | — |

**Propostas 🔎 a validar com Augusto e Frank:**
- lista de stacks aceitas;
- condições de contrato do F0;
- fluxo = módulo com até 8 itens A(cli)D;
- volume alto = 1.000 ou mais usuários simultâneos;
- rotina agendada = +0,5 (em vez de virar RN específica);
- offline só leitura = +0,5;
- `uni_sem_doc` = 2/2,5/3;
- F4 proporcional aos fluxos;
- TestFlight externo = +0,5;
- teto do F5;
- o que o painel admin do template cobre;
- teste de concordância: 2 CNs e o Claude classificam os Projetos A–D sem ver a resposta um do outro.

## 5. O que falta

- [ ] Levar `fatores/` para `.claude/skills/dimensionamento-ntec/fatores/` no repositório e aplicar o `alteracoes-skill.patch`.
- [ ] Atualizar `SKILL.md`: tabela de arquivos, passo 0 = F0, "Status da skill".
- [ ] Atualizar o `README.md` do repositório.
- [ ] Atualizar `regua-dimensionamento.md`: apontar para `fatores/`; tirar Claude Code, buffer e a calibração com Claude Code.
- [ ] Atualizar `leitura-prd.md`: `demanda_pouco_detalhada` não é mais sempre false; tirar a disponibilidade do Passo 4; usar os nomes novos.
- [ ] Atualizar `insumos-e-perguntas.md`.
- [ ] Atualizar o texto de `exemplos/*.md` e do `ficticio-petagenda-proposta.json`. O cronograma tem 9 sprints, feito com Claude Code; a conta agora dá 22 semanas (11 sprints).
- [ ] Remover o "efeito cloud" de `docs/Dimensionamento-NTec-Skill.pdf` (via `docs/gerar_pdf.py`).
- [ ] Gerar o PDF da proposta para conferir (precisa do `reportlab`).
- [ ] Enviar para revisão de Augusto e Frank.
- [ ] Fechar D1–D5 e atualizar as constantes do script (marcadas `D1`…`D5` nos comentários).

## 6. Cuidados técnicos

- **Caminho longo no Windows.** Se o clone ficar num caminho longo, usar `git config core.longpaths true`. Mesmo assim, o Python pode não abrir arquivos nesses caminhos. Melhor clonar num caminho curto.
- **Diff dos JSONs.** O `json.dump` reformatou as listas dos JSONs de exemplo, então o diff deles é maior que a mudança real.
