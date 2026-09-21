#!/usr/bin/env python3
"""
canvases/render_guide.py — A4 walkthrough guides (HTML for Chromium print → PDF).
guide_html(c, full=True, watermark=False)
  full=True   the paid guide: cover, why, box-by-box (do / what good looks like / example), agenda, mistakes, what next
  full=False  the free two-page quick guide: what/when + the box-by-box 'do' column and the agenda
"""
import html as H
import os, base64
from render_canvas import font_css, mark, TILE_SVG, SITE, LIB, ROOT

def _img(slug):
    p = os.path.join(ROOT, "assets", f"preview-canvas-{slug}.png")
    if not os.path.exists(p): return ""
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()

CSS = """
:root{--ink:#1A1633;--deep:#2A1B5E;--purple:#5B4BC4;--violet:#8A7BE8;--pop:#D9D1FF;--lilac:#F2EFFB;--line:#E3E0F0;--muted:#6E6A8A;--coral:#F96167;--coral-ink:#B3252B;
--sans:'Schibsted Grotesk',system-ui,sans-serif;--mono:'Martian Mono',ui-monospace,monospace}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font:10pt/1.5 var(--sans);color:#3A3560;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:210mm;height:297mm;overflow:hidden;padding:18mm 18mm 20mm;position:relative;page-break-after:always;break-after:page;display:flex;flex-direction:column}
.pg:last-child{page-break-after:auto;break-after:auto}
h1,h2,h3{color:var(--ink);font-weight:800;letter-spacing:-.02em;line-height:1.1}
h1{font-size:30pt}h2{font-size:17pt;margin:0 0 4mm}h3{font-size:11pt;margin-bottom:1.5mm}
p+p{margin-top:3mm}
.eyebrow{font-family:var(--mono);font-size:7pt;letter-spacing:.12em;text-transform:uppercase;color:var(--coral-ink);font-weight:500}
.eyebrow:before{content:'';display:inline-block;width:6mm;height:1.6pt;background:var(--coral);vertical-align:middle;margin-right:2.2mm}
.top{display:flex;justify-content:space-between;align-items:center;padding-bottom:3mm;border-bottom:.6pt solid var(--line);margin-bottom:8mm;font-family:var(--mono);font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.top svg{width:7mm;height:7mm;color:var(--ink)}
.foot{margin-top:auto;padding-top:4mm;gap:6mm;white-space:nowrap;border-top:.6pt solid var(--line);display:flex;justify-content:space-between;font-family:var(--mono);font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.foot b{color:var(--ink);font-weight:600}
/* cover */
.cover{background:var(--deep);color:#D8D2F5}
.cover .top,.cover .foot{border-color:rgba(255,255,255,.18);color:#B6AEDD}.cover .top svg{color:#fff}.cover .foot b{color:#fff}
.cover h1{color:#fff;font-size:36pt;margin:4mm 0 5mm}.cover .eyebrow{color:var(--pop)}.cover .eyebrow:before{background:var(--coral)}
.cover .lede{font-size:14pt;color:#fff;font-weight:600;max-width:140mm;line-height:1.3}
.cover .meta{display:flex;gap:4mm;flex-wrap:wrap;margin-top:8mm}
.cover .pill{border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:2mm 4mm;font-family:var(--mono);font-size:7pt;letter-spacing:.06em;color:#fff}
.cover img{width:100%;border-radius:2mm;margin-top:10mm;box-shadow:0 10mm 20mm -10mm rgba(0,0,0,.6)}
.cover .who{margin-top:auto;padding-top:8mm;font-size:9.5pt;color:#D8D2F5}.cover .who b{color:#fff;display:block;font-size:11pt}
/* body */
.lead{font-size:12pt;color:var(--ink);font-weight:500;line-height:1.45}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
ul.clean{list-style:none;display:grid;gap:2mm}ul.clean li{padding-left:5mm;position:relative}
ul.clean li:before{content:'';position:absolute;left:0;top:.55em;width:2mm;height:2mm;border-radius:50%;background:var(--violet)}
ul.coral li:before{background:var(--coral)}
.step{display:grid;grid-template-columns:34mm 1fr;gap:5mm;padding:4mm 0;border-top:.6pt solid var(--line);page-break-inside:avoid;break-inside:avoid}
.step .k{font-weight:800;color:var(--ink);font-size:10.5pt;line-height:1.2}
.step .k small{display:block;font-family:var(--mono);font-size:6.6pt;letter-spacing:.1em;color:var(--muted);font-weight:500;margin-bottom:1.5mm}
.step .row{display:grid;grid-template-columns:22mm 1fr;gap:3mm;margin-top:1.5mm}.step .row:first-child{margin-top:0}
.step .lab{font-family:var(--mono);font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;color:var(--coral-ink);padding-top:1mm}
.step .ex{background:var(--lilac);border-radius:1.5mm;padding:2mm 3mm;font-style:normal;color:var(--ink)}
table.ag{width:100%;border-collapse:collapse;font-size:9.5pt}
table.ag td{padding:2.4mm 0;border-bottom:.6pt solid var(--line);vertical-align:top}
table.ag td:first-child{font-family:var(--mono);font-size:7pt;letter-spacing:.06em;color:var(--coral-ink);width:26mm;white-space:nowrap;padding-top:3mm}
.callout{background:var(--pop);border-radius:2mm;padding:5mm 6mm;color:var(--ink)}
.callout .eyebrow{color:#3F31A8}.callout .eyebrow:before{background:#3F31A8}
.dark{background:var(--deep);color:#D8D2F5;border-radius:2mm;padding:5mm 6mm}.dark h3{color:#fff}.dark .eyebrow{color:var(--pop)}.dark a{color:#fff}
.sec{margin-bottom:8mm}
/* quick guide grid */
.qgrid{display:grid;grid-template-columns:1fr 1fr;gap:3mm 6mm}
.qs{font-size:8.4pt;line-height:1.38;padding:1.6mm 0;border-top:.6pt solid var(--line)}
.qs small{display:block;font-family:var(--mono);font-size:6.4pt;letter-spacing:.08em;text-transform:uppercase;color:var(--coral-ink);margin-bottom:1mm}
/* watermark */
.wm{position:fixed;inset:0;pointer-events:none;z-index:5;overflow:hidden}
.wm .tile{position:absolute;inset:-40mm;background-image:url("data:image/svg+xml;utf8,__TILE__");background-size:34mm 34mm;opacity:.045;transform:rotate(-18deg)}
.wm .txt{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-30deg);font-family:var(--mono);font-weight:600;font-size:22pt;letter-spacing:.12em;color:var(--purple);opacity:.12;white-space:nowrap}
"""

