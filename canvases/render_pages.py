#!/usr/bin/env python3
"""
canvases/render_pages.py — landing page per canvas (/canvas/<slug>/), the hub (/canvas/) and the
frameworks.json entries. Uses the v2 library CSS from pages/lib_pages.py so it matches STAKE and the case study.
"""
import html as H
import os, sys, json
from render_canvas import ROOT, SITE, LIB
sys.path.insert(0, os.path.join(ROOT, "pages"))
from lib_pages import CSS as LIB_CSS, MAIN

EMAIL = "dianasimpsonhernandez@gmail.com"

EXTRA_CSS = """
.hero.canvas{padding:56px 0 48px}
.hero .grid-hero{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center}
@media(max-width:820px){.hero .grid-hero{grid-template-columns:1fr}}
.thumb{border-radius:10px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.6);background:#fff;border:1px solid rgba(255,255,255,.15)}
.thumb img{display:block;width:100%;height:auto}
.dl{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:12px 20px;font-weight:700;font-size:15px;text-decoration:none;border:2px solid transparent}
.btn.primary{background:var(--coral);color:#1A1633}.btn.primary:hover{background:#ff7a7f}
.btn.ghost{border-color:rgba(255,255,255,.35);color:#fff}.btn.ghost:hover{border-color:#fff}
.btn.ink{background:var(--ink);color:#fff}.btn.ink:hover{background:var(--deep)}
.btn.line{border-color:var(--line);color:var(--ink)}.btn.line:hover{border-color:var(--ink)}
.btn small{font-weight:500;opacity:.75}
.boxes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;counter-reset:b}
@media(max-width:820px){.boxes{grid-template-columns:1fr 1fr}}@media(max-width:560px){.boxes{grid-template-columns:1fr}}
.boxes .card{padding:18px 20px}.boxes .card h4{margin-bottom:6px;font-size:15px}.boxes .card p{font-size:14px;color:var(--muted)}
.boxes .card .k{font-family:var(--mono);font-size:10px;letter-spacing:.09em;color:var(--coral-ink);margin-bottom:8px;display:block}
.tiers{display:grid;grid-template-columns:1fr 1.15fr;gap:20px;align-items:stretch}
@media(max-width:820px){.tiers{grid-template-columns:1fr}}
.tier{border-radius:var(--r);padding:30px;min-width:0}
.tier.free{background:var(--lilac)}.tier.paid{background:var(--deep);color:#D8D2F5}
.tier h3{display:flex;justify-content:space-between;align-items:baseline;gap:12px}.tier.paid h3,.tier.paid b,.tier.paid strong{color:#fff}
.tier .price{font-family:var(--mono);font-size:13px;letter-spacing:.04em;color:var(--coral-ink);white-space:nowrap}.tier.paid .price{color:var(--pop)}
.tier ul{margin:16px 0 22px}.tier.paid ul.clean li:before{background:var(--coral)}
.tier .fine{font-size:12.5px;color:var(--muted);margin-top:14px}.tier.paid .fine{color:#B6AEDD}
.canvas-list{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
@media(max-width:700px){.canvas-list{grid-template-columns:1fr}}
.canvas-list a.card{text-decoration:none;color:inherit;display:block;padding:0;overflow:hidden}
.canvas-list a.card img{display:block;width:100%;height:auto;border-bottom:1px solid var(--line)}
.canvas-list a.card .in{padding:20px 22px}.canvas-list a.card h3{font-size:19px;margin-bottom:6px}.canvas-list a.card p{font-size:14.5px;color:var(--muted)}
.canvas-list a.card:hover{border-color:var(--purple)}
.steps-mini{display:grid;gap:0}.steps-mini div{display:grid;grid-template-columns:96px 1fr;gap:16px;padding:12px 0;border-top:1px solid var(--line);font-size:15px}
.steps-mini div span:first-child{font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--coral-ink);padding-top:3px}
.faq details{border-top:1px solid var(--line);padding:14px 0}.faq summary{cursor:pointer;font-weight:700;color:var(--ink);list-style:none;display:flex;justify-content:space-between}.faq summary:after{content:'+';color:var(--purple)}.faq details[open] summary:after{content:'–'}.faq p{margin-top:8px;font-size:15px}
"""

