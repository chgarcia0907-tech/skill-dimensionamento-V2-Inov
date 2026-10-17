"""Calcula a faixa de semanas de um projeto do NTec a partir da Régua.

Uso:
    python calcular_faixa.py entrada.json

A entrada é um JSON com os fatores levantados (ver `regua-dimensionamento.md`
e os exemplos em `exemplos/*.json`). A saída é o detalhamento por fase em
(mínimo / central / máximo) e a faixa final: otimista, provável e conservador.

Os pesos daqui são a fonte da verdade da Régua. Se mudar um número aqui,
mude também na tabela de `regua-dimensionamento.md` (e vice-versa).
"""

import json
import math
import sys

# (mínimo, central, máximo) em semanas
F1_BASE = (1.5, 2, 2.5)
F1_DEMANDA_POUCO_DETALHADA = (0.5, 1, 1)
F1_ATIPICO = (0.5, 0.5, 1)
F1_STACK_FORA_TEMPLATE = (1, 1.5, 2)
F1_TETO = 4

F2_NIVEIS = {
    "nenhum": (0, 0, 0),
    "1": (0.5, 0.5, 1),
    "2-6-baixa": (0.5, 1, 1.5),
    "2-6-alta": (1.5, 2, 2.5),
    "6+": (2.5, 3, 4),
}
F2_MULTITENANCY = {
    "nao": (0, 0, 0),
    "separado": (0.5, 0.5, 1),
    "isolado": (1, 1.5, 2),
    "instancias": (0, 0, 0),  # 🚩 não dimensiona, para
}
F2_TETO = 4

F3_FLUXO_COMUM = (1, 1.25, 1.5)
F3_FLUXO_RN = (2, 3, 4)
F3_FEATURE_ATIPICA = (1, 1.5, 2)
F3_FORMATO = {"web": 1.0, "webapp": 1.1, "pwa": 1.1, "app": 1.2}
F3_FORMATO_EXTRA = 0.1  # por formato adicional em código separado
F3_INTEGRACAO = {
    "template": (0, 0, 0),
    "uni_doc": (0.5, 0.5, 1),
    "bi_doc": (0.5, 1, 1.5),
    "uni_sem_doc": (1, 1.5, 2),
    "bi_sem_doc": (1.5, 2.5, 3.5),
    "sem_api": (0, 0, 0),  # 🚩 não dimensiona, para
}
F3_DEPENDENCIA_DADOS = (1, 1.5, 2)
F3_OFFLINE = {"nao": (0, 0, 0), "local": (0, 0, 0), "sync": (1.5, 2, 3)}
F3_VOLUME_ALTO = (1, 1.5, 2)

# Fator Claude Code (17/10/2026): dupla com ~20 h/semana somadas, codando com Claude Code.
# Multiplica só o que é código escrito pelo time: o núcleo do F3 e o F2. Imersão, extras
# do F3 (integrações, offline com sincronização, dados, volume), testes com o cliente,
# deploy e lojas dependem do cliente, de terceiros ou de revisão humana e ficam iguais.
# Meio-termo calibrado em 2 projetos (17/10/2026): Projeto B (vender 12) e um app + painel de 8 fluxos
# com offline (~24 semanas, 12 sprints). O ganho da ferramenta é parcialmente comido pelas ~20 h/semana
# (antes a régua supunha 3 a 4 h/dia por pessoa) e pela coordenação de projetos maiores.
# Projetos antigos da calibração rodam com "claude_code": false.
CLAUDE_CODE_F3_NUCLEO = (0.6, 0.75, 0.9)
CLAUDE_CODE_F2 = (0.7, 0.85, 1.0)

F4_BASE = (1, 1.5, 2)
F4_RN_CRITICA = (0.5, 0.5, 1)
F4_POUCA_DISPONIBILIDADE = (0.5, 0.5, 1)
F4_TETO = 4

F5_WEB = (0.5, 0.5, 1)
F5_APP_SOZINHO = (0.5, 0.5, 1)
F5_APP_JUNTO_WEB = (0, 0.5, 0.5)
F5_INFRA_CLIENTE = (1, 1, 2)

