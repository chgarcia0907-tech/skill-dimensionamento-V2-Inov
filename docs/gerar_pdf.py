import datetime as dt
import sys

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

OUT = sys.argv[1]
F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("UI", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("UI-B", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("UI-SB", F + "seguisb.ttf"))
pdfmetrics.registerFont(TTFont("UI-L", F + "segoeuil.ttf"))
pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-B", italic="UI", boldItalic="UI-B")

TXT = colors.HexColor("#37352F")
MUTED = colors.HexColor("#787774")
LINE = colors.HexColor("#E9E9E7")
BLUE_BG = colors.HexColor("#E7F3F8")
BLUE = colors.HexColor("#2E7BB4")
GREEN = colors.HexColor("#448361")
GREEN_BG = colors.HexColor("#EDF3EC")
YEL = colors.HexColor("#CB912F")
YEL_BG = colors.HexColor("#FBF3DB")
RED = colors.HexColor("#D44C47")
RED_BG = colors.HexColor("#FDEBEC")
GREY_BG = colors.HexColor("#F7F6F3")

st = {
    "title": ParagraphStyle("t", fontName="UI-B", fontSize=28, leading=34, textColor=TXT, spaceAfter=10),
    "h1": ParagraphStyle("h1", fontName="UI-SB", fontSize=17, leading=22, textColor=TXT, spaceBefore=16, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="UI-SB", fontSize=12.5, leading=16, textColor=TXT, spaceBefore=10, spaceAfter=4, keepWithNext=1),
    "p": ParagraphStyle("p", fontName="UI", fontSize=10, leading=14.5, textColor=TXT, spaceAfter=5, alignment=TA_LEFT),
    "small": ParagraphStyle("s", fontName="UI", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": ParagraphStyle("c", fontName="UI", fontSize=8.8, leading=11.5, textColor=TXT),
    "cellb": ParagraphStyle("cb", fontName="UI-SB", fontSize=8.8, leading=11.5, textColor=TXT),
    "toc": ParagraphStyle("toc", fontName="UI", fontSize=9.5, leading=15, textColor=MUTED),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=8.8, leading=12, textColor=TXT),
}


def P(t, s="p"):
    return Paragraph(t, st[s])


def bullets(items, s="p"):
    return ListFlowable(
        [ListItem(P(i, s), leftIndent=12, value="•") for i in items],
        bulletType="bullet", start="•", leftIndent=12, bulletFontName="UI", bulletFontSize=9,
        bulletColor=TXT,
    )


def callout(html, bg=BLUE_BG, bar=None):
    t = Table([[P(html)]], colWidths=[170 * mm])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if bar:
        style.append(("LINEBEFORE", (0, 0), (0, -1), 3, bar))
    t.setStyle(TableStyle(style))
    return t


def table(rows, widths, header=True, zebra=False, bold_last=False):
    data = []
    for r, row in enumerate(rows):
        s = "cellb" if (header and r == 0) or (bold_last and r == len(rows) - 1) else "cell"
        data.append([c if not isinstance(c, str) else P(c, s) for c in row])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), GREY_BG))
    if bold_last:
        style.append(("BACKGROUND", (0, -1), (-1, -1), GREY_BG))
    t.setStyle(TableStyle(style))
    return t


def tag(text, fg, bg):
    return f'<font backColor="{bg.hexval().replace("0x", "#")}" color="{fg.hexval().replace("0x", "#")}">&nbsp;{text}&nbsp;</font>'


OK = tag("OK", GREEN, GREEN_BG)
REV = tag("Revisar", YEL, YEL_BG)
STOP = tag("Parado", RED, RED_BG)


def icon():
    d = Drawing(34, 34)
    d.add(Rect(0, 0, 34, 34, rx=7, ry=7, fillColor=BLUE_BG, strokeColor=None))
    d.add(Rect(7, 13, 20, 8, fillColor=YEL, strokeColor=None))
    for i, x in enumerate(range(9, 27, 3)):
        d.add(Line(x, 21, x, 18 if i % 2 else 16, strokeColor=TXT, strokeWidth=0.8))
    return d


