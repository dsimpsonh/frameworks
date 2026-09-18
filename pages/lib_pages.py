#!/usr/bin/env python3
"""
pages/lib_pages.py — generates the v2-register library pages that have no recovered source:
    /stake/                          STAKE — the partnership method (with live calculator)
    /case-study-language-kids-world/ the named case study

    python3 pages/lib_pages.py
Head SEO/OG/analytics are injected afterwards by build_library.py.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = "https://dianasimpsonhernandez.com"
EMAIL = "dianasimpsonhernandez@gmail.com"

CSS = """
:root{--deep:#2A1B5E;--purple:#5B4BC4;--violet:#8A7BE8;--pop:#D9D1FF;--lilac:#F2EFFB;--coral:#F96167;--coral-ink:#B3252B;--corals:#FFEFF0;
--ink:#1A1633;--body:#3A3560;--muted:#6E6A8A;--line:#E3E0F0;--white:#fff;--r:10px;--rs:6px;
--sans:'Schibsted Grotesk',system-ui,sans-serif;--mono:'Martian Mono',ui-monospace,monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;color:var(--body);font:16px/1.6 var(--sans);-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 32px}@media(max-width:700px){.wrap{padding:0 16px}}
h1,h2,h3,h4{color:var(--ink);font-weight:800;letter-spacing:-.02em;line-height:1.1}
h1{font-size:clamp(40px,6vw,62px)}h2{font-size:clamp(28px,3.6vw,37px);margin-bottom:8px}h3{font-size:22px;margin-bottom:8px}h4{font-size:16px}
p+p{margin-top:12px}a{color:var(--coral-ink)}strong,b{color:var(--ink)}
em{font-style:normal;font-weight:700;color:var(--coral-ink)}
.eyebrow{font-family:var(--mono);font-size:10.5px;font-weight:500;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
section .wrap>.eyebrow:first-child:before{content:'';display:inline-block;width:22px;height:2px;background:var(--coral);vertical-align:middle;margin-right:9px}
.dsh-nav{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30}
.dsh-nav .wrap{display:flex;align-items:center;gap:20px;min-height:56px}
.dsh-nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}
.dsh-nav .lib{font-family:var(--mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:500}
.dsh-nav ul{list-style:none;display:flex;gap:18px;margin-left:auto}
.dsh-nav .btn{background:var(--ink);color:#fff;border-radius:999px;padding:8px 14px}
@media(max-width:700px){.dsh-nav ul li:not(:last-child){display:none}}
.hero{background:var(--deep);color:#fff;padding:72px 0 60px;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;right:-140px;top:-140px;width:460px;height:460px;border-radius:50%;background:rgba(217,209,255,.11)}
.hero h1{color:#fff}.hero h1 em{color:var(--pop)}.hero .eyebrow{color:var(--pop)}
.hero .lede{font-size:19.5px;color:#D8D2F5;max-width:700px;margin-top:20px}
.hero .tag{margin-top:26px;font-size:21px;font-weight:700;color:var(--pop)}
.metaline{margin-top:32px;display:flex;gap:10px;flex-wrap:wrap}
.pill{border-radius:999px;padding:7px 14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;background:rgba(255,255,255,.09);color:#fff;border:1px solid rgba(255,255,255,.18)}
section{padding:62px 0;border-bottom:1px solid var(--line)}
.sub{color:var(--muted);font-size:17px;max-width:760px;margin-bottom:30px}
.card{background:#fff;border:1px solid var(--line);box-shadow:0 1px 2px rgba(42,27,94,.035);border-radius:var(--r);padding:26px;min-width:0}
.card.dark{background:var(--deep);border:0;color:#D8D2F5}.card.dark h3,.card.dark h4,.card.dark b,.card.dark strong{color:#fff}.card.dark em{color:var(--coral)}.card.dark .eyebrow{color:var(--pop)}
.card.pop{background:var(--pop);border:0}.card.pop .eyebrow{color:#3F31A8}
.card.coral{border:2px solid var(--coral)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.grid2>*,.grid3>*,.grid4>*{min-width:0}
@media(max-width:820px){.grid2,.grid3,.grid4{grid-template-columns:1fr 1fr}}@media(max-width:560px){.grid2,.grid3,.grid4{grid-template-columns:1fr}}
.stat{padding:22px;border-radius:var(--r);background:var(--lilac)}.stat b{display:block;font-size:44px;line-height:1;color:var(--ink);font-variant-numeric:tabular-nums;margin-bottom:8px;letter-spacing:-.03em}.stat span{font-size:14px;color:var(--muted)}
.formula{background:var(--deep);color:#fff;border-radius:var(--r);padding:34px;text-align:center}
.formula .eq{font-size:clamp(22px,3vw,32px);color:#fff;letter-spacing:.01em;line-height:1.5;font-weight:600}
.formula .eq b{color:var(--pop)}.formula .eq i{color:var(--coral);font-style:normal}.formula p{color:#B6AEDD;font-size:14px;margin-top:14px}
.tblwrap{overflow-x:auto;max-width:100%}table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:560px}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
ul.clean{list-style:none;display:grid;gap:8px}ul.clean li{padding-left:18px;position:relative}ul.clean li:before{content:'';position:absolute;left:0;top:.62em;width:8px;height:8px;border-radius:50%;background:var(--violet)}
ul.gate li:before{background:var(--coral)}
.calc{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:820px){.calc{grid-template-columns:1fr}}
.calc label{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:14px 0 6px}
.calc input{width:100%;font:16px var(--sans);padding:10px 12px;border:1px solid var(--line);border-radius:var(--rs);color:var(--ink);font-variant-numeric:tabular-nums}
.calc input:focus{outline:2px solid var(--purple);outline-offset:1px}
.out{display:grid;gap:10px}.out div{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}.out div b{font-variant-numeric:tabular-nums;font-size:20px}
.verdict{margin-top:16px;padding:16px 18px;border-radius:var(--rs);font-weight:700;font-size:15px}
.v-yes{background:#E6F4EC;color:#1B5E3A}.v-no{background:var(--corals);color:var(--coral-ink)}.v-mid{background:#FFF5DD;color:#7A5200}
blockquote{margin:0;font-size:clamp(20px,2.4vw,26px);font-weight:600;line-height:1.3;color:var(--ink)}blockquote:before{content:'“';color:var(--coral)}
.who{margin-top:14px;font-size:14px;color:var(--muted)}.who b{display:block;color:var(--ink)}
.dsh-foot{background:#1A1633;color:#C9C0F0;padding:56px 0 28px}
.dsh-foot a{color:#fff;font-weight:600}.dsh-foot .q{font-size:22px;color:#fff;line-height:1.3;max-width:34ch;margin:0 0 20px;font-weight:600}.dsh-foot .q b{color:var(--coral)}
.dsh-foot .row{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:22px;font-size:14px}.dsh-foot p{max-width:70ch}
/* mailto fallback */
.mailfb{flex-basis:100%;display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:10px;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);font-size:14px;box-shadow:0 12px 30px -18px rgba(42,27,94,.35)}
.mailfb b{font-weight:600;user-select:all;-webkit-user-select:all;word-break:break-all}
.mailfb button,.mailfb a.gm{font:600 13px/1 var(--sans);padding:8px 12px;border-radius:999px;border:1px solid var(--ink);background:var(--ink);color:#fff;cursor:pointer;text-decoration:none}
.mailfb a.gm{background:transparent;color:var(--ink)}
.mailfb .x{margin-left:auto;background:transparent;border:0;color:var(--muted);font-size:18px;padding:4px 8px}
.mailfb.fixed{position:fixed;right:16px;top:72px;z-index:50;max-width:min(420px,calc(100vw - 32px));flex-basis:auto}
.mailfb .ok{color:#1B5E3A;font-weight:600}
.dsh-foot .base{margin-top:36px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8F87B8;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between}
"""

def shell(title, active, body, footer_note):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<nav class="dsh-nav" aria-label="Site"><div class="wrap"><a class="lib" href="/">Open Frameworks</a><span class="lib">· {active}</span><ul><li><a href="/">Library</a></li><li><a href="{MAIN}/work-with-me/">Work with me</a></li><li><a href="{MAIN}/learn/">Learn</a></li><li><a href="{MAIN}/">Main site</a></li><li><a class="btn" data-umami-event="cta_click" data-umami-event-kind="work-with-me" data-umami-event-position="method-nav" href="{MAIN}/work-with-me/">Hire the method →</a></li></ul></div></nav>
{body}
<footer class="dsh-foot"><div class="wrap">
<div class="eyebrow" style="color:#D9D1FF">The routing question</div>
<p class="q">“When this goes wrong, is it because someone <b>chose badly</b>, or because someone <b>couldn't find out</b>?”</p>
<p>Chose badly → <a data-umami-event="framework_open" data-umami-event-framework="lever" href="/lever/">LEVER</a>. Couldn't find out → <a data-umami-event="framework_open" data-umami-event-framework="recall" href="/recall/">RECALL</a>. Neither, but you own a vertical and need a product → <a href="/stake/">STAKE</a>.</p>
<div class="row"><a data-umami-event="cta_click" data-umami-event-kind="work-with-me" data-umami-event-position="method-footer" href="{MAIN}/work-with-me/">Fees and the free Friction Teardown →</a><a href="/case-study-language-kids-world/">Case study: Language Kids World →</a><a href="/">Every framework →</a></div>
<div class="base"><span>{footer_note}</span><span>Free to read. Not free to run on your company — <a href="{MAIN}/work-with-me/" style="font-weight:500">that's the job</a>.</span></div>
</div></footer>
<script>
(function(){{
  var GM='https://mail.google.com/mail/?view=cm&fs=1&to=';
  function show(a,addr,subj){{
    var old=document.querySelector('.mailfb'); if(old) old.remove();
    var box=document.createElement('div'); box.className='mailfb'+(a.closest('.nav, .dsh-nav')?' fixed':''); box.setAttribute('role','dialog');
    box.innerHTML='<span>Write to <b>'+addr+'</b></span><button type="button" class="cp">Copy address</button><a class="gm" target="_blank" rel="noopener" href="'+GM+encodeURIComponent(addr)+(subj?'&su='+encodeURIComponent(subj):'')+'">Open in Gmail</a><button type="button" class="x" aria-label="Close">×</button>';
    box.querySelector('.cp').onclick=function(){{var b=this;(navigator.clipboard?navigator.clipboard.writeText(addr):Promise.reject()).then(function(){{b.textContent='Copied';b.classList.add('ok')}},function(){{var r=document.createRange();r.selectNodeContents(box.querySelector('b'));var s=getSelection();s.removeAllRanges();s.addRange(r)}})}};
    box.querySelector('.x').onclick=function(){{box.remove()}};
    if(box.classList.contains('fixed')) document.body.appendChild(box); else a.insertAdjacentElement('afterend',box);
  }}
  document.querySelectorAll('a[href^="mailto:"]').forEach(function(a){{
    a.addEventListener('click',function(){{
      var href=a.getAttribute('href'),addr=href.slice(7).split('?')[0],q=href.split('?')[1]||'',subj='';
      try{{subj=new URLSearchParams(q).get('subject')||''}}catch(e){{}}
      var t=setTimeout(function(){{show(a,addr,subj)}},900);
      window.addEventListener('blur',function(){{clearTimeout(t)}},{{once:true}});
      document.addEventListener('visibilitychange',function(){{if(document.hidden)clearTimeout(t)}},{{once:true}});
    }});
  }});
}})();
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
STAKE_BODY = f"""
<div class="hero"><div class="wrap">
<div class="eyebrow">Partnership method · v2 · August 2026 · companion to LEVER and RECALL</div>
<h1>The <em>STAKE</em> Method</h1>
<p class="lede">For a business that owns a vertical and needs a product it can't build. I build it and run it on low input; you sell it into the market you already stand in and keep the larger share. The method prices both halves so neither side is quietly subsidising the other.</p>
<p class="tag">I build it. I run it. You sell it.</p>
<div class="metaline"><span class="pill">Partner keeps ~82%</span><span class="pill">Royalty + service fee, priced separately</span><span class="pill">Carry a stream only if RQ ≥ 4</span><span class="pill">Engine-neutral · zero Aletheai IP</span></div>
</div></div>

<section><div class="wrap">
<div class="eyebrow">Where this sits</div>
<h2>The third method, for a different situation</h2>
<p class="sub">LEVER and RECALL are diagnostics: a client pays to find out what to build. STAKE is a partnership: a business that already knows what it needs, owns the route to the buyer, and lacks the capability to build and run it. The unit of analysis is a revenue stream, and the question is whether it pays both parties for years — not whether it launches.</p>
<div class="grid3">
<div class="card"><div class="eyebrow">The partner</div><h3>Owns the vertical</h3><p>Standing in the market, credibility with the buyer, the selling relationship. They do the selling and take the larger share.</p></div>
<div class="card"><div class="eyebrow">Me</div><h3>Builds and runs it</h3><p>System, domain method, hosting, updates, second-line support. Paid by a royalty for the asset and a service fee for the running — two lines, because they fall at different rates.</p></div>
<div class="card coral"><div class="eyebrow">The origin</div><h3>A Houston language-education company</h3><p>Ten full-time staff and around fifty contract teachers. While automating their operations, the tools the founder needed turned out to be tools the whole industry needed. <a href="/case-study-language-kids-world/">The case study →</a></p></div>
</div></div></section>

<section><div class="wrap">
<div class="eyebrow">The model</div>
<h2>Two lines, two equations</h2>
<p class="sub">A royalty pays for the asset and falls as the partner's cash covers more of the build. A service fee pays for the running and does not fall when the build is paid for — because the support calls arrive in year two regardless.</p>
<div class="grid2">
<div class="formula"><div class="eq"><b>Ry</b> = 20% × <i>AS</i> × (1 − 0.4<i>c</i>)</div><p>Royalty. AS = asset share from the Motion Ledger (0–1). c = share of the build funded in cash (0–1). Clamped to 5–18%.</p></div>
<div class="formula"><div class="eq"><b>Sv</b> = 10% × <i>RS</i></div><p>Service fee. RS = run share from the Motion Ledger (0–1). Clamped to 3–12%. Paid as a percentage with a monthly floor.</p></div>
</div>
<div class="tblwrap" style="margin-top:20px"><table>
<thead><tr><th>Line</th><th>Equation</th><th class="n">Case</th><th>Pays for</th></tr></thead>
<tbody>
<tr><td><b>Royalty</b></td><td>Ry = 20% × AS × (1 − 0.4c), clamp 5–18%</td><td class="n"><b>9.0%</b></td><td>The asset. Falls as cash covers more of the build.</td></tr>
<tr><td><b>Service fee</b></td><td>Sv = 10% × RS, clamp 3–12%</td><td class="n"><b>8.1%</b></td><td>The running. Does not fall when the build is paid for.</td></tr>
<tr><td><b>Total</b></td><td>T = Ry + Sv</td><td class="n"><b>17.1%</b></td><td>The partner keeps <b>82.9%</b>.</td></tr>
</tbody></table></div>
<div class="grid2" style="margin-top:20px">
<div class="card"><div class="eyebrow">The Motion Ledger</div><h3>Who does the work that produces each pound</h3><p><b>Asset</b> — system 50 · domain method 30 · concept 20 → <b>AS</b>.<br><b>Run</b> — hosting 25 · updates 40 · second-line support 20 · first-line support 15 → <b>RS</b>.</p><p>Score each row by who actually does it. The shares fall out of the ledger; nobody negotiates them.</p></div>
<div class="card pop"><div class="eyebrow">The floor</div><h3>Floor = monthly run cost × 1.3</h3><p>A pure revenue percentage is a second royalty wearing a different name, and it pays nothing in the year the support calls arrive. In the case: <b>£350/month</b>, with the percentage overtaking the floor at <b>£52,174</b> of annual partner revenue.</p></div>
</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">The decision</div>
<h2>Carry the stream if RQ ≥ 4</h2>
<p class="sub">RQ = annual income ÷ annual run cost. Below four, the stream is a hobby with an invoice attached. Try it with your own numbers — the calculator runs the equations above.</p>
<div class="calc">
<div class="card">
<label for="rev">Partner revenue from the product, per year (£)</label><input id="rev" type="number" value="100000" min="0" step="1000">
<label for="as">Asset share AS (0–1) — from the Motion Ledger</label><input id="as" type="number" value="0.45" min="0" max="1" step="0.01">
<label for="c">Share of the build funded in cash, c (0–1)</label><input id="c" type="number" value="0" min="0" max="1" step="0.05">
<label for="rs">Run share RS (0–1)</label><input id="rs" type="number" value="0.81" min="0" max="1" step="0.01">
<label for="hrs">Your hours per month to run it</label><input id="hrs" type="number" value="2" min="0" step="0.5">
<label for="rate">Your loaded hourly cost (£)</label><input id="rate" type="number" value="120" min="0" step="5">
<label for="host">Hosting and tooling per month (£)</label><input id="host" type="number" value="30" min="0" step="5">
</div>
<div class="card">
<div class="eyebrow" style="margin-bottom:12px">Output</div>
<div class="out">
<div><span>Royalty Ry</span><b id="o-ry">—</b></div>
<div><span>Service fee Sv</span><b id="o-sv">—</b></div>
<div><span>Total take T</span><b id="o-t">—</b></div>
<div><span>Partner keeps</span><b id="o-keep">—</b></div>
<div><span>Your income, per year</span><b id="o-inc">—</b></div>
<div><span>Monthly floor (run cost × 1.3)</span><b id="o-floor">—</b></div>
<div><span>Your run cost, per year</span><b id="o-cost">—</b></div>
<div><span>RQ</span><b id="o-rq">—</b></div>
</div>
<div class="verdict" id="verdict">—</div>
</div>
</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">Three findings</div>
<h2>What the model taught me</h2>
<div class="grid3">
<div class="card"><div class="eyebrow">01</div><h3>Profitability is an engineering problem, not a negotiating one</h3><p>At £100k of partner revenue: two hours a month to run it gives RQ 5.7 — carry. Eight hours gives RQ 2.2 — don't. The rate is irrelevant next to the hours.</p></div>
<div class="card"><div class="eyebrow">02</div><h3>“Passive revenue” is a three-to-six-year build</h3><p>Raising maturity revenue from £100k to £150k pulls year six to year four — as powerful as doubling the signing rate. The take rate barely registers.</p></div>
<div class="card"><div class="eyebrow">03</div><h3>Reporting outranks the rate</h3><p>Not honesty — capability. A business that invoices everything as one line cannot report product revenue separately even when it wants to. Build the reporting before the product.</p></div>
</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">Gates</div>
<h2>Six reasons to walk away</h2>
<div class="grid2">
<div class="card"><ul class="clean gate">
<li><b>TI &lt; 0.50</b> on the Motion Ledger — the split isn't defensible.</li>
<li><b>No second buyer named</b> — one customer is a project, not a product.</li>
<li><b>No service floor</b> — the running is unpaid in the year it costs the most.</li>
<li><b>No reporting obligation</b> — the royalty can't be verified, so it can't be collected.</li>
<li><b>RQ &lt; 4</b> — the stream doesn't pay for its own upkeep.</li>
<li><b>First-line support drifting to you</b> — the named failure mode of the whole model.</li>
</ul></div>
<div class="card dark"><div class="eyebrow">Structure</div><h3>Royalties from a UK company, no US membership interest</h3><p>Both lines are characterised as royalties paid to the UK company. No LLC membership interest in the partner. Structured for 0% withholding under Article 12 of the UK–US treaty. <em>Not tax advice</em> — confirm with counsel on both sides before signing.</p></div>
</div>
</div></section>

<script>
(function(){{
  var ids=['rev','as','c','rs','hrs','rate','host'],el={{}};ids.forEach(function(i){{el[i]=document.getElementById(i)}});
  var gbp=function(n){{return '£'+Math.round(n).toLocaleString('en-GB')}};
  var pct=function(n){{return (n*100).toFixed(1)+'%'}};
  var clamp=function(v,a,b){{return Math.min(b,Math.max(a,v))}};
  function calc(){{
    var rev=+el.rev.value||0, AS=clamp(+el.as.value||0,0,1), c=clamp(+el.c.value||0,0,1), RS=clamp(+el.rs.value||0,0,1);
    var hrs=+el.hrs.value||0, rate=+el.rate.value||0, host=+el.host.value||0;
    var ry=clamp(0.20*AS*(1-0.4*c),0.05,0.18), sv=clamp(0.10*RS,0.03,0.12), t=ry+sv;
    var runMonth=hrs*rate+host, floor=runMonth*1.3, cost=runMonth*12;
    var inc=ry*rev+Math.max(sv*rev, floor*12);  // service fee never falls below the floor
    var rq=cost>0?inc/cost:Infinity;
    document.getElementById('o-ry').textContent=pct(ry); document.getElementById('o-sv').textContent=pct(sv);
    document.getElementById('o-t').textContent=pct(t); document.getElementById('o-keep').textContent=pct(1-t);
    document.getElementById('o-inc').textContent=gbp(inc); document.getElementById('o-floor').textContent=gbp(floor)+'/mo';
    document.getElementById('o-cost').textContent=gbp(cost); document.getElementById('o-rq').textContent=isFinite(rq)?rq.toFixed(2):'∞';
    var v=document.getElementById('verdict'),cls,msg;
    if(rq>=4){{cls='v-yes';msg='Carry the stream. Income covers upkeep '+rq.toFixed(1)+'× over — the running is paid for in the year the support calls arrive.';}}
    else if(rq>=2.5){{cls='v-mid';msg='Marginal. Cut the hours before you touch the rate: every hour a month you remove is worth more than a point of royalty.';}}
    else{{cls='v-no';msg='Do not carry it. Below RQ 4 the stream is a hobby with an invoice attached — raise revenue or engineer the hours out.';}}
    v.className='verdict '+cls; v.textContent=msg;
  }}
  ids.forEach(function(i){{el[i].addEventListener('input',calc)}}); calc();
}})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
CASE_BODY = f"""
<div class="hero"><div class="wrap">
<div class="eyebrow">Case study · 2026 · Houston, Texas · published with the client's permission</div>
<h1>Sixty people, <em>one bottleneck</em>.</h1>
<p class="lede">Language Kids World is a Houston language-education company: ten full-time staff and around fifty contract teachers, founder-led. At that size the founder isn't a busy individual — she is the single-threaded dependency for the output of a whole delivery organisation. This is what it took to move the bottleneck, what it returned, and the product business that fell out of it.</p>
<div class="metaline"><span class="pill">10 full-time · ~50 contract teachers</span><span class="pill">AI automations across operations</span><span class="pill">STAKE partnership</span><span class="pill">Figures are the client's own measurements</span></div>
</div></div>

<section><div class="wrap">
<div class="eyebrow">Outcomes</div>
<h2>What came back</h2>
<div class="grid4">
<div class="stat"><b>92%</b><span>less curriculum-development time</span></div>
<div class="stat"><b>10–15</b><span>working weeks a year returned to the founder</span></div>
<div class="stat"><b>$28–42k</b><span>annual value of founder time returned, at the client's own loaded cost</span></div>
<div class="stat"><b>1</b><span>security breach found unprompted, and closed</span></div>
</div>
<p style="margin-top:18px;font-size:14px;color:var(--muted)">No revenue uplift is claimed for the automations. The value model counts the founder's returned time only; the new product lines are reported separately under the partnership.</p>
</div></section>

<section><div class="wrap"><div class="grid2">
<div>
<div class="eyebrow">The situation</div>
<h2>Founder as the critical path</h2>
<p>Every curriculum, every teacher onboarding, every parent-facing document passed through one person. Curriculum development alone ran to weeks per cycle. Growth was capped not by demand but by the hours in the founder's week — the classic capacity-vs-demand shape that LEVER is built for.</p>
<p>The starting point was the one <a href="/lever/">LEVER</a> is built around: find where the founder's time actually goes, from observation rather than interviews, before automating anything.</p>
</div>
<div>
<div class="eyebrow">What was built</div>
<h2>Automations, in the order that didn't break anything</h2>
<p>A set of AI automations across the operation, sequenced so that each one relieved the next rather than moving the load somewhere else. Curriculum development went from weeks to hours and became the headline, but the returned time came from the whole sequence — the handoffs, the rework and the effort that sat around the founder rather than the single task.</p>
<p>Along the way, a security problem nobody had asked about was found in the existing systems and fixed before it cost anything. It is in the case study because it is the kind of thing a blueprint surfaces and a feature request never does.</p>
</div>
</div></div></section>

<section><div class="wrap">
<div class="eyebrow">In her words</div>
<div class="grid2">
<div class="card"><blockquote>I was the bottleneck for a sixty-person delivery team and didn't know it. Diana built the automations that took curriculum development from weeks to hours and gave me back months of my year. For the first time I'm working on the business instead of inside it.</blockquote><div class="who"><b>Vanessa</b>Founder &amp; CEO, Language Kids World · Houston</div></div>
<div style="display:grid;gap:20px">
<div class="card"><blockquote>What I expected was time savings. What I got was time savings and two new revenue lines. While automating our operations Diana saw that the tools we needed were tools the whole industry needed — so we built them as products.</blockquote></div>
<div class="card"><blockquote>She found a security problem in our systems that nobody had asked her to look for, and fixed it before it cost us.</blockquote></div>
</div>
</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">The second half</div>
<h2>From time saved to revenue <em>created</em></h2>
<p class="sub">The tools the founder needed were tools every operator in the vertical needed. Rather than hand them over as internal software, they became products and services sold under the <a href="/stake/">STAKE</a> model: I build and run them, Language Kids World sells them into the market it already stands in and keeps around 82% of the revenue.</p>
<div class="grid3">
<div class="card"><div class="eyebrow">Why it works</div><h3>They own the vertical</h3><p>Fifteen years of standing in the market, credibility with the buyer, the selling relationship. Nobody I could hire would replace that.</p></div>
<div class="card"><div class="eyebrow">Priced properly</div><h3>Royalty 9.0% · service fee 8.1%</h3><p>Two lines from the Motion Ledger, a £350/month service floor, and a reporting obligation so the royalty can actually be collected.</p></div>
<div class="card dark"><div class="eyebrow">The lesson</div><h3>Time returned is the smaller half</h3><p>An automation engagement that stops at hours saved leaves the larger asset on the table: the products the operation needed were the products the industry needed. <em>Look for the second buyer</em> in month one.</p></div>
</div>
</div></section>

<section><div class="wrap"><div class="card pop" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between">
<div><div class="eyebrow">Your operation</div><h3>Founder as the critical path? Start with the free Friction Teardown.</h3><p style="margin:0">Thirty minutes. I tell you which method fits — or that neither does.</p></div>
<a data-umami-event="email_click" data-umami-event-position="case-study" href="mailto:{EMAIL}?subject=Friction%20Teardown" style="background:var(--ink);color:#fff;border-radius:999px;padding:12px 20px;text-decoration:none;font-weight:600;white-space:nowrap">Book it →</a>
</div></div></section>
"""

if __name__ == "__main__":
    for slug, title, active, body, note in [
        ("stake", "The STAKE Method — I build it. I run it. You sell it.", "STAKE", STAKE_BODY, "STAKE v2 · Diana Simpson-Hernandez · engine-neutral · zero Aletheai IP"),
        ("case-study-language-kids-world", "Sixty people, one bottleneck — Language Kids World case study", "Case study", CASE_BODY, "Case study · Language Kids World · figures are the client's own measurements"),
    ]:
        out = os.path.join(ROOT, slug, "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
        html = shell(title, active, body, note)
        tmp = out + ".tmp"; open(tmp, "w", encoding="utf-8").write(html); os.replace(tmp, out)
        assert os.path.getsize(out) > 8000; print(f"  ✓ {slug}/index.html {len(html)//1024} KB")
