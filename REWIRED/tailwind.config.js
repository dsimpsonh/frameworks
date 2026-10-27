// Tailwind v3 for /REWIRED/ (no CDN at runtime). Rebuild from the repo root:
//   npx tailwindcss@3 -c REWIRED/tailwind.config.js -i REWIRED/tw.in.css -o REWIRED/tw.css --minify
module.exports = Object.assign({}, require('./tailwind.theme.js'), { content: { relative: true, files: ["./index.html"] } });