def top(c, label):
    return f'<div class="top"><span>{H.escape(c["title"])} · {label}</span>{mark("gm")}</div>'
def foot(c, n=None):
    return (f'<div class="foot"><span><b>{SITE}</b> · canvas page: /canvas/{c["slug"]}/</span><span>© {c["year"]} Diana Simpson-Hernandez{(" · page " + str(n)) if n else ""}</span></div>')

def cover(c, full):
    g = c["guide"]
    kind = "Walkthrough guide" if full else "Quick guide · free edition"
    img = _img(c["slug"])
    return (f'<section class="pg cover">{top(c, kind)}'
            f'<div class="eyebrow">DSH canvas · {H.escape(c["short"])} · {kind}</div><h1>{H.escape(c["title"])}</h1>'
            f'<p class="lede">{H.escape(c["subtitle"])}</p>'
            f'<div class="meta"><span class="pill">{H.escape(c["time"])}</span><span class="pill">{" · ".join(H.escape(t) for t in c["tags"])}</span><span class="pill">A3 landscape</span><span class="pill">v1 · {c["year"]}</span></div>'
            + (f'<img src="{img}" alt="">' if img else "") +
            f'<div class="who"><b>Diana Simpson-Hernandez</b>Founder, Aletheai · AI product strategist · {SITE}</div>{foot(c)}</section>')

