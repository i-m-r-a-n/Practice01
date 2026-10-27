// Render book HTML -> A3 landscape PDF.  node export_render_book.js PRESENTATION_DIR
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'Garment_Office_Render_Book.html'), { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
  });
  const broken = await page.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src));
  if (broken.length) { console.error('missing images:', broken); process.exit(1); }
  await page.pdf({ path: path.join(dir, 'Garment_Office_Render_Book.pdf'), preferCSSPageSize: true, printBackground: true });
  console.log('render book pdf written');
  await browser.close();
})();
