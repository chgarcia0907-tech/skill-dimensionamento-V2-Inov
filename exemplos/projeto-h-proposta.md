# Proposta Técnica — Projeto H

Proposta completa do Projeto H, montada a partir das transcrições da AT Diag e da AT Aprof (`leitura-transcricoes.md`). Ficha do caso: [projeto-h.md](projeto-h.md).

Gerar o PDF: `python ../scripts/gerar_proposta.py projeto-h-proposta.md --saida <pasta>`. O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "Projeto H",
  "status": "atencao",
  "cabecalho": {
    "cliente_projeto": "Projeto H · Calculadora de soro para prescrição pediátrica",
    "responsavel_comercial": "",
    "data_envio": "",
    "transcricoes": [
      {"call": "AT Diag", "data": "14/07", "link": "gravação no Fathom (19 min)"},
      {"call": "AT Aprof", "data": "21/07", "link": "gravação no Fathom (11 min)"}
    ],
    "prototipo_link": "protótipo no Lovable apresentado na AT Aprof (link sem token de acesso)"
  },
  "problema": {
    "dor": "Médicos que atendem crianças em pronto-socorro e no interior calculam o soro de cabeça ou em planilhas próprias, e o erro de cálculo põe o paciente em risco.",
    "problemas": [
      "O cálculo do soro em pediatria depende do peso e do tipo de soro, e quem não é da área erra com facilidade.",
      "A planilha da cliente resolve, mas só no computador dela.",
      "Em muitos lugares do interior não há internet para usar uma página na web."
    ]
  },
  "visao_geral": {
    "tipo": "App mobile nativo (App Store e Play Store), que funciona sem internet.",
    "publico": "Médicos que prescrevem soro para crianças, a começar por pronto-socorro e UTI.",
    "proposta_valor": "O médico informa o peso, o tipo de soro e as quantidades desejadas e recebe na hora o volume de cada componente e a velocidade de infusão.",
    "principios": [
      "Rápido de usar no plantão: os parâmetros em cima e o resultado logo abaixo, na mesma tela.",
      "Funciona sem internet: todo o cálculo roda no aparelho.",
      "Não guarda dados do paciente: não é prontuário."
    ]
  },
  "entidades": {
    "centrais": "Cálculo do soro (parâmetros de entrada e resultado).",
    "apoio": "Faixas de peso, tipos de soro, substâncias e limites de concentração, vindos da planilha da cliente."
  },
  "perfis": {
    "tabela": [
      ["Médico (usuário do app)", "Informa peso, tipo de soro e quantidades; lê o resultado.", "Login em aberto (ponto 1): a conta considera 1 perfil com login."]
    ],
    "matriz_permissoes": "Não há permissões diferentes: um tipo de usuário só."
  },
  "fluxo": [
    {"etapa": "O médico informa o peso do paciente.", "quem": "Médico", "dados": "Entra: peso. O app identifica a faixa (0 a 10 kg, 10 a 20 kg, acima de 20 kg).", "validacoes": "Peso dentro de limites plausíveis."},
    {"etapa": "Escolhe o tipo de soro.", "quem": "Médico", "dados": "Entra: um dos tipos de soro da planilha (ex.: soro para recém-nascido).", "validacoes": "Tipo compatível com a faixa de peso."},
    {"etapa": "Informa as quantidades desejadas de glicose e de cada íon.", "quem": "Médico", "dados": "Entra: glicose, sódio, potássio, cálcio (com escolha da unidade do cálcio).", "validacoes": "Valores numéricos e unidade escolhida."},
    {"etapa": "Lê o resultado logo abaixo dos parâmetros.", "quem": "App", "dados": "Sai: volume de cada componente, volume total e velocidade de infusão.", "validacoes": "Aviso quando a concentração passa do máximo permitido (ex.: glicose em veia periférica).", "pendente": "Fórmulas e limites conforme a planilha final (ponto 3)."}
  ],
  "regras": [
    ["Faixa de peso define o cálculo (0 a 10 kg, 10 a 20 kg, acima de 20 kg)", "O cálculo usa a regra certa para cada criança."],
    ["Cada tipo de soro tem a sua composição", "O volume de cada componente sai conforme o soro escolhido."],
    ["Aviso de concentração máxima", "O médico é alertado antes de prescrever uma solução acima do limite."],
    ["Unidade do cálcio selecionável (mg ou outra usada no serviço)", "O resultado bate com o padrão de cada hospital."],
    ["Nenhum dado do paciente é guardado", "Não há prontuário nem histórico de pacientes."]
  ],
  "arquitetura": [
    ["Frontend", "App mobile nativo, uma tela de cálculo."],
    ["Backend", "O cálculo roda no aparelho, sem internet. Servidor só se o login ou a cobrança forem confirmados (pontos 1 e 2)."],
    ["Banco de dados", "Não há banco de pacientes. As tabelas da planilha ficam dentro do app."],
    ["Autenticação", "Em aberto (ponto 1)."],
    ["Integrações externas", "Cobrança pelas lojas (compra dentro do app), em aberto (ponto 2)."]
  ],
  "seguranca": [
    ["Tipos de dado", "Peso e parâmetros clínicos digitados na hora, sem identificar o paciente e sem guardar. Dado de saúde só em uso, não armazenado."],
    ["Login e controle por perfil", "Em aberto (ponto 1). Um perfil só."],
    ["Histórico e logs", "Sem histórico de cálculos: a cliente disse que não precisa."],
    ["Dados públicos", "Não há links públicos nem formulários."]
  ],
  "modulos_criticos": [
    {"nome": "Cálculo do soro (regra crítica)", "detalhe": ["Fórmulas por faixa de peso e tipo de soro, vindas da planilha da cliente.", "Erro de cálculo causa dano ao paciente: testes conferem cada faixa e cada tipo contra a planilha."], "mvp": "Os tipos de soro da planilha, o aviso de concentração máxima e a unidade do cálcio.", "futuro": "Outros cálculos pediátricos não foram discutidos."},
    {"nome": "Cobrança (compra dentro do app)", "detalhe": ["A cliente quer vender o app, sem dizer como (ponto 2)."], "mvp": "Na conta como assinatura ou compra dentro do app.", "futuro": ""}
  ],
  "roadmap": [
    ["MVP", "Cálculo do soro: peso, tipo de soro, quantidades, resultado e aviso de concentração máxima", "Prioritário"],
    ["MVP", "Funcionamento sem internet", "Prioritário"],
    ["MVP", "Login de um perfil (depende do ponto em aberto 1)", "Prioritário"],
    ["MVP", "Cobrança dentro do app (depende do ponto em aberto 2)", "Prioritário"],
    ["MVP", "Publicação na App Store e na Play Store", "Prioritário"],
    ["Futuro", "Histórico de cálculos", "Futuro"]
  ],
  "pontos_abertos": [
    "**1. Login (muda a faixa):** a cliente disse \"não sei se seria interessante um login\". A conta considera login de 1 perfil (+0,5 semana no central). Pergunta: \"A pessoa precisa criar conta e entrar com login, ou abre o app e já usa?\"",
    "**2. Cobrança (muda a faixa):** a cliente quer vender o app, sem dizer como. A conta considera compra ou assinatura dentro do app (+1 semana no central). Login e cobrança somam 2 das 14 semanas. Pergunta: \"Como você quer cobrar: o app é pago na loja, tem assinatura dentro do app, ou é gratuito?\"",
    "**3. Planilha final:** a cliente passou a tabela depois da AT Diag. Confirmar que é a versão final, com todos os tipos de soro e os limites de concentração, antes da Sprint 3.",
    "**4. Contas de desenvolvedor Apple e Google:** abrir na imersão, no nome de quem vai publicar o app.",
    "**5. Data de início:** a cliente disse que é \"para esse ano, mas não tem pressa\". Semanas off não somadas."
  ],
  "stack": {
    "itens": [
      ["App mobile", "Expo (React Native), template NTec."],
      ["Cálculo", "No próprio app, sem servidor."],
      ["Testes", "Vitest, com um caso de teste por faixa de peso e tipo de soro, tirado da planilha."]
    ],
    "nao_validado": [
      "Toda a stack é premissa a validar na Sprint de Refino e Prototipação (as calls não fixaram tecnologia).",
      "Servidor, banco e autenticação só entram se os pontos 1 e 2 forem confirmados."
    ]
  },
  "cronograma": {
    "sprints": [
      ["Sprint 1", "Imersão, refino do escopo, validação do protótipo com a planilha da cliente e setup. Pedir as contas Apple e Google.", "pontos 3 e 4", "imersao"],
      ["Sprint 2", "Deploy inicial (0,5 semana), login e tela de parâmetros: peso, faixa de peso e tipo de soro.", "ponto 1", "desenvolvimento"],
      ["Sprint 3", "Cálculo do soro: volume de cada componente, volume total e velocidade de infusão.", "ponto 3", "desenvolvimento"],
      ["Sprint 4", "Aviso de concentração máxima, unidade do cálcio, funcionamento sem internet e cobrança dentro do app.", "ponto 2", "desenvolvimento"],
      ["Sprint 5", "Testes com a cliente, conferindo cada faixa e cada tipo de soro contra a planilha.", "", "testes"],
      ["Sprint 6", "Correções dos testes, versão de produção e envio para as lojas.", "", "testes"],
      ["Sprint 7", "Revisão das lojas (categoria de saúde), correções finais e entrega.", "", "desenvolvimento"]
    ],
    "duracao_obs": "das quais 2 semanas dependem dos pontos 1 e 2"
  },
  "prototipo": {
    "recebido": true,
    "tabela": [
      ["Tela de cálculo", "Os tipos de soro e as fórmulas da planilha da cliente", "Valores ilustrativos e tipos de soro provisórios", "O protótipo foi feito antes de a tabela chegar; serviu para validar o fluxo", "Sim, depois de trocar pelos dados da planilha"]
    ],
    "declaracao": "A cliente validou o fluxo na AT Aprof (\"é isso mesmo, é uma calculadora\"). Os valores do protótipo são ilustrativos e serão trocados pelos da planilha."
  },
  "dependencia_externa_sem_confirmacao": false,
  "dimensionamento": {
    "entrada": {
      "projeto": "Projeto H — calculadora clínica (app nativo, a partir da AT Diag e da AT Aprof)",
      "f0": {
        "stack_exigida_fora_da_lista": false,
        "sla_ou_sustentacao": false,
        "infra_cliente_sem_acesso": false,
        "multa_por_atraso": false,
        "feature_sem_referencia_nem_doc": false,
        "hardware": false,
        "prazo_exigido_semanas": null
      },
      "demanda_pouco_detalhada": false,
      "atipico": false,
      "stack_fora_template": false,
      "niveis_acesso": "1",
      "multitenancy": "nao",
      "fluxos_comuns": 0,
      "fluxos_rn_especifica": 1,
      "features_atipicas": 0,
      "formatos": ["app"],
      "integracoes": ["bi_doc"],
      "dependencia_dados": false,
      "offline": "local",
      "volume_alto": false,
      "rn_critica": true,
      "deploy_infra_cliente": false,
      "lojas": "sensivel",
      "fathom": true,
      "lacunas_fathom": {"niveis_acesso": "nenhum", "integracoes": []}
    },
    "criterios": {
      "F1": "Base. As duas calls existem e a jornada está clara; referência citada pela cliente (\"as [calculadoras] que eu já vi\", AT Aprof 2:32), então não é atípico.",
      "F2": "1 perfil com login, em lacuna: \"não sei se seria interessante um login\" (AT Diag 13:32). Valor leve: sem login. Uma pessoa só usa, sem várias empresas.",
      "F3": "1 jornada com RN específica (calcular o soro pela planilha da cliente, AT Diag 7:46), app nativo ×1,2. Cobrança em lacuna como bi_doc (\"é pra venda mesmo\", AT Diag 14:37). Offline local: o cálculo roda no aparelho e nada sobe depois (AT Diag 3:02).",
      "F4": "Base + RN crítica: o app calcula volume e velocidade de infusão de soro para crianças.",
      "F5": "Só app nativo.",
      "F6": "App sensível: categoria de saúde, dado clínico, público pediátrico. Lojas confirmadas (AT Diag 15:04 / 15:27)."
    },
    "inventario": [
      ["Calcular o soro", "Médico", "App", "Fórmula da planilha da cliente por faixa de peso e tipo de soro; aviso de concentração máxima; unidade do cálcio. Cobrança e login em aberto", "AT Diag 7:46 — \"a pessoa jogaria o peso do paciente\"; AT Aprof 1:35 — \"é isso mesmo, é uma calculadora\""]
    ],
    "atencao": [
      "**Prazo já falado à cliente:** a CN disse \"dois a três meses\" na AT Aprof (6:36). Dois meses (~9 semanas) fica abaixo do otimista da skill (10). Alinhar a expectativa antes da proposta.",
      "**Regra da App Store para calculadoras de dose (a confirmar com a área de projetos):** a diretriz 1.4.2 da Apple pede que calculadoras de dose venham de fabricante, hospital, universidade ou outra entidade aprovada, ou tenham aprovação regulatória. Uma médica publicando em nome próprio pode ser recusada. As calls não cobrem isso. Verificar antes de vender a publicação na App Store.",
      "**Responsabilidade pelo cálculo:** erro de dose causa dano. As calls não cobrem termo de uso nem quem responde pelo resultado. Os testes conferem cada faixa e cada tipo de soro contra a planilha.",
      "**Planilha é a fonte da regra:** o app reproduz a planilha da cliente. Qualquer mudança de fórmula depois da Sprint 3 vira mudança de escopo."
    ],
    "lacunas": [
      ["Login (niveis_acesso)", "AT Diag 13:32: \"não sei se seria interessante um login\"; a AT Aprof não volta ao assunto", "A pessoa precisa criar conta e entrar com login, ou abre o app e já usa?", "1 perfil com login (+0,5 semana)"],
      ["Cobrança (integracoes)", "AT Diag 14:37: \"é pra venda mesmo\", sem dizer como; a AT Aprof não volta ao assunto", "Como você quer cobrar: o app é pago na loja, tem assinatura dentro do app, ou é gratuito?", "Compra ou assinatura dentro do app, bi_doc (+1 semana)"],
      ["Data de início", "AT Aprof 7:14: \"seria mesmo para esse ano, mas não tem pressa\"", "Qual é a data prevista de início?", "Semanas off não somadas"]
    ],
    "precedente": "Sem precedente comparável: os Projetos A a D têm de 2 a 6 fluxos; este é um app de uma jornada só, com regra crítica e loja sensível. O peso está quase todo em F4 e F6 (testes e lojas), não no desenvolvimento.",
    "cortes": [
      ["Sem cobrança dentro do app (app pago na loja ou gratuito)", "−2 semanas na venda (14 → 12)"],
      ["Sem login e sem cobrança", "−2 semanas na venda (14 → 12)"],
      ["PWA (instala pelo navegador), sem lojas", "−4 semanas na venda (14 → 10). Muda o pedido da cliente, que quer as lojas"]
    ],
    "suposicoes": [
      "\"EES\" na transcrição da AT Diag (15:04) foi lido como Play Store (\"tanto para a [Play Store] quanto para a App Store\").",
      "Os três tipos de soro e a escolha da unidade do cálcio são a mesma jornada (Calcular o soro), não jornadas separadas.",
      "Sem histórico de cálculos: a cliente descartou (\"não é prontuário\", AT Diag 13:32).",
      "Prazo exigido: nenhum. \"Para esse ano, mas não tem pressa\" não é exigência.",
      "A planilha com as fórmulas é o documento da RN específica, não dependência de dados."
    ],
    "fronteira": [],
    "imersao": [
      "Cores, nomes e ordem dos campos: a cliente aprovou o leiaute do protótipo, com o resultado abaixo dos parâmetros.",
      "Texto explicativo de cada tipo de soro (ex.: soro para recém-nascido), para quem não é da área.",
      "Unidades usadas em cada serviço (cálcio em mg ou outra)."
    ],
    "observacoes": [
      "A CN falou \"dois a três meses\" na AT Aprof. A skill dá otimista 10, provável 13 e vende 14 semanas (12 se login e cobrança caírem). Três meses (~13 semanas) bate com a venda; dois meses não.",
      "A CN também falou um valor de investimento na AT Aprof. Não entra no dimensionamento."
    ]
  }
}
```
