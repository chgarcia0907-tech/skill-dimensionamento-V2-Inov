# Insumos da revisão de 20/10/2026

Material de trabalho que levou à revisão da régua (F0, `fatores/` por fase e script sem padrões), mergeada no PR #1. O estado atual da skill está no `README.md` da raiz e em `fatores/README.md`. Os arquivos desta pasta são o registro de **como** se chegou lá.

| Arquivo | O que é |
|---|---|
| `analise-criterios-F0-F6.md` | Relatório do LLM Council: critérios mal definidos, fator a fator, e checklist das mudanças pedidas na reunião de 20/10 |
| `testes-comparativos.md` | Original × v1 × v2: correções da v2 e casos hipotéticos H1 a H8, com e sem as sugestões para D2 e D3 |
| `testes/` | `comparar.py`, os scripts da original (`orig/`) e da v1 (`v1/`) e a saída completa em `resultado.json` |
| `alteracoes-skill-v1.patch` | Primeira versão do patch sobre o commit `39875e8`, guardada só para comparação |
| `alteracoes-skill.patch` | Versão v2 do patch, a que entrou no repositório (commit `ed01191`) |
| `contexto-21-10.md` | Retrato do trabalho em 21/10/2026, escrito para retomar em outra conversa. Os caminhos locais e a lista "O que falta" são daquele dia |

Para reproduzir os testes, a partir desta pasta:

```bash
python -I testes/comparar.py testes ../../scripts/calcular_faixa.py
```
