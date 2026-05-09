# frameworks

Frameworks From Diana Simpson-Hernandez Substack.
Lives at **dianasimpsonhernandez.com**

---

## 🏗️ Architecture

```
/                              ← serves dianasimpsonhernandez.com
├── index.html                 ← MAIN LANDING PAGE (you, frameworks, links)
├── data/
│   └── frameworks.json        ← single source of truth — edit to update gallery
├── styles/
│   └── main.css               ← shared design system
├── assets/                    ← images, OG, CV PDF
├── REWIRED/index.html         ← /REWIRED/
├── flywheel/index.html        ← /flywheel/
├── rediscovery-canvas/...     ← /rediscovery-canvas/
├── teamscale/index.html       ← /teamscale/
├── vibecoding/index.html      ← /vibecoding/
├── CNAME                      ← dianasimpsonhernandez.com
└── README.md
```

The root `index.html` is the **homepage** — bio, framework gallery (auto-rendered from `frameworks.json`), writing links, contact.

---

## ➕ How to add a new framework (3 steps)

**1.** Create the folder + `index.html`:
```bash
mkdir new-framework-name
# add new-framework-name/index.html with your content
```

**2.** Add an entry to `data/frameworks.json`:
```json
{
  "slug": "new-framework-name",
  "title": "Your Framework Name",
  "subtitle": "One-line italic positioning",
  "category": "Methodology | Strategy | Canvas | Operating Model | Course",
  "year": "2026",
  "tags": ["AI", "Strategy"],
  "summary": "2–3 sentence description.",
  "status": "Live",
  "url": "/new-framework-name/"
}
```

**3.** Commit, push. The homepage gallery picks it up automatically.

> ⚠️ Folder name must match `slug` and `url` exactly. Case-sensitive on GitHub Pages (e.g. `REWIRED`, not `rewired`).

---

## 🎨 Design System

Tokens in `styles/main.css` under `:root`:

| Token | Value | Use |
|---|---|---|
| `--paper` | `#f6f4ef` | Background |
| `--ink` | `#1a1a1a` | Primary text |
| `--accent` | `#c8462c` | Signal red — links, italic emphasis |
| `--font-display` | Fraunces | Headings, italic emphasis |
| `--font-body` | Inter Tight | Body text, UI |
| `--font-mono` | JetBrains Mono | Eyebrows, metadata, code |

To rebrand: change CSS variables only.

---

## 🔗 Apply the design system to your existing 5 framework pages (optional)

To make REWIRED, flywheel, etc. visually consistent with the homepage, add this to the `<head>` of each framework's `index.html`:

```html
<link rel="stylesheet" href="/styles/main.css">
```

Then wrap navigation in:
```html
<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-mark">Diana Simpson <span>Hernandez</span></a>
    <ul class="nav-links">
      <li><a href="/#about">About</a></li>
      <li><a href="/#frameworks">Frameworks</a></li>
    </ul>
  </div>
</nav>
```

This is optional — your existing framework pages keep working as-is.

---

## 🔧 Local dev

The gallery uses `fetch()` to load JSON, which requires HTTP (won't work on `file://`).

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

---

## ✅ Pre-launch checklist

- [ ] Replace LinkedIn / Substack / YouTube / GitHub URLs in footer
- [ ] Replace Aletheai URL if different
- [ ] Add `assets/og-image.png` (1200×630) for social previews
- [ ] Add `assets/diana-simpson-hernandez-cv.pdf`
- [ ] Add `favicon.ico` to root
- [ ] Edit framework subtitles in `data/frameworks.json` to match your real positioning
- [ ] Verify `CNAME` contains `dianasimpsonhernandez.com`
- [ ] (Optional) Add Plausible / Fathom analytics snippet

---

## 🗺️ Roadmap

| Version | What |
|---|---|
| **v1.0** | This — landing page + gallery driven by `frameworks.json` |
| v1.1 | Apply shared `main.css` to all 5 framework pages for visual consistency |
| v1.2 | Add `/now` page (current focus, monthly updated) |
| v1.3 | Auto-generate OG images per framework |
| v2.0 | Migrate to Astro for SSG with components — same JSON, same CSS |

Built v1.0 — 2026.
