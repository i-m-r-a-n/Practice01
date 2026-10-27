// HTML deck -> PDF (1920x1080 pages) + slide PNG thumbnails for QC.  node export_presentation.js PRESENTATION_DIR
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(dir, 'Garment_Office_Design_Pitch.html'), { waitUntil: 'networkidle' });
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.pdf({ path: path.join(dir, 'Garment_Office_Design_Pitch.pdf'), width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
  const thumbs = path.join(dir, 'slide_png'); fs.mkdirSync(thumbs, { recursive: true });
  const n = await page.evaluate(() => document.querySelectorAll('.slide').length);
  for (let i = 0; i < n; i++) {
    const el = (await page.$$('.slide'))[i];
    await el.screenshot({ path: path.join(thumbs, `slide_${String(i + 1).padStart(2, '0')}.png`) });
  }
  console.log('pdf + ' + n + ' slide images');
  await browser.close();
})();