F6_LOJAS = {"nao": (0, 0, 0), "normal": (2, 2.5, 4), "sensivel": (2.5, 3, 6)}

PROVAVEL_CALIBRADO_ATE = 26  # acima disso a régua ainda não foi calibrada


def soma(*partes):
    return tuple(sum(p[i] for p in partes) for i in range(3))


def vezes(parte, n):
    return tuple(v * n for v in parte)


def limita(parte, teto):
    return tuple(min(v, teto) for v in parte)


def calcular(e):
    alertas = []
    paradas = []

    # F1 — Imersão, refinamento, setup e acessos
    f1 = [F1_BASE]
    if e.get("demanda_pouco_detalhada"):
        f1.append(F1_DEMANDA_POUCO_DETALHADA)
    if e.get("atipico"):
        f1.append(F1_ATIPICO)
        alertas.append("Setor ou feature atípica: pedir benchmark ou referência antes de fechar o prazo.")
    if e.get("stack_fora_template"):
        f1.append(F1_STACK_FORA_TEMPLATE)
        alertas.append("Stack fora do template NTec: confirmar com a área de projetos se o time domina.")
    f1 = soma(*f1)
    if f1[2] > F1_TETO:
        alertas.append("Imersão/setup bateu no teto de 4 semanas: revisar com a área de projetos.")
    f1 = limita(f1, F1_TETO)

    # F2 — Infra, níveis de acesso, cadastro e login
    niveis = e.get("niveis_acesso", "1")
    multi = e.get("multitenancy", "nao")
    if niveis == "6+":
        alertas.append("6+ níveis de acesso: complexidade alta, confirmar se todos são mesmo necessários no MVP.")
    if multi == "instancias":
        paradas.append("Multitenancy com instâncias e regras de negócio isoladas por cliente: projeto beira o inviável.")
    if multi == "isolado":
        alertas.append("Multitenancy com isolamento de dados: complexidade média/alta.")
    f2 = soma(F2_NIVEIS[niveis], F2_MULTITENANCY[multi])
    claude = e.get("claude_code", True)
    if claude:
        f2 = tuple(v * k for v, k in zip(f2, CLAUDE_CODE_F2))
    if f2[2] > F2_TETO:
        alertas.append("Acesso/infra bateu no teto de 4 semanas: revisar com a área de projetos.")
    f2 = limita(f2, F2_TETO)

    # F3 — Desenvolvimento
    formatos = e.get("formatos", ["web"])
    fator = max(F3_FORMATO[f] for f in formatos) + F3_FORMATO_EXTRA * (len(formatos) - 1)
    nucleo = soma(
        vezes(F3_FLUXO_COMUM, e.get("fluxos_comuns", 0)),
        vezes(F3_FLUXO_RN, e.get("fluxos_rn_especifica", 0)),
        vezes(F3_FEATURE_ATIPICA, e.get("features_atipicas", 0)),
    )
    nucleo = vezes(nucleo, fator)
    if claude:
        nucleo = tuple(v * k for v, k in zip(nucleo, CLAUDE_CODE_F3_NUCLEO))
    if e.get("features_atipicas", 0):
        alertas.append("Feature atípica: validar se é possível e se existe benchmark (pode exigir prova de conceito).")

    integracoes = e.get("integracoes", [])
    extras = [F3_INTEGRACAO[i] for i in integracoes]
    for i in integracoes:
        if i == "sem_api":
            paradas.append("Integração bidirecional que a PRD diz não ter API: avaliar alternativa; potencial motivo de inviabilidade.")
        if i in ("uni_sem_doc", "bi_sem_doc"):
            alertas.append("Integração com sistema do cliente: incluir a cláusula de contrato (acesso à API até o início da sprint; sem acesso, vira planilha) e o plano B em 'O que cortar'.")
    if e.get("dependencia_dados"):
        extras.append(F3_DEPENDENCIA_DADOS)
        alertas.append("Dependência de dados de bases soltas: chamar o núcleo de Dados para avaliar.")
    offline = e.get("offline", "nao")
    extras.append(F3_OFFLINE[offline])
    if offline == "sync":
        alertas.append("Offline com sincronização: revisar a estrutura do banco antes de fechar o prazo.")
    if e.get("volume_alto"):
        extras.append(F3_VOLUME_ALTO)
        alertas.append("Volume de uso alto: requisitos de performance precisam estar escritos.")
    f3 = soma(nucleo, *extras) if extras else nucleo

    # F4 — Testes com o cliente
    f4 = [F4_BASE]
    if e.get("rn_critica"):
        f4.append(F4_RN_CRITICA)
    if e.get("cliente_pouca_disponibilidade"):
        f4.append(F4_POUCA_DISPONIBILIDADE)
    f4 = limita(soma(*f4), F4_TETO)

    # F5 — Deploy
    tem_web = any(f in ("web", "webapp", "pwa") for f in formatos)
    tem_app = "app" in formatos
    f5 = []
    if tem_web:
        f5.append(F5_WEB)
    if tem_app:
        f5.append(F5_APP_JUNTO_WEB if tem_web else F5_APP_SOZINHO)
    if e.get("deploy_infra_cliente"):
        f5.append(F5_INFRA_CLIENTE)
        alertas.append("Deploy na infra do cliente: pedir as regras de deploy e os acessos já na imersão.")
    f5 = soma(*f5)

    # F6 — Publicação nas lojas
    lojas = e.get("lojas", "nao")
    if tem_app and lojas == "nao":
        alertas.append("Tem app nativo mas as lojas não foram marcadas: confirmar se o cliente quer publicar.")
    f6 = F6_LOJAS[lojas]

    fases = {
        "F1 Imersão, refinamento e setup": f1,
        "F2 Infra, níveis de acesso e login": f2,
        "F3 Desenvolvimento": f3,
        "F4 Testes com o cliente": f4,
        "F5 Deploy": f5,
        "F6 Publicação nas lojas": f6,
    }
    total = soma(*fases.values())

    otimista, provavel, conservador = total
    if provavel > PROVAVEL_CALIBRADO_ATE:
        alertas.append(
            f"Provável acima de {PROVAVEL_CALIBRADO_ATE} semanas: fora da faixa calibrada da régua; "
            "validar com a área de projetos e considerar quebrar em fases."
        )

    return {
        "fases": fases,
        "fator_formato": fator,
        "claude_code": claude,
        "otimista": otimista,
        "provavel": provavel,
        "conservador": conservador,
        "alertas": alertas,
        "paradas": paradas,
    }


