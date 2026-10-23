"""Teste de regressão dos exemplos: a régua de hoje ainda dá a faixa escrita nas fichas?

Uso:
    python testar_exemplos.py

Roda `calcular_faixa.calcular` em cada `exemplos/*.md` que tem bloco ```json e
compara o otimista / provável / conservador com a coluna "Faixa da régua" da
tabela de `exemplos/README.md`. Nas propostas, a entrada da régua fica em
`dimensionamento.entrada`, como em `gerar_proposta.py`.

Rodar sempre que um peso mudar (no script e no `fatores/F*.md`). Cada linha
"DIVERGE" é uma ficha (e a linha da tabela) para atualizar.

Sai com código 1 se alguma ficha divergir, não tiver linha na tabela ou der erro.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calcular_faixa import EntradaInvalida, calcular, ler_entrada, semanas  # noqa: E402

EXEMPLOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exemplos")
TEM_JSON = re.compile(r"^```json[ \t]*\n", re.M)
# Linha da tabela: "| [Nome](arquivo.md) | ... | 9 / 12 / 16 | ..."
LINHA = re.compile(r"^\|\s*\[[^\]]+\]\(([^)]+\.md)\)(.*)$", re.M)
FAIXA = re.compile(r"\|\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*\|")


def faixas_da_tabela():
    """{arquivo.md: (otimista, provável, conservador)} da tabela do README."""
    with open(os.path.join(EXEMPLOS, "README.md"), encoding="utf-8") as f:
        texto = f.read()
    faixas = {}
    for arquivo, resto in LINHA.findall(texto):
        m = FAIXA.search(resto)
        if m:
            faixas[arquivo] = tuple(int(x) for x in m.groups())
    return faixas


def entrada_da_regua(caminho):
    d = ler_entrada(caminho)
    return d["dimensionamento"]["entrada"] if "dimensionamento" in d else d


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    esperadas = faixas_da_tabela()
    falhas = 0
    for nome in sorted(os.listdir(EXEMPLOS)):
        caminho = os.path.join(EXEMPLOS, nome)
        if not nome.endswith(".md") or nome == "README.md":
            continue
        with open(caminho, encoding="utf-8") as f:
            if not TEM_JSON.search(f.read()):
                continue
        try:
            r = calcular(entrada_da_regua(caminho))
        except (EntradaInvalida, KeyError, ValueError) as erro:
            print(f"ERRO     {nome}: {erro}")
            falhas += 1
            continue
        if r["rejeicoes"]:
            print(f"ERRO     {nome}: rejeitado no F0")
            falhas += 1
            continue
        hoje = tuple(semanas(r[k]) for k in ("otimista", "provavel", "conservador"))
        txt = " / ".join(map(str, hoje))
        if nome not in esperadas:
            print(f"SEM LINHA {nome}: régua dá {txt}, mas a ficha não está na tabela de exemplos/README.md")
            falhas += 1
        elif esperadas[nome] != hoje:
            antes = " / ".join(map(str, esperadas[nome]))
            print(f"DIVERGE  {nome}: tabela diz {antes}, régua de hoje dá {txt}")
            falhas += 1
        else:
            print(f"OK       {nome}: {txt}")
    print(f"\n{'Tudo bate com a tabela.' if not falhas else f'{falhas} ficha(s) para conferir.'}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
