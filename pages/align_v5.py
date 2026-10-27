#!/usr/bin/env python3
"""
pages/align_v5.py — align the library with dianasimpsonhernandez.com v5 (researcher, entrepreneur, lecturer profile)

    python3 pages/align_v5.py            # apply (idempotent: safe to run any number of times)
    python3 pages/align_v5.py --check    # report anything still out of line; exit 1 if so

Run it BEFORE build_library.py (which injects head SEO/OG/analytics on top).

What it does
  CONTENT (every page + the page generators in pages/)
    • retired main-site URLs → v5 pages:  /work-with-me/ /contract/ → /contact/,  /learn/ /speaking/ → /teaching/
    • "Hire the method", "Fees and the free Friction Teardown", "that's the job" → contact / published-in-full wording
    • no course funnel: Skool + Instagram links and the Skool product fields go
    • REWIRED and TeamScale removed from the library (Diana, 28 Oct 2026); --check fails if anything links to them
    • aletheai.com → aletheai.ai · substack.com/@… → dianasimpsonhernandez.substack.com · location "London" (no Texas/Madrid)
  STYLE (legacy pages that predate design system v2: flywheel, vibecoding, rediscovery-canvas)
    • v1 palette (navy/gold/cream) → v2 tokens (ink/deep/purple/pop/lilac/line); coral unchanged
    • Fraunces / Inter / JetBrains Mono / Calibri / Georgia → self-hosted Schibsted Grotesk + Martian Mono; no italics
    • Google Fonts removed; library nav + footer injected (the same chrome as LEVER, RECALL, STAKE, canvases)
  NO THIRD-PARTY CDNs at runtime: chart.js (FLYWHEEL) is served from /assets/vendor/. Python only, no node.
"""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = "https://dianasimpsonhernandez.com"
SANS = "'Schibsted Grotesk',system-ui,-apple-system,sans-serif"
MONO = "'Martian Mono',ui-monospace,monospace"
LEGACY = {"flywheel": "FLYWHEEL", "vibecoding": "Vibecoding", "rediscovery-canvas": "Rediscovery Canvas"}
SKIP_DIRS = {"assets", "data", "styles", "pages", "og", "canvases", "STFC_faq", ".git", "node_modules"}

# ── 1. content: exact substitutions (order matters) ─────────────────────────────────────────────────────────
SUBS = [
    # method-page nav (rendered + generator source)
    (f'<li><a href="{MAIN}/work-with-me/">Work with me</a></li><li><a href="{MAIN}/learn/">Learn</a></li>',
     f'<li><a href="{MAIN}/writing/">Writing</a></li><li><a href="{MAIN}/teaching/">Teaching</a></li>'),
    ('<li><a href="{MAIN}/work-with-me/">Work with me</a></li><li><a href="{MAIN}/learn/">Learn</a></li>',
     '<li><a href="{MAIN}/writing/">Writing</a></li><li><a href="{MAIN}/teaching/">Teaching</a></li>'),
    ('(f"{MAIN}/work-with-me/", "Work with me"), (f"{MAIN}/learn/", "Learn")',
     '(f"{MAIN}/writing/", "Writing"), (f"{MAIN}/teaching/", "Teaching")'),
    ('Hire the method →', 'Contact →'),
    ('Fees and the free Friction Teardown →', 'Questions about this method? Get in touch →'),
    ('Methods, fees and the free Friction Teardown', 'Get in touch'),
    ('<div class="eyebrow">Your operation</div><h3>Founder as the critical path? Start with the free Friction Teardown.</h3><p style="margin:0">Thirty minutes. I tell you which method fits — or that neither does.</p>',
     '<div class="eyebrow">Working on something similar?</div><h3>Happy to talk it through.</h3><p style="margin:0">How the work was sequenced, what I would do differently, or how the methods might apply to your organisation or your teaching.</p>'),
    ('href="mailto:dianasimpsonhernandez@gmail.com?subject=Friction%20Teardown"', 'href="mailto:dianasimpsonhernandez@gmail.com?subject=Language%20Kids%20World%20case%20study"'),
    ('white-space:nowrap">Book it →</a>', 'white-space:nowrap">Email me →</a>'),
    # footer base line on method pages
    (f'Free to read. Not free to run on your company — <a href="{MAIN}/work-with-me/" style="font-weight:500">that\'s the job</a>.', 'Published in full. Free to read, use and cite.'),
    ('Free to read. Not free to run on your company — <a href="{MAIN}/work-with-me/" style="font-weight:500">that\'s the job</a>.', 'Published in full. Free to read, use and cite.'),
    # canvas footer
    (f'href="{MAIN}/work-with-me/">Work with me →</a>', f'href="{MAIN}/">About Diana →</a>'),
    # generic retired URLs and labels
    (f'{MAIN}/work-with-me/', f'{MAIN}/contact/'), ('{MAIN}/work-with-me/', '{MAIN}/contact/'),
    (f'{MAIN}/contract/', f'{MAIN}/contact/'), ('{MAIN}/contract/', '{MAIN}/contact/'),
    (f'{MAIN}/learn/', f'{MAIN}/teaching/'), ('{MAIN}/learn/', '{MAIN}/teaching/'),
    (f'{MAIN}/speaking/', f'{MAIN}/teaching/'), ('{MAIN}/speaking/', '{MAIN}/teaching/'),
    (f'/teaching/">Learn</a>', '/teaching/">Teaching</a>'),
    (f'/contact/">Work with me</a>', '/contact/">Contact</a>'),
    ('data-umami-event-kind="work-with-me"', 'data-umami-event-kind="contact"'),
    ('data-umami-event-kind="work-with-me"'.replace('"', "'"), "data-umami-event-kind='contact'"),
    # identity
    ('https://aletheai.com"', 'https://aletheai.ai"'),
    ('https://substack.com/@dianasimpsonhernandez', 'https://dianasimpsonhernandez.substack.com'),
    ('London · Texas', 'London'), ('LONDON · TEXAS', 'LONDON'),
    ('© 2026 Diana Simpson Hernandez', '© 2026 Diana Simpson-Hernandez'),
]