def semanas(v):
    return math.ceil(v - 1e-9)


def sprints(v):
    return math.ceil(semanas(v) / 2)


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def imprimir(e, r):
    print(f"# Projeto {e.get('projeto', '?')}\n")
    if r["paradas"]:
        print("🚩 PARADO — não dimensionar até a área de projetos avaliar:")
        for p in r["paradas"]:
            print(f"  - {p}")
        print()
    print("| Fase | Mín | Central | Máx |")
    print("|---|---|---|---|")
    for nome, (a, b, c) in r["fases"].items():
        print(f"| {nome} | {fmt(a)} | {fmt(b)} | {fmt(c)} |")
    cc = (" · Claude Code: núcleo do F3 x0,6/0,75/0,9 e F2 x0,7/0,85/1" if r["claude_code"]
          else " · sem fator Claude Code")
    print(f"\nFator de formato no desenvolvimento: x{fmt(r['fator_formato'])}{cc}\n")
    print("| Cenário | Semanas | Sprints (2 sem) |")
    print("|---|---|---|")
    rotulos = {
        "otimista": "Otimista (piso)",
        "provavel": "Provável (recomendado)",
        "conservador": "Conservador (teto de risco)",
    }
    for nome, rotulo in rotulos.items():
        v = r[nome]
        print(f"| {rotulo} | {semanas(v)} ({fmt(round(v, 2))}) | {sprints(v)} |")
    venda = sprints(r["provavel"]) * 2
    print(f"\nRecomendação de venda: {venda} semanas ({venda // 2} sprints) + semanas off do calendário.")
    if r["alertas"]:
        print("\nAlertas:")
        for a in r["alertas"]:
            print(f"  - {a}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        entrada = json.load(f)
    sys.stdout.reconfigure(encoding="utf-8")
    imprimir(entrada, calcular(entrada))
