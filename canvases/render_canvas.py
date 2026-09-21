#!/usr/bin/env python3
"""
canvases/render_canvas.py — A3-landscape canvas HTML in the DSH v2 library register.
Pure functions: canvas_html(c, watermark=False) -> str. build_canvases.py renders them.
"""
import html as H
import os, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
SITE = "dianasimpsonhernandez.com"
LIB = "frameworks.dianasimpsonhernandez.com"

def _b64(n): return base64.b64encode(open(os.path.join(FONTS, n), "rb").read()).decode()
FONT_CSS = None
def font_css():
    global FONT_CSS
    if FONT_CSS is None:
        FONT_CSS = (f"@font-face{{font-family:'Schibsted Grotesk';font-weight:400 900;src:url(data:font/woff2;base64,{_b64('SchibstedGrotesk-var.woff2')}) format('woff2')}}"
                    f"@font-face{{font-family:'Martian Mono';font-weight:100 800;src:url(data:font/woff2;base64,{_b64('MartianMono-var.woff2')}) format('woff2')}}")
    return FONT_CSS

# DSH mark (dot, rounded square, bar, diagonal) — stroke colour via currentColor
MARK = ('<svg viewBox="0 0 480 480" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><clipPath id="{id}"><rect x="13.5" y="91.5" width="283" height="284" rx="14"/></clipPath></defs>'
        '<g transform="translate(84.5 45)"><g clip-path="url(#{id})"><line x1="87.4" y1="91.5" x2="294.7" y2="376" stroke="currentColor" stroke-width="23"/></g>'
        '<rect x="13.5" y="91.5" width="283" height="284" rx="14" fill="none" stroke="currentColor" stroke-width="23"/>'
        '<line x1="85" y1="91.5" x2="85" y2="376" stroke="currentColor" stroke-width="23"/><circle cx="88" cy="33.5" r="31.5" fill="currentColor"/></g></svg>')
def mark(id="m"): return MARK.replace("{id}", id)

# simple 24px stroke icons
_I = {
 "frown": '<circle cx="12" cy="12" r="9"/><path d="M8.5 15.5c1-1.2 2.2-1.8 3.5-1.8s2.5.6 3.5 1.8"/><path d="M9 9.5h.01M15 9.5h.01"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "megaphone": '<path d="M4 10v4h3l8 4V6l-8 4H4z"/><path d="M18 9.5a3 3 0 010 5"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4V5z"/>',
 "puzzle": '<path d="M10 3h4v3a2 2 0 002 2h3v4h-3a2 2 0 00-2 2v3h-4v-3a2 2 0 00-2-2H5V8h3a2 2 0 002-2V3z"/>',
 "speech": '<path d="M5 4h14v10H11l-4 4v-4H5V4z"/><path d="M8 8h8M8 11h5"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3z"/>',
 "box": '<path d="M3 8l9-4 9 4v9l-9 4-9-4V8z"/><path d="M3 8l9 4 9-4M12 12v9"/>',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.5-7 10-7 10z"/>',
 "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "hand": '<path d="M7 11V6a1.5 1.5 0 013 0v5M10 10V4.5a1.5 1.5 0 013 0V11M13 10.5V6a1.5 1.5 0 013 0v6M16 12V9a1.5 1.5 0 013 0v5c0 4-3 7-7 7s-6-2-7.5-5L3 13a1.5 1.5 0 012.5-1.6L7 13"/>',
 "bubble": '<path d="M12 4c5 0 9 3 9 7s-4 7-9 7c-.8 0-1.6-.1-2.3-.2L5 20l1-3.2C4.1 15.5 3 13.4 3 11c0-4 4-7 9-7z"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
 "robot": '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
 "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 "brain": '<path d="M9 4a3 3 0 00-3 3v1a3 3 0 00-2 3 3 3 0 002 3v1a3 3 0 003 3h1V4H9zM15 4a3 3 0 013 3v1a3 3 0 012 3 3 3 0 01-2 3v1a3 3 0 01-3 3h-1V4h1z"/>',
 "plug": '<path d="M9 3v4M15 3v4M6 7h12v4a6 6 0 01-12 0V7zM12 17v4"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "people": '<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2.5 20c0-3.5 3-6 6.5-6s6.5 2.5 6.5 6M15.5 14c3 0 5.5 2 5.5 5"/>',
 "chart": '<path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3"/>',
 "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/>',
 "tools": '<path d="M14.5 4.5a4 4 0 00-4.9 5.2L3 16.3V21h4.7l6.6-6.6a4 4 0 005.2-4.9l-2.6 2.6-2.8-.7-.7-2.8 2.6-2.6z"/>',
}
def icon(name):
    return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{_I.get(name, _I["target"])}</svg>'