def nav(active):
    return (f'<nav class="dsh-nav" aria-label="Site"><div class="wrap"><a class="lib" href="/">Open Frameworks</a><span class="lib">· {active}</span><ul>'
            f'<li><a href="/">Library</a></li><li><a href="/canvas/">Canvases</a></li><li><a href="{MAIN}/learn/">Learn</a></li><li><a href="{MAIN}/">Main site</a></li>'
            f'<li><a class="btn" data-umami-event="cta_click" data-umami-event-kind="canvas-pack" data-umami-event-position="canvas-nav" href="/canvas/#pack">Canvas Pack £49 →</a></li></ul></div></nav>')

def footer(note):
    return (f'<footer class="dsh-foot"><div class="wrap">'
            f'<div class="eyebrow" style="color:#D9D1FF">Use it, then tell me</div>'
            f'<p class="q">“Which box did the room <b>argue about</b>? That is the one that was <b>worth the session</b>.”</p>'
            f'<p>Every canvas here is free to run in your company and your workshops. If you run one and something in it doesn\'t work, <a data-umami-event="email_click" data-umami-event-position="canvas-footer" href="mailto:{EMAIL}?subject=Canvas%20feedback">email me</a> — the next version is built from that.</p>'
            f'<div class="row"><a href="/canvas/">All five canvases →</a><a href="/">Every framework →</a><a data-umami-event="cta_click" data-umami-event-kind="work-with-me" data-umami-event-position="canvas-footer" href="{MAIN}/work-with-me/">Work with me →</a></div>'
            f'<div class="base"><span>{note}</span><span>Free to use. Not free to resell.</span></div></div></footer>')

TOAST_JS = """<script>
(function(){
  var toast;
  function say(addr,copied){
    if(!toast){toast=document.createElement('div');toast.className='etoast';toast.setAttribute('role','status');toast.setAttribute('aria-live','polite');document.body.appendChild(toast);}
    toast.innerHTML='<i>✓</i><div><b>'+addr+'</b> <span>'+(copied?'copied — opening your email app':'— opening your email app')+'</span></div>';
    toast.classList.add('on'); clearTimeout(toast._t); toast._t=setTimeout(function(){toast.classList.remove('on')},3800);
  }
  document.querySelectorAll('a[href^="mailto:"]').forEach(function(a){
    a.addEventListener('click',function(){
      var addr=a.getAttribute('href').slice(7).split('?')[0];
      var p=navigator.clipboard&&window.isSecureContext?navigator.clipboard.writeText(addr):Promise.reject();
      p.then(function(){say(addr,true)},function(){say(addr,false)});
    });
  });
})();
</script>"""

def shell(title, active, body, note):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{H.escape(title)}</title><link rel="stylesheet" href="/assets/fonts/fonts.css"><style>{LIB_CSS}{EXTRA_CSS}</style></head><body>'
            f'{nav(active)}{body}{footer(note)}{TOAST_JS}</body></html>')

def pack_tier(D, slug=None, position="landing"):
    p = D["pack"]
    inc = "".join(f"<li>{H.escape(x)}</li>" for x in p["includes"])
    return (f'<div class="tier paid" id="pack"><div class="eyebrow">The paid pack</div><h3>{H.escape(p["name"])}<span class="price">{H.escape(p["price"])} · one-off</span></h3>'
            f'<p>All five canvases, clean and print-ready, with the full walkthrough guides. Buy once, use it in every workshop you ever run.</p>'
            f'<ul class="clean">{inc}</ul>'
            f'<a class="btn primary" data-umami-event="cta_click" data-umami-event-kind="canvas-pack" data-umami-event-position="{position}" data-umami-event-canvas="{slug or "hub"}" href="{H.escape(p["checkout_url"])}" target="_blank" rel="noopener">Buy the Canvas Pack — {H.escape(p["price"])} →</a>'
            f'<p class="fine">Secure checkout by Lemon Squeezy. Instant download. VAT handled at checkout. Single-team licence — run it on your company and your clients, don\'t resell it.</p></div>')

