# Template de Proposta Técnica (original do NTec)

_Transcrição em Markdown do PDF "Template de Proposta Técnica" (Padrão de documentação · NTEC, Comercial → Validação de Projeto). Serve de referência: como a skill preenche cada seção está em `proposta-tecnica.md`._

> **Diferença da V2-Inov:** o template original pede **PRD + protótipo** como pré-requisito. Desde a V2-Inov (22/10/2026), a skill usa as **transcrições da AT Diag e da AT Aprof + protótipo** no lugar do PRD. Onde o template diz "PRD", a skill lê "o que foi combinado nas calls" (o cabeçalho, a seção 14 e o primeiro item do checklist mudam por isso).
>
> **Seção 15, Precificação (23/10/2026):** não está no template original. A skill acrescenta o preço do cenário provável por tipo de sprint (`proposta-tecnica.md`, *Precificação*).

---

**Padrão de documentação · NTEC**

## Template de Proposta Técnica

**Comercial → Validação de Projeto**

> Preencher antes de enviar para validação técnica. Campos marcados com **OBRIGATÓRIO** são obrigatórios: proposta sem eles não deve ser aceita para análise.
>
> **Pré-requisito para enviar à validação:** documento de requisitos (PRD) + protótipo.
> - Sem os dois, a proposta não é aceita para validação.
> - O PRD deve ter no mínimo 5 páginas e no máximo em torno de 10.
> - Dê atenção ao protótipo: ele deve seguir as regras de negócio da documentação. Se alguma regra for adaptada no protótipo, justifique e deixe claro o que vale para o MVP (seção 14).

**Cliente/Projeto:** ______ · **Responsável comercial:** ______ · **Data de envio:** ______
**Link do PRD (nº de páginas):** ______ · **Link do protótipo:** ______

### 1. Problema que a solução resolve

- Qual a dor atual do cliente? (processo manual, planilha, retrabalho etc.)
- Liste de 2 a 4 problemas concretos que a solução ataca.

### 2. Visão geral e princípios da solução

- Tipo de aplicação (web, mobile, PWA etc.), público-alvo, proposta de valor em 1 frase.

### 3. Entidades principais do sistema

- Liste as entidades centrais (ex.: Paciente, Consulta, Pagamento) e entidades de apoio.

### 4. Perfis de acesso — OBRIGATÓRIO

Monte uma tabela com as colunas:

| Perfil | O que faz | Observações de permissão |
|---|---|---|

- Indicar se já existe matriz de permissões por ação ou se ainda está em aberto.

### 5. Fluxo completo, etapa por etapa

- Para cada etapa do fluxo: o que acontece, quem faz, quais dados entram/saem, quais validações existem.
- Marcar explicitamente qualquer etapa que dependa de decisão futura do cliente.

### 6. Regras de negócio — OBRIGATÓRIO

Monte uma tabela com as colunas:

| Regra | O que garante |
|---|---|

- Toda regra crítica (evitar duplicidade, conflito de horário, limites etc.) precisa estar aqui.

### 7. Arquitetura / como o sistema é construído

- Frontend, backend, banco de dados, autenticação, integrações externas previstas.

### 8. Segurança, dados e rastreabilidade — OBRIGATÓRIO

- Tipos de dado tratados (sensíveis? pessoais? LGPD aplicável?).
- Login, controle por perfil, histórico de alterações, logs de auditoria.
- Como dados públicos (links sem login, formulários públicos) serão protegidos.

### 9. Módulos críticos (pagamentos, integrações externas, automações)

- Detalhar cada módulo crítico separadamente.
- Indicar claramente: o que entra no MVP × o que é integração futura/dependente de terceiro.

### 10. Roadmap — MVP × futuro — OBRIGATÓRIO

Monte uma tabela com as colunas:

| Fase | Entrega | Natureza (Prioritário / A confirmar / Futuro) |
|---|---|---|

- Checar contradição: nada marcado como "futuro" ou "a confirmar" pode aparecer no cronograma do MVP.

### 11. Pontos em aberto para validação conjunta — OBRIGATÓRIO

- Lista explícita de tudo que depende de decisão externa (API de terceiro, fornecedor, definição de regra, volume esperado etc.).
- Se esta lista estiver vazia, é sinal de alerta: a proposta provavelmente está escondendo incerteza.

### 12. Stack de execução proposta

- Linguagens, frameworks, banco de dados, hospedagem, ferramentas de teste.
- Indicar qualquer peça da stack ainda não validada (ex.: API ainda não definida).

### 13. Cronograma sprint a sprint

Monte uma tabela com as colunas:

| Sprint | Entregas previstas |
|---|---|

- Duração total e nº de sprints.
- Qualquer entrega que dependa de item da seção 11 deve estar sinalizada aqui também.

### 14. Protótipo × regras de negócio — OBRIGATÓRIO

Monte uma tabela com as colunas:

| Tela/fluxo | Regra do PRD | Adaptação no protótipo | Justificativa | Vale para o MVP? |
|---|---|---|---|---|

- O protótipo deve seguir as regras de negócio da documentação (seção 6).
- Se alguma regra foi adaptada no protótipo, justifique e deixe claro qual versão vale para o MVP.
- Se não houve adaptação, declarar: "O protótipo segue integralmente as regras do PRD".

### Checklist final antes de enviar (comercial)

- [ ] PRD (entre 5 e ~10 páginas) e protótipo anexados
- [ ] Todos os campos OBRIGATÓRIO preenchidos
- [ ] Protótipo segue as regras de negócio do PRD — ou as adaptações estão justificadas e claras para o MVP (seção 14)
- [ ] Roadmap e cronograma não se contradizem
- [ ] Pontos em aberto (seção 11) listados explicitamente, não escondidos no meio do texto
- [ ] Nenhuma dependência externa (API, fornecedor) tratada como certa sem confirmação