CSS = """
:root{--ink:#1A1633;--deep:#2A1B5E;--purple:#5B4BC4;--violet:#8A7BE8;--pop:#D9D1FF;--lilac:#F2EFFB;--line:#E3E0F0;--muted:#6E6A8A;--coral:#F96167;--coral-ink:#B3252B;
--sans:'Schibsted Grotesk',system-ui,sans-serif;--mono:'Martian Mono',ui-monospace,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:420mm;height:297mm;background:#fff}
body{font:9.2pt/1.35 var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.sheet{position:absolute;inset:0;padding:11mm 12mm 9mm;display:flex;flex-direction:column;gap:5mm}
header{display:flex;align-items:flex-end;justify-content:space-between;gap:10mm;padding-bottom:3.5mm;border-bottom:1.2pt solid var(--ink)}
header .t h1{font-size:23pt;font-weight:800;letter-spacing:-.025em;line-height:1}
header .t .sub{margin-top:2mm;font-size:10.5pt;color:var(--muted);font-weight:500}
header .t .eyebrow{font-family:var(--mono);font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--coral-ink);font-weight:500;margin-bottom:2.2mm}
header .t .eyebrow:before{content:'';display:inline-block;width:6mm;height:1.6pt;background:var(--coral);vertical-align:middle;margin-right:2.2mm}
header .brand{display:flex;align-items:center;gap:4mm;text-align:right}
header .brand svg{width:13mm;height:13mm;color:var(--ink)}
header .brand .n{font-weight:800;font-size:9.5pt;letter-spacing:-.01em;line-height:1.15}
header .brand .n small{display:block;font-family:var(--mono);font-size:6.2pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;margin-top:1mm}
main{flex:1;min-height:0;display:grid;gap:3.2mm}
.box{border:1pt solid var(--ink);border-radius:2.2mm;padding:3.4mm 3.8mm;display:flex;flex-direction:column;gap:1.6mm;min-width:0;min-height:0;position:relative;background:#fff}
.box .h{display:flex;align-items:center;gap:2.2mm;font-weight:800;font-size:10.2pt;letter-spacing:-.01em;line-height:1.1}
.box .h .ic{width:5.2mm;height:5.2mm;flex:0 0 auto;color:var(--purple)}
.box .n{position:absolute;top:2.6mm;right:3.2mm;font-family:var(--mono);font-size:6.4pt;color:var(--muted);letter-spacing:.06em}
.box ul{list-style:none;display:grid;gap:1.1mm}
.box li{color:#3A3560;font-size:8.3pt;padding-left:3.2mm;position:relative}
.box li:before{content:'';position:absolute;left:0;top:.52em;width:1.6mm;height:1.6mm;border-radius:50%;background:var(--violet)}
.box.star{background:var(--pop);border-color:var(--pop)}.box.star .h .ic{color:var(--coral-ink)}.box.star li:before{background:var(--coral)}
.box.dark{background:var(--deep);border-color:var(--deep);color:#fff}.box.dark .h{color:#fff}.box.dark .h .ic{color:var(--pop)}.box.dark li{color:#D8D2F5}.box.dark li:before{background:var(--coral)}.box.dark .n{color:#B6AEDD}
.box.lilac{background:var(--lilac);border-color:var(--lilac)}
.box .q{font-family:var(--mono);font-size:6.6pt;letter-spacing:.06em;text-transform:uppercase;color:var(--coral-ink);font-weight:500}
.box .space{flex:1}
footer{display:flex;justify-content:space-between;align-items:center;gap:8mm;padding-top:3mm;border-top:.6pt solid var(--line);font-family:var(--mono);font-size:6.6pt;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
footer b{color:var(--ink);font-weight:600}
footer .r{display:flex;gap:6mm;flex:0 0 auto}footer .r span{white-space:nowrap}footer>span:first-child{min-width:0}
/* watermark */
.wm{position:absolute;inset:0;pointer-events:none;z-index:5;overflow:hidden}
.wm .tile{position:absolute;inset:-40mm;background-image:url("data:image/svg+xml;utf8,__TILE__");background-size:38mm 38mm;opacity:.045;transform:rotate(-18deg)}
.wm .txt{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-18deg);font-family:var(--mono);font-weight:600;font-size:36pt;letter-spacing:.12em;color:var(--purple);opacity:.13;white-space:nowrap}
.wm .txt small{display:block;text-align:center;font-size:11pt;letter-spacing:.3em;margin-top:2mm}
"""