INDEX_SUBS = [  # the library landing page (index.html): positioning copy, channels, CTA, footer
    ('''      <li><a href="https://dianasimpsonhernandez.com/contact/">Contact</a></li>
      <li><a href="https://dianasimpsonhernandez.com/teaching/">Teaching</a></li>
      <li><a href="https://dianasimpsonhernandez.com/">Main site</a></li>''',
     '''      <li><a href="https://dianasimpsonhernandez.com/writing/">Writing</a></li>
      <li><a href="https://dianasimpsonhernandez.com/teaching/">Teaching</a></li>
      <li><a href="https://dianasimpsonhernandez.com/">Main site</a></li>'''),
    ('''        Read the method<br>
        <em>before</em> you<br>
        hire it.''', '''        Methods,<br>
        <em>published</em><br>
        in full.'''),
    ("Interactive frameworks, consulting methods and case studies from fifteen years of building. Run them on your own business. If one of them fits, that's what the consulting page is for.",
     "Frameworks, canvases and case studies from fifteen years of design, product and AI work. Each one is written down with its instruments and its gates, so you can check the reasoning, run it on your own work, or argue with it."),
    ('data-umami-event-position="library-hero">Work with me</a>', 'data-umami-event-position="library-hero">About Diana</a>'),
    ('<a href="https://dianasimpsonhernandez.com/contact/" class="btn" data-umami-event="cta_click" data-umami-event-kind="contact" data-umami-event-position="library-hero">',
     '<a href="https://dianasimpsonhernandez.com/" class="btn" data-umami-event="cta_click" data-umami-event-kind="about" data-umami-event-position="library-hero">'),
    ('<h2>Where the frameworks <em>come from</em>.</h2>', '<h2>Where the thinking <em>comes from</em>.</h2>'),
    ("<h2>One of these fits your business? <em>That's the job.</em></h2>", "<h2>Using a method in teaching or research? <em>Get in touch.</em></h2>"),
    ('Frameworks, methods and case studies. Read them before you hire them.', 'Frameworks, methods and case studies, published in full. Free to read, use and cite.'),
    ('''          <li><a href="https://dianasimpsonhernandez.com/contact/">Contact</a></li>
          <li><a href="https://dianasimpsonhernandez.com/teaching/">Teaching</a></li>
          <li><a href="https://dianasimpsonhernandez.com/contact/">Contract</a></li>''',
     '''          <li><a href="/canvas/">Canvases</a></li>
          <li><a href="https://dianasimpsonhernandez.com/writing/">Writing</a></li>
          <li><a href="https://dianasimpsonhernandez.com/teaching/">Teaching</a></li>
          <li><a href="https://dianasimpsonhernandez.com/contact/">Contact</a></li>'''),
    ('<h4>Ventures</h4>', '<h4>Work</h4>'),
]

