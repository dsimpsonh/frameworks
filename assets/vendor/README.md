# Vendored libraries (self-hosted, no third-party CDN at runtime)

| File | Source | Version | Used by |
|---|---|---|---|
| chart.umd.min.js | npm chart.js | 4.4.0 | /flywheel/ |
| react.production.min.js | npm react (UMD) | 18.2.0 | /teamscale/ |
| react-dom.production.min.js | npm react-dom (UMD) | 18.2.0 | /teamscale/ |
| html2pdf.bundle.min.js | npm html2pdf.js | 0.10.1 | /teamscale/ (PDF export) |

Tailwind is compiled to static CSS per page (`/REWIRED/tw.css`, `/teamscale/tw.css`) and the teamscale JSX is
precompiled to `/teamscale/app.js` by `pages/align_v5.py`, so neither page loads the Tailwind or Babel CDNs.
Licences: MIT (all four).
