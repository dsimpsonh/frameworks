# frameworks
Frameworks From Diana Simpson-Hernandez Substack

# dianasimpsonhernandez.com

Personal site + frameworks directory. Editorial-minimal aesthetic, AI-founder positioning.

---

## 🏗️ Architecture

```
/
├── index.html                    Landing page (about, frameworks, writing, contact)
├── styles/main.css               Shared design system (CSS variables, type, palette)
├── data/frameworks.json          Single source of truth for all frameworks
├── x/
│   ├── index.html                Frameworks directory page (auto-renders from JSON)
│   └── [slug]/index.html         One folder per framework
└── assets/                       Images, OG tags, CV PDF
```

**Why this design:**
- `frameworks.json` drives both the landing-page gallery AND the `/x/` directory. Add a framework once, it appears in both.
- Each framework has its own URL (`/x/signal-factory/`) — clean, shareable, indexable.
- Pure static HTML/CSS/vanilla JS. No build, no dependencies, ships on GitHub Pages.

---

## 🚀 Deploy to GitHub Pages

1. Push this directory to your repo (e.g. `dianasimpsonhernandez/dianasimpsonhernandez.com`).
2. Settings → Pages → Source: **Deploy from branch** → `main` / root.
3. Custom domain: add `dianasimpsonhernandez.com` and create a `CNAME` file at the repo root containing only that domain.
4. Point your domain's DNS:
   - `A` records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - or `CNAME` → `<username>.github.io`

---

## ➕ How to add a new framework (3 steps)

**Step 1.** Add an entry to `data/frameworks.json`:

```json
{
  "slug": "your-framework",
  "title": "Your Framework Name",
  "subtitle": "One-line italic positioning",
  "category": "Framework | Architecture | Methodology",
  "year": "2025",
  "tags": ["AI", "Strategy"],
  "summary": "2–3 sentence description.",
  "status": "Live | Draft | Archive",
  "url": "/x/your-framework/"
}
```

**Step 2.** Duplicate `x/signal-factory/` → `x/your-framework/` and edit the content inside `index.html`. The structure (hero, architecture diagram, layer cards, application steps) is reusable.

**Step 3.** Commit and push. Both the landing page and `/x/` directory will pick it up automatically.

---

## 🎨 Design System

All tokens in `styles/main.css` under `:root`:

| Token | Value | Use |
|---|---|---|
| `--paper` | `#f6f4ef` | Background |
| `--ink` | `#1a1a1a` | Primary text |
| `--accent` | `#c8462c` | Signal red — links, hover, italic emphasis |
| `--font-display` | Fraunces | Headings, lede, italic emphasis |
| `--font-body` | Inter Tight | Body text, UI |
| `--font-mono` | JetBrains Mono | Eyebrows, metadata, code |

To rebrand: change CSS variables, no other changes needed.

---

## 🔧 Local dev

The frameworks gallery uses `fetch()` to load JSON, which requires HTTP (won't work on `file://`).

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

---

## 📋 Pre-launch checklist

- [ ] Replace placeholder LinkedIn / Substack / YouTube URLs in `index.html` footer
- [ ] Add `assets/og-image.png` (1200×630) for social previews
- [ ] Add `assets/diana-simpson-hernandez-cv.pdf`
- [ ] Add `favicon.ico` and apple-touch-icon
- [ ] Update meta description and OG tags with final copy
- [ ] Verify all `/x/[slug]/` framework pages exist for entries in `frameworks.json`
- [ ] Add Plausible / Fathom / GA4 analytics snippet if needed
- [ ] Add `CNAME` file with `dianasimpsonhernandez.com`

---

## 🗺️ Roadmap (suggested)

| Version | What |
|---|---|
| **v1.0** | This — landing + 3 framework pages |
| v1.1 | Add MDX-style markdown rendering for framework bodies (write in `.md`, render in HTML shell) |
| v1.2 | Add `/now` page (current focus, monthly updated) |
| v1.3 | Add `/library` — Esoterica book series landing |
| v2.0 | Migrate to Astro if you want SSG with components — same JSON, same CSS, faster auth |

---

Built v1.0 — 2026.
