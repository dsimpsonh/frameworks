#!/usr/bin/env python3
"""
canvases/build_canvases.py — renders the DSH canvas collection.

  python3 canvases/build_canvases.py            # everything
  python3 canvases/build_canvases.py preview    # HTML + PNG previews only (fast)
  python3 canvases/build_canvases.py pages      # landing pages + hub + frameworks.json only

Free (in repo, watermarked):   canvas/<slug>/<slug>-canvas.pdf      raster A3, 150dpi, tiled mark
                                canvas/<slug>/<slug>-quick-guide.pdf 2-page guide, watermarked
                                assets/preview-canvas-<slug>.png     landing/OG preview
Paid (NOT in repo):             dist/canvas-pack/<slug>-canvas.pdf    vector A3
                                dist/canvas-pack/<slug>-canvas-4k.png 3840px wide
                                dist/canvas-pack/<slug>-guide.pdf     full guide
Head SEO/OG/analytics for the landing pages are injected afterwards by build_library.py.
"""
import os, sys, json, io, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_canvas import canvas_html, ROOT
from render_guide import guide_html
from render_pages import landing_html, hub_html, update_frameworks_json

DATA = json.load(open(os.path.join(ROOT, "canvases", "data", "canvases.json")))
DIST = os.path.join(os.path.dirname(ROOT), "dist", "canvas-pack")
A3 = {"width": "420mm", "height": "297mm"}
A3_PX = (1587, 1123)          # 96dpi
A4 = {"width": "210mm", "height": "297mm"}