def gantt():
    """Linha do tempo do Projeto A pela régua (central), com datas reais."""
    inicio = dt.date(2026, 7, 20)
    fases = [
        ("F1 Imersão e setup", 2, BLUE),
        ("F2 Acesso e login", 1, BLUE),
        ("F3 Desenvolvimento", 5, GREEN),
        ("Semana off", 1, colors.HexColor("#C9C7C2")),
        ("F3 Desenvolvimento (cont.)", 1.5, GREEN),
        ("F4 Testes com cliente", 1.5, YEL),
        ("F5 Deploy + arredondamento", 1, RED),
    ]
    total = 13
    W, label_w, row_h = 480, 140, 17
    H = row_h * len(fases) + 40
    d = Drawing(W, H)
    scale = (W - label_w - 5) / total
    top = H - 22
    for w in range(total + 1):
        x = label_w + w * scale
        d.add(Line(x, 8, x, top + 4, strokeColor=LINE, strokeWidth=0.5))
        if w < total - 1 and w % 2 == 0:
            data = inicio + dt.timedelta(weeks=w)
            d.add(String(x + 1, top + 8, data.strftime("%d/%m"), fontName="UI", fontSize=6.5, fillColor=MUTED))
    d.add(String(W - 30, top + 8, "19/10", fontName="UI-SB", fontSize=6.5, fillColor=TXT))
    pos = 0
    for i, (nome, dur, cor) in enumerate(fases):
        y = top - (i + 1) * row_h
        d.add(String(0, y + 4, nome, fontName="UI", fontSize=7.5, fillColor=TXT))
        d.add(Rect(label_w + pos * scale, y + 2, dur * scale, row_h - 6, rx=2, ry=2, fillColor=cor, strokeColor=None))
        sem = f"{str(dur).replace('.', ',').rstrip('0').rstrip(',') if isinstance(dur, float) else dur} sem"
        d.add(String(label_w + pos * scale + 3, y + 5.5, sem, fontName="UI-SB", fontSize=6.5, fillColor=colors.white))
        pos += dur
    return d


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("UI", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "Dimensionamento NTec — Skill · v1 · 16/10/2026")
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


s = []
s += [icon(), Spacer(1, 8), P("Dimensionamento NTec — Skill", "title")]
s.append(callout(
    "<b>Para que serve este documento:</b> explicar o que tem na skill <b>dimensionamento-ntec</b>, "
    "como ela chega a uma <b>faixa de semanas</b> e como o coordenador de negócios (CN) usa no dia a dia. "
    "<br/><b>Para quem:</b> CNs e área de projetos do Núcleo de Tecnologia. A skill não substitui a "
    "validação da área de projetos: ela evita que chegue à equipe um prazo \"nada a ver\"."
))
s.append(Spacer(1, 10))
toc = ["1. O que é a skill", "2. Como acessar e usar", "3. Arquitetura (o que tem dentro)",
       "4. Procedimento", "5. Régua de dimensionamento (F1 a F6)", "6. Buffer de risco adaptável",
       "7. Faixa final e negociação", "8. Perguntas para o CN", "9. Calibração com projetos reais",
       "10. Linha do tempo de exemplo (Projeto A)", "11. Parar e sinalizar", "12. Histórico, datas e pendências"]
for t in toc:
    s.append(P(t, "toc"))

# 1
s.append(P("1. O que é a skill", "h1"))
s.append(P("Uma skill do Claude que transforma o que o CN levantou com o cliente (formulário "
           "<i>Dimensionamento Tec</i>, ficha de qualificação, briefing ou transcrição de call) numa faixa "
           "de semanas calibrada nos projetos reais do NTec. A arquitetura segue a skill de dimensionamento "
           "do NCiv (Gabrielle Lobo). A estrutura de fases segue o formulário Dimensionamento Tec."))
s.append(bullets([
    "<b>Entrega três números:</b> otimista (piso), provável (recomendado) e conservador (teto de risco), em semanas e sprints de 2 semanas.",
    "<b>Pergunta em linguagem de negócio</b> o que falta, e traduz a resposta para os fatores técnicos.",
    "<b>Mostra o que cortar</b> quando o cliente quer menos prazo, com quantas semanas cada corte economiza.",
    "<b>Gera um bloco pronto</b> para colar nas seções 7 (Baseline) e 8 (Buffer) do formulário.",
]))

# 2
s.append(P("2. Como acessar e usar", "h1"))
s.append(bullets([
    "<b>Pelo nome:</b> em qualquer conversa do Claude Code, digitar <font name='Courier'>/dimensionamento-ntec</font> e colar o formulário, a ficha ou a transcrição.",
    "<b>Pedindo direto:</b> \"dimensiona esse projeto\", \"cabe em 12 semanas?\", \"isso é viável?\". A skill é acionada sozinha.",
    "<b>Onde está instalada:</b> <font name='Courier'>~\\.claude\\skills\\dimensionamento-ntec\\</font> (pasta pessoal; vale para qualquer projeto).",
    "<b>Cópia de trabalho (para editar e versionar):</b> <font name='Courier'>Projetos\\skill-dimensionamento-ntec\\</font>. As duas cópias não se sincronizam sozinhas.",
    "<b>No claude.ai:</b> compactar a pasta em .zip e enviar em Settings → Capabilities → Skills.",
]))