def free_tier(c):
    slug = c["slug"]
    return (f'<div class="tier free"><div class="eyebrow">Free edition</div><h3>Download and run it today<span class="price">£0</span></h3>'
            f'<p>The full canvas at A3 with every prompt, and a two-page quick guide. Watermarked with the DSH mark, otherwise complete.</p>'
            f'<ul class="clean"><li>{H.escape(c["title"])} — A3 PDF, watermarked</li><li>Quick guide — what it is, when to use it, the box-by-box short version</li><li>No email required</li></ul>'
            f'<div class="dl"><a class="btn ink" data-umami-event="canvas_download" data-umami-event-canvas="{slug}" data-umami-event-file="canvas" href="/canvas/{slug}/{slug}-canvas.pdf" download>Download the canvas (PDF)</a>'
            f'<a class="btn line" data-umami-event="canvas_download" data-umami-event-canvas="{slug}" data-umami-event-file="quick-guide" href="/canvas/{slug}/{slug}-quick-guide.pdf" download>Quick guide (PDF)</a></div>'
            f'<p class="fine">Print at A3 landscape. Or open the PDF in Miro / FigJam as a board background.</p></div>')

def boxes_for(c):
    """Numbered summary of the canvas boxes for the landing page."""
    items = []
    if c["layout"] in ("grid9", "grid7"):
        items = [(b["title"], b["prompts"][0]) for b in c["boxes"]]
    elif c["layout"] == "rings":
        items = [(b["title"], b["prompts"][0]) for b in c["boxes"]] + [(f'{r["title"]} — {r["question"]}', r["prompts"][0]) for r in c["rings"]]
    elif c["layout"] == "agent":
        items = [(b["title"], b["prompts"][0]) for b in c["boxes"]] + [("the four rings", "See, do, think and say, feel — worked from the outside in.")] + [(a["title"], a["prompts"][0]) for a in c["agent"]]
    elif c["layout"] == "matrix":
        items = [("the rows", "Your user stories, from research: as a [who], I need to [what], so that [why]."), ("the columns", "Every real alternative — direct, indirect, the spreadsheet, doing nothing."), ("the scores", c["matrix"]["scale"]), ("your column", "Yourself, scored today, not the roadmap."), ("reading the grid", "Columns of 3s are table stakes; rows of 0s are your opening; rows that disagree are contested.")]
    return "".join(f'<div class="card"><span class="k">{i:02d}</span><h4>{H.escape(t)}</h4><p>{H.escape(p)}</p></div>' for i, (t, p) in enumerate(items, 1))