def w(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(s)

def raster_pdf(png_bytes, out, dpi):
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    im.save(out, "PDF", resolution=dpi, quality=92, optimize=True)

def render_all(mode="all"):
    from playwright.sync_api import sync_playwright
    os.makedirs(DIST, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for c in DATA["canvases"]:
            slug = c["slug"]; cdir = os.path.join(ROOT, "canvas", slug)
            os.makedirs(cdir, exist_ok=True)
            # ── canvas, clean (paid) ──
            pg = b.new_page(viewport={"width": A3_PX[0], "height": A3_PX[1]}, device_scale_factor=1)
            pg.set_content(canvas_html(c, watermark=False)); pg.wait_for_timeout(150)
            pg.emulate_media(media="screen")
            if mode == "all":
                pg.pdf(path=os.path.join(DIST, f"{slug}-canvas.pdf"), print_background=True, prefer_css_page_size=False, **A3, margin={"top":"0","right":"0","bottom":"0","left":"0"})
                pg4 = b.new_page(viewport={"width": A3_PX[0], "height": A3_PX[1]}, device_scale_factor=3840/A3_PX[0])
                pg4.set_content(canvas_html(c, watermark=False)); pg4.wait_for_timeout(150)
                pg4.screenshot(path=os.path.join(DIST, f"{slug}-canvas-4k.png"), full_page=False); pg4.close()
            pg.close()
            # ── canvas, watermarked (free) ──
            pg = b.new_page(viewport={"width": A3_PX[0], "height": A3_PX[1]}, device_scale_factor=150/96)
            pg.set_content(canvas_html(c, watermark=True)); pg.wait_for_timeout(150)
            png = pg.screenshot(full_page=False)
            raster_pdf(png, os.path.join(cdir, f"{slug}-canvas.pdf"), 150)
            pg.close()
            # thumbnail for landing pages (1400px wide, free edition) + 1200x630 OG card
            thumb = os.path.join(ROOT, "assets", f"canvas-{slug}-thumb.png")
            pg = b.new_page(viewport={"width": A3_PX[0], "height": A3_PX[1]}, device_scale_factor=1400/A3_PX[0])
            pg.set_content(canvas_html(c, watermark=True)); pg.wait_for_timeout(150)
            pg.screenshot(path=thumb); pg.close()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            pg.set_content(og_html(c, thumb)); pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(ROOT, "assets", f"preview-canvas-{slug}.png")); pg.close()
            w(os.path.join(ROOT, "canvases", "out", f"{slug}.html"), canvas_html(c, watermark=True))  # for eyeballing
            if mode == "all":
                # ── guides ──
                pg = b.new_page(viewport={"width": 794, "height": 1123})
                pg.emulate_media(media="print")
                pg.set_content(guide_html(c, full=True, watermark=False)); pg.wait_for_timeout(150)
                pg.pdf(path=os.path.join(DIST, f"{slug}-guide.pdf"), print_background=True, prefer_css_page_size=True)
                pg.set_content(guide_html(c, full=False, watermark=True)); pg.wait_for_timeout(150)
                pg.pdf(path=os.path.join(cdir, f"{slug}-quick-guide.pdf"), print_background=True, prefer_css_page_size=True)
                w(os.path.join(ROOT, "canvases", "out", f"{slug}-guide.html"), guide_html(c, full=True, watermark=False))
                pg.close()
            print("rendered", slug)
        b.close()
    if mode == "all":
        # pack README + licence
        w(os.path.join(DIST, "README.txt"), pack_readme())

def og_html(c, thumb):
    import base64, html as H
    from render_canvas import font_css
    img = "data:image/png;base64," + base64.b64encode(open(thumb, "rb").read()).decode()
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{font_css()}
body{{margin:0;width:1200px;height:630px;background:#2A1B5E;color:#fff;font-family:'Schibsted Grotesk',sans-serif;position:relative;overflow:hidden}}
.bar{{position:absolute;left:0;top:0;width:1200px;height:14px;background:linear-gradient(100deg,#5B4BC4 6%,#8A7BE8 46%,#F96167 94%)}}
.k{{position:absolute;left:64px;top:64px;font:500 16px 'Martian Mono';letter-spacing:.12em;text-transform:uppercase;color:#D9D1FF}}
.t{{position:absolute;left:64px;top:120px;width:520px;font:800 {58 if len(c["title"])<26 else 48}px/1.02 'Schibsted Grotesk';letter-spacing:-.03em}}
.s{{position:absolute;left:64px;top:{330 if len(c["title"])<26 else 300}px;width:500px;font:500 22px/1.35 'Schibsted Grotesk';color:#D8D2F5}}
.d{{position:absolute;left:64px;bottom:52px;font:500 15px 'Martian Mono';letter-spacing:.1em;text-transform:uppercase;color:#B6AEDD}}.d b{{color:#F96167}}
.f{{position:absolute;left:64px;bottom:96px;background:#F96167;color:#1A1633;font:700 15px 'Schibsted Grotesk';padding:9px 16px;border-radius:999px}}
.img{{position:absolute;left:640px;top:90px;width:760px;border-radius:10px;box-shadow:0 40px 80px -30px rgba(0,0,0,.7);transform:rotate(-4deg)}}
</style></head><body><div class="bar"></div><div class="k">DSH canvas · free download</div><div class="t">{H.escape(c["title"])}</div><div class="s">{H.escape(c["subtitle"])}</div>
<div class="f">Free A3 PDF + quick guide</div><div class="d">frameworks.dianasimpsonhernandez.com <b>·</b> canvas pack £49</div><img class="img" src="{img}"></body></html>"""

def pack_readme():
    p = DATA["pack"]
    lines = [p["name"], "=" * len(p["name"]), "", "Thank you for buying the pack. What's inside:", ""]
    for c in DATA["canvases"]:
        lines += [f"  {c['slug']}-canvas.pdf      {c['title']} — A3 landscape, vector, print-ready",
                  f"  {c['slug']}-canvas-4k.png   same canvas, 3840px PNG for Miro / FigJam / Figma / Notion",
                  f"  {c['slug']}-guide.pdf       full walkthrough guide (A4)", ""]
    lines += ["Licence: single-team use. Run it in your company, your workshops and your client work.",
              "Please don't resell it or upload it to template marketplaces.",
              "Updates: new versions are sent to the email you bought with.",
              "", "Questions: dianasimpsonhernandez@gmail.com", "https://dianasimpsonhernandez.com"]
    return "\n".join(lines) + "\n"

def build_pages():
    for c in DATA["canvases"]:
        w(os.path.join(ROOT, "canvas", c["slug"], "index.html"), landing_html(c, DATA))
    w(os.path.join(ROOT, "canvas", "index.html"), hub_html(DATA))
    update_frameworks_json(DATA)
    print("pages written")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "preview"): render_all(mode)
    if mode in ("all", "pages"): build_pages()