# 3
s.append(P("3. Arquitetura (o que tem dentro)", "h1"))
s.append(P("Igual à skill do NCiv: um arquivo curto que coordena, e arquivos de conhecimento lidos só quando precisa."))
s.append(table([
    ["Arquivo", "O que faz", "Quando é lido"],
    ["SKILL.md", "Orquestrador: procedimento, regras gerais, quando parar e o formato fixo da resposta", "Sempre"],
    ["insumos-e-perguntas.md", "Como ler o que o CN mandou, perguntas prontas e tradução negócio → técnico", "Sempre, primeiro"],
    ["regua-dimensionamento.md", "Pesos de cada fase (F1 a F6), buffer, faixa final, calibração e fontes", "Sempre"],
    ["regra-fronteira-e-faixa.md", "Desempate quando um fator cabe em duas linhas; o que fazer quando o cliente pede menos prazo", "Em caso de dúvida ou negociação"],
    ["scripts/calcular_faixa.py", "Faz a conta (fonte da verdade dos pesos), para o número não sair de cabeça", "Sempre"],
    ["exemplos/", "Precedentes reais (Projeto A, Projeto B, Projeto C, Projeto D), Projetos E e F pendentes e um caso fictício completo", "Para comparar com projeto parecido"],
], [45, 90, 35]))

# 4
s.append(P("4. Procedimento", "h1"))
s.append(ListFlowable([ListItem(P(t), leftIndent=14) for t in [
    "<b>Ler a entrada</b> e separar o que é fato declarado do que é palpite (cada dado leva a origem).",
    "<b>Preencher os fatores</b> da régua. O que faltar vira pergunta para o CN (até 5 por rodada, as que mais mexem no prazo primeiro). Sem resposta, usar o valor mais pesado e registrar em Suposições.",
    "<b>Rodar o script</b> com os fatores e obter as fases em mínimo, central e máximo.",
    "<b>Comparar com o precedente</b> mais parecido. Diferença acima de 30% precisa de explicação.",
    "<b>Aplicar a regra de fronteira</b> se precisar, e responder no formato fixo: status, prazo em uma frase, faixa, resumo, pontos de atenção, perguntas, detalhamento, precedente, o que cortar, bloco do formulário e observações.",
]], bulletType="1", leftIndent=14, bulletFontName="UI", bulletFontSize=9.5))

# 5
s.append(PageBreak())
s.append(P("5. Régua de dimensionamento (F1 a F6)", "h1"))
s.append(P("Cada linha tem <b>mínimo / central / máximo</b> em semanas. Os pesos já consideram o time típico do NTec "
           "(empresa júnior, 3 a 4 h/dia, sprints de 2 semanas, template Next.js + Expo + MongoDB + Better Auth). "
           "Login com Google, e-mail e upload para S3 já vêm no template e não somam prazo."))
s.append(P("F1 — Imersão, refinamento, setup e acessos (teto 4)", "h2"))
s.append(table([
    ["Fator", "Mín", "Central", "Máx"],
    ["Base (sempre)", "1,5", "2", "2,5"],
    ["Demanda pouco detalhada (sem requisitos nem protótipo)", "+0,5", "+1", "+1"],
    ["Setor ou produto atípico (sem benchmark)", "+0,5", "+0,5", "+1"],
    ["Stack fora do template NTec", "+1", "+1,5", "+2"],
], [110, 20, 20, 20]))
s.append(P("F2 — Infra, níveis de acesso, cadastro e login (teto 4)", "h2"))
s.append(table([
    ["Níveis de acesso / multitenancy", "Mín", "Central", "Máx"],
    ["Nenhum (sem login nem backend)", "0", "0", "0"],
    ["1 nível", "0,5", "0,5", "1"],
    ["2 a 6, poucas diferenças", "0,5", "1", "1,5"],
    ["2 a 6, grandes diferenças (telas e regras próprias, aprovação de cadastro)", "1,5", "2", "2,5"],
    ["6 ou mais", "2,5", "3", "4"],
    ["Multitenancy: dados separados, não isolados", "+0,5", "+0,5", "+1"],
    ["Multitenancy: isolamento de dados", "+1", "+1,5", "+2"],
    ["Multitenancy: instâncias com regras isoladas por cliente", "Parado", "—", "—"],
], [110, 20, 20, 20]))
s.append(P("F3 — Desenvolvimento", "h2"))
s.append(P("<b>Fluxo crítico</b> = jornada completa que, se quebrar, torna o produto inútil. Ex.: \"o cidadão fotografa "
           "a espécie, o app pega a localização e o registro aparece no mapa\". O núcleo é multiplicado pelo "
           "fator de formato: <b>Web x1,0 · WebApp/PWA x1,1 · App nativo x1,2 · +0,1 por formato extra em código separado</b>."))