def landing_html(c, D):
    g = c["guide"]; slug = c["slug"]
    when = "".join(f"<li>{H.escape(x)}</li>" for x in g["when"])
    steps = "".join(f'<div><span>{i:02d}</span><span><b>{H.escape(s["box"])}</b> — {H.escape(s["do"])}</span></div>' for i, s in enumerate(g["steps"], 1))
    others = "".join(f'<a class="card" data-umami-event="framework_open" data-umami-event-framework="canvas-{o["slug"]}" href="/canvas/{o["slug"]}/"><img src="/assets/canvas-{o["slug"]}-thumb.png" alt="{H.escape(o["title"])}" loading="lazy" width="1400" height="990"><div class="in"><h3>{H.escape(o["title"])}</h3><p>{H.escape(o["subtitle"])}</p></div></a>' for o in D["canvases"] if o["slug"] != slug)
    body = f"""
<div class="hero canvas"><div class="wrap"><div class="grid-hero"><div>
<div class="eyebrow">DSH canvas · {H.escape(c["short"])} · v1 · {c["year"]} · {H.escape(c["time"])}</div>
<h1>{H.escape(c["title"])}</h1>
<p class="lede">{H.escape(c["subtitle"])} {H.escape(c["summary"])}</p>
<div class="dl"><a class="btn primary" data-umami-event="canvas_download" data-umami-event-canvas="{slug}" data-umami-event-file="canvas" data-umami-event-position="hero" href="/canvas/{slug}/{slug}-canvas.pdf" download>Download free (A3 PDF)</a>
<a class="btn ghost" data-umami-event="cta_click" data-umami-event-kind="canvas-pack" data-umami-event-position="hero" data-umami-event-canvas="{slug}" href="#pack">Get the clean version + full guide · £49</a></div>
<div class="metaline">{"".join(f'<span class="pill">{H.escape(t)}</span>' for t in c["tags"])}<span class="pill">Free · watermarked</span><span class="pill">Pack · clean + 4K PNG</span></div>
</div><div class="thumb"><img src="/assets/canvas-{slug}-thumb.png" alt="{H.escape(c["title"])} — preview" width="1400" height="990"></div></div></div></div>

<section><div class="wrap"><div class="grid2">
<div><div class="eyebrow">What it does</div><h2>Why this canvas exists</h2><p class="sub" style="margin-bottom:0">{H.escape(g["what"])}</p></div>
<div class="card"><div class="eyebrow">Reach for it when</div><ul class="clean" style="margin-top:12px">{when}</ul><p style="margin-top:18px;font-size:14px;color:var(--muted)"><b>Built for:</b> {H.escape(c["for"])}</p></div>
</div></div></section>

<section><div class="wrap"><div class="eyebrow">On the canvas</div><h2>What you fill in</h2><p class="sub">Work the boxes in the numbered order. The order is the method.</p><div class="boxes">{boxes_for(c)}</div></div></section>

<section id="download"><div class="wrap"><div class="eyebrow">Get it</div><h2>Free edition, or the pack</h2><p class="sub">The free edition is the whole canvas — nothing held back except the watermark. The pack is for people who will run it more than once and want it clean, in Miro, with the full guide.</p>
<div class="tiers">{free_tier(c)}{pack_tier(D, slug)}</div></div></section>

<section><div class="wrap"><div class="grid2">
<div><div class="eyebrow">Box by box</div><h2>The short version</h2><p class="sub">The full guide in the pack adds what good looks like for each box, a worked example, the agenda and the mistakes.</p><div class="steps-mini">{steps}</div></div>
<div><div class="eyebrow">What next</div><h2>After the canvas</h2><p class="sub">{H.escape(g["next"])}</p>
<div class="faq"><details><summary>Can I use this with clients?</summary><p>Yes — both editions. Run it in your workshops, your company and your client work. The one thing you can't do is resell the files or upload them to template marketplaces.</p></details>
<details><summary>What does the watermark look like?</summary><p>A light tiled DSH mark and the site address across the sheet. Prompts, boxes and layout are identical to the pack version. The preview above is the free edition.</p></details>
<details><summary>Miro or FigJam?</summary><p>The pack includes a 4K PNG of each canvas. Drop it on a board, lock it, and put sticky notes on top.</p></details>
<details><summary>Do I get updates?</summary><p>Pack buyers get every new version of every canvas by email. The free edition is always the current version on this page.</p></details></div></div>
</div></div></section>

<section><div class="wrap"><div class="eyebrow">The collection</div><h2>The other canvases</h2><div class="canvas-list">{others}</div></div></section>
"""
    return shell(c["seo"]["title"], c["short"], body, f"{H.escape(c['title'])} · v1 · {c['year']}")