CHANNEL_CARDS = '''    <div class="writing-grid">
      <a href="https://dianasimpsonhernandez.substack.com?utm_source=dsh-frameworks&utm_medium=channels&utm_campaign=substack" class="writing-card fade-up" data-umami-event="channel_click" data-umami-event-channel="substack" data-umami-event-position="library" target="_blank" rel="noopener">
        <span class="eyebrow">Substack</span>
        <h4>Essays on decision intelligence and AI that can be held to account.</h4>
        <p>Long-form thinking. Several of the frameworks here started as essays.</p>
      </a>
      <a href="https://linkedin.com/in/dianasimpson" class="writing-card fade-up" data-umami-event="channel_click" data-umami-event-channel="linkedin" data-umami-event-position="library" target="_blank" rel="noopener">
        <span class="eyebrow">LinkedIn</span>
        <h4>Field notes from building Aletheai.</h4>
        <p>Shorter notes on the work in progress.</p>
      </a>
      <a href="https://dianasimpsonhernandez.com/writing/" class="writing-card fade-up" data-umami-event="cta_click" data-umami-event-kind="writing" data-umami-event-position="library">
        <span class="eyebrow">Research &amp; writing</span>
        <h4>Essays, papers, the 2012 RCA dissertation and a book.</h4>
        <p>Everything published, in one place on the main site.</p>
      </a>
      <a href="https://github.com/dsimpsonh" class="writing-card fade-up" data-umami-event="channel_click" data-umami-event-channel="github" data-umami-event-position="library" target="_blank" rel="noopener">
        <span class="eyebrow">GitHub</span>
        <h4>The library itself, versioned and forkable.</h4>
        <p>Every page here is open source.</p>
      </a>
    </div>'''

FOOTER_CHANNELS = '''        <h4>Channels</h4>
        <ul>
          <li><a href="https://dianasimpsonhernandez.substack.com">Substack</a></li>
          <li><a href="https://linkedin.com/in/dianasimpson">LinkedIn</a></li>
          <li><a href="https://github.com/dsimpsonh">GitHub</a></li>
        </ul>'''

# ── 2. style: v1 → v2 palette, fonts, chrome ────────────────────────────────────────────────────────────────
PALETTE = {  # v1 (navy / gold / cream) → design system v2 tokens. Coral #F96167 is shared and unchanged.
    "#1E2761": "#2A1B5E", "#2A3276": "#5B4BC4", "#0B2545": "#1A1633", "#122E55": "#2A1B5E", "#0E1330": "#1A1633",
    "#1A1A1A": "#1A1633", "#1B1A17": "#1A1633", "#F9E795": "#D9D1FF", "#FAEBA9": "#EAE6FB", "#C9A227": "#5B4BC4",
    "#E5C964": "#8A7BE8", "#FFF9E8": "#F2EFFB", "#FAF7F2": "#FFFFFF", "#F2EEE6": "#F2EFFB", "#F6F4EC": "#F2EFFB",
    "#F5EFE6": "#F2EFFB", "#6B7089": "#6E6A8A", "#6B6B6B": "#6E6A8A", "#E4E6EE": "#E3E0F0", "#C9CCD9": "#E3E0F0",
    "#E2DCCF": "#E3E0F0", "#E8E2D2": "#E3E0F0", "#3D4451": "#3A3560",
    "rgba(30,39,97,": "rgba(42,27,94,", "rgba(14,19,48,": "rgba(26,22,51,", "rgba(250,247,242,": "rgba(255,255,255,",
}
FONT_RX = [
    (re.compile(r'"Georgia, serif"'), '"\'Schibsted Grotesk\', system-ui, sans-serif"'),
    (re.compile(r'fontFamily="Georgia"'), 'fontFamily="Schibsted Grotesk"'),
    (re.compile(r"font-family:\s*'?Georgia'?(?:,\s*'Times New Roman')?,\s*serif"), "font-family:'Schibsted Grotesk',system-ui,sans-serif"),
    (re.compile(r"""(['"])Fraunces\1"""), "'Schibsted Grotesk'"), (re.compile(r"""(['"])Inter\1"""), "'Schibsted Grotesk'"),
    (re.compile(r"""(['"])JetBrains Mono\1"""), "'Martian Mono'"), (re.compile(r"""(['"])Calibri\1"""), "'Schibsted Grotesk'"),
    (re.compile(r"""(['"])Carlito\1"""), "'Schibsted Grotesk'"), (re.compile(r"""(['"])Courier New\1"""), "'Martian Mono'"),
    (re.compile(r"""(['"])Georgia\1,\s*(['"])Times New Roman\2,\s*(['"])serif\3"""), "'Schibsted Grotesk', 'system-ui', 'sans-serif'"),
    (re.compile(r"""('Schibsted Grotesk'\s*,\s*)["']?Georgia["']?\s*,\s*serif"""), r"\1system-ui, sans-serif"),
    (re.compile(r"font-family:\s*Fraunces\b"), "font-family:'Schibsted Grotesk'"), (re.compile(r"font-family:\s*Inter\b"), "font-family:'Schibsted Grotesk'"),
]
GFONTS_RX = re.compile(r'\s*<link[^>]+(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>', re.I)
FONT_LINK = '<link rel="stylesheet" href="/assets/fonts/fonts.css">'
CDN_SWAPS = [
    ('<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>', '<script src="/assets/vendor/chart.umd.min.js"></script>'),
    ('<script crossorigin src="https://unpkg.com/react@18.2.0/umd/react.production.min.js"></script>', '<script src="/assets/vendor/react.production.min.js"></script>'),
    ('<script crossorigin src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js"></script>', '<script src="/assets/vendor/react-dom.production.min.js"></script>'),
    ('<script src="https://unpkg.com/html2pdf.js@0.10.1/dist/html2pdf.bundle.min.js"></script>', '<script src="/assets/vendor/html2pdf.bundle.min.js"></script>'),
]

