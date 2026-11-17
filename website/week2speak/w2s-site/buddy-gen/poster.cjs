// Static pictures of the active Buddies (the no-WebGL fallback and the placeholder before the 3D loads), rendered from the real models.
// Reads the roster from the served site (assets/config.js). A Buddy whose model lives in buddy-models/ gets its picture there too.
const {chromium} = require('playwright'); const fs = require('fs'); const {execFileSync} = require('child_process');
(async () => { const b = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']});
  const probe = await b.newPage(); await probe.goto('http://localhost:8765/speech-mode/'); const roster = await probe.evaluate(() => window.W2S_BUDDIES || []); await probe.close();
  const made = [];
  for (const {id, file: served} of roster) { const file = served.replace(/\.[0-9a-f]{10}$/, '');   /* the served name carries a content hash */ const ctx = await b.newContext({viewport: {width: 360, height: 640}, deviceScaleFactor: 1.5, isMobile: true, hasTouch: true}); const p = await ctx.newPage();
    await p.addInitScript(i => { try { const s = JSON.parse(localStorage.getItem('w2s.v1') || '{}'); s.buddy = i; localStorage.setItem('w2s.v1', JSON.stringify(s)); } catch (e) {} }, id);
    await p.goto('http://localhost:8765/speech-mode/', {waitUntil: 'networkidle'}); await p.waitForFunction(() => window.W2SBuddies && window.W2SBuddies.ready, null, {timeout: 90000}); await p.evaluate(() => { window.W2SBuddies.lockQuality = true; window.W2SBuddies.setQuality(0); }); await p.waitForTimeout(2600);
    const url = await p.evaluate(() => { const D = window.W2SBuddies; D.view({rot: 0, blink: 0}); return D.snap(); });
    const dir = fs.existsSync(`buddy-models/${file}.glb`) ? 'buddy-models' : 'buddy-gen/out';
    fs.writeFileSync(`${dir}/${file}.png`, Buffer.from(url.split(',')[1], 'base64')); made.push(`${dir}/${file}`);
    console.log(file, await p.evaluate(() => window.W2SBuddies.id + ' ' + JSON.stringify(window.W2SBuddies.info))); await ctx.close(); }
  await b.close();
  execFileSync('python3', ['-c', "import sys\nfrom PIL import Image\nfor n in sys.argv[1:]:\n    im=Image.open(n+'.png'); im.save(n+'.webp','WEBP',quality=84,method=6); print(n, im.size)", ...made], {stdio: 'inherit'}); })();