s.append(table([
    ["Item", "Mín", "Central", "Máx"],
    ["Cada fluxo crítico comum (CRUD, listagem, mapa com filtros, agenda)", "1", "1,25", "1,5"],
    ["Cada fluxo com regra de negócio específica (fórmula, cálculo que não pode errar)", "2", "3", "4"],
    ["Cada feature atípica (sem benchmark)", "1", "1,5", "2"],
    ["Integração unidirecional, API documentada", "+0,5", "+0,5", "+1"],
    ["Integração bidirecional, API documentada", "+0,5", "+1", "+1,5"],
    ["Integração unidirecional, sem documentação", "+1", "+1,5", "+2"],
    ["Integração bidirecional, sem documentação", "+1,5", "+2,5", "+3,5"],
    ["Integração bidirecional sem API", "Parado", "—", "—"],
    ["Dependência de dados (planilhas, CSV, tabelas externas) — chamar núcleo de Dados", "+1", "+1,5", "+2"],
    ["Offline com sincronização (offline só local = 0)", "+1,5", "+2", "+3"],
    ["Volume de uso alto (milhares simultâneos)", "+1", "+1,5", "+2"],
], [110, 20, 20, 20]))
s.append(P("F4, F5 e F6 — Testes, deploy e lojas", "h2"))
s.append(table([
    ["Fase / fator", "Mín", "Central", "Máx"],
    ["F4 Testes com cliente — base (teto 4)", "1", "1,5", "2"],
    ["F4 + regra de negócio crítica (saúde, dinheiro, legal)", "+0,5", "+0,5", "+1"],
    ["F4 + cliente com pouca disponibilidade para validar", "+0,5", "+0,5", "+1"],
    ["F5 Deploy web (infra NTec)", "0,5", "0,5", "1"],
    ["F5 Deploy de app sem web / app junto com web", "0,5 / +0", "0,5 / +0,5", "1 / +0,5"],
    ["F5 + infra ou regras de deploy do cliente", "+1", "+1", "+2"],
    ["F6 Lojas — app comum", "2", "2,5", "4"],
    ["F6 Lojas — app sensível (saúde, finanças, infantil)", "2,5", "3", "6"],
], [110, 20, 20, 20]))
s.append(Spacer(1, 4))
s.append(P("Semanas off (férias, provas, recessos) e a garantia gratuita de 30 dias ficam fora da régua: as semanas off são somadas depois, pelo calendário.", "small"))

# 6
s.append(P("6. Buffer de risco adaptável", "h1"))
s.append(P("Aplicado sobre o central e o máximo (o otimista não leva buffer). <b>Não aplicar só \"porque o time é júnior\"</b>: isso já está nos pesos."))
s.append(table([
    ["Risco", "Buffer"],
    ["Maioria do time no primeiro projeto (menos de 6 meses de prática)", "+10%"],
    ["Troca ou saída de membros prevista durante o projeto", "+10% a +20%"],
    ["Terceiros envolvidos (outro fornecedor, entrega externa)", "+10%"],
    ["3 ou mais integrações fora do template", "+10% (automático)"],
    ["Teto — acima disso, a área de projetos revisa", "30%"],
], [130, 40]))

