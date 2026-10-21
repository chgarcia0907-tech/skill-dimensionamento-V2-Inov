"""Compara a régua original (39875e8), a v1 (patch de 21/10) e a v2 (patch corrigido) em casos hipotéticos.

Uso: python -I comparar.py <pasta-scratchpad> <calcular_faixa.py da v2>
"""
import copy
import importlib.util
import io
import json
import math
import sys
from contextlib import redirect_stdout

SP, V2 = sys.argv[1], sys.argv[2]
sys.stdout.reconfigure(encoding="utf-8")


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ORIG = carregar("orig", f"{SP}/orig/calcular_faixa.py")
V1 = carregar("v1", f"{SP}/v1/calcular_faixa.py")
V2M = carregar("v2", V2)
# v2 com as sugestões das decisões em aberto (D1 ×1,2 composto fica de fora: é a alternativa, não a sugestão)
V2S = carregar("v2s", V2)
V2S.F2_NIVEIS["2-5-grandes"] = (2, 2.5, 3)
V2S.F2_MULTITENANCY["isolado"] = (1.5, 2, 3)
V2S.F4_RN_CRITICA = (1, 1, 1.5)
V2S.F3_INTEGRACAO["bi_sem_doc"] = (4, 4.5, 5.5)
V2S.F3_INTEGRACAO["uni_sem_doc"] = (2, 2.5, 3)
V2S.F3_MARGEM = 0.125

F0_LIMPO = {
    "stack_exigida_fora_da_lista": False, "offline_sync_com_mongodb_exigido": False,
    "sla_ou_sustentacao": False, "infra_cliente_sem_acesso": False, "multa_por_atraso": False,
    "sem_validador_nomeado": False, "feature_sem_referencia_nem_doc": False, "hardware": False,
    "prazo_exigido_semanas": None,
}
BASE = {
    "demanda_pouco_detalhada": False, "atipico": False, "stack_fora_template": False,
    "niveis_acesso": "1", "multitenancy": "nao", "fluxos_comuns": 0, "fluxos_rn_especifica": 0,
    "features_atipicas": 0, "formatos": ["web"], "integracoes": [], "dependencia_dados": False,
    "offline": "nao", "volume_alto": False, "rn_critica": False, "deploy_infra_cliente": False,
    "lojas": "nao",
}


def caso(nome, f0=None, **campos):
    e = dict(copy.deepcopy(BASE), projeto=nome, f0=dict(F0_LIMPO, **(f0 or {})))
    e.update(campos)
    return e


CASOS = [
    ("H1 Marketplace B2B: 6+ perfis, isolado, ERP bidirecional sem doc, RN crítica",
     caso("H1", niveis_acesso="6+", multitenancy="isolado", fluxos_comuns=4, fluxos_rn_especifica=2,
          integracoes=["bi_sem_doc", "uni_doc"], rn_critica=True)),
    ("H2 App de campo: offline com sync, troca Mongo→Supabase, demanda vaga, atípico",
     caso("H2", demanda_pouco_detalhada=True, atipico=True, stack_fora_template=True,
          niveis_acesso="2-5-grandes", fluxos_comuns=3, fluxos_rn_especifica=1, formatos=["app"],
          integracoes=["uni_sem_doc"], offline="sync", lojas="normal")),
    ("H3 SaaS web + PWA + app, 3 bases de código",
     caso("H3", niveis_acesso="2-5-poucas", multitenancy="separado", fluxos_comuns=5,
          formatos=["web", "pwa", "app"], integracoes=["bi_doc", "template"], lojas="normal")),
    ("H4 Site institucional com prazo exigido de 4 semanas",
     caso("H4", f0={"prazo_exigido_semanas": 4}, fluxos_comuns=2)),
    ("H5 Cliente exige .NET; o CN só preencheu o F0",
     {"projeto": "H5", "f0": dict(F0_LIMPO, stack_exigida_fora_da_lista=True)}),
    ("H6 = H1 com multitenancy, lojas e formatos esquecidos no JSON",
     {k: v for k, v in caso("H6", niveis_acesso="6+", multitenancy="isolado", fluxos_comuns=4,
                              fluxos_rn_especifica=2, integracoes=["bi_sem_doc", "uni_doc"],
                              rn_critica=True).items()
      if k not in ("multitenancy", "lojas", "formatos")}),
    ("H7 Tecnologia exigida em lacuna do Fathom",
     caso("H7", stack_fora_template=True, lacunas_fathom=["stack_fora_template"], fluxos_comuns=3,
          niveis_acesso="2-5-poucas", formatos=["web"])),
    ("H8 Formato repetido por engano: [app, app]",
     caso("H8", fluxos_comuns=3, formatos=["app", "app"], lojas="normal")),
]

ANTIGO = {"2-5-poucas": "2-6-baixa", "2-5-grandes": "2-6-alta"}


def para_original(e, claude):
    o = {k: v for k, v in e.items() if k != "f0"}
    if "niveis_acesso" in o:
        o["niveis_acesso"] = ANTIGO.get(o["niveis_acesso"], o["niveis_acesso"])
    o["claude_code"] = claude
    o["cliente_pouca_disponibilidade"] = False
    return o


def venda(p):
    return math.ceil(math.ceil(p - 1e-9) / 2) * 2


def rodar(mod, e):
    try:
        with redirect_stdout(io.StringIO()):
            r = mod.calcular(copy.deepcopy(e))
    except Exception as erro:  # EntradaInvalida das versões novas, KeyError da original
        primeira = str(erro).splitlines()
        return {"status": "ERRO DE ENTRADA", "detalhe": " | ".join(l.strip(" -") for l in primeira[1:4]) or repr(erro)}
    if r.get("rejeicoes"):
        return {"status": "REJEITADO", "detalhe": r["rejeicoes"][0]}
    fases = {k.split()[0]: tuple(round(x, 2) for x in v) for k, v in r["fases"].items()}
    return {
        "status": "PARADO" if r["paradas"] else "ok",
        "faixa": (round(r["otimista"], 1), round(r["provavel"], 1), round(r["conservador"], 1)),
        "venda": venda(r["provavel"]),
        "fases": fases,
        "paradas": r["paradas"],
        "alertas": r["alertas"],
        "internos": r.get("avisos_internos", []),
    }


VERSOES = [
    ("Original (sem Claude Code)", lambda e: rodar(ORIG, para_original(e, False))),
    ("Original (com Claude Code, padrão)", lambda e: rodar(ORIG, para_original(e, True))),
    ("v1 (patch de 21/10)", lambda e: rodar(V1, e)),
    ("v2 (corrigida, valores provisórios)", lambda e: rodar(V2M, e)),
    ("v2 + sugestões D2/D3", lambda e: rodar(V2S, e)),
]

saida = []
for titulo, e in CASOS:
    linha = {"caso": titulo, "resultados": {}}
    for nome, f in VERSOES:
        linha["resultados"][nome] = f(e)
    saida.append(linha)

print(json.dumps(saida, ensure_ascii=False, indent=1))