V5_CSS = f"""<style id="dsh-v5">
/* design system v2 · library register (injected by pages/align_v5.py) */
body{{font-family:{SANS}}}
h1,h2{{font-family:{SANS};font-weight:800;letter-spacing:-.02em}}
h3,h4{{font-family:{SANS};font-weight:700;letter-spacing:-.01em}}
em,i,h1 em,h2 em,h3 em,.serif em,.italic{{font-style:normal}}
code,kbd,pre,samp{{font-family:{MONO}}}
.dsh-nav,.dsh-foot{{font-family:{SANS};-webkit-font-smoothing:antialiased}}
.dsh-nav *,.dsh-foot *{{box-sizing:border-box}}
.dsh-nav{{background:#fff;border-bottom:1px solid #E3E0F0;position:relative;z-index:60}}
.dsh-wrap{{max-width:1120px;margin:0 auto;padding:0 32px}}
.dsh-nav .dsh-wrap{{display:flex;align-items:center;gap:20px;min-height:56px}}
.dsh-nav a{{color:#1A1633;text-decoration:none;font-weight:600;font-size:14px;line-height:1.2}}
.dsh-nav .lib{{font-family:{MONO};font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:#6E6A8A;font-weight:500}}
.dsh-nav ul{{list-style:none;display:flex;align-items:center;gap:18px;margin:0 0 0 auto;padding:0}}
.dsh-nav .btn{{background:#1A1633;color:#fff;border-radius:999px;padding:8px 14px}}
.dsh-foot{{background:#1A1633;color:#C9C0F0;padding:56px 0 28px;margin-top:0;font-size:16px;line-height:1.6}}
.dsh-foot .eyebrow{{font-family:{MONO};font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:#D9D1FF;font-weight:500}}
.dsh-foot p{{max-width:70ch;margin:0}}
.dsh-foot a{{color:#fff;font-weight:600;text-decoration:none}}
.dsh-foot .q{{font-size:22px;color:#fff;line-height:1.3;max-width:34ch;margin:12px 0 16px;font-weight:700}}
.dsh-foot .q b{{color:#F96167}}
.dsh-foot .row{{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:22px;font-size:14px}}
.dsh-foot .base{{margin-top:36px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);font-family:{MONO};font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8F87B8;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between}}
@media(max-width:700px){{.dsh-wrap{{padding:0 16px}}.dsh-nav ul li:not(:last-child){{display:none}}}}
</style>"""

PAGE_CSS: dict[str, str] = {}  # page-specific fixes, keyed by slug

def chrome_nav(name: str) -> str:
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/", "Library"), (f"{MAIN}/writing/", "Writing"), (f"{MAIN}/teaching/", "Teaching"), (f"{MAIN}/", "Main site")])
    return (f'<!--dsh:v5-nav--><nav class="dsh-nav" aria-label="Site"><div class="dsh-wrap"><a class="lib" href="/">Open Frameworks</a><span class="lib">· {name}</span>'
            f'<ul>{lis}<li><a class="btn" data-umami-event="cta_click" data-umami-event-kind="contact" data-umami-event-position="legacy-nav" href="{MAIN}/contact/">Contact →</a></li></ul></div></nav><!--dsh:/v5-nav-->')

