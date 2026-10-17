"""Gera a Proposta Técnica do NTec em PDF, no template oficial do núcleo.

Uso:
    python gerar_proposta.py proposta.json [--saida PASTA]

A entrada é um JSON com as 14 seções do template e o bloco `dimensionamento`
(ver `proposta-tecnica.md` e `exemplos/ficticio-petagenda-proposta.json`).
A faixa de semanas NÃO é digitada: o script roda `calcular_faixa.calcular`
sobre `dimensionamento.entrada`, para que a proposta e a régua nunca divirjam.

Saída: "[Proposta Técnica] {projeto}.pdf" e, no terminal, a faixa e o
resultado do checklist final do template.

Precisa de `reportlab` (pip install reportlab).
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calcular_faixa import calcular, fmt, semanas, sprints  # noqa: E402

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        KeepTogether, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
    )
except ImportError:
    sys.exit("Erro: falta o reportlab. Instale com: pip install reportlab")

# ---------------------------------------------------------------- aparência
NAVY = colors.HexColor("#17344F")
ORANGE = colors.HexColor("#D9782D")
TXT = colors.HexColor("#2B2B2B")
MUTED = colors.HexColor("#7A8794")
LINE = colors.HexColor("#D9DEE3")
BOX_BG = colors.HexColor("#EEF2F6")
WARN_BG = colors.HexColor("#FDF3E7")
HEAD_BG = colors.HexColor("#E4EAF0")
OK = colors.HexColor("#3D7A55")
BAD = colors.HexColor("#C0453B")

FONTES = [
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]
F, FB = "Helvetica", "Helvetica-Bold"
for normal, negrito in FONTES:
    if os.path.exists(normal) and os.path.exists(negrito):
        pdfmetrics.registerFont(TTFont("Prop", normal))
        pdfmetrics.registerFont(TTFont("Prop-B", negrito))
        pdfmetrics.registerFontFamily("Prop", normal="Prop", bold="Prop-B", italic="Prop", boldItalic="Prop-B")
        F, FB = "Prop", "Prop-B"
        break

ST = {
    "h1": ParagraphStyle("h1", fontName=FB, fontSize=13.5, leading=17, textColor=NAVY, spaceBefore=12, spaceAfter=2),
    "h2": ParagraphStyle("h2", fontName=FB, fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=6, spaceAfter=2),
    "p": ParagraphStyle("p", fontName=F, fontSize=9.3, leading=13.2, textColor=TXT, spaceAfter=3),
    "cell": ParagraphStyle("c", fontName=F, fontSize=8.4, leading=11, textColor=TXT),
    "cellh": ParagraphStyle("ch", fontName=FB, fontSize=8.4, leading=11, textColor=NAVY),
    "small": ParagraphStyle("s", fontName=F, fontSize=8, leading=10.5, textColor=MUTED),
    "box": ParagraphStyle("b", fontName=F, fontSize=9, leading=12.6, textColor=TXT),
}

OBRIGATORIAS = {4, 6, 8, 10, 11, 14}
STATUS = {  # (selo, cor, texto) — selo em texto porque as fontes do PDF não têm emoji
    "pronto": ("PRONTO", "#3D7A55", "Pronto para proposta"),
    "atencao": ("REVISÃO", "#D9782D", "Precisa de revisão da área de projetos"),
    "preliminar": ("PRELIMINAR", "#D9782D", "Estimativa preliminar, sem PRD"),
    "parado": ("PARADO", "#C0453B", "Restrição técnica ou possível inviabilidade"),
}


def inline(t):
    """Escapa o texto e converte **negrito**."""
    t = str(t if t is not None else "")
    if F == "Helvetica":  # fonte sem glifos fora do Latin-1
        t = t.replace("→", "->").replace("✅", "[OK]").replace("⚠️", "[!]").replace("🚩", "[PARADO]")
        t = t.encode("latin-1", "replace").decode("latin-1")
    else:  # Arial/DejaVu não têm emoji
        t = t.replace("✅", "").replace("⚠️", "").replace("🚩", "").strip()
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def P(t, s="p"):
    return Paragraph(inline(t), ST[s])


def bullets(itens):
    return ListFlowable(
        [ListItem(P(i), leftIndent=10, value="•") for i in itens],
        bulletType="bullet", start="•", leftIndent=10, bulletFontName=F, bulletFontSize=8, bulletColor=TXT,
    )


def tabela(cab, linhas, larguras):
    total = 174 * mm
    w = [total * x for x in larguras]
    dados = [[P(c, "cellh") for c in cab]] + [[P(c, "cell") for c in l] for l in linhas]
    t = Table(dados, colWidths=w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def caixa(conteudo, fundo=BOX_BG, barra=NAVY):
    t = Table([[conteudo]], colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fundo),
        ("LINEBEFORE", (0, 0), (0, -1), 3, barra),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def titulo(n, texto):
    selo = ' <font backColor="#D9782D" color="white" size="6.5">&nbsp;OBRIGATÓRIO&nbsp;</font>' if n in OBRIGATORIAS else ""
    h = Paragraph(f"{n}. {inline(texto)}{selo}" if n else inline(texto), ST["h1"])
    linha = Table([[""]], colWidths=[174 * mm], rowHeights=[1])
    linha.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE)]))
    return [h, linha, Spacer(1, 3)]


def rotulados(pares):
    return [P(f"**{r}:** {t}") for r, t in pares]


def vazio(v):
    return v in (None, "", [], {})


# ---------------------------------------------------------------- checklist
def checklist(d, r):
    cab = d.get("cabecalho", {})
    pag = cab.get("prd_paginas")
    proto = d.get("prototipo", {})
    itens = []
    itens.append((
        "PRD (entre 5 e ~10 páginas) e protótipo anexados",
        bool(cab.get("prd_link")) and isinstance(pag, int) and 5 <= pag <= 12 and bool(cab.get("prototipo_link")),
    ))
    obrig = {
        4: d.get("perfis", {}).get("tabela"), 6: d.get("regras"), 8: d.get("seguranca"),
        10: d.get("roadmap"), 11: d.get("pontos_abertos"), 14: proto.get("tabela") or proto.get("declaracao"),
    }
    itens.append(("Todos os campos OBRIGATÓRIO preenchidos", all(not vazio(v) for v in obrig.values())))
    itens.append((
        "Protótipo segue as regras de negócio do PRD — ou as adaptações estão justificadas e claras para o MVP (seção 14)",
        bool(proto.get("recebido")) and not vazio(obrig[14]),
    ))
    cron = " ".join(str(s[1]) for s in d.get("cronograma", {}).get("sprints", [])).lower()
    fora = [l[1] for l in d.get("roadmap", []) if str(l[2]).lower() != "prioritário"]
    itens.append(("Roadmap e cronograma não se contradizem", not any(str(e).lower() in cron for e in fora)))
    itens.append((
        "Pontos em aberto (seção 11) listados explicitamente, não escondidos no meio do texto",
        not vazio(d.get("pontos_abertos")),
    ))
    itens.append((
        "Nenhuma dependência externa (API, fornecedor) tratada como certa sem confirmação",
        not d.get("dependencia_externa_sem_confirmacao", False),
    ))
    return itens


# ---------------------------------------------------------------- documento
def montar(d, r):
    s = []
    cab = d.get("cabecalho", {})
    dim = d.get("dimensionamento", {})
    venda = sprints(r["provavel"]) * 2

    selo, cor, texto = STATUS.get(d.get("status", "atencao"), STATUS["atencao"])
    s.append(caixa(Paragraph(
        f'<b>Status do dimensionamento:</b> <font backColor="{cor}" color="white" size="7">&nbsp;{inline(selo)}&nbsp;</font> '
        f"{inline(texto)}<br/>"
        + inline(f"**Prazo recomendado:** {venda} semanas ({venda // 2} sprints de 2 semanas), mais as semanas off. "
                 f"Faixa: otimista {semanas(r['otimista'])} · provável {semanas(r['provavel'])} · "
                 f"conservador {semanas(r['conservador'])} semanas. Detalhe no Anexo."), ST["box"])))
    s.append(Spacer(1, 6))
    pag = cab.get("prd_paginas")
    s.append(caixa(P(
        "**Pré-requisito para enviar à validação: documento de requisitos (PRD) + protótipo.** "
        f"PRD: {cab.get('prd_link') or 'não informado'}"
        f"{f' ({pag} páginas)' if pag else ''} · Protótipo: {cab.get('prototipo_link') or 'não informado'}", "box"),
        fundo=WARN_BG, barra=ORANGE))
    s.append(Spacer(1, 7))
    meta = [
        f"**Cliente/Projeto:** {cab.get('cliente_projeto', d.get('projeto', ''))}",
        f"**Responsável comercial:** {cab.get('responsavel_comercial') or '______'}",
        f"**Data de envio:** {cab.get('data_envio') or '______'}",
    ]
    s.append(Paragraph(" &nbsp;&nbsp;&nbsp; ".join(inline(m) for m in meta), ST["p"]))

    # 1
    s += titulo(1, "Problema que a solução resolve")
    pb = d.get("problema", {})
    if pb.get("dor"):
        s.append(P(pb["dor"]))
    s.append(bullets(pb.get("problemas", [])))
    # 2
    s += titulo(2, "Visão geral e princípios da solução")
    vg = d.get("visao_geral", {})
    s += rotulados([(k, vg[c]) for k, c in (("Tipo de aplicação", "tipo"), ("Público-alvo", "publico"),
                                             ("Proposta de valor", "proposta_valor")) if vg.get(c)])
    if vg.get("principios"):
        s.append(bullets(vg["principios"]))
    # 3
    s += titulo(3, "Entidades principais do sistema")
    en = d.get("entidades", {})
    s += rotulados([("Centrais", en.get("centrais", "")), ("De apoio", en.get("apoio", ""))])
    # 4
    s += titulo(4, "Perfis de acesso")
    pf = d.get("perfis", {})
    s.append(tabela(["Perfil", "O que faz", "Observações de permissão"], pf.get("tabela", []), [0.18, 0.45, 0.37]))
    if pf.get("matriz_permissoes"):
        s.append(Spacer(1, 3))
        s.append(P(f"**Matriz de permissões por ação:** {pf['matriz_permissoes']}"))
    # 5
    s += titulo(5, "Fluxo completo, etapa por etapa")
    linhas = []
    for i, e in enumerate(d.get("fluxo", []), 1):
        etapa = e.get("etapa", "")
        if e.get("pendente"):
            etapa += f" **[Decisão futura do cliente: {e['pendente']}]**"
        linhas.append([str(i), etapa, e.get("quem", ""), e.get("dados", ""), e.get("validacoes", "")])
    s.append(tabela(["#", "O que acontece", "Quem faz", "Dados que entram/saem", "Validações"], linhas,
                    [0.04, 0.34, 0.14, 0.26, 0.22]))
    # 6
    s += titulo(6, "Regras de negócio")
    s.append(tabela(["Regra", "O que garante"], d.get("regras", []), [0.5, 0.5]))
    # 7
    s += titulo(7, "Arquitetura / como o sistema é construído")
    s += rotulados(d.get("arquitetura", []))
    # 8
    s += titulo(8, "Segurança, dados e rastreabilidade")
    s += rotulados(d.get("seguranca", []))
    # 9
    s += titulo(9, "Módulos críticos (pagamentos, integrações externas, automações)")
    mods = d.get("modulos_criticos", [])
    if not mods:
        s.append(P("Não há módulo crítico de pagamento, integração externa ou automação no PRD."))
    for m in mods:
        bloco = [P(m.get("nome", ""), "h2"), bullets(m.get("detalhe", []))]
        bloco += rotulados([(k, m[c]) for k, c in (("Entra no MVP", "mvp"),
                                                    ("Futuro / dependente de terceiro", "futuro")) if m.get(c)])
        s.append(KeepTogether(bloco))
    # 10
    s += titulo(10, "Roadmap — MVP vs. futuro")
    s.append(tabela(["Fase", "Entrega", "Natureza"], d.get("roadmap", []), [0.2, 0.6, 0.2]))
    # 11
    s += titulo(11, "Pontos em aberto para validação conjunta")
    s.append(bullets(d.get("pontos_abertos", [])) if d.get("pontos_abertos") else
             P("**Alerta:** nenhum ponto em aberto listado."))
    # 12
    s += titulo(12, "Stack de execução proposta")
    st = d.get("stack", {})
    s += rotulados(st.get("itens", []))
    if st.get("nao_validado"):
        s.append(P("**Ainda não validado:**"))
        s.append(bullets(st["nao_validado"]))
    # 13
    s += titulo(13, "Cronograma sprint a sprint")
    cr = d.get("cronograma", {})
    linhas = [[str(x[0]), x[1] + (f" **[depende de: {x[2]}]**" if len(x) > 2 and x[2] else "")]
              for x in cr.get("sprints", [])]
    s.append(tabela(["Sprint", "Entregas previstas"], linhas, [0.16, 0.84]))
    s.append(Spacer(1, 3))
    s.append(P(f"**Duração total:** {venda} semanas, {venda // 2} sprints de 2 semanas"
               f"{', ' + cr['duracao_obs'] if cr.get('duracao_obs') else ''}."))
    # 14
    s += titulo(14, "Protótipo × regras de negócio")
    pr = d.get("prototipo", {})
    if pr.get("tabela"):
        s.append(tabela(["Tela/fluxo", "Regra do PRD", "Adaptação no protótipo", "Justificativa", "Vale para o MVP?"],
                        pr["tabela"], [0.18, 0.24, 0.22, 0.22, 0.14]))
    if pr.get("declaracao"):
        s.append(P(pr["declaracao"]))
    if not pr.get("recebido"):
        s.append(caixa(P("**Protótipo não recebido pela skill.** O comercial precisa preencher esta seção "
                         "antes de enviar para a validação.", "box"), fundo=WARN_BG, barra=ORANGE))

    # checklist
    s += titulo(0, "Checklist final antes de enviar (comercial)")
    for texto, ok in checklist(d, r):
        marca = ('<font backColor="#3D7A55" color="white" size="7">&nbsp;OK&nbsp;</font>' if ok
                 else '<font backColor="#C0453B" color="white" size="7">&nbsp;PENDENTE&nbsp;</font>')
        s.append(Paragraph(f"{marca} {inline(texto)}", ST["p"]))

    # anexo
    s += titulo(0, "Anexo — Memória do dimensionamento (para a validação técnica)")
    s.append(P("Calculado com a skill dimensionamento-ntec sobre o PRD. Sem buffer percentual: o risco está no "
               "intervalo mínimo / central / máximo de cada fase. Semanas off e garantia de 30 dias ficam fora da faixa.",
               "small"))
    s.append(P("Faixa de semanas", "h2"))
    s.append(tabela(["Cenário", "Semanas", "Sprints", "Quando acontece"], [
        ["Otimista (piso)", str(semanas(r["otimista"])), str(sprints(r["otimista"])),
         "Escopo congelado, cliente responde rápido. Não vender abaixo disto."],
        ["**Provável (recomendado)**", f"**{semanas(r['provavel'])}**", f"**{sprints(r['provavel'])}**",
         "O que costuma acontecer no NTec."],
        ["Conservador (teto de risco)", str(semanas(r["conservador"])), str(sprints(r["conservador"])),
         "Se os pontos em aberto e os riscos se confirmarem."],
    ], [0.27, 0.12, 0.12, 0.49]))
    s.append(P("Detalhamento por fase", "h2"))
    crit = dim.get("criterios", {})
    linhas = []
    for nome, (a, b, c) in r["fases"].items():
        linhas.append([nome, fmt(a), fmt(b), fmt(c), crit.get(nome.split()[0], "")])
    linhas.append(["**Total**", f"**{fmt(r['otimista'])}**", f"**{fmt(r['provavel'])}**",
                   f"**{fmt(r['conservador'])}**", f"Fator de formato no desenvolvimento: x{fmt(r['fator_formato'])}"])
    s.append(tabela(["Fase", "Mín", "Central", "Máx", "Critério"], linhas, [0.25, 0.07, 0.08, 0.07, 0.53]))
    if r["paradas"] or r["alertas"]:
        s.append(P("Alertas da régua", "h2"))
        s.append(bullets([f"**PARADO:** {p}" for p in r["paradas"]] + r["alertas"]))
    if dim.get("atencao"):
        s.append(P("Pontos de atenção", "h2"))
        s.append(bullets(dim["atencao"]))
    if dim.get("lacunas"):
        s.append(P("Lacunas para o CN", "h2"))
        s.append(tabela(["Fator", "Procurado e não achado", "Pergunta para o cliente", "Valor provisório"],
                        dim["lacunas"], [0.16, 0.24, 0.36, 0.24]))
    if dim.get("precedente"):
        s.append(P("Precedente", "h2"))
        s.append(P(dim["precedente"]))
    if dim.get("cortes"):
        s.append(P("O que cortar", "h2"))
        s.append(tabela(["Corte", "Economia estimada"], dim["cortes"], [0.72, 0.28]))
    for rot, chave in (("Suposições", "suposicoes"), ("Ajustes de fronteira", "fronteira"),
                       ("Pontos para a imersão", "imersao")):
        if dim.get(chave):
            s.append(P(rot, "h2"))
            s.append(bullets(dim[chave]))
    return s


def pagina(projeto):
    def desenhar(c, doc):
        w, h = A4
        c.saveState()
        if doc.page == 1:
            c.setFillColor(NAVY)
            c.rect(0, h - 45 * mm, w, 45 * mm, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#B8C4CF"))
            c.setFont(F, 7.5)
            c.drawString(18 * mm, h - 13 * mm, "PADRÃO DE DOCUMENTAÇÃO · NTEC")
            c.setFillColor(colors.white)
            c.setFont(FB, 19)
            c.drawString(18 * mm, h - 24 * mm, f"Proposta Técnica — {projeto}")
            c.setFont(F, 9)
            c.drawString(18 * mm, h - 32 * mm, "Comercial → Validação de Projeto" if F != "Helvetica"
                         else "Comercial -> Validação de Projeto")
            c.setStrokeColor(ORANGE)
            c.setLineWidth(2.2)
            c.line(18 * mm, h - 45 * mm, w - 18 * mm, h - 45 * mm)
        c.setFillColor(MUTED)
        c.setFont(F, 7.5)
        c.drawString(18 * mm, 10 * mm, f"NTEC · Proposta Técnica · {projeto}")
        c.drawRightString(w - 18 * mm, 10 * mm, f"Página {doc.page}")
        c.restoreState()
    return desenhar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proposta")
    ap.add_argument("--saida", default=None, help="pasta do PDF (padrão: a pasta do JSON)")
    a = ap.parse_args()
    with open(a.proposta, encoding="utf-8") as f:
        d = json.load(f)
    sys.stdout.reconfigure(encoding="utf-8")
    entrada = d.get("dimensionamento", {}).get("entrada")
    if not entrada:
        sys.exit("Erro: falta dimensionamento.entrada (o JSON da régua).")
    r = calcular(entrada)
    projeto = d.get("projeto", entrada.get("projeto", "Projeto"))
    pasta = a.saida or os.path.dirname(os.path.abspath(a.proposta))
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, f"[Proposta Técnica] {projeto}.pdf")
    doc = SimpleDocTemplate(destino, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=18 * mm, bottomMargin=17 * mm, title=f"Proposta Técnica — {projeto}",
                            author="NTEC")
    first_top = Spacer(1, 32 * mm)
    doc.build([first_top] + montar(d, r), onFirstPage=pagina(projeto), onLaterPages=pagina(projeto))

    venda = sprints(r["provavel"]) * 2
    print(f"PDF: {destino}")
    print(f"Faixa: otimista {semanas(r['otimista'])} · provável {semanas(r['provavel'])} · "
          f"conservador {semanas(r['conservador'])} · vender {venda} semanas ({venda // 2} sprints)")
    print("Checklist:")
    for texto, ok in checklist(d, r):
        print(f"  [{'x' if ok else ' '}] {texto}")
    if r["paradas"]:
        print("PARADO:", *r["paradas"], sep="\n  - ")


if __name__ == "__main__":
    main()