# 7
s.append(PageBreak())
s.append(P("7. Faixa final e negociação", "h1"))
s.append(table([
    ["Cenário", "Conta", "Para que serve"],
    ["<b>Otimista (piso)</b>", "Soma dos mínimos", "Nunca vender abaixo disto"],
    ["<b>Provável (recomendado)</b>", "Soma dos centrais × (1 + buffer)", "O valor para a proposta"],
    ["<b>Conservador (teto)</b>", "Soma dos máximos × (1 + buffer)", "O que acontece se os riscos se confirmarem"],
], [45, 65, 60]))
s.append(Spacer(1, 4))
s.append(P("Semanas são sempre arredondadas para cima. A <b>recomendação de venda</b> é o provável fechado em sprints inteiras (número par de semanas), mais as semanas off."))
s.append(P("Quando o cliente pede menos prazo", "h2"))
s.append(table([
    ["Prazo pedido", "Status", "O que fazer"],
    ["Igual ou acima do provável", OK and P(OK, "cell"), "Vender"],
    ["Entre o otimista e o provável", P(REV, "cell"), "Só com escopo congelado em contrato e cliente disponível; propor 1 ou 2 cortes"],
    ["Abaixo do otimista", P(STOP, "cell"), "Não vender o prazo: negociar escopo e recalcular sem os itens cortados"],
], [50, 25, 95]))
s.append(P("Cortes que mais economizam", "h2"))
s.append(table([
    ["Corte", "Economia típica (central)"],
    ["Publicar como PWA em vez de app nas lojas", "F6 inteira (2,5 a 3) + fator de formato"],
    ["Tirar o segundo formato do MVP (só app ou só web)", "~10% do desenvolvimento + parte do deploy"],
    ["Juntar perfis de usuário", "0,5 a 1 em F2"],
    ["Mover fluxos não essenciais para uma fase 2", "1,25 por fluxo comum; 3 por fluxo com regra específica"],
    ["Trocar integração automática por importação manual no MVP", "0,5 a 2,5"],
], [95, 75]))
s.append(P("Na dúvida entre duas linhas da régua, a skill vai sempre para a mais pesada, com um comentário de duas linhas "
           "explicando o ajuste (máximo de 3 ajustes por projeto). O histórico do NTec é vender para menos.", "small"))

# 8
s.append(P("8. Perguntas para o CN", "h1"))
s.append(P("A skill faz estas perguntas, prontas para repassar ao cliente, quando o fator não está claro:"))
s.append(table([
    ["Fator", "Pergunta"],
    ["Fluxos críticos", "Quais são as 3 a 6 coisas principais que alguém faz no sistema, do começo ao fim?"],
    ["Regra de negócio", "Tem algum cálculo ou regra que, se errar, causa prejuízo, risco à saúde ou problema legal? Já existe escrito?"],
    ["Formato", "Vão usar pelo navegador, por um app da loja, ou os dois? Precisa estar na App Store / Play Store?"],
    ["Níveis de acesso", "Quantos tipos de pessoa usam? Cada tipo vê telas diferentes? Alguém aprova o cadastro de outro?"],
    ["Integrações", "Precisa conversar com outro sistema? Só puxa, só manda ou os dois? Esse sistema tem documentação (link)?"],
    ["Offline", "Precisa funcionar sem internet? Quando a internet volta, os dados precisam subir para algum lugar?"],
    ["Multitenancy", "Várias empresas vão usar? Cada uma tem regras próprias, ou só não pode ver os dados da outra?"],
    ["Disponibilidade", "Quem vai testar e aprovar as entregas? Tem umas 2 horas por semana para isso?"],
], [32, 138]))

# 9
s.append(PageBreak())
s.append(P("9. Calibração com projetos reais", "h1"))
s.append(P("A régua foi rodada sobre os projetos do NTec com dados levantados no Notion (estado em 16/10/2026). "
           "Faixa = otimista / provável / conservador, em semanas."))
s.append(table([
    ["Projeto", "Formato", "Início → fim previsto", "Vendido", "Faixa da régua", "Situação", "Leitura"],
    ["Projeto A", "PWA", "20/07/2026 → 19/10/2026", "12 (+1 off)", "9 / <b>12</b> / 16", "Finalizando, no prazo", P(OK, "cell")],
    ["Projeto D", "App + web", "27/07/2026 → 23/11/2026", "18 (+3 off)", "13 / <b>17→18</b> / 23", "Execução, 47,6%, sem atraso", P(OK, "cell")],
    ["Projeto C", "Web + app", "13/04/2026 → 10/07/2026", "11 (+2 off)", "13 / <b>18</b> / 23", "Entregue com atraso (~14 sem)", P(REV, "cell")],
    ["Projeto B", "App nativo", "01/09/2026 → 23/11/2026", "12 (+1 off)", "11 / <b>15→16</b> / 23", "Execução, 45,2%", P(REV, "cell")],
    ["Projeto E", "?", "20/07/2026 → 15/01 ou 15/02/2027", "34", "não calibrado", "Execução, 37%", "—"],
    ["Projeto F", "?", "22/04/2026 → 06/01/2027 ou 25/10/2026", "38 (+3 off)", "não calibrado", "Execução, 58,7%", "—"],
], [20, 18, 34, 18, 26, 30, 24]))
s.append(Spacer(1, 6))
s.append(bullets([
    "<b>Projeto A e Projeto D:</b> a recomendação da régua bate com o vendido, e os dois estão no prazo.",
    "<b>Projeto C:</b> vendido abaixo do piso (11 contra 13) e atrasou. A régua ficou ~3 semanas acima do real, porque o time juntou setup e login em 2 semanas. É um viés conhecido, não corrigido com um único projeto.",
    "<b>Projeto B:</b> vendido entre o piso e o provável. O hand-off já registrava o prazo como apertado. Resultado a confirmar em 23/11/2026.",
    "<b>Projetos E e F:</b> sem ficha técnica. Por isso, todo provável acima de <b>26 semanas</b> sai com alerta de \"fora da faixa calibrada\".",
]))

