# Exemplo de resposta completa (caso fictício)

Este caso **não é um projeto real**. Serve para mostrar ao CN como a resposta da skill fica do começo ao fim. Entrada: o bloco JSON em *Entrada da régua*, no fim deste arquivo.

**O que o CN mandou:**
> "Rede de 3 clínicas veterinárias quer um app pro tutor marcar consulta, ver a carteirinha de vacina do pet e receber lembrete. A clínica quer um painel pra recepção e pro veterinário. Querem pagar a consulta pelo app (Mercado Pago). Não tem documento, foi só uma call."

**Respostas do CN às perguntas da skill:** cada clínica só vê os próprios dados, mas as regras são as mesmas para todas; o tutor baixa o app na loja; o veterinário registra o atendimento e a recepção gerencia a agenda; o lembrete é por notificação no celular.

---

# Projeto PetAgenda

⚠️ **Estimativa preliminar, sem transcrição das calls.** Mandar as transcrições da AT Diag e da AT Aprof antes de fechar a proposta.

**1. Prazo em uma frase.** Recomendado vender **18 semanas (9 sprints)** + semanas off. Não vender abaixo de 14.

**2. Faixa de semanas**

| Cenário | Semanas | Sprints | Quando acontece |
|---|---|---|---|
| Otimista (piso) | 14 | 7 | Escopo congelado, clínica responde rápido |
| **Provável (recomendado)** | **18** | **9** | O que costuma acontecer no NTec |
| Conservador (teto de risco) | 24 | 12 | Se pagamento e lojas derem problema |

**3. Resumo.** App nativo para tutores (lojas) + painel web para as clínicas. 4 perfis (tutor, recepção, veterinário, admin da rede). 4 fluxos críticos: agendar consulta, carteirinha de vacina com lembretes, registro de atendimento, gestão da agenda. Pagamento online e notificações. 3 clínicas com dados separados.

**4. Pontos de atenção**
1. **Pagamento pelo app (Mercado Pago):** a integração é bidirecional (cobra e recebe a confirmação). É um serviço de mercado com API pública, então entra com o peso fixo "com documentação", sem precisar perguntar nada.
2. **Dados separados por clínica (multitenancy (um mesmo sistema atendendo várias empresas com os dados separados)):** confirmar por escrito que as **regras** são iguais para as 3. Se cada clínica quiser regras próprias, o projeto para (🚩).
3. **Demanda sem documento:** veio só de uma call. A imersão fica mais longa (+1 semana no central).

**5. Perguntas para o cliente**
- "Cada clínica tem regras próprias (horários, preços, tipos de consulta) ou todas seguem as mesmas regras?"
- "O pagamento precisa ser pelo app no lançamento, ou pode ser na clínica no começo?"
- "Precisa estar na App Store e na Play Store, ou um app que se instala pelo navegador resolve no início?"

**6. Detalhamento por fase**

| Fase | Critério | Mín | Central | Máx |
|---|---|---|---|---|
| F1 Imersão e setup | base + demanda sem documento | 2 | 3 | 3,5 |
| F2 Acesso e login | 4 perfis com telas próprias → 2 a 5 com grandes diferenças; dados separados por clínica | 2 | 2,5 | 3,5 |
| F3 Desenvolvimento | 4 fluxos comuns, com o fator do código de cada um: carteirinha só no app (x1,2), registro de atendimento e gestão da agenda só no painel (x1), agendamento nos dois (x1,4); Mercado Pago (bi, doc); push (uni, doc) | 5,6 | 7,25 | 9,4 |
| F4 Testes com cliente | base | 1 | 1,5 | 2 |
| F5 Deploy | web + app | 0,5 | 1 | 1,5 |
| F6 Lojas | app comum | 2 | 2,5 | 4 |
| **Total** | | **14** | **18** | **24** |

**7. Precedente.** **Projeto D** (app nas lojas + painel web, 5 fluxos comuns): vendido 18, sem atraso até agora. O PetAgenda chega à mesma venda: tem pagamento, perfis com mais diferenças e demanda sem documento, mas só um dos fluxos existe nos dois códigos, enquanto no Projeto D os cinco estão como compartilhados.

**8. O que cortar** (recalculado com o script)

| Corte | Provável | Venda |
|---|---|---|
| Escopo completo | 18 | 18 |
| PWA (app instalado pelo navegador) em vez de app nas lojas | 15 | 16 |
| + pagamento na clínica no MVP (sem Mercado Pago) | 14 | 14 |
| + carteirinha de vacina na fase 2 | 13 | **14** |

**9. Observações**
- *Suposições:* lembretes de vacina são notificações push simples (sem SMS ou WhatsApp); o painel da recepção e o do veterinário estão no mesmo código web; o login por e-mail e o upload de foto do pet usam o template.
- *Ajustes de fronteira:*
  ```
  F2 níveis de acesso: 2-6 poucas diferenças → 2-6 grandes diferenças (+1)
  Motivo: veterinário e recepção têm telas e permissões próprias (registro de atendimento × agenda); na dúvida, a régua vai para o mais pesado.
  ```

## Entrada da régua

O JSON que o script lê (`python ../scripts/calcular_faixa.py ficticio-petagenda.md`). O script usa o primeiro bloco `json` deste arquivo.

```json
{
  "projeto": "PetAgenda (exemplo fictício)",
  "f0": {
    "stack_exigida_fora_da_lista": false,
    "sla_ou_sustentacao": false,
    "infra_cliente_sem_acesso": false,
    "multa_por_atraso": false,
    "feature_sem_referencia_nem_doc": false,
    "hardware": false,
    "prazo_exigido_semanas": null
  },
  "demanda_pouco_detalhada": true,
  "atipico": false,
  "stack_fora_template": false,
  "niveis_acesso": "2-5-grandes",
  "multitenancy": "separado",
  "fluxos_comuns": 4,
  "fluxos_rn_especifica": 0,
  "features_atipicas": 0,
  "formatos": [
    "app",
    "web"
  ],
  "fluxos_por_formato": {
    "app": {
      "comuns": 1,
      "rn_especifica": 0,
      "atipicas": 0
    },
    "web": {
      "comuns": 2,
      "rn_especifica": 0,
      "atipicas": 0
    },
    "compartilhado": {
      "comuns": 1,
      "rn_especifica": 0,
      "atipicas": 0
    }
  },
  "integracoes": [
    "bi_doc",
    "uni_doc",
    "template"
  ],
  "dependencia_dados": false,
  "offline": "nao",
  "volume_alto": false,
  "rn_critica": false,
  "deploy_infra_cliente": false,
  "lojas": "normal"
}
```
