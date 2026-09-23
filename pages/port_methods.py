#!/usr/bin/env python3
"""
pages/port_methods.py — port the recovered LEVER v3 / RECALL v1 method pages onto the v2 library register.

    python3 pages/port_methods.py <lever_source.html> <recall_source.html>

What it does (idempotent, source files untouched):
  • strips Google Fonts, links the self-hosted Schibsted Grotesk + Martian Mono
  • Fraunces/Inter → Schibsted Grotesk; display weight 800; no italics (no serif in this register)
  • adds --coral-ink and remaps coral TEXT to it (coral stays a background / large-display colour);
    a per-page DARK list restores bright coral where the ground is dark
  • normalises the fee pill to the published ladder
  • adds site nav, a dark footer with the routing question + companion link, and lang/viewport hygiene
  • removes any pre-doctype scaffolding
Head SEO/OG/analytics are NOT added here — build_library.py injects those for every page.
"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = "https://dianasimpsonhernandez.com"

FONT_LINK = '<link rel="stylesheet" href="/assets/fonts/fonts.css">'
SANS = "'Schibsted Grotesk',system-ui,sans-serif"
MONO = "'Martian Mono',ui-monospace,monospace"

CHROME_CSS = """
/* ── v2 library chrome ── */
.dsh-nav{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30}
.dsh-nav .wrap{display:flex;align-items:center;gap:20px;min-height:56px}
.dsh-nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}
.dsh-nav .lib{font-family:%(mono)s;font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:500}
.dsh-nav ul{list-style:none;display:flex;gap:18px;margin-left:auto;padding:0}
.dsh-nav .btn{background:var(--ink);color:#fff;border-radius:999px;padding:8px 14px}
@media(max-width:700px){.dsh-nav ul li:not(:last-child){display:none}}
.dsh-foot{background:#1A1633;color:#C9C0F0;padding:56px 0 28px;margin-top:40px}
.dsh-foot h2{color:#fff;font-size:30px;margin-bottom:14px;font-weight:800}
.dsh-foot p{max-width:70ch}
.dsh-foot a{color:#fff;font-weight:600}
.dsh-foot .q{font-size:22px;color:#fff;line-height:1.3;max-width:34ch;margin:0 0 20px}
.dsh-foot .q b{color:#F96167}
.dsh-foot .row{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:22px;font-size:14px}
.dsh-foot .base{margin-top:36px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);font-family:%(mono)s;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8F87B8;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between}
/* register: no serif → no italics; display weight 800; mono labels sized for Martian Mono */
h1,h2,h3,h4{font-weight:800;letter-spacing:-.02em}
em,.tag,.ex{font-style:normal}
em{font-weight:700}
.eyebrow{font-family:%(mono)s;font-size:10.5px;letter-spacing:.09em;font-weight:500}
.pill{font-family:%(mono)s;font-size:10.5px;letter-spacing:.04em;font-weight:500}
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%%}
.grid2>*,.grid3>*,.terms>*,.stage>*,.rung>*{min-width:0}
.tblwrap table{min-width:640px}
.tblwrap table.plain{min-width:0}
.tabular,td,th{font-variant-numeric:tabular-nums}
@media(max-width:700px){.wrap{padding:0 16px}.grid2,.grid3{grid-template-columns:1fr}.hero h1{font-size:42px}}
""" % {"mono": MONO}

def nav(active):
    items = [("/", "Library"), (f"{MAIN}/work-with-me/", "Work with me"), (f"{MAIN}/learn/", "Learn"), (f"{MAIN}/", "Main site")]
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items)
    return f"""<nav class="dsh-nav" aria-label="Site"><div class="wrap"><a class="lib" href="/">Open Frameworks</a><span class="lib">· {active}</span><ul>{lis}<li><a class="btn" data-umami-event="cta_click" data-umami-event-kind="work-with-me" data-umami-event-position="method-nav" href="{MAIN}/work-with-me/">Hire the method →</a></li></ul></div></nav>
"""

def footer(this, other, other_slug, other_line):
    return f"""<footer class="dsh-foot"><div class="wrap">
<div class="eyebrow" style="color:#D9D1FF">The routing question</div>
<p class="q">“When this goes wrong, is it because someone <b>chose badly</b>, or because someone <b>couldn't find out</b>?”</p>
<p>Chose badly → LEVER. Couldn't find out → RECALL. Neither, but you own a vertical and need a product → <a href="/stake/">STAKE</a>. The companion method to {this} is <a data-umami-event="framework_open" data-umami-event-framework="{other_slug}" href="/{other_slug}/">{other}</a> — {other_line}</p>
<div class="row"><a data-umami-event="cta_click" data-umami-event-kind="work-with-me" data-umami-event-position="method-footer" href="{MAIN}/work-with-me/">Fees and the free Friction Teardown →</a><a href="/case-study-language-kids-world/">Case study: Language Kids World →</a><a href="/">Every framework →</a></div>
<div class="base"><span>{this} · Diana Simpson-Hernandez · engine-neutral · zero Aletheai IP</span><span>Free to read. Not free to run on your company — <a href="{MAIN}/work-with-me/" style="font-weight:500">that's the job</a>.</span></div>
</div></footer>
"""


# ── public-facing cleanup ────────────────────────────────────────────────────
# The recovered sources were written as Diana's own operating notes. Everything here removes or rewrites
# material addressed to her (targeting, IP strategy, pricing tactics, roadmap) so the page reads for a client.
def public_cleanup(s, drop_headings, trim_after_tiers, subs):
    def keep(sec):
        body = re.sub(r"<[^>]+>", " ", sec); body = re.sub(r"\s+", " ", body)
        return not any(h in body for h in drop_headings)
    parts = re.split(r"(<section[^>]*>.*?</section>)", s, flags=re.S)
    out = []
    for part in parts:
        if part.startswith("<section"):
            if not keep(part): continue
            if trim_after_tiers and 'class="tiers"' in part:
                part = re.sub(r'<div class="grid2"[^>]*>.*?(</div>\s*</section>)', r"\1", part, flags=re.S)
        out.append(part)
    s = "".join(out)
    for a, b in subs:   # whitespace-insensitive match, so line breaks in the source don't matter
        rx = re.compile(r"\s+".join(re.escape(t) for t in a.split()))
        s, n = rx.subn(lambda m: b, s)
        assert n, f"cleanup substitution not found: {a[:70]}"
    return s

LEVER_DROP = ["What changed in v3", "Sector strategy", "IP and disclosure guards", "What we build next"]
LEVER_SUBS = [
    ("The market gap this exploits", "The market gap"),
    ("You are not selling adoption. You are selling <em>provable attribution</em> to people who have already spent the money and cannot show the board a result.", "This is not about adoption. It is about <em>provable attribution</em> — for people who have already spent the money and cannot yet show the board a result."),
    ("The other 62% is your entire addressable market.", "The other 62% is where LEVER works."),
    ("Say this out loud in the kickoff. It kills the client's pet projects diplomatically, kills your own scope creep, and means the final readout is structurally incapable of drifting from what the board asked for.", "Said out loud at kickoff, it rules out pet projects diplomatically, prevents scope creep, and means the final readout is structurally incapable of drifting from what the board asked for."),
    ("This is the honest recommendation that wins the follow-on.", "This is the honest recommendation."),
    ("That turns the model from your spreadsheet into their number — and makes the build fee unarguable.", "That turns the model from a consultant's spreadsheet into the client's own number."),
    ("and let the client argue you into their own business case.", "and let the room build its own business case."),
    ("and it is the single hardest thing for a competitor to copy, because it requires the blueprint to exist first.", "and it only works because the blueprint exists first."),
    ("single-tenant, your reusable app shell re-skinned", "single-tenant, in the client's environment"),
    ("<b>The rule that protects your margin:</b> the baseline always ships first. Roughly a third of the time the honest answer is \"you didn't need ML for this one\" — the most trust-building sentence available to you, and the reason the diagnostic must be priced to stand alone.", "<b>The rule:</b> the baseline always ships first. Roughly a third of the time the honest answer is \"you didn't need ML for this one\" — which is why the diagnostic is priced to stand alone."),
    ("the artefact that makes tool #2 a conversation rather than a pitch, and lets you raise your Diagnostic price.", "the artefact that makes tool #2 a conversation rather than a pitch."),
    ("Commercials · revised", "Commercials"),
    ("Illustrative revenue is a capacity model, not a forecast.", ""),
]
RECALL_DROP = ["IP guards", "What I took, and what I left", "What we build next"]
RECALL_SUBS = [
    ("One routing question decides which you sell.", "One routing question decides which applies."),
    ("The answer tells you which method to sell, and asking it out loud makes you sound like someone who has done this before — because most sellers only have one product and will bend the client's problem to fit it.", "The answer decides which method applies. Most sellers have one product and bend the problem to fit it; the question exists so that does not happen here."),
    ("and it is the reason your   build quote is safe when everyone else's is a guess.", "and it is the reason the   build quote is safe when everyone else's is a guess."),
    ("<b>This is the   sellable artefact.</b>", "<b>This is the   artefact the client keeps.</b>"),
    ("say so and bill for finding out.", "say so."),
    ("Several clients will buy the remediation and postpone the system — and that is a good outcome, not a lost sale.", "Some clients remediate and postpone the system — and that is a good outcome."),
    ("The two sentences that win the room", "Two sentences from the first meeting"),
    ("Nobody selling a RAG build says this. It costs you scope and buys you the entire engagement.", "Nobody selling a RAG build says this."),
    ("If the client insists, this is where your professional-indemnity conversation starts.", "If a client insists, this is a professional-indemnity conversation, not a build."),
    ("H is what stops you selling that system.", "H is what stops that system being built."),
    ("which is the entire argument for selling remediation first.", "which is the entire argument for remediation first."),
    ("Sell a corpus remediation project", "Run a corpus remediation project"),
    ("This is the honest recommendation that wins the follow-on, and it is a real revenue line, not a delay.", "This is the honest recommendation, and it is real work, not a delay."),
    ("This gate alone will save you one doomed build a year.", "This gate alone saves one doomed build a year."),
    ("The scope shrinks, the fee shrinks, and you keep your professional indemnity and your reputation.", "The scope shrinks, the fee shrinks, and the answer stays defensible."),
    ("Sells on its own merits", "Stands on its own merits"),
]

def port(src, slug, this, other, other_slug, other_line, dark_selectors, fee_from=None, fee_to=None, drop=(), subs=()):
    s = open(src, encoding="utf-8").read()
    s = s[s.find("<!DOCTYPE"):] if "<!DOCTYPE" in s else s          # drop anything before the doctype
    s = public_cleanup(s, drop, True, subs)
    s = re.sub(r'<link[^>]+fonts\.g(?:oogleapis|static)\.com[^>]*>\s*', "", s)
    s = s.replace("<head>", f"<head>\n{FONT_LINK}", 1)
    # fonts
    s = re.sub(r"font-family:\s*Fraunces\s*,\s*Georgia\s*,\s*serif", f"font-family:{SANS}", s)
    s = re.sub(r"font-family:\s*'?Fraunces'?(?=[;}])", f"font-family:{SANS}", s)
    s = re.sub(r"font-family:\s*Inter\s*,\s*system-ui\s*,\s*sans-serif", f"font-family:{SANS}", s)
    s = re.sub(r"font-family:\s*'?Inter'?(?=[;}])", f"font-family:{SANS}", s)
    s = re.sub(r"font-family:\s*'?JetBrains Mono'?[^;}]*", f"font-family:{MONO}", s)
    # coral text → coral-ink, with dark-ground exceptions
    s = s.replace("--coral:#F96167;", "--coral:#F96167; --coral-ink:#B3252B;", 1)
    s = re.sub(r"color:\s*var\(--coral\)", "color:var(--coral-ink)", s)
    dark = "".join(f"{sel}{{color:var(--coral)}}" for sel in dark_selectors)
    # fee pill normalisation
    if fee_from: s = s.replace(fee_from, fee_to)
    # chrome css + nav + footer
    s = s.replace("</style>", CHROME_CSS + dark + "\n</style>", 1)
    s = re.sub(r"<body>\s*", "<body>\n" + nav(this), s, count=1)
    s = s.replace("</body>", footer(this, other, other_slug, other_line) + "</body>", 1)
    # wide tables scroll inside their own box
    s = re.sub(r"(<table[^>]*>)", r'<div class="tblwrap">\1', s); s = s.replace("</table>", "</table></div>")
    out = os.path.join(ROOT, slug, "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp"; open(tmp, "w", encoding="utf-8").write(s); os.replace(tmp, out)
    assert os.path.getsize(out) > 20000, out
    print(f"  ✓ {slug}/index.html {len(s)//1024} KB")

if __name__ == "__main__":
    lever_src, recall_src = sys.argv[1], sys.argv[2]
    port(lever_src, "lever", "LEVER", "RECALL", "recall", "for when the problem is that people can't find or trust what the company already knows.",
         dark_selectors=[".hero em", ".hero .eyebrow", ".dsh-foot b", ".formula .eq i", ".term[style*='--navy'] em", ".term[style*='--deep'] em"],
         fee_from="Diagnostic £28–35k · Build £45–95k", fee_to="Diagnostic £32,000 · Build from £45,000", drop=LEVER_DROP, subs=LEVER_SUBS)
    port(recall_src, "recall", "RECALL", "LEVER", "lever", "for when the problem is that a recurring decision keeps being made badly.",
         dark_selectors=[".hero em", ".hero .eyebrow", ".dsh-foot b", ".formula .eq i", ".term[style*='--navy'] em", ".term[style*='--deep'] em"],
         fee_from="Diagnostic £34k · Build £55–120k", fee_to="Diagnostic £34,000 · Build from £55,000", drop=RECALL_DROP, subs=RECALL_SUBS)
