// Tailwind v3 for /teamscale/ (no CDN at runtime). Rebuild from the repo root:
//   npx tailwindcss@3 -c teamscale/tailwind.config.js -i teamscale/tw.in.css -o teamscale/tw.css --minify
module.exports = Object.assign({}, require('./tailwind.theme.js'), { content: { relative: true, files: ["./index.html", "./app.jsx"] } });