def why(c, full):
    g = c["guide"]
    when = "".join(f"<li>{H.escape(x)}</li>" for x in g["when"])
    if full:
        body = (f'<div class="sec"><div class="eyebrow">What it is</div><h2>What this canvas does</h2><p class="lead">{H.escape(g["what"])}</p></div>'
                f'<div class="two"><div><div class="eyebrow">When to use it</div><h3 style="margin-top:2mm">Reach for it when</h3><ul class="clean">{when}</ul></div>'
                f'<div><div class="eyebrow">Who it is for</div><h3 style="margin-top:2mm">Built for</h3><p>{H.escape(c["for"])}</p>'
                f'<h3 style="margin-top:5mm">How long</h3><p>{H.escape(c["time"])} with a group of three to eight. Print it at A3, or drop the PNG into Miro or FigJam.</p></div></div>')
        return f'<section class="pg">{top(c, "why")}{body}{foot(c, 2)}</section>'
    # quick guide: one dense page
    what = " ".join(g["what"].split(". ")[:2]).rstrip(".") + "."
    steps = "".join(f'<div class="qs"><small>{i:02d} · {H.escape(s["box"])}</small>{H.escape(s["do"])}</div>' for i, s in enumerate(g["steps"], 1))
    body = (f'<div class="sec" style="margin-bottom:5mm"><div class="eyebrow">What it is</div><h2>What this canvas does</h2><p class="lead" style="font-size:10pt">{H.escape(what)}</p></div>'
            f'<div class="two" style="margin-bottom:5mm"><div><div class="eyebrow">When to use it</div><ul class="clean" style="margin-top:2mm;font-size:9pt">{when}</ul></div>'
            f'<div><div class="eyebrow">Who it is for</div><p style="margin-top:2mm;font-size:9pt">{H.escape(c["for"])} {H.escape(c["time"])} with three to eight people.</p></div></div>'
            f'<div class="sec" style="margin-bottom:4mm"><div class="eyebrow">Box by box</div><h2>The short version</h2><div class="qgrid">{steps}</div></div>'
            f'<div class="callout" style="padding:3.5mm 5mm;font-size:9pt;margin-top:auto"><b>The Canvas Pack (£{PRICE})</b> has the full walkthrough for every canvas — what good looks like for each box, a worked example, the agenda and the mistakes — plus clean A3 PDFs and 4K PNGs. {LIB}/canvas/</div>')
    return f'<section class="pg">{top(c, "why")}{body}{foot(c, 2)}</section>'

PRICE = "49"

def steps(c):
    g = c["guide"]; out = []
    for i, s in enumerate(g["steps"], 1):
        out.append(f'<div class="step"><div class="k"><small>{i:02d}</small>{H.escape(s["box"])}</div><div>'
                   f'<div class="row"><span class="lab">Do</span><span>{H.escape(s["do"])}</span></div>'
                   f'<div class="row"><span class="lab">Good looks like</span><span>{H.escape(s["good"])}</span></div>'
                   f'<div class="row"><span class="lab">Example</span><span class="ex">{H.escape(s["example"])}</span></div></div></div>')
    pages = []; per = 4
    for k in range(0, len(out), per):
        first = k == 0
        intro = ('<div class="eyebrow">Box by box</div><h2>How to fill it in</h2><p style="margin-bottom:4mm">Work in the numbered order on the canvas. Each box has what to do, what a good answer looks like, and a worked example from one running case.</p>' if first
                 else '<div class="eyebrow">Box by box · continued</div><h2>How to fill it in</h2>')
        pages.append(f'<section class="pg">{top(c, "box by box")}{intro}{"".join(out[k:k+per])}{foot(c, 3 + k // per)}</section>')
    return "".join(pages)

def run(c):
    g = c["guide"]
    ag = "".join(f"<tr><td>{H.escape(a)}</td><td>{H.escape(b)}</td></tr>" for a, b in g["agenda"])
    ms = "".join(f"<li>{H.escape(m)}</li>" for m in g["mistakes"])
    return (f'<section class="pg">{top(c, "running it")}'
            f'<div class="sec"><div class="eyebrow">Facilitation</div><h2>A {H.escape(c["time"])} agenda</h2><table class="ag">{ag}</table></div>'
            f'<div class="sec"><div class="eyebrow">Watch for</div><h2>The mistakes that waste the session</h2><ul class="clean coral">{ms}</ul></div>'
            f'<div class="dark"><div class="eyebrow">What next</div><h3 style="margin-top:2mm">After the canvas</h3><p>{H.escape(g["next"])}</p>'
            f'<p style="margin-top:4mm">Every framework in the library is free to read at {LIB}. If you want the method run on your company rather than by it, the fees are at {SITE}/work-with-me/.</p></div>'
            f'{foot(c, 3 + (len(g["steps"]) + 3) // 4)}</section>')

def guide_html(c, full=True, watermark=False):
    css = CSS.replace("__TILE__", TILE_SVG)
    pages = cover(c, full) + why(c, full) + (steps(c) + run(c) if full else "")
    wm = f'<div class="wm"><div class="tile"></div><div class="txt">{SITE} · free edition</div></div>' if watermark else ""
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{H.escape(c["title"])} — guide</title>'
            f'<style>{font_css()}{css}</style></head><body>{wm}{pages}</body></html>')
