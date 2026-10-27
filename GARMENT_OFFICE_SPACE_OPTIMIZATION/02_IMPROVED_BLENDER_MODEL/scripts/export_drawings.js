// Convert the SVG drawings to PNG (high resolution) and vector PDF (A3 landscape) with Chromium.
// node export_drawings.js DIR
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2100, height: 2973 }, deviceScaleFactor: 1 });
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8').replace(/width="[0-9.]+" height="[0-9.]+">/, 'width="2100" height="2973">');
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>@page{size:297mm 420mm;margin:0}html,body{margin:0;background:#fff}svg{display:block;width:100%;height:auto}</style></head><body>${svg}</body></html>`;
    await page.setContent(html, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(dir, f.replace('.svg', '.png')), fullPage: true });
    await page.pdf({ path: path.join(dir, f.replace('.svg', '.pdf')), width: '297mm', height: '420mm', printBackground: true });
    console.log('exported', f);
  }
  await browser.close();
})();