# 10
s.append(P("10. Linha do tempo de exemplo (Projeto A)", "h1"))
s.append(P("As fases no valor central da régua, encaixadas no calendário real do projeto: início em 20/07/2026, 12 semanas de trabalho "
           "+ 1 semana off entre a S4 e a S5, fim previsto em 19/10/2026."))
s.append(gantt())
s.append(P("Datas no topo = segunda-feira de cada sprint. A barra de deploy inclui o arredondamento de 11,5 para 12 semanas.", "small"))

# 11
s.append(P("11. Parar e sinalizar", "h1"))
s.append(P("A skill não decide sozinha nestes casos. Ela marca e devolve para a área de projetos:"))
s.append(bullets([
    f"{STOP} Multitenancy com instâncias e regras isoladas por cliente (\"beira o inviável\").",
    f"{STOP} Integração bidirecional sem API.",
    f"{STOP} Feature atípica sem benchmark e sem documentação (pode exigir prova de conceito).",
    f"{REV} Dependência de dados de bases soltas → chamar o núcleo de Dados.",
    f"{REV} Provável acima de 26 semanas (fora da faixa calibrada) → considerar quebrar em fases.",
    f"{REV} Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.",
    f"{REV} Divergência entre o que o CN declarou e o que aparece nos documentos ou na call.",
    f"{REV} Teto de fase atingido ou buffer acima de 30%.",
]))

# 12
s.append(P("12. Histórico, datas e pendências", "h1"))
s.append(table([
    ["Data", "O que aconteceu"],
    ["13/04/2026", "Início do Projeto C (primeiro projeto da base de calibração)"],
    ["10/07/2026", "Deploy do Projeto C, com atraso: 11 semanas vendidas, ~14 realizadas"],
    ["20/07/2026", "Início do Projeto A e do Projeto E"],
    ["01/09/2026", "Início do Projeto B"],
    ["16/10/2026", "Leitura da skill do NCiv, do formulário Dimensionamento Tec e do levantamento no Notion; criação e calibração da skill (v1); instalação em ~/.claude/skills"],
    ["19/10/2026", "Fim previsto do Projeto A — confirmar se a calibração continua valendo"],
    ["23/11/2026", "Fim previsto do Projeto B e do Projeto D — atualizar a calibração com o realizado"],
], [28, 142]))
s.append(P("Pendências", "h2"))
s.append(bullets([
    "Fichas técnicas de Projetos E e F, para calibrar projetos grandes (o levantamento recebido veio cortado).",
    "Conteúdo da subpágina \"Régua de Dimensionamento\" do Notion, citada no formulário mas não incluída no PDF. Se tiver números, eles valem mais que os da skill.",
    "Conferir no hand-off do Projeto D os fatores marcados como palpite (perfis, fluxos, offline).",
    "Preencher as retrospectivas: hoje quase todas estão vazias, e sem elas o buffer não tem base histórica.",
]))
s.append(Spacer(1, 6))
s.append(callout("<b>Manutenção:</b> pesos mudam no <font name='Courier'>scripts/calcular_faixa.py</font> <b>e</b> na "
                 "<font name='Courier'>regua-dimensionamento.md</font>, com uma linha no Registro das fontes. Quando um projeto "
                 "termina, ele entra em <font name='Courier'>exemplos/</font> com vendido × realizado.", GREY_BG))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                        bottomMargin=20 * mm, title="Dimensionamento NTec — Skill", author="NTec · Poli Júnior")
doc.build(s, onFirstPage=rodape, onLaterPages=rodape)
print("ok", OUT)