TILE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480"><defs><clipPath id="c"><rect x="13.5" y="91.5" width="283" height="284" rx="14"/></clipPath></defs><g transform="translate(84.5 45)" fill="none" stroke="%235B4BC4" stroke-width="23">'
            '<rect x="13.5" y="91.5" width="283" height="284" rx="14"/><line x1="85" y1="91.5" x2="85" y2="376"/><line x1="87.4" y1="91.5" x2="294.7" y2="376" clip-path="url(%23c)"/>'
            '<circle cx="88" cy="33.5" r="31.5" fill="%235B4BC4" stroke="none"/></g></svg>').replace('"', "'")

def watermark_html():
    return ('<div class="wm"><div class="tile"></div>'
            f'<div class="txt">{SITE}<small>free edition · canvas pack removes this</small></div></div>')

def box(b, cls="", n=None, icon_name=None, q=None, extra=""):
    ic = icon(icon_name or b.get("icon", "target"))
    lis = "".join(f"<li>{H.escape(p)}</li>" for p in b["prompts"])
    num = f'<span class="n">{n}</span>' if n else ""
    qq = f'<div class="q">{H.escape(q)}</div>' if q else ""
    return f'<div class="box {cls}" style="grid-area:{b["id"]}">{num}<div class="h">{ic}{H.escape(b["title"])}</div>{qq}<ul>{lis}</ul><div class="space"></div>{extra}</div>'

def header(c):
    return (f'<header><div class="t"><div class="eyebrow">DSH canvas · {H.escape(c["short"])} · v1 · {c["year"]}</div><h1>{H.escape(c["title"])}</h1>'
            f'<div class="sub">{H.escape(c["subtitle"])}</div></div>'
            f'<div class="brand"><div class="n">Diana Simpson-Hernandez<small>{SITE}</small></div>{mark("hm")}</div></header>')

def footer(c):
    return (f'<footer><span><b>{SITE}</b> · walkthrough guide and canvas pack at {LIB}/canvas/{c["slug"]}/</span>'
            f'<span class="r"><span>{H.escape(c["time"])} · {H.escape(c["tags"][0])}</span><span>© {c["year"]} Diana Simpson-Hernandez · free to use, not to resell</span></span></footer>')

# ── layouts ─────────────────────────────────────────────────────────────────
def grid9(c):
    B = {b["id"]: b for b in c["boxes"]}
    order = ["problem","customers","landscape","pov","frame","solution","name","advantage","model","lead"]
    css = "grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1.05fr .9fr;grid-template-areas:'problem customers landscape pov' 'frame solution name advantage' 'model model lead advantage'"
    out = []
    for i, k in enumerate(order, 1):
        cls = "star" if k == "advantage" else ("dark" if k == "lead" else ("lilac" if k == "pov" else ""))
        out.append(box(B[k], cls, n=f"{i:02d}"))
    return f'<main style="{css}">{"".join(out)}</main>'

def grid7(c):
    B = {b["id"]: b for b in c["boxes"]}
    icons = {"goal":"target","stakeholders":"people","user":"user","insights":"chart","strategy":"compass","principles":"shield","tactics":"tools"}
    css = "grid-template-columns:repeat(4,1fr);grid-template-rows:.8fr 1.2fr;grid-template-areas:'goal stakeholders user user' 'insights strategy principles tactics'"
    order = ["goal","stakeholders","user","insights","strategy","principles","tactics"]
    out = [box(B[k], "dark" if k=="strategy" else ("lilac" if k=="goal" else ""), n=f"{i:02d}", icon_name=icons[k]) for i,k in enumerate(order,1)]
    return f'<main style="{css}">{"".join(out)}</main>'