def chrome_foot(name: str) -> str:
    return (f'<!--dsh:v5-foot--><footer class="dsh-foot"><div class="dsh-wrap"><div class="eyebrow">Open Frameworks</div>'
            f'<p class="q">Published in full. <b>Free to read, use and cite.</b></p>'
            f'<p>Part of an open library of methods by Diana Simpson-Hernandez, designer, educator and founder, and author of <a href="{MAIN}/design-poiesis/">Design Poiesis</a>. '
            f'If you use one in teaching or research, <a data-umami-event="email_click" data-umami-event-position="legacy-footer" href="mailto:dianasimpsonhernandez@gmail.com?subject={name}">tell me how it went</a>.</p>'
            f'<div class="row"><a href="/">Every framework →</a><a href="{MAIN}/methods/">Methods on the main site →</a><a href="{MAIN}/contact/">Contact →</a></div>'
            f'<div class="base"><span>{name} · Diana Simpson-Hernandez</span><span>frameworks.dianasimpsonhernandez.com</span></div></div></footer><!--dsh:/v5-foot-->')

# ── helpers ───────────────────────────────────────────────────────────────────────────────────────────────────
def pages():
    out = [os.path.join(ROOT, "index.html")]
    for d in sorted(os.listdir(ROOT)):
        if d in SKIP_DIRS: continue
        p = os.path.join(ROOT, d, "index.html")
        if os.path.isfile(p): out.append(p)
    cdir = os.path.join(ROOT, "canvas")
    for d in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        p = os.path.join(cdir, d, "index.html")
        if os.path.isfile(p): out.append(p)
    return out

def write(path, s):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: f.write(s)
    os.replace(tmp, path); assert os.path.getsize(path) > 0, path

def subs(s, table):
    for a, b in table: s = s.replace(a, b)
    return s

def strip_course_funnel(s):
    # Skool + Instagram channel cards and footer items; the landing page gets the v5 channel set instead
    s = re.sub(r'\n\s*<li><a href="https://www\.(?:instagram|skool)\.com[^"]*">(?:Instagram|Skool)</a></li>', "", s)
    s = re.sub(r'\n\s*<li><a href="https://www\.youtube\.com/@DianaSimpsonHernandez">YouTube</a></li>', "", s)  # channel has no content yet
    return s

def align_index(s):
    s = subs(s, INDEX_SUBS)
    s = re.sub(r'    <div class="writing-grid">.*?\n    </div>(?=\n  </div>\n</section>)', lambda m: CHANNEL_CARDS, s, count=1, flags=re.S)
    s = re.sub(r'        <h4>Channels</h4>\n        <ul>.*?</ul>', lambda m: FOOTER_CHANNELS, s, count=1, flags=re.S)
    return s

def css_only(s, fn):
    """Apply fn to CSS contexts only (<style> blocks, style="…" attributes, quoted colour/font strings in scripts),
    so example text inside the pages (e.g. hex codes and font names in vibecoding's prompts) is left alone."""
    s = re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + fn(m.group(2)) + m.group(3), s, flags=re.S)
    s = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + fn(m.group(2)) + m.group(3), s)
    def scripts(m):
        body = re.sub(r"""(['"])(#[0-9a-fA-F]{6})\1""", lambda q: q.group(1) + PALETTE.get(q.group(2).upper(), q.group(2)) + q.group(1), m.group(2))
        body = re.sub(r"rgba\((?:30,39,97|14,19,48),", lambda q: PALETTE[q.group(0)], body)
        for rx, b in FONT_RX[:2] + FONT_RX[3:9]: body = rx.sub(b, body)
        return m.group(1) + body + m.group(3)
    return re.sub(r"(<script(?![^>]*\bsrc=)[^>]*>)(.*?)(</script>)", scripts, s, flags=re.S)

def css_fn(t):
    for a, b in PALETTE.items(): t = re.sub(re.escape(a), b, t, flags=re.I)
    for rx, b in FONT_RX: t = rx.sub(b, t)
    return re.sub(r"font-style:\s*italic", "font-style:normal", t)