def hub_html(D):
    cards = "".join(f'<a class="card" data-umami-event="framework_open" data-umami-event-framework="canvas-{c["slug"]}" href="/canvas/{c["slug"]}/"><img src="/assets/canvas-{c["slug"]}-thumb.png" alt="{H.escape(c["title"])}" loading="lazy" width="1400" height="990"><div class="in"><div class="eyebrow" style="margin-bottom:8px">{H.escape(c["time"])} · {H.escape(c["tags"][0])}</div><h3>{H.escape(c["title"])}</h3><p>{H.escape(c["subtitle"])}</p></div></a>' for c in D["canvases"])
    body = f"""
<div class="hero canvas"><div class="wrap">
<div class="eyebrow">DSH canvases · five sheets · free to download</div>
<h1>Canvases that make the <em>room argue</em> about the right thing</h1>
<p class="lede">Five one-page tools I run in workshops, with founders and with my own products: category design, empathy, competitive scoring, UX strategy and AI agent design. Each one is free as a watermarked A3 PDF with a quick guide. The pack has them clean, in 4K for Miro, with the full walkthroughs.</p>
<div class="dl"><a class="btn primary" href="#canvases">See the five canvases</a><a class="btn ghost" data-umami-event="cta_click" data-umami-event-kind="canvas-pack" data-umami-event-position="hub-hero" href="#pack">The Canvas Pack · £49</a></div>
</div></div>

<section id="canvases"><div class="wrap"><div class="eyebrow">The collection</div><h2>Five canvases, one method</h2><p class="sub">They chain. Empathy feeds the story matrix; the matrix feeds category design; category design and UX strategy share a user; the agent canvas starts with empathy and ends with an integration plan. Run one, or run the sequence.</p>
<div class="canvas-list">{cards}</div></div></section>

<section><div class="wrap"><div class="eyebrow">Get them</div><h2>Free, or the pack</h2>
<div class="tiers"><div class="tier free"><div class="eyebrow">Free edition</div><h3>Every canvas, watermarked<span class="price">£0</span></h3><p>Complete prompts and layout, A3 PDF plus a two-page quick guide for each. Download from each canvas page. No email required.</p>
<ul class="clean"><li>All five canvases at A3</li><li>Quick guide for each</li><li>Free to run in your company and with clients</li></ul>
<a class="btn ink" href="#canvases">Pick a canvas ↑</a></div>{pack_tier(D, None, "hub")}</div></div></section>

<section><div class="wrap"><div class="grid2">
<div><div class="eyebrow">How they were made</div><h2>Built in rooms, not in a template library</h2><p class="sub" style="margin-bottom:0">Each canvas started on a whiteboard in a real session — client workshops, founder sessions and my own products — and was cut down until the boxes people skipped were gone and the boxes they argued about were bigger. The prompts are the questions I actually ask. The order is the method.</p></div>
<div class="card dark"><div class="eyebrow">Want it run, not just read?</div><h3>I facilitate these</h3><p>Half-day and full-day sessions for product teams and founders, in London or on video, in English or Spanish. The FLYWHEEL and REWIRED workshops sit alongside them.</p><p style="margin-top:16px"><a data-umami-event="cta_click" data-umami-event-kind="speaking" data-umami-event-position="canvas-hub" href="{MAIN}/speaking/" style="color:#fff;font-weight:700">Workshops and speaking →</a></p></div>
</div></div></section>
"""
    return shell("DSH Canvases — five strategy canvases, free to download", "Canvases", body, "DSH canvases · v1 · 2026")

def update_frameworks_json(D):
    p = os.path.join(ROOT, "data", "frameworks.json")
    data = json.load(open(p, encoding="utf-8"))
    fws = [f for f in data["frameworks"] if not f["url"].startswith("/canvas/")]
    for c in D["canvases"]:
        fws.append({"slug": f"canvas-{c['slug']}", "title": c["title"], "subtitle": c["subtitle"], "category": "Canvas", "year": c["year"],
                    "tags": c["tags"], "summary": c["summary"], "status": "Live", "seo_title": c["seo"]["title"], "description": c["seo"]["description"], "url": f"/canvas/{c['slug']}/", "access": "free",
                    "product": {"name": D["pack"]["name"], "price": D["pack"]["price"], "url": f"/canvas/{c['slug']}/#pack"}})
    data["frameworks"] = fws
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2); open(p, "a").write("\n")