RING_ICONS = {"social":"eye","physical":"hand","personal":"bubble","emotional":"heart"}
def rings_svg(c, size_mm=150):
    """Concentric rings with the ring titles set in the top of each band; centre holds the person."""
    R = c["rings"]; n = len(R)
    S = 1000; cx = cy = 500; rmax = 480; step = rmax / (n + .85)
    tints = ["#F2EFFB", "#E6E1F8", "#D9D1FF", "#C7BCF7"]
    parts = []
    for i, r in enumerate(R):
        rad = rmax - i*step
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rad:.0f}" fill="{tints[i]}" stroke="#2A1B5E" stroke-width="2.5"/>')
    core = rmax - n*step
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{core:.0f}" fill="#2A1B5E"/>')
    parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="800" font-size="34" fill="#fff">who</text>')
    parts.append(f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-family="Martian Mono" font-size="14" letter-spacing="2" fill="#D9D1FF">ONE PERSON</text>')
    for i, r in enumerate(R):
        rad = rmax - i*step; y = cy - rad + step*0.36
        parts.append(f'<text x="{cx}" y="{y:.0f}" text-anchor="middle" font-family="Martian Mono" font-size="15" letter-spacing="2" fill="#B3252B">{i+1:02d} · {r["title"].upper()}</text>')
        parts.append(f'<text x="{cx}" y="{y+40:.0f}" text-anchor="middle" font-family="Schibsted Grotesk" font-weight="800" font-size="34" fill="#1A1633">{H.escape(r["question"])}</text>')
    return f'<svg viewBox="0 0 {S} {S}" style="width:{size_mm}mm;height:{size_mm}mm;display:block;margin:auto" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'

def ring_legend(c, cls=""):
    out = []
    for i, r in enumerate(c["rings"], 1):
        b = {"id": r["id"], "title": r["title"], "prompts": r["prompts"]}
        out.append(box(b, cls, n=f"{i:02d}", icon_name=RING_ICONS[r["id"]], q=r["question"]))
    return "".join(out)

def rings(c):
    B = {b["id"]: b for b in c["boxes"]}
    icons = {"who":"user","need":"list","pains":"frown","gains":"bolt"}
    left = "".join(box(B[k], "lilac" if k=="who" else "", n=f"{'ABCD'[i]}", icon_name=icons[k]) for i,k in enumerate(["who","need","pains","gains"]))
    css = "grid-template-columns:1fr 1.55fr 1fr;grid-template-rows:repeat(4,1fr);grid-template-areas:'who ring social' 'need ring physical' 'pains ring personal' 'gains ring emotional'"
    ring = (f'<div style="grid-area:ring;display:flex;flex-direction:column;justify-content:center;gap:3mm;min-height:0">{rings_svg(c, 196)}'
            f'<div style="text-align:center;font-family:var(--mono);font-size:6.6pt;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)">work from the outside in — see, do, think, then feel</div></div>')
    return f'<main style="{css}">{left}{ring}{ring_legend(c)}</main>'

def agent(c):
    B = {b["id"]: b for b in c["boxes"]}
    icons = {"who":"user","need":"list","pains":"frown","gains":"bolt"}
    left = "".join(box(B[k], "lilac" if k=="who" else "", n=f"{'ABCD'[i]}", icon_name=icons[k]) for i,k in enumerate(["who","need","pains","gains"]))
    aic = {"personality":"robot","tasks":"list","specialisms":"brain","actions":"plug"}
    right = "".join(box({"id":a["id"],"title":a["title"],"prompts":a["prompts"]}, "dark" if a["id"]=="personality" else "", n=f"{i:02d}", icon_name=aic[a["id"]]) for i,a in enumerate(c["agent"],1))
    css = ("grid-template-columns:.85fr 1.05fr 1.05fr 1.25fr 1.25fr;grid-template-rows:1fr 1fr 1fr 1fr 11mm;"
           "grid-template-areas:'who ring ring personality tasks' 'need ring ring personality tasks' 'pains social physical specialisms actions' 'gains personal emotional specialisms actions' 'ctx ctx ctx ctx ctx'")
    ring = (f'<div style="grid-area:ring;display:flex;align-items:center;justify-content:center;min-height:0;position:relative">{rings_svg(c, 118)}'
            f'<div style="position:absolute;right:-4mm;top:50%;transform:translateY(-50%);width:6mm;height:6mm;border-radius:50%;background:var(--coral);color:#fff;display:grid;place-items:center;font-weight:800;font-size:9pt">→</div></div>')
    ctx = ('<div class="box" style="grid-area:ctx;flex-direction:row;align-items:center;gap:4mm;padding:2.4mm 3.8mm;border-style:dashed">'
           '<div class="h" style="font-size:9pt">context</div><div style="font-size:8pt;color:#3A3560">the single situation this agent serves — moment, channel, constraint. One line, written after the left side and before the right.</div>'
           '<div style="flex:1;border-bottom:.8pt solid var(--line);height:1px"></div></div>')
    return f'<main style="{css}">{left}{ring}{ring_legend(c)}{right}{ctx}</main>'

def matrix(c):
    m = c["matrix"]; rows, cols = m["rows"], m["cols"]
    th = "".join(f'<th><span class="lab">competitor {i}</span><span class="line"></span></th>' for i in range(1, cols+1))
    th += '<th class="you"><span class="lab">you · today</span><span class="line"></span></th>'
    trs = ""
    for r in range(1, rows+1):
        tds = "".join('<td><span class="cell"></span></td>' for _ in range(cols)) + '<td class="you"><span class="cell"></span></td>'
        trs += f'<tr><td class="story"><span class="idx">{r:02d}</span><span class="line"></span><span class="l2">as a … I need to … so that …</span></td>{tds}</tr>'
    table = (f'<div class="box" style="grid-area:tbl;padding:0;overflow:hidden"><table><thead><tr><th class="story"><span class="lab">user story</span></th>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
    side = [
        box({"id":"scale","title":"the scale","prompts":[m["scale"], "Score with evidence: a demo, a review, an interview. Leave unknowns blank — never guess."]}, "lilac", icon_name="chart"),
        box({"id":"read","title":"reading the grid","prompts":["A column of 3s — table stakes. Match it, don't lead with it.","A row of 0s — nobody serves this story. Your opening.","A row where scores disagree — contested. Win it with proof.","Your own column, scored today, not the roadmap."]}, "", icon_name="compass"),
        box({"id":"out","title":"the one sentence","prompts":["“Everyone does ___; nobody does ___. The ___ is the product.”","Three stories to build first:","1. ______________________","2. ______________________","3. ______________________"]}, "dark", icon_name="star"),
    ]
    css = "grid-template-columns:2.6fr 1fr;grid-template-rows:auto 1fr auto;grid-template-areas:'tbl scale' 'tbl read' 'tbl out'"
    extra = """<style>
table{width:100%;height:100%;border-collapse:collapse;table-layout:fixed}
th,td{border:0.6pt solid var(--line);vertical-align:top;padding:2.2mm 2.6mm}
th{background:var(--lilac);text-align:left;height:16mm}th.story{width:34%}th.you{background:var(--pop)}
th .lab{display:block;font-family:var(--mono);font-size:6.6pt;letter-spacing:.09em;text-transform:uppercase;color:var(--coral-ink);font-weight:500}
th .line,td .line{display:block;border-bottom:.7pt solid var(--ink);height:6mm}
td.story{position:relative}td.story .idx{position:absolute;left:2.6mm;top:2.2mm;font-family:var(--mono);font-size:6.4pt;color:var(--muted)}
td.story .line{margin-left:6mm;height:7.5mm}td.story .l2{display:block;margin-top:1.4mm;font-size:6.8pt;color:var(--muted)}
td.you{background:#F7F5FE}td .cell{display:block;height:100%}
</style>"""
    return f'{extra}<main style="{css}">{table}{"".join(side)}</main>'

LAYOUTS = {"grid9": grid9, "grid7": grid7, "rings": rings, "agent": agent, "matrix": matrix}

def canvas_html(c, watermark=False):
    css = CSS.replace("__TILE__", TILE_SVG)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{H.escape(c["title"])} — DSH canvas</title>'
            f'<style>{font_css()}{css}</style></head><body><div class="sheet">{header(c)}{LAYOUTS[c["layout"]](c)}{footer(c)}</div>'
            f'{watermark_html() if watermark else ""}</body></html>')