def restyle(s, slug):
    s = css_only(s, css_fn)
    s = GFONTS_RX.sub("", s)
    for a, b in CDN_SWAPS: s = s.replace(a, b)
    if FONT_LINK not in s: s = re.sub(r"(<title>)", FONT_LINK + "\n\\1", s, count=1)
    s = re.sub(r'<style id="dsh-v5">.*?</style>\n?', "", s, flags=re.S)
    s = s.replace("</head>", V5_CSS.replace("</style>", PAGE_CSS.get(slug, "") + "\n</style>") + "\n</head>", 1)
    s = re.sub(r"\n?<!--dsh:v5-nav-->.*?<!--dsh:/v5-nav-->|<!--dsh:v5-foot-->.*?<!--dsh:/v5-foot-->\n?", "", s, flags=re.S)
    s = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + chrome_nav(LEGACY[slug]), s, count=1)
    i = s.rfind("</body>")
    s = s[:i] + chrome_foot(LEGACY[slug]) + "\n" + s[i:]
    return s

def restyle_text(s):
    for a, b in PALETTE.items(): s = re.sub(re.escape(a), b, s, flags=re.I)
    for rx, b in FONT_RX: s = rx.sub(b, s)
    return s

# ── main ──────────────────────────────────────────────────────────────────────────────────────────────────────
CHECKS = {
    "retired main-site URL": r"dianasimpsonhernandez\.com/(?:work-with-me|learn|contract|speaking)/",
    "course funnel": r"skool\.com|instagram\.com|Build Room|Ship It cohort|FLYWHEEL Masterclass|£297|£997|£4,997|\$497|Enroll in|Internal cohort data|TeamScale·AI users",
    "consulting sell": r"Hire the method|Friction Teardown|that's the job|Read them before you hire|Become \$\{",
    "wrong domain/location": r"aletheai\.com\b|London · Texas|LONDON · TEXAS",
    "retired fonts": r"Georgia|font-family:[^;}\"]*(?:Fraunces|JetBrains|\bInter\b|Calibri|Carlito)|['\"](?:Fraunces|Inter|JetBrains Mono|Calibri|Carlito)['\"]",
    "removed page": r"/REWIRED/|/teamscale/|REWIRED|TeamScale|McKenna|hypnosis",
    "client deal terms": r"9\.0%|8\.1%|17\.1%|82\.9%|£350|52,174|28–42k",
    "third-party CDN": r"cdn\.tailwindcss\.com|unpkg\.com|cdn\.jsdelivr\.net|fonts\.googleapis\.com|text/babel",
}

def check() -> int:
    bad = 0
    for p in pages() + [os.path.join(ROOT, "data", "frameworks.json")]:
        s = open(p, encoding="utf-8").read(); rel = os.path.relpath(p, ROOT)
        legacy = rel.split("/")[0] in LEGACY
        for name, rx in CHECKS.items():
            if name in ("retired fonts", "third-party CDN") and not (legacy or rel == "index.html" or rel.startswith(("lever", "recall", "stake", "canvas", "case-study"))): continue
            for m in re.finditer(rx, s):
                bad += 1; print(f"  ✗ {rel}: {name}: …{s[max(0, m.start()-40):m.end()+20]!r}")
    print("  ✓ nothing out of line" if not bad else f"  {bad} issue(s)")
    return bad

def main():
    if "--check" in sys.argv: sys.exit(1 if check() else 0)
    # catalogue: no course products
    jp = os.path.join(ROOT, "data", "frameworks.json"); d = json.load(open(jp, encoding="utf-8"))
    for fw in d["frameworks"]:
        if "skool.com" in json.dumps(fw.get("product", {})): fw.pop("product")
        if fw.get("category") == "Course" and fw["slug"] == "vibecoding": fw["category"] = "Method"
    write(jp, json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    for p in pages():
        rel = os.path.relpath(p, ROOT); slug = rel.split("/")[0]
        s0 = s = open(p, encoding="utf-8").read()
        s = strip_course_funnel(subs(s, SUBS))
        if rel == "index.html": s = align_index(s)
        if slug in LEGACY: s = restyle(s, slug)
        if s != s0: write(p, s); print(f"  ✓ {rel}")
    for py in ("pages/port_methods.py", "pages/lib_pages.py"):
        p = os.path.join(ROOT, py); s0 = open(p, encoding="utf-8").read(); s = subs(s0, SUBS)
        if s != s0: write(p, s); print(f"  ✓ {py} (generator source)")
    check()

if __name__ == "__main__":
    main()
