/* Week2Speak Language Buddies, version 2: Ruby and Max, two human avatars loaded from GLB files.
   The page talks to them with window events: w2s:speak, w2s:word, w2s:speakend, w2s:mic, w2s:good, w2s:oops, w2s:help, w2s:done, w2s:buddy.
   Face rig: morph targets when the model has them (jawOpen, mouthPucker, mouthWide, mouthSmile, mouthFrown, or ARKit / viseme names), eyelids, eyes and brows as nodes.
   Body rig: bones named Hips, Spine, Neck, Head, Left/RightArm, Left/RightForeArm, Left/RightHand, Left/RightUpLeg. See buddy-models/README.md. */
import * as THREE from './vendor/three-0.170.0.module.min.js';
import {GLTFLoader} from './vendor/GLTFLoader-0.170.0.js';

const wrap = document.getElementById('buddy'), stage = document.getElementById('buddyStage'), sm = document.getElementById('sm');
const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const ROSTER = (window.W2S_BUDDIES && window.W2S_BUDDIES.length) ? window.W2S_BUDDIES : [{id: 'mila', file: 'ruby'}, {id: 'rio', file: 'max'}];   // buddy_roster.py, via config.js
const FILE = {}; ROSTER.forEach(b => { FILE[b.id] = b.file; });
const pick = id => FILE[id] ? id : ROSTER[0].id;
const D = window.W2SBuddies = {ready: false, id: null, log: [], fps: 0, turns: 0, spun: 0, mouth: 0, blink: 0, speaking: false, listening: false, info: {}, delights: {}, quality: 0, renderer: '', reduced: RM, rig: ''};
const lerp = (a, b, t) => a + (b - a) * t, clamp = (v, a, b) => v < a ? a : v > b ? b : v, rnd = (a, b) => a + Math.random() * (b - a);
class Spring { constructor(x = 0, k = 140, d = 17) { this.x = x; this.t = x; this.v = 0; this.k = k; this.d = d; } step(dt) { this.v += ((this.t - this.x) * this.k - this.v * this.d) * dt; this.x += this.v * dt; return this.x; } }

/* ---------- sound effects (tiny synth, silent until the first tap) ---------- */
let AC = null, muted = false, touched = false; try { muted = localStorage.getItem('w2s.buddyMute') === '1'; } catch (e) {}
function tone(f, dur = 0.12, type = 'sine', vol = 0.08, slide = 0, delay = 0) {
  if (muted || !touched) return; try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); const t = AC.currentTime + delay, o = AC.createOscillator(), g = AC.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (slide) o.frequency.exponentialRampToValueAtTime(Math.max(40, f + slide), t + dur); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.connect(g); g.connect(AC.destination); o.start(t); o.stop(t + dur + 0.03); } catch (e) {}
}
const SFX = {pop: () => tone(520, 0.09, 'triangle', 0.09, 380), boop: () => tone(300, 0.12, 'sine', 0.1, 260), whoosh: () => tone(900, 0.22, 'sawtooth', 0.03, -700), giggle: () => { tone(660, 0.07, 'triangle', 0.06); tone(820, 0.07, 'triangle', 0.06, 0, 0.09); tone(740, 0.09, 'triangle', 0.06, 0, 0.18); }, good: () => { tone(660, 0.1, 'triangle', 0.08); tone(990, 0.16, 'triangle', 0.08, 0, 0.1); }, hmm: () => tone(260, 0.2, 'sine', 0.07, -60), win: () => [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.16, 'triangle', 0.08, 0, i * 0.1)), sip: () => tone(180, 0.25, 'sine', 0.05, 120)};
const buzz = ms => { if (touched && navigator.vibrate && !RM) try { navigator.vibrate(ms); } catch (e) {} };

/* ---------- renderer, scene, lights ---------- */
let renderer, scene, camera, canvas, shadowLight, ground, blob, raf = 0, running = false, visible = true, W = 1, H = 1, last = 0;
const QUAL = [{pr: 2, sh: true}, {pr: 1.5, sh: true}, {pr: 1.5, sh: false}, {pr: 1, sh: false}];   // steps down: pixel ratio, then the shadow pass
// phones start lighter: no shadow pass (the soft contact shadow stays), textures at 1024 px, the second Buddy not on the GPU until it is shown
const LIGHT = window.matchMedia('(max-width: 899px), (pointer: coarse)').matches;
function boot() {
  try { if (!document.createElement('canvas').getContext('webgl2')) throw new Error('no WebGL 2'); canvas = document.createElement('canvas'); canvas.className = 'buddy-canvas'; canvas.tabIndex = 0; canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', 'Tu Buddy. Arrástralo para girarlo y tócalo para que reaccione.');
    renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: true, powerPreference: 'high-performance'}); } catch (e) { wrap.classList.add('no-3d'); return false; }
  const gl = renderer.getContext(); try { const x = gl.getExtension('WEBGL_debug_renderer_info'); D.renderer = String(x ? gl.getParameter(x.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER)); } catch (e) {}
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.setClearColor(0x000000, 0);
  scene = new THREE.Scene(); camera = new THREE.PerspectiveCamera(24, 1, 0.5, 60);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xe2d8ea, 1.3));
  shadowLight = new THREE.DirectionalLight(0xfff1dd, 2.1); shadowLight.position.set(2.4, 4.6, 5); shadowLight.castShadow = true; shadowLight.shadow.mapSize.set(1024, 1024); Object.assign(shadowLight.shadow.camera, {left: -1.7, right: 1.7, top: 2.9, bottom: -0.6, near: 1, far: 16}); shadowLight.shadow.bias = -0.0006; shadowLight.shadow.normalBias = 0.025; scene.add(shadowLight);
  const rim = new THREE.DirectionalLight(0xffc58a, 2.6); rim.position.set(-3, 3.2, -4); scene.add(rim);     // warm rim light from behind
  const fill = new THREE.DirectionalLight(0xcdd7ff, 0.55); fill.position.set(-3.5, 1.5, 3); scene.add(fill);
  ground = new THREE.Mesh(new THREE.PlaneGeometry(8, 8), new THREE.ShadowMaterial({opacity: 0.2})); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 4, 64, 64, 62); gr.addColorStop(0, 'rgba(11,16,58,.5)'); gr.addColorStop(0.55, 'rgba(11,16,58,.2)'); gr.addColorStop(1, 'rgba(11,16,58,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  blob = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.95), new THREE.MeshBasicMaterial({map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false})); blob.rotation.x = -Math.PI / 2; blob.position.y = 0.006; scene.add(blob);   // contact shadow under the feet
  stage.appendChild(canvas); return true;
}
function setQuality(q) { D.quality = clamp(q, 0, QUAL.length - 1); const Q = QUAL[D.quality]; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, Q.pr)); renderer.shadowMap.enabled = Q.sh; shadowLight.castShadow = Q.sh; ground.visible = Q.sh; renderer.setSize(W, H, false);  if (B && scene && camera) renderer.render(scene, camera); }

/* ---------- a Buddy: model, rig lookup, pose channels ---------- */
const buddies = {}, loading = {}; let B = null, pending = null;
const IDLE = {hx: 0, hy: 0, hz: 0, sx: 0, sy: 0, sz: 0, lax: 0.1, lay: -0.62, laz: -0.04, lfx: -1.32, lfz: 0.1, rax: 0, ray: 0, raz: 0, rfx: -0.14, rfz: 0, rhz: 0, shrug: 0, brow: 0, browTilt: 0, squint: 0, cross: 0, legL: 0, legR: 0, lean: 0, headS: 1, armsOut: 0};
const FACE_KEYS = ['brow', 'browTilt', 'squint', 'cross', 'hx', 'hz', 'hy'];
const RIM = {value: new THREE.Color(1.0, 0.8, 0.58).multiplyScalar(0.34)};
function rimPatch(m) { if (m.userData.rim) return; m.userData.rim = 1; m.onBeforeCompile = s => { s.uniforms.uRim = RIM; s.fragmentShader = s.fragmentShader.replace('void main() {', 'uniform vec3 uRim;\nvoid main() {').replace('#include <opaque_fragment>', 'float rimF = pow(1.0 - saturate(dot(normalize(vViewPosition), normal)), 2.6);\noutgoingLight += uRim * rimF * smoothstep(-0.35, 0.7, normal.y);\n#include <opaque_fragment>'); }; }
async function fetchModel(name) {
  const base = '/assets/buddies/' + name + '.glb';
  if ('DecompressionStream' in window) try { const r = await fetch(base + '.gz'); if (r.ok) { const buf = await r.arrayBuffer(), u = new Uint8Array(buf, 0, 4); if (u[0] === 0x67 && u[1] === 0x6C) return buf; return await new Response(new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer(); } } catch (e) {}
  let r = await fetch(base); if (!r.ok) r = await fetch(base + '?retry=' + Date.now(), {cache: 'no-store'});   // a 404 kept from a deploy in progress
  if (!r.ok) throw new Error('model ' + r.status); return r.arrayBuffer();
}
function load(id) { if (buddies[id]) return Promise.resolve(buddies[id]); if (loading[id]) return loading[id];
  return loading[id] = fetchModel(FILE[id]).then(buf => new Promise((ok, no) => new GLTFLoader().parse(buf, '', g => ok(buddies[id] = make(g, id)), no))); }
function shrinkMap(m) {   // phones: the 2048 px texture at 1024 px (a quarter of the GPU memory; the face is ~150 px wide on screen)
  const t = m && m.map, im = t && t.image; if (!im || !im.width || im.width <= 1024) return;
  const c = document.createElement('canvas'); c.width = Math.round(im.width / 2); c.height = Math.round(im.height / 2); c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); t.image = c; t.needsUpdate = true;
}
function make(gltf, id) {
  const model = gltf.scene, ex = model.userData.w2s || {}, full = ex.rig === 'w2s-1';
  const N = (...names) => { for (const n of names) { const o = model.getObjectByName(n); if (o) return o; } return null; };
  const b = {id, model, ex, full, P: {}, M: {jaw: 0, pucker: 0, wide: 0, smile: 0.3, frown: 0}, Mt: {jaw: 0, pucker: 0, wide: 0, smile: 0.3, frown: 0}, morph: [], blink: 0, gaze: {x: new Spring(0, 90, 14), y: new Spring(0, 90, 14)}, rot: 0, rotV: 0, hop: 0, hopV: 0, sq: new Spring(1, 260, 14), pop: new Spring(1, 170, 13), pony: new Spring(0, 60, 5), pony2: new Spring(0, 60, 5), nextBlink: rnd(1.5, 3.5), shades: null, shadesS: new Spring(0, 180, 13)};
  for (const k in IDLE) b.P[k] = new Spring(IDLE[k], k === 'headS' ? 90 : 130, k === 'headS' ? 9 : 16);
  b.spin = new THREE.Group(); b.tilt = new THREE.Group(); b.sqG = new THREE.Group(); b.spin.add(b.tilt); b.tilt.add(b.sqG); b.sqG.add(model);
  model.traverse(o => { if (!o.isMesh) return; o.frustumCulled = false; o.castShadow = !/Shine/.test(o.name); o.receiveShadow = !/Eye|Shine|Lid|Lash|Head|Mouth|Brow|Freckle/.test(o.name); const m = o.material; if (m && m.isMeshStandardMaterial) { if (LIGHT) shrinkMap(m); if (!/Eye|Shine/.test(m.name)) rimPatch(m); if (/Shine/.test(m.name)) m.emissive = new THREE.Color(1, 1, 1); }
    if (o.morphTargetDictionary) b.morph.push(o); });
  b.bones = {hips: N('Hips', 'mixamorigHips', 'pelvis'), spine: N('Spine', 'Spine1', 'Chest', 'mixamorigSpine1'), neck: N('Neck', 'mixamorigNeck'), head: N('Head', 'mixamorigHead'), la: N('LeftArm'), lf: N('LeftForeArm'), lh: N('LeftHand'), ra: N('RightArm'), rf: N('RightForeArm'), rh: N('RightHand'), ll: N('LeftUpLeg'), rl: N('RightUpLeg')};
  b.lid = [N('LidL'), N('LidR')]; b.low = [N('LowLidL'), N('LowLidR')]; b.eye = [N('EyeL'), N('EyeR')]; b.brow = [N('BrowL'), N('BrowR')]; b.ponyN = N('Pony'); b.prop = N('Prop');
  b.rest = {}; for (const k of ['la', 'ra']) if (b.bones[k]) b.rest[k] = b.bones[k].position.y; b.browY = b.brow.map(n => n ? n.position.y : 0);
  const box = new THREE.Box3().setFromObject(model); b.H = ex.height || box.max.y; b.fw = ex.faceWidth || b.H * 0.34; b.lidOpen = ex.lidOpen != null ? ex.lidOpen : -0.6; b.lidClosed = ex.lidClosed || 1.25; b.lowLid = ex.lowLid || 0.9;
  // which morph target names this model offers for each mouth control
  const ALIAS = {jaw: ['jawOpen', 'mouthOpen', 'viseme_aa', 'MouthOpen'], pucker: ['mouthPucker', 'mouthFunnel', 'viseme_U', 'viseme_O'], wide: ['mouthWide', 'mouthStretchLeft', 'mouthStretchRight', 'viseme_I', 'viseme_E'], smile: ['mouthSmile', 'mouthSmileLeft', 'mouthSmileRight'], frown: ['mouthFrown', 'mouthFrownLeft', 'mouthFrownRight'], blink: ['eyeBlinkLeft', 'eyeBlinkRight', 'eyesClosed', 'blink', 'Blink']};
  b.mt = {}; for (const k in ALIAS) { b.mt[k] = []; for (const o of b.morph) for (const n of ALIAS[k]) if (n in o.morphTargetDictionary) { b.mt[k].push([o, o.morphTargetDictionary[n]]); if (k === 'jaw' || k === 'pucker') break; } }
  b.chibi = ex.rig === 'w2s-chibi-1' && !!b.bones.head;
  if (b.chibi) { const r_ = ROSTER.find(x => x.id === id) || {}; b.persona = PERSONA[r_.persona] || PERSONA.laidback; chibiSetup(b); }
  D.rig = full ? 'w2s-1' : b.chibi ? 'w2s-chibi-1' : (b.mt.jaw.length ? 'generic with morph targets' : 'generic');
  return b;
}
const setM = (b, k, v) => { for (const [o, i] of b.mt[k]) o.morphTargetInfluences[i] = v; };


/* ---------- chibi Buddies (rig "w2s-chibi-1", made by buddy-gen/build_buddy.py) ----------
   One fused mesh with a painted face and a small skeleton: Hips, Spine, Head. The body breathes and shifts
   through Spine and Hips, the head turns, nods and tilts. The painted eyes cannot move, so gaze is carried by
   the head. Two kinds of face "cards" (small canvases fitted to the face, following the head):
   - eyelids: invisible while the eye is open, they close over the painted eye to blink;
   - mouth: invisible at rest (the painted mouth shows), it draws an animated mouth over it while the Buddy
     speaks or reacts, then fades back to the painted one.
   Lip shapes come from the letters of each word, timed by the voice's word events (exact where the browser
   reports word boundaries, estimated where it does not). There is no phoneme timing in browser speech. */
const PERSONA = {
  laidback: {breath: 4.6, breathAmt: 0.010, tilt: 0.035, look: [3.2, 6.5], lookAmt: 0.06, sway: [6, 11], swayAmt: 0.016, blink: [2.8, 6.5], dbl: 0.08, nod: 0.7, wing: false},
  playful: {breath: 3.8, breathAmt: 0.012, tilt: -0.03, look: [1.8, 4.2], lookAmt: 0.09, sway: [4, 8], swayAmt: 0.02, blink: [2.0, 5.0], dbl: 0.22, nod: 1.0, wing: true}
};
const _q = new THREE.Quaternion(), _e = new THREE.Euler();
function boneRot(b, k, x, y, z) { const n = b.bones[k]; if (!n) return; n.quaternion.copy(b.restQ[k]).multiply(_q.setFromEuler(_e.set(x, y, z))); }
function texSampler(map) {   // read colours from the model's own texture, to match skin and lip tones exactly
  const im = map && map.image; if (!im || !im.width) return null;
  const c = document.createElement('canvas'), W_ = c.width = Math.min(512, im.width), H_ = c.height = Math.min(512, im.height), g = c.getContext('2d', {willReadFrequently: true});
  g.drawImage(im, 0, 0, W_, H_); const data = g.getImageData(0, 0, W_, H_).data;
  return uv => { const x = clamp(Math.floor(uv.x * W_), 0, W_ - 1), y = clamp(Math.floor(uv.y * H_), 0, H_ - 1), i = (y * W_ + x) * 4; return [data[i], data[i + 1], data[i + 2]]; };
}
// Raycasts against a SkinnedMesh re-skin every triangle on every ray (~25 ms for these 70 k triangles).
// In the rest pose the skinned surface equals the plain geometry, so rays go to plain copies instead:
// a small face patch for fitting the face cards, and the whole body for taps.
function proxyMesh(skin, keep) {
  const g = skin.geometry, P = g.attributes.position, U = g.attributes.uv, I = g.index, M = skin.matrixWorld, n = I ? I.count : P.count;
  const pos = [], uv = [], v = [new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()];
  for (let t = 0; t < n; t += 3) { const ids = [0, 1, 2].map(k => I ? I.getX(t + k) : t + k); ids.forEach((id, k) => v[k].fromBufferAttribute(P, id).applyMatrix4(M));
    if (keep && !keep((v[0].x + v[1].x + v[2].x) / 3, (v[0].y + v[1].y + v[2].y) / 3, (v[0].z + v[1].z + v[2].z) / 3)) continue;
    ids.forEach((id, k) => { pos.push(v[k].x, v[k].y, v[k].z); if (U) uv.push(U.getX(id), U.getY(id)); }); }
  const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); if (U) pg.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); pg.computeBoundingSphere(); pg.computeBoundingBox();
  const m = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({side: THREE.DoubleSide})); m.updateMatrixWorld(true); return m;
}
const hitRay = new THREE.Raycaster(), DOWN_Z = new THREE.Vector3(0, 0, -1);
function hitAt(b, x, y, zf) { hitRay.set(new THREE.Vector3(x, y, zf + 0.6), DOWN_Z); return hitRay.intersectObject(b.faceHit || b.skin, false)[0] || null; }
function colourAt(b, pts) {
  const acc = [0, 0, 0]; let n = 0;
  for (const [x, y, zf] of pts) { const h = hitAt(b, x, y, zf); if (h && h.uv && b.sample) { const c = b.sample(h.uv); acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]; n++; } }
  return n ? `rgb(${Math.round(acc[0] / n)},${Math.round(acc[1] / n)},${Math.round(acc[2] / n)})` : 'rgb(240,200,170)';
}
function faceCard(b, c, w, h, cw, ch) {   // a small grid fitted to the face surface, in the Head bone's space
  const nx = 12, ny = 8, pos = [], uv = [], idx = [], head = b.bones.head;
  for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++) {
    const x = c[0] + (i / nx - 0.5) * w, y = c[1] + (j / ny - 0.5) * h, hit = hitAt(b, x, y, c[2]);
    const p = hit ? hit.point.clone() : new THREE.Vector3(x, y, c[2]); p.z += 0.004;
    head.worldToLocal(p); pos.push(p.x, p.y, p.z); uv.push(i / nx, j / ny);
  }
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const a = j * (nx + 1) + i; idx.push(a, a + 1, a + nx + 2, a, a + nx + 2, a + nx + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
  const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch; const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({map: tex, transparent: true, depthWrite: false, roughness: 0.75, metalness: 0, polygonOffset: true, polygonOffsetFactor: -4}));
  m.renderOrder = 2; m.visible = false; m.frustumCulled = false; m.castShadow = false; m.receiveShadow = false; m.name = 'FaceCard'; head.add(m);
  return {mesh: m, cv, g2: cv.getContext('2d'), tex, last: ''};
}

/* ---------- the integrated face (models built with face2 data, see buddy-gen/face_map.py) ----------
   No pieces are laid over the face. The body's own material does the work, before lighting, so the
   features keep the model's skin tone, texture, light and shading:
   - blink: the eye's own painted lash line (and any wings) slides down over the eye; the white, iris
     and pupil it passes give way to the skin painted out of a small front-view raster of the eye band;
   - mouth: the mesh deforms (lower lip and jaw down, upper lip up a little, corners in, out or up) along
     the line where the lips part, and only the gap that opens between them is shaded. */
const FACE_VS_HEAD = `
uniform mat4 uSkinToModel; uniform mat3 uModelToSkin; uniform vec4 uSeam; uniform vec4 uMouth; uniform vec4 uMouthA;
varying vec3 vFaceP; varying vec3 vFaceN; varying float vFaceDy;
vec3 w2sMouthDisp(vec3 p, vec3 n) {
  float hw = uMouth.x, ys = uSeam.x + uSeam.y * p.x + uSeam.z * p.x * p.x, dx = p.x - uSeam.w, u = dx / hw;
  float front = smoothstep(uMouth.w - 0.13, uMouth.w - 0.07, p.z) * step(-0.2, n.z);
  float lens = pow(clamp(1.0 - u * u, 0.0, 1.0), 0.6);
  float jaw = clamp(1.0 - (dx * dx) / (2.6 * hw * hw), 0.0, 1.0);
  float below = step(p.y, ys), dn = ys - p.y, upd = p.y - ys;
  float lower = mix(lens, jaw, smoothstep(0.0, 0.05, dn)) * (1.0 - smoothstep(0.09, 0.2, dn)) * below;
  float upper = lens * (1.0 - smoothstep(0.0, 0.035, upd)) * (1.0 - below);
  float lipR = clamp(1.0 - u * u / 1.7, 0.0, 1.0) * (1.0 - smoothstep(0.02, 0.07, abs(p.y - ys)));
  float J = uMouthA.x, P = uMouthA.y, W = uMouthA.z, S = uMouthA.w;
  vec3 d = vec3(0.0);
  d.y = -J * uMouth.y * lower + J * uMouth.z * upper + S * 0.009 * u * u * lipR;
  d.x = dx * (W * 0.2 - P * 0.3) * lipR;
  d.z = P * 0.012 * lipR - J * 0.006 * lower;
  return d * front;
}`;
const FACE_VS_BODY = `
  vFaceP = (uSkinToModel * vec4(position, 1.0)).xyz; vFaceN = normalize(mat3(uSkinToModel) * normal);
  { vec3 w2sD = w2sMouthDisp(vFaceP, vFaceN); vFaceDy = w2sD.y; transformed += uModelToSkin * w2sD; }`;
const FACE_FS_HEAD = `
uniform sampler2D uFaceAtlas; uniform sampler2D uFaceProf; uniform vec4 uFaceBox; uniform vec4 uFaceEye;
uniform vec4 uSeam; uniform vec4 uMouth; uniform vec4 uMouthA; uniform float uMouthKind; uniform float uFaceDbg;
varying vec3 vFaceP; varying vec3 vFaceN; varying float vFaceDy;
vec4 w2sAtlas(float col, float row) { float H2 = uFaceBox.w * 2.0; return texture2D(uFaceAtlas, vec2((col + 0.5) / uFaceBox.z, 1.0 - (row + 0.5) / H2)); }
vec4 w2sProf(float col) { float c0 = floor(col); vec4 a = texelFetch(uFaceProf, ivec2(int(c0), 0), 0), b = texelFetch(uFaceProf, ivec2(int(c0) + 1, 0), 0);
  if (a.b < 0.5) return b; if (b.b < 0.5) return a; return mix(a, b, col - c0); }`;
const FACE_FS_BODY = `
  if (uFaceEye.x > 0.002 && vFaceN.z > 0.25 && vFaceP.z > uFaceEye.y) {
    float col = (vFaceP.x - uFaceBox.x) / uFaceEye.z, row = (uFaceBox.y - vFaceP.y) / uFaceEye.z, H = uFaceBox.w;
    if (col >= 0.0 && col < uFaceBox.z - 1.0 && row >= 0.0 && row < H - 1.0) {
      vec4 pr = w2sProf(col);
      if (pr.b > 0.5) {
        float s = uFaceEye.x * pr.g, edge = pr.r + s, cover = 1.0 - smoothstep(edge - 0.6, edge + 0.6, row);
        if (cover > 0.0) {
          vec4 cl = w2sAtlas(col, clamp(row, 0.0, H - 1.0) + H);
          vec3 base = mix(diffuseColor.rgb, cl.rgb, cl.a);                 // the eye gives way to skin
          float src = row - s; vec4 ln = w2sAtlas(col, clamp(src, 0.0, H - 1.0));
          base = mix(base, ln.rgb, smoothstep(0.12, 0.55, ln.a) * step(0.0, src));   // its own lash line, moved down (crisp, as painted)
          base *= 1.0 - 0.07 * uFaceEye.x * (1.0 - smoothstep(0.0, 9.0, edge - row));   // the lid's soft shade
          diffuseColor.rgb = mix(diffuseColor.rgb, base, cover);
          if (uFaceDbg > 0.5) diffuseColor.rgb = uFaceDbg < 1.5 ? vec3(ln.a, cl.a, 0.0) : ln.rgb;
        }
      }
    }
  }
  float w2sGap = 0.0; vec3 w2sInside = vec3(0.0);
  if (uMouthA.x > 0.01) {
    float hw = uMouth.x, ys = uSeam.x + uSeam.y * vFaceP.x + uSeam.z * vFaceP.x * vFaceP.x, u = (vFaceP.x - uSeam.w) / hw;
    float lens = pow(clamp(1.0 - u * u, 0.0, 1.0), 0.6), J = uMouthA.x;
    float top = ys + J * uMouth.z * lens, bot = ys - J * uMouth.y * lens, y = vFaceP.y + vFaceDy;
    float g = smoothstep(bot - 0.0006, bot + 0.0012, y) * (1.0 - smoothstep(top - 0.0012, top + 0.0006, y)) * step(abs(u), 1.0)
            * smoothstep(uMouth.w - 0.13, uMouth.w - 0.07, vFaceP.z) * step(0.0, top - bot - 0.0004);
    if (g > 0.0) {
      w2sInside = vec3(0.020, 0.005, 0.005) * (0.5 + 0.5 * lens); w2sGap = g;   // the mouth's shadowed inside, applied after lighting (no facet shading)
      diffuseColor.rgb = mix(diffuseColor.rgb, w2sInside, g);
    }
  }`;
function faceSetup(b) {
  const f2 = b.ex.face2, skin = b.skin; if (!f2 || !skin || !skin.material) return false;
  const m = skin.material, Wc = f2.w, Hr = f2.h, mo = f2.mouth || {a: -99, b: 0, c: 0, cx: 0, hw: 0.01, kind: 'teeth', front: 0};
  const img = new Image(); const atlas = new THREE.Texture(img); img.onload = () => { atlas.needsUpdate = true; }; img.src = f2.atlas;
  atlas.colorSpace = THREE.SRGBColorSpace; atlas.generateMipmaps = false; atlas.minFilter = THREE.LinearFilter; atlas.magFilter = THREE.LinearFilter; atlas.flipY = true;
  const pd = new Float32Array(Wc * 4); for (let i = 0; i < Wc; i++) { const t = f2.T[i]; pd[i * 4] = t; pd[i * 4 + 1] = f2.S[i]; pd[i * 4 + 2] = t >= 0 ? 1 : 0; pd[i * 4 + 3] = 1; }
  const prof = new THREE.DataTexture(pd, Wc, 1, THREE.RGBAFormat, THREE.FloatType); prof.needsUpdate = true;
  b.model.updateMatrixWorld(true);
  const s2m = new THREE.Matrix4().copy(b.model.matrixWorld).invert().multiply(skin.matrixWorld), m2s = new THREE.Matrix3().setFromMatrix4(s2m).invert();
  const lips = mo.kind === 'lips';
  const U = b.faceU = {uSkinToModel: {value: s2m}, uModelToSkin: {value: m2s}, uFaceAtlas: {value: atlas}, uFaceProf: {value: prof},
    uFaceBox: {value: new THREE.Vector4(f2.x0, f2.top, Wc, Hr)}, uFaceEye: {value: new THREE.Vector4(0, f2.front - 0.15, f2.px, 0)},
    uSeam: {value: new THREE.Vector4(mo.a, mo.b, mo.c, mo.cx)}, uMouth: {value: new THREE.Vector4(mo.hw, lips ? 0.046 : 0.028, lips ? 0.007 : 0.0, mo.front)},
    uMouthA: {value: new THREE.Vector4(0, 0, 0, 0)}, uMouthKind: {value: lips ? 1 : 0}, uFaceDbg: {value: 0}};
  const prev = m.onBeforeCompile;
  m.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); Object.assign(sh.uniforms, U);
    sh.vertexShader = sh.vertexShader.replace('void main() {', FACE_VS_HEAD + '\nvoid main() {').replace('#include <begin_vertex>', '#include <begin_vertex>' + FACE_VS_BODY);
    sh.fragmentShader = sh.fragmentShader.replace('void main() {', FACE_FS_HEAD + '\nvoid main() {').replace('#include <map_fragment>', '#include <map_fragment>' + FACE_FS_BODY)
      .replace('#include <opaque_fragment>', 'outgoingLight = mix(outgoingLight, w2sInside, w2sGap);\n#include <opaque_fragment>'); };
  m.customProgramCacheKey = () => 'w2s-face2'; m.needsUpdate = true;
  b.face2 = true; b.lids = []; b.mouthCard = null;
  return true;
}
function faceUpdate(b, lid) {
  const U = b.faceU; if (!U) return; const M = b.M;
  U.uFaceEye.value.x = clamp(lid, 0, 1);
  U.uMouthA.value.set(clamp(M.jaw, 0, 1), clamp(M.pucker, 0, 1), clamp(M.wide, 0, 1), clamp(M.smile - 0.3, -0.4, 0.7) - clamp(M.frown, 0, 1) * 0.5);
}
function chibiSetup(b) {
  const f = b.ex.face || {}; b.model.updateMatrixWorld(true);
  b.skin = null; b.model.traverse(o => { if (o.isSkinnedMesh || (o.isMesh && !b.skin)) b.skin = o; });
  b.sample = texSampler(b.skin && b.skin.material && b.skin.material.map);
  if (b.skin) { const pts = [f.eye_l, f.eye_r, f.mouth].filter(Boolean); b.hitBody = proxyMesh(b.skin);   // taps: the whole body, unskinned (rest pose)
    if (pts.length) { const xs = pts.map(e => e.c[0]), ys = pts.map(e => e.c[1]), zs = pts.map(e => e.c[2]), x0 = Math.min(...xs) - 0.2, x1 = Math.max(...xs) + 0.2, y0 = Math.min(...ys) - 0.2, y1 = Math.max(...ys) + 0.2, z0 = Math.min(...zs) - 0.3;
      b.faceHit = proxyMesh(b.skin, (x, y, z) => x > x0 && x < x1 && y > y0 && y < y1 && z > z0); } }
  b.restQ = {}; for (const k of ['hips', 'spine', 'head']) if (b.bones[k]) b.restQ[k] = b.bones[k].quaternion.clone();
  b.idle = {lx: new Spring(0, 30, 9), ly: new Spring(0, 30, 9), lz: new Spring(0, 30, 9), sw: new Spring(0, 12, 6), lookT: 1, swayT: 2, nodT: 2};
  b.lids = []; b.mouthA = new Spring(0, 220, 26);
  if (faceSetup(b)) return;
  for (const k of ['eye_l', 'eye_r']) { const e = f[k]; if (!e) continue;
    const card = faceCard(b, e.c, e.w * 1.35, e.h * 1.8, 128, 96);
    card.outer = e.c[0] > 0 ? 1 : -1;     // which canvas side is the outer corner
    card.skin = colourAt(b, [[e.c[0], e.c[1] + e.h * 0.95, e.c[2]], [e.c[0] - e.w * 0.25, e.c[1] + e.h * 0.9, e.c[2]], [e.c[0] + e.w * 0.25, e.c[1] + e.h * 0.9, e.c[2]]]);
    b.lids.push(card); }
  const mo = f.mouth;
  if (mo) { const lips = mo.kind === 'lips', w = lips ? Math.max(mo.w * 1.9, 0.13) : mo.w * 1.5, h = lips ? 0.11 : Math.max(mo.h * 3, 0.1);
    b.mouthCard = faceCard(b, mo.c, w, h, 256, 128); b.mouthCard.lips = lips;
    b.mouthCard.skin = colourAt(b, [[mo.c[0] + w * 0.62, mo.c[1] + 0.012, mo.c[2]], [mo.c[0] - w * 0.62, mo.c[1] + 0.012, mo.c[2]]]);
    b.mouthCard.lip = lips ? colourAt(b, [[mo.c[0], mo.c[1] + 0.012, mo.c[2]], [mo.c[0], mo.c[1] - 0.015, mo.c[2]]]) : b.mouthCard.skin;
    b.mouthCard.cover = [w ? (mo.w / w) * 0.5 * (lips ? 1.25 : 1.3) : 0.45, lips ? 0.36 : Math.min(0.46, (mo.h / h) * 0.5 * 2.2)]; }
  b.mouthA = new Spring(0, 220, 26);
}
function drawLids(card, t, wing) {
  const key = (t * 40 | 0) + (wing ? 'w' : ''); if (key === card.last) return; card.last = key;
  const g = card.g2, Wc = card.cv.width, Hc = card.cv.height, cx = Wc / 2, cy = Hc / 2, rx = Wc / 2 / 1.35, ry = Hc / 2 / 1.8;
  g.clearRect(0, 0, Wc, Hc); card.mesh.visible = t > 0.03; if (!card.mesh.visible) { card.tex.needsUpdate = true; return; }
  const top = cy - ry * 1.15, closed = cy + ry * 0.7, edge = top + (closed - top) * Math.min(1, t), bow = ry * (0.15 + 0.35 * Math.min(1, t));
  // canvas y runs down; the card's v runs up, so the eye's top is at small canvas y after the texture flip
  g.save(); g.beginPath(); g.ellipse(cx, cy, rx * 1.1, ry * 1.25, 0, 0, Math.PI * 2); g.clip();
  g.beginPath(); g.moveTo(cx - rx * 1.2, 0); g.lineTo(cx + rx * 1.2, 0); g.lineTo(cx + rx * 1.2, edge); g.quadraticCurveTo(cx, edge + bow, cx - rx * 1.2, edge); g.closePath();
  g.fillStyle = card.skin; g.fill();
  g.beginPath(); g.moveTo(cx - rx * 1.05, edge + 1); g.quadraticCurveTo(cx, edge + bow, cx + rx * 1.05, edge + 1);
  g.lineWidth = 5; g.strokeStyle = '#1b1414'; g.lineCap = 'round'; g.stroke(); g.restore();
  if (wing && t > 0.5) { const ox = cx + card.outer * rx * 1.02; g.beginPath(); g.moveTo(ox, edge + 1); g.lineTo(ox + card.outer * 12, edge - 9); g.lineWidth = 4; g.strokeStyle = '#1b1414'; g.stroke(); }
  card.tex.needsUpdate = true;
}
function drawMouth(card, M, a) {
  const key = [a, M.jaw, M.pucker, M.wide, M.smile].map(v => (v * 24) | 0).join(); if (key === card.last) return; card.last = key;
  const g = card.g2, Wc = card.cv.width, Hc = card.cv.height, cx = Wc / 2, cy = Hc / 2;
  g.clearRect(0, 0, Wc, Hc); card.mesh.visible = a > 0.02; if (!card.mesh.visible) { card.tex.needsUpdate = true; return; }
  g.save(); g.globalAlpha = Math.min(1, a);
  // 1) cover the painted mouth (skin for a painted grin; lip colour over modelled lips)
  const prx = card.cover[0] * Wc, pry = card.cover[1] * Hc;
  const grd = g.createRadialGradient(cx, cy, Math.min(prx, pry) * 0.5, cx, cy, Math.max(prx, pry));
  grd.addColorStop(0, card.lips ? card.lip : card.skin); grd.addColorStop(0.82, card.lips ? card.lip : card.skin); grd.addColorStop(1, 'rgba(0,0,0,0)');
  g.save(); g.scale(1, pry / prx); g.beginPath(); g.arc(cx, cy * prx / pry, prx, 0, Math.PI * 2); g.restore(); g.fillStyle = grd; g.fill();
  // 2) the mouth shape: width from wide/pucker, height from the jaw, corners lifted by the smile
  const base = Wc * (card.lips ? 0.36 : 0.31), ow = base * (0.6 + 0.4 * M.wide - 0.35 * M.pucker + 0.15 * M.jaw), oh = 2 + M.jaw * Hc * (card.lips ? 0.42 : 0.38) * (1 + 0.3 * M.pucker), lift = M.smile * 7;
  if (oh < 4.5) {   // closed: a lip line, curving up a little with the smile
    g.beginPath(); g.moveTo(cx - ow, cy - lift); g.quadraticCurveTo(cx, cy + 3 + lift, cx + ow, cy - lift); g.lineWidth = 3.5; g.strokeStyle = card.lips ? 'rgba(120,45,55,0.9)' : 'rgba(80,35,30,0.9)'; g.lineCap = 'round'; g.stroke();
  } else {
    g.beginPath(); g.moveTo(cx - ow, cy - lift); g.bezierCurveTo(cx - ow * 0.6, cy - oh * 0.9, cx + ow * 0.6, cy - oh * 0.9, cx + ow, cy - lift); g.bezierCurveTo(cx + ow * 0.7, cy + oh * 1.25, cx - ow * 0.7, cy + oh * 1.25, cx - ow, cy - lift); g.closePath();
    g.fillStyle = '#3d1418'; g.fill(); g.save(); g.clip();
    if (M.jaw > 0.12) { g.fillStyle = '#fbf7f2'; g.fillRect(cx - ow, cy - oh, ow * 2, oh * 0.62); }
    if (M.jaw > 0.3) { g.fillStyle = '#c4545f'; g.beginPath(); g.ellipse(cx, cy + oh * 0.95, ow * 0.55, oh * 0.45, 0, 0, Math.PI * 2); g.fill(); }
    g.restore();
    g.lineWidth = card.lips ? 7 : 2.5; g.strokeStyle = card.lips ? card.lip : 'rgba(80,35,30,0.8)'; g.stroke();
  }
  g.restore(); card.tex.needsUpdate = true;
}
function chibiUpdate(b, dt, t, gx, gy, bl, idle) {
  const P = b.P, ps = b.persona, I = b.idle;
  // idle life: small look-arounds and posture shifts at varied intervals; calmer while listening
  I.lookT -= dt; if (I.lookT <= 0) { I.lookT = rnd(ps.look[0], ps.look[1]) * (listening ? 1.7 : 1); const a = ps.lookAmt * (listening ? 0.35 : thinking ? 0.5 : 1) * idle; I.ly.t = rnd(-a, a); I.lx.t = rnd(-a * 0.5, a * 0.4); I.lz.t = rnd(-a * 0.6, a * 0.6); }
  I.swayT -= dt; if (I.swayT <= 0) { I.swayT = rnd(ps.sway[0], ps.sway[1]); I.sw.t = rnd(-1, 1) * ps.swayAmt * idle * (listening ? 0.4 : 1); }
  if (listening && idle) { I.nodT -= dt; if (I.nodT <= 0) { I.nodT = rnd(2.4, 4.4); P.hx.v += 0.8 * ps.nod; } }   // an occasional small nod while you talk
  I.lx.step(dt); I.ly.step(dt); I.lz.step(dt); I.sw.step(dt);
  const br = Math.sin(t * Math.PI * 2 / ps.breath) * idle, th = thinking ? 1 : 0;
  boneRot(b, 'hips', 0, I.sw.x * 0.6, I.sw.x);
  boneRot(b, 'spine', P.sx.x + br * ps.breathAmt + P.lean.x * 0.6, P.sy.x, P.sz.x - I.sw.x * 0.5);
  if (b.bones.spine) b.bones.spine.scale.set(1 + br * ps.breathAmt * 0.4, 1 + br * ps.breathAmt * 0.7, 1 + br * ps.breathAmt * 0.4);
  boneRot(b, 'head', P.hx.x - gy * 0.1 + I.lx.x - th * 0.07, P.hy.x + gx * 0.2 + I.ly.x + th * 0.1, P.hz.x + ps.tilt * idle + I.lz.x - I.sw.x * 0.5 + th * 0.06);
  if (b.bones.head) b.bones.head.scale.setScalar(P.headS.x);
  const lid = Math.max(bl, th * 0.28, b.hold || 0);
  if (b.face2) faceUpdate(b, lid);
  for (const c of b.lids) drawLids(c, lid, ps.wing);
  if (b.mouthCard) { const want = (speaking && audioOn) || performance.now() < sayUntil ? 1 : 0; b.mouthA.t = want; b.mouthA.step(dt); drawMouth(b.mouthCard, b.M, clamp(b.mouthA.x, 0, 1)); }
}

/* ---------- mouth shapes and lip sync ---------- */
const SHAPE = {rest: [0, 0, 0], A: [0.8, 0, 0.2], E: [0.42, 0, 0.6], I: [0.26, 0, 0.85], O: [0.6, 0.75, 0], U: [0.3, 1, 0], closed: [0, 0.12, 0], F: [0.12, 0, 0.25], cons: [0.3, 0, 0.25], L: [0.4, 0, 0.1], laugh: [0.7, 0, 0.7], oh: [0.55, 0.6, 0], hmm: [0, 0.3, 0]};
const VIS = {a: 'A', e: 'E', i: 'I', y: 'I', o: 'O', u: 'U', w: 'U', m: 'closed', b: 'closed', p: 'closed', f: 'F', v: 'F', l: 'L', t: 'cons', d: 'cons', n: 'cons', s: 'cons', z: 'cons', r: 'cons', k: 'cons', g: 'cons', c: 'cons', j: 'cons', h: 'A', q: 'U', x: 'cons'};
let speaking = false, listening = false, thinking = false, audioOn = false, lastWord = 0, vq = [], vqT = 0, sayUntil = 0;
function mouth(shape) { if (!B) return; const s = SHAPE[shape] || SHAPE.rest; B.Mt.jaw = s[0]; B.Mt.pucker = s[1]; B.Mt.wide = s[2]; }
function say(shape, sec) { mouth(shape); sayUntil = performance.now() + sec * 1000; }
function sayWord(w) { const q = []; let prev = ''; for (const ch of String(w).toLowerCase()) { const v = VIS[ch]; if (v && v !== prev) { q.push(v); prev = v; } } if (!q.length) q.push('cons'); vq = q.slice(0, 5); vqT = 0; lastWord = performance.now(); }
function lipSync(dt, now) {
  if (now < sayUntil) { /* a reaction is holding the mouth */ }
  else if (speaking) { vqT -= dt; if (vqT <= 0) { if (vq.length) { mouth(vq.shift()); vqT = 0.075; } else if (now - lastWord > 420) { mouth(['A', 'E', 'O', 'cons', 'I', 'closed', 'A', 'U'][Math.floor(Math.random() * 8)]); vqT = rnd(0.09, 0.16); } else { mouth('cons'); B.Mt.jaw = 0.14; vqT = 0.06; } } }
  else if (sayUntil) { sayUntil = 0; mouth('rest'); }
  const k = 1 - Math.exp(-dt * 22); for (const key of ['jaw', 'pucker', 'wide', 'smile', 'frown']) { B.M[key] = lerp(B.M[key], B.Mt[key], k); setM(B, key, B.M[key]); }
  D.mouth = +B.M.jaw.toFixed(3);
}

/* ---------- timeline, poses, reactions ---------- */
let timers = [], lastR = '', pokes = [], busyUntil = 0, recent = [];
const at = (ms, fn) => { const t = setTimeout(() => { timers = timers.filter(x => x !== t); fn(); }, ms); timers.push(t); };
const cancel = () => { timers.forEach(clearTimeout); timers = []; if (B) { B.hold = null; B.gazeHold = null; } };
function pose(o) { if (!B) return; for (const k in o) { if (RM && !FACE_KEYS.includes(k)) continue; if (B.P[k]) B.P[k].t = o[k]; } }
const talkPose = () => pose({rfx: -1.05, rax: 0.12, raz: -0.1, hz: 0, brow: 0.25});
const listenPose = () => pose({hz: 0.15, hx: 0.05, brow: 0.6, lean: 0.07, rfx: -0.14, raz: 0});
function relax() { if (!B) return; for (const k in IDLE) B.P[k].t = IDLE[k]; B.Mt.smile = speaking ? 0.15 : 0.3; B.Mt.frown = 0; if (!speaking) mouth('rest'); if (listening) listenPose(); else if (speaking) talkPose(); }
const hop = v => { if (B && !RM && B.hop <= 0.001) B.hopV = v; };
const eyes = (amount, ms) => { if (!B) return; B.hold = amount; at(ms, () => { if (B) B.hold = null; }); };
function seq(name, steps, total, o = {}) { cancel(); D.log.push(name); lastR = name; busyUntil = performance.now() + total; steps.forEach(([ms, what]) => at(ms, () => typeof what === 'function' ? what() : pose(what))); at(total, relax); if (o.sfx) SFX[o.sfx](); if (o.buzz) buzz(o.buzz); }
const R = {
  giggle: () => seq('giggle', [[0, {hx: -0.14, hz: 0.1, squint: 1, sx: -0.04}], [0, () => { B.Mt.smile = 1; say('laugh', 0.75); eyes(0.85, 700); hop(1.6); }], [170, () => hop(1.4)], [340, () => hop(1.2)]], 800, {sfx: 'giggle', buzz: 12}),
  boop: () => seq('boop', [[0, {cross: 1, brow: 1, hx: 0.06}], [0, () => { B.sq.v = -3; say('oh', 0.3); }], [260, () => eyes(1, 140)]], 620, {sfx: 'boop', buzz: 10}),
  hairflick: () => { const p = !!B.ponyN; seq('hairflick', [[0, {hy: -0.55, hz: -0.14, raz: p ? 0 : -2.45, rfz: p ? 0 : -1.5, rfx: p ? -0.14 : -0.6}], [0, () => { B.pony.v = 9; B.pony2.v = -7; B.Mt.smile = 0.8; }], [190, {hy: 0.5, hz: 0.12}], [190, () => { B.pony2.v = 9; }], [430, {hy: 0, hz: 0}]], 760, {sfx: 'whoosh', buzz: 8}); },
  tickle: () => seq('tickle', [[0, {sz: 0.13, hz: -0.1, squint: 0.8}], [0, () => { B.Mt.smile = 1; say('laugh', 0.6); B.sq.v = 2.4; }], [130, {sz: -0.13, hz: 0.1}], [260, {sz: 0.1, hz: -0.08}], [390, {sz: -0.07, hz: 0.05}]], 640, {sfx: 'giggle', buzz: 14}),
  shrug: () => seq('shrug', [[0, {shrug: 1, hz: 0.17, rfx: -0.95, rfz: -0.4, raz: -0.28, brow: 1, lfz: 0.3}], [0, () => { B.Mt.smile = 0.7; say('hmm', 0.5); }]], 820, {sfx: 'pop'}),
  wave: () => seq('wave', [[0, {raz: -2.3, rfz: -0.55, hz: -0.08, brow: 0.5}], [0, () => { B.Mt.smile = 1; }], [190, {rfz: 0.3}], [350, {rfz: -0.6}], [510, {rfz: 0.3}], [670, {rfz: -0.5}]], 900, {sfx: 'pop', buzz: 8}),
  sip: () => seq('sip', [[0, {lfx: -2.3, lax: -0.42, lay: -0.8, hx: -0.14}], [250, () => { eyes(0.8, 420); mouth('U'); SFX.sip(); }], [720, {hx: 0, lfx: -1.6}], [760, () => { B.Mt.smile = 1; mouth('rest'); }]], 1050, {buzz: 8}),
  startled: () => seq('startled', [[0, {brow: 1, hx: -0.1, shrug: 0.8}], [0, () => { hop(2.6); say('oh', 0.4); }]], 620, {sfx: 'pop', buzz: 16}),
  tapdance: () => seq('tapdance', [[0, {legL: -0.55, sz: 0.06}], [0, () => hop(1.2)], [130, {legL: 0, legR: -0.55, sz: -0.06}], [130, () => hop(1.2)], [260, {legR: 0, legL: -0.55, sz: 0.06}], [260, () => hop(1.2)], [390, {legL: 0, legR: -0.55, sz: -0.06}], [390, () => hop(1.2)], [520, {legR: 0, sz: 0}]], 700, {sfx: 'pop', buzz: 10}),
  spinjump: () => seq('spinjump', [[0, () => { hop(3.2); if (!RM) B.rotV += 13; B.Mt.smile = 1; }], [0, {armsOut: 0.6}]], 800, {sfx: 'whoosh', buzz: 14}),
  sideeye: () => seq('sideeye', [[0, {hy: -0.14, browTilt: 1, hz: 0.06}], [0, () => { B.gazeHold = [0.95, 0.05]; B.Mt.smile = 0; B.Mt.frown = 0.25; say('hmm', 0.9); }], [1000, () => { B.gazeHold = null; }]], 1150, {sfx: 'hmm'})
};
const PARTS = {face: ['giggle', 'boop'], hair: ['hairflick', 'startled'], torso: ['tickle', 'shrug'], arm: ['wave', 'shrug'], prop: ['sip', 'wave'], legs: ['tapdance', 'spinjump']};
const ALL = ['giggle', 'hairflick', 'tickle', 'wave', 'sip', 'tapdance', 'boop', 'shrug', 'startled', 'spinjump'];
function poke(part) {
  if (!B) return; const now = performance.now(); pokes = pokes.filter(t => now - t < 1900); pokes.push(now); B.pop.v = 2.2;
  if (pokes.length >= 5) { pokes = []; R.sideeye(); return; }
  let opts = (PARTS[part] || ALL).filter(n => n !== lastR); if (!opts.length) opts = ALL.filter(n => n !== lastR);   // never the same reaction twice in a row
  const age = n => { const i = recent.lastIndexOf(n); return i < 0 ? 99 : recent.length - i; }; opts.sort((a, b) => age(b) - age(a) || Math.random() - 0.5);   // and the one seen longest ago comes first
  recent.push(opts[0]); if (recent.length > 8) recent.shift(); R[opts[0]]();
}

/* ---------- conversation reactions ---------- */
function onSpeak() { thinking = false; }   // the line was requested; the voice may take a moment to start
function onSpeakStart(e) { speaking = D.speaking = true; audioOn = true; D.audio = !!(e && e.detail && e.detail.audio); D.timing = 'estimated'; if (!B) return; B.Mt.smile = 0.15; if (performance.now() > busyUntil) talkPose(); }
function onWord(e) { if (!B) return; sayWord(e.detail && e.detail.word || ''); if (performance.now() > busyUntil && !RM) { B.P.rfx.v += rnd(-2.2, 2.2); B.P.rfz.v += rnd(-1.6, 1.6); B.P.rhz.v += rnd(-3, 3); B.P.hx.v += rnd(-0.5, 0.7); B.P.hz.v += rnd(-0.4, 0.4); } }
function onSpeakEnd() { speaking = D.speaking = false; audioOn = false; vq = []; if (!B) return; mouth('rest'); if (performance.now() > busyUntil) relax(); }
function onMic(e) { listening = D.listening = !!(e.detail && e.detail.on); if (B && performance.now() > busyUntil) relax(); }
function onGood() { if (!B) return; seq('good', [[0, {hx: 0.24, brow: 0.6}], [0, () => { B.Mt.smile = 1; hop(1.5); }], [170, {hx: -0.04}], [330, {hx: 0.2}], [480, {hx: 0}]], 760, {sfx: 'good'}); if (!RM) confetti(14); }
function onOops() { if (!B) return; seq('oops', [[0, {hx: 0.15, hz: -0.12, brow: 0.7, rfx: -0.8, rfz: 0.2}], [0, () => { B.gazeHold = [0, -0.55]; B.Mt.smile = 0.1; say('oh', 0.35); }], [900, {hx: 0.16, hz: 0}], [900, () => { B.gazeHold = null; B.Mt.smile = 0.8; }], [1060, {hx: 0}], [1220, {hx: 0.14}]], 1500, {sfx: 'hmm'}); }   // looks down at the correction card, then nods
function onHelp() { if (!B) return; seq('help', [[0, {raz: -0.55, rfx: -2.25, rfz: 0.5, hz: 0.13, brow: 0.9}], [0, () => { B.gazeHold = [-0.5, 0.6]; say('hmm', 0.9); }], [1100, () => { B.gazeHold = null; B.Mt.smile = 0.9; }]], 1400, {sfx: 'pop'}); }
function onDone() { if (!B) return; seq('done', [[0, {raz: -2.7, rfz: -0.2, lax: -1.2, lfx: -1.5, brow: 1, hx: -0.12}], [0, () => { B.Mt.smile = 1; say('laugh', 1.1); hop(3); }], [420, () => hop(2.6)], [840, () => hop(2)]], 1500, {sfx: 'win', buzz: 30}); if (!RM) confetti(70); }

/* ---------- three hidden extras: sunglasses (double tap the face), big head (long press), helicopter (three full turns) ---------- */
function shadesOn() { if (!B) return; D.delights.shades = true; D.log.push('shades');
  if (!B.shades && B.eye[0] && B.bones.head) { const g = new THREE.Group(), dark = new THREE.MeshStandardMaterial({color: 0x0b103a, roughness: 0.15, metalness: 0.3}), yel = new THREE.MeshStandardMaterial({color: 0xffd93b, roughness: 0.4});
    const ex = B.eye[0].position, ax = Math.abs(ex.x), r = ax * 0.92; for (const s of [1, -1]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 0.96, 0.03, 28), dark); l.rotation.x = Math.PI / 2; l.position.set(ax * s, 0, 0); g.add(l); const a = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.025, 0.32), yel); a.position.set((ax + r) * s, 0.01, -0.16); g.add(a); }
    const br = new THREE.Mesh(new THREE.BoxGeometry(ax * 0.5, 0.03, 0.03), yel); br.position.y = 0.02; g.add(br); g.position.set(0, ex.y + 0.005, ex.z + 0.115); B.shadesY = ex.y + 0.005; B.bones.head.add(g); B.shades = g; g.scale.setScalar(0.001); }
  B.shadesOn = !B.shadesOn; B.shadesS.t = B.shadesOn ? 1 : 0; B.Mt.smile = 1; SFX.good(); buzz(20); if (!RM) { B.P.hx.v -= 2.5; confetti(18); } }
let inflating = false, heliBlock = 0;
function inflateStart() { if (!B || inflating) return; inflating = true; cancel(); B.P.headS.t = RM ? 1.12 : 1.36; pose({brow: 1}); mouth('U'); sayUntil = performance.now() + 60000; SFX.whoosh(); }
function inflateEnd() { if (!B || !inflating) return; inflating = false; D.delights.inflate = true; D.log.push('inflate'); heliBlock = performance.now() + 3000; B.P.headS.t = 1; B.P.headS.v = -6; sayUntil = 0; say('oh', 0.3); relax(); SFX.pop(); buzz(25); if (!RM) confetti(24); }
function helicopter() { if (!B) return; D.delights.helicopter = true; seq('helicopter', [[0, {armsOut: 1, lfx: -0.3, brow: 1}], [0, () => { B.heli = RM ? 0 : 1.6; B.Mt.smile = 1; say('laugh', 1.4); }], [1500, {cross: 1}]], 2300, {sfx: 'win', buzz: 30}); if (!RM) confetti(40); }

/* ---------- confetti ---------- */
let conf = null; const CN = 90, cp = [], dummy = new THREE.Object3D();
function confetti(n) { if (!scene) return; if (!conf) { conf = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.05, 0.03), new THREE.MeshBasicMaterial({side: THREE.DoubleSide}), CN); conf.frustumCulled = false; const cols = [0x2d4bff, 0xffd93b, 0xffffff, 0x19c79c, 0xff8fb1]; for (let i = 0; i < CN; i++) { conf.setColorAt(i, new THREE.Color(cols[i % cols.length])); cp.push({life: 0}); } scene.add(conf); }
  let k = 0; for (const p of cp) { if (k >= n) break; if (p.life > 0) continue; k++; p.life = rnd(0.9, 1.6); p.x = rnd(-0.3, 0.3); p.y = (B ? B.H : 2) * rnd(0.55, 0.95); p.z = rnd(0.2, 0.5); p.vx = rnd(-1.6, 1.6); p.vy = rnd(1.5, 3.6); p.vz = rnd(-0.4, 1); p.r = rnd(0, 6); p.vr = rnd(-9, 9); } }
function confStep(dt) { if (!conf) return; let any = false; cp.forEach((p, i) => { if (p.life > 0) { any = true; p.life -= dt; p.vy -= 5.5 * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt; p.r += p.vr * dt; dummy.position.set(p.x, p.y, p.z); dummy.rotation.set(p.r, p.r * 0.7, p.r * 1.3); dummy.scale.setScalar(p.life > 0.25 ? 1 : Math.max(0.001, p.life * 4)); } else dummy.scale.setScalar(0.0001); dummy.updateMatrix(); conf.setMatrixAt(i, dummy.matrix); }); conf.instanceMatrix.needsUpdate = true; conf.visible = any; }

/* ---------- which Buddy is on stage ---------- */
let firstShow = true, firstLoad = true;
// once the first Buddy is on stage, the others load quietly in the background so Switch Buddy is instant
function preloadOthers(id) { const c = navigator.connection; if (c && (c.saveData || /2g/.test(c.effectiveType || ''))) return;
  const go = () => ROSTER.filter(r => r.id !== id && FILE[r.id]).forEach(r => load(r.id).then(b => { if (!LIGHT) b.model.traverse(o => { if (o.material && o.material.map) renderer.initTexture(o.material.map); }); }).catch(() => {}));
  setTimeout(go, 600); }   // not requestIdleCallback: the render loop keeps the page from ever being idle
function show(id, instant) {
  pending = id;
  if (B && !buddies[id]) wrap.classList.remove('is-3d');   // not loaded yet: the new Buddy's picture shows at once, the 3D follows
  return load(id).then(b => { if (pending !== id) return; const old = B;
    const swap = () => { if (old && old !== b) scene.remove(old.spin); B = b; D.id = id; scene.add(b.spin); b.rot = 0; b.rotV = 0; turnAcc = 0; frameCam(); relax();
      if (instant || RM) { b.pop.x = 1; b.pop.t = 1; b.pop.v = 0; } else { b.pop.x = 0.02; b.pop.t = 1; b.pop.v = 6; hop(2.4); confetti(26); SFX.pop(); }
      if (!RM && (firstShow || !instant)) at(firstShow ? 700 : 280, () => { if (performance.now() > busyUntil) R.wave(); }); firstShow = false;
      wrap.classList.add('is-3d'); D.ready = true; if (firstLoad) { firstLoad = false; preloadOthers(id); } };
    if (old && old !== b && !instant && !RM && wrap.classList.contains('is-3d')) { cancel(); D.ready = false; old.pop.t = 0.02; old.rotV = 18; SFX.whoosh(); setTimeout(swap, 170); } else swap(); })
    .catch(() => { if (!B) wrap.classList.add('no-3d'); });
}

/* ---------- camera: the face is large; on a phone the body runs on behind the subtitle ---------- */
let camForce = null;
function frameCam() {
  if (!B || !camera) return; const kb = sm && sm.classList.contains('kb'), phone = window.matchMedia('(max-width: 899px)').matches;
  const topPad = kb ? 10 : phone ? 62 : Math.max(64, H * 0.08), headH = B.fw * 1.14;
  // phones: head and upper body (the top ~65% of the Buddy) between the buttons and the conversation panel
  let ppu = phone ? Math.min(0.25 * W / B.fw, (H - topPad - 26) / (B.H * 0.65)) : Math.min(0.36 * W / B.fw, 0.6 * H / headH), cy;
  const fit = (H - topPad - 16) / (B.H * 1.04); if (ppu < fit) ppu = fit;          // never smaller than "the whole body fits"
  if (camForce === 'full') { ppu = (H - 40) / (B.H * 1.08); cy = B.H * 0.5; } else if (camForce === 'face') { ppu = 0.62 * H / headH; cy = B.H - headH * 0.5; }
  else cy = B.H + 0.035 - (H / 2 - topPad) / ppu;
  const d = H / (2 * ppu * Math.tan(camera.fov * Math.PI / 360)); camera.aspect = W / H; camera.position.set(0, cy, d); camera.lookAt(0, cy, 0); camera.updateProjectionMatrix(); if (sm && !camForce) sm.style.setProperty('--sm-chin', Math.round(topPad + headH * ppu * 0.93) + 'px');   // cards over the stage stop below the chin
  D.info.ppu = Math.round(ppu); D.info.faceShare = +(B.fw * ppu / W).toFixed(2);
}
function resize() { const r = stage.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return; const w = Math.round(r.width), h = Math.round(r.height); if (w === W && h === H) return; W = w; H = h; renderer.setSize(W, H, false); frameCam(); if (B && scene) renderer.render(scene, camera); }   // setSize clears the canvas: draw now, not next frame

/* ---------- per-frame update ---------- */
let ptr = {x: 0, y: 0, t: -1e9}, dragging = false, turnAcc = 0;
function update(dt, now) {
  const b = B; if (!b) return; const P = b.P, t = now / 1000, idle = RM ? 0 : 1;
  for (const k in P) P[k].step(dt);
  // spin with inertia, then settle facing the learner
  if (!dragging) { if (Math.abs(b.rotV) > 1.2 && !(b.heli > 0)) turnAcc += b.rotV * dt; b.rot += b.rotV * dt; b.rotV *= Math.exp(-dt * (b.heli > 0 ? 0.2 : 2.6));
    if (b.heli > 0) { b.heli -= dt; b.rotV = lerp(b.rotV, 15, dt * 4); } else if (Math.abs(b.rotV) < 1.2 && D.hold == null) { const home = Math.round(b.rot / (Math.PI * 2)) * Math.PI * 2; b.rot = lerp(b.rot, home, 1 - Math.exp(-dt * 5)); if (Math.abs(b.rot - home) < 0.02) turnAcc = 0; } }
  if (D.hold != null) { b.rot = D.hold; b.rotV = 0; }
  D.turns = +(Math.abs(turnAcc) / (Math.PI * 2)).toFixed(2); D.settled = !dragging && !(b.heli > 0) && Math.abs(b.rotV) < 0.3 && Math.abs(b.rot - Math.round(b.rot / (Math.PI * 2)) * Math.PI * 2) < 0.05 && now > busyUntil;
  if (!dragging && Math.abs(turnAcc) >= Math.PI * 6 && !b.heliDone && now > heliBlock) { b.heliDone = true; helicopter(); } if (Math.abs(turnAcc) < 0.5) b.heliDone = false;
  // hop with gravity and a landing squash
  if (b.hop > 0 || b.hopV > 0) { b.hopV -= 14 * dt; b.hop += b.hopV * dt; if (b.hop <= 0) { b.hop = 0; b.sq.v = -Math.min(4, Math.abs(b.hopV) * 1.1); b.hopV = 0; } } if (b.heli > 0) b.hop = lerp(b.hop, 0.35, dt * 3);
  b.sq.step(dt); b.pop.step(dt); b.shadesS.step(dt);
  const sq = clamp(b.sq.x, 0.8, 1.2), pop = Math.max(0.001, b.pop.x);
  D.hopY = +b.hop.toFixed(3); b.spin.rotation.y = b.rot; b.spin.position.y = b.hop; b.spin.scale.setScalar(pop);
  b.tilt.rotation.z = Math.sin(t * 0.9) * 0.012 * idle; b.tilt.rotation.x = P.lean.x;
  b.sqG.scale.set(1 + (1 - sq) * 0.6, sq, 1 + (1 - sq) * 0.6);
  blob.scale.setScalar(pop * (1 - Math.min(0.5, b.hop * 0.5))); blob.material.opacity = 1 - Math.min(0.6, b.hop * 0.7);
  // gaze follows the pointer or the last touch for a few seconds, then drifts
  const g = b.gazeHold || (now - ptr.t < 4000 ? [ptr.x, ptr.y] : [Math.sin(t * 0.31) * 0.12 * idle, Math.sin(t * 0.23) * 0.06 * idle]);
  const sgn = Math.cos(b.rot) >= 0 ? 1 : -1; b.gaze.x.t = clamp(g[0], -1, 1) * sgn; b.gaze.y.t = clamp(g[1], -1, 1); const gx = b.gaze.x.step(dt), gy = b.gaze.y.step(dt);
  // blinking with the eyelids
  b.nextBlink -= dt; if (b.nextBlink <= 0) { b.blinkT = 0.16; const pb = b.persona && b.persona.blink; b.nextBlink = pb ? (Math.random() < b.persona.dbl ? 0.28 : rnd(pb[0], pb[1])) : rnd(2.2, 5.5); } let bl = 0; if (b.blinkT > 0) { b.blinkT -= dt; bl = Math.sin(clamp(1 - b.blinkT / 0.16, 0, 1) * Math.PI); } if (b.hold != null) bl = Math.max(bl, b.hold); b.blink = bl; D.blink = +bl.toFixed(2);
  const K = b.bones, smile = b.M.smile;
  if (b.full) {
    const br = Math.sin(t * 1.7) * 0.009 * idle;   // breathing
    if (K.spine) { K.spine.rotation.set(P.sx.x + br * 0.6, P.sy.x, P.sz.x); K.spine.scale.set(1 + br * 0.5, 1 + br, 1 + br * 1.2); }
    if (K.head) { K.head.rotation.set(P.hx.x - gy * 0.16 + Math.sin(t * 0.7) * 0.012 * idle, P.hy.x + gx * 0.26, P.hz.x + Math.sin(t * 0.53) * 0.014 * idle); K.head.scale.setScalar(P.headS.x); }
    const ao = P.armsOut.x;
    if (K.la) { K.la.rotation.set(P.lax.x, P.lay.x * (1 - ao), P.laz.x + ao * 0.9); K.la.position.y = b.rest.la + P.shrug.x * 0.055; } if (K.lf) K.lf.rotation.set(P.lfx.x * (1 - ao * 0.7), 0, P.lfz.x);
    if (K.ra) { K.ra.rotation.set(P.rax.x, P.ray.x, P.raz.x - ao * 0.9 + Math.sin(t * 1.1) * 0.012 * idle); K.ra.position.y = b.rest.ra + P.shrug.x * 0.055; } if (K.rf) K.rf.rotation.set(P.rfx.x, 0, P.rfz.x); if (K.rh) K.rh.rotation.z = P.rhz.x;
    if (K.ll) K.ll.rotation.x = P.legL.x; if (K.rl) K.rl.rotation.x = P.legR.x; if (K.hips) K.hips.rotation.z = Math.sin(t * 0.6) * 0.008 * idle;
    const open = b.lidOpen + 0.3 * clamp(P.squint.x * 0.6 + smile * 0.12, 0, 1) - gy * 0.12 - P.brow.x * 0.08;
    b.lid.forEach(n => { if (n) n.rotation.x = lerp(open, b.lidClosed, bl); }); b.low.forEach(n => { if (n) n.rotation.x = b.lowLid - clamp(P.squint.x * 0.3 + smile * 0.14, 0, 0.45) - bl * 0.2; });
    b.eye.forEach((n, i) => { if (n) n.rotation.set(-gy * 0.3, gx * 0.42 + P.cross.x * (i ? 0.4 : -0.4), 0); });
    b.brow.forEach((n, i) => { if (n) { n.position.y = b.browY[i] + P.brow.x * 0.03 - P.squint.x * 0.008; n.rotation.z = (i ? 1 : -1) * P.brow.x * 0.06 + P.browTilt.x * 0.22; } });
    if (b.ponyN) { b.pony.t = clamp(-b.rotV * 0.02, -0.6, 0.6) + P.hx.x * 0.5; b.pony2.t = -P.hy.x * 0.5; b.ponyN.rotation.set(clamp(b.pony.step(dt), -0.9, 0.9) + Math.sin(t * 1.3) * 0.02 * idle, 0, clamp(b.pony2.step(dt), -0.9, 0.9)); }
  } else if (b.chibi) chibiUpdate(b, dt, t, gx, gy, bl, idle);
  else setM(b, 'blink', bl);
  if (b.shades) { const s = b.shadesS.x; b.shades.visible = s > 0.02; b.shades.scale.setScalar(Math.max(0.001, s)); b.shades.position.y = b.shadesY + (1 - s) * 0.5; }
  lipSync(dt, now); confStep(dt);
}

/* ---------- frame loop, pausing, automatic quality, optional readout ---------- */
let frames = 0, slowFor = 0, settle = 0, fpsT = 0; const FPS = /[?&]fps=1/.test(location.search), fpsEl = document.getElementById('smFps');
function frame(now) {
  raf = requestAnimationFrame(frame); const dt = Math.min(0.25, (now - last) / 1000 || 0.016), steps = Math.max(1, Math.ceil(dt / 0.034)); last = now;
  for (let i = 0; i < steps; i++) update(dt / steps, now);   // on a slow device the motion keeps real time (several small steps per drawn frame), so lip sync stays with the voice
  renderer.render(scene, camera);
  frames++; if (!fpsT) fpsT = now; const span = (now - fpsT) / 1000;          // measured on the real clock, not the clamped step
  if (span >= 0.5) { D.fps = Math.round(frames / span); D.info.calls = renderer.info.render.calls; D.info.tris = renderer.info.render.triangles; settle += span;
    if (settle > 2 && D.ready && !D.lockQuality) { slowFor = D.fps < 40 ? slowFor + span : 0; if (slowFor >= 2 && D.quality < QUAL.length - 1) { setQuality(D.quality + 1); slowFor = 0; settle = 0.5; } }   // under 40 fps for two seconds: step down
    D.info.slowFor = +slowFor.toFixed(1); frames = 0; fpsT = now;
    if (FPS && fpsEl) { fpsEl.hidden = false; fpsEl.textContent = D.fps + ' fps\n' + D.info.calls + ' draw calls, ' + Math.round(D.info.tris / 1000) + 'k triangles\nquality step ' + D.quality + ' of ' + (QUAL.length - 1) + ' (' + renderer.getPixelRatio().toFixed(2) + 'x, shadows ' + (QUAL[D.quality].sh ? 'on' : 'off') + ')\n' + D.renderer.slice(0, 46); } }
}
function run() { const want = visible && !document.hidden && !wrap.classList.contains('is-hidden'); if (want && !running) { running = true; last = performance.now(); settle = 0; slowFor = 0; fpsT = 0; frames = 0; raf = requestAnimationFrame(frame); } else if (!want && running) { running = false; cancelAnimationFrame(raf); } D.running = running; }

/* ---------- pointer: spin, poke, double tap, long press ---------- */
const ray = new THREE.Raycaster();
function partAt(cx, cy) {
  if (!B) return null; const r = canvas.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2((cx - r.left) / r.width * 2 - 1, -((cy - r.top) / r.height) * 2 + 1), camera);
  let hits; if (B.hitBody) { B.hitBody.matrixWorld.copy(B.spin.matrixWorld); hits = ray.intersectObject(B.hitBody, false); } else hits = ray.intersectObject(B.model, true);   // the unskinned proxy follows the spin and hop
  if (!hits.length) return null; const n = hits[0].object.name, p = B.model.worldToLocal(hits[0].point.clone());
  if (B.prop && hits[0].point.distanceTo(B.prop.getWorldPosition(new THREE.Vector3())) < 0.19) return 'prop';   // the cup or flask, and the hand round it
  if (/Hair|Pony/.test(n)) return 'hair'; if (/Head|Mouth|Eye|Lid|Lash|Brow|Shine|Freckle/.test(n)) return 'face'; if (/Prop|Headphones|Badge|HandL/.test(n)) return 'prop'; if (/Hand/.test(n)) return 'arm'; if (/Trousers|Shoe/.test(n)) return 'legs';
  if (/Jacket/.test(n)) return Math.abs(p.x) > 0.34 ? 'arm' : 'torso';
  if (!B.full) {   // one fused mesh (no part names): classify by where on the body the tap landed
    if (B.hw == null) { const bx = new THREE.Box3().setFromObject(B.model); B.hw = (bx.max.x - bx.min.x) / 2; }
    const ax = Math.abs(p.x) / B.hw, ty = p.y / B.H;
    if (ty > 0.86) return 'hair'; if (ty > 0.5) return ax > 0.6 ? 'hair' : 'face';
    if (ty > 0.2) return ax > 0.36 ? (ty < 0.33 ? 'prop' : 'arm') : 'torso'; return 'legs'; }
  return p.y > B.H * 0.63 ? 'face' : p.y > B.H * 0.28 ? 'torso' : 'legs';
}
function bindPointer() {
  let down = null, lastTap = 0, lastPart = '', press = 0, lx = 0, lt = 0, vel = 0;
  canvas.addEventListener('pointerdown', e => { touched = true; down = {x: e.clientX, y: e.clientY, part: partAt(e.clientX, e.clientY), moved: false}; lx = e.clientX; lt = e.timeStamp; vel = 0; try { canvas.setPointerCapture(e.pointerId); } catch (x) {}
    clearTimeout(press); if (down.part) press = setTimeout(() => { if (down && !down.moved) { down.long = true; inflateStart(); } }, 560); });
  canvas.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); ptr = {x: clamp(((e.clientX - r.left) / r.width - 0.5) * 2.4, -1, 1), y: clamp(-((e.clientY - r.top) / r.height - 0.3) * 2.2, -1, 1), t: performance.now()};
    if (!down || !B) return; const dx = e.clientX - down.x, dy = e.clientY - down.y; if (!down.moved && !down.long && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { down.moved = true; dragging = true; clearTimeout(press); canvas.classList.add('grabbing'); }
    if (down.moved) { const d = (e.clientX - lx) * Math.PI * 2.5 / Math.max(160, W); B.rot += d; turnAcc += d; D.spun = +(D.spun + Math.abs(d)).toFixed(3); vel = lerp(vel, d / (Math.max(1, e.timeStamp - lt) / 1000), 0.5); lx = e.clientX; lt = e.timeStamp; } });
  canvas.addEventListener('pointerup', e => { clearTimeout(press); if (!down) return; const d = down; down = null; canvas.classList.remove('grabbing'); ptr.t = performance.now();
    if (d.long) { inflateEnd(); dragging = false; return; }
    if (d.moved) { dragging = false; if (B) B.rotV = RM ? 0 : clamp(vel, -22, 22); return; }
    if (!d.part) return; if (d.part === 'face' && lastPart === 'face' && e.timeStamp - lastTap < 500) { lastTap = 0; cancel(); shadesOn(); return; } lastTap = e.timeStamp; lastPart = d.part; poke(d.part); });
  canvas.addEventListener('pointercancel', () => { clearTimeout(press); if (down && down.long) inflateEnd(); down = null; dragging = false; canvas.classList.remove('grabbing'); });
  canvas.addEventListener('keydown', e => { touched = true; if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); poke(['face', 'hair', 'torso', 'arm', 'prop', 'legs'][Math.floor(Math.random() * 6)]); } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); if (B) { const d = (e.key === 'ArrowLeft' ? -1 : 1) * 0.5; B.rot += d; turnAcc += d; D.spun = +(D.spun + 0.5).toFixed(3); } } });
  window.addEventListener('pointerdown', () => { touched = true; }, {passive: true});
}

/* ---------- start ---------- */
function start() {
  if (!wrap || !stage || !boot()) return;
  resize(); setQuality(LIGHT ? 2 : 0); bindPointer();
  new ResizeObserver(resize).observe(stage);
  new IntersectionObserver(es => { visible = es[0].isIntersecting; run(); }, {threshold: 0.02}).observe(stage);
  document.addEventListener('visibilitychange', run);
  const on = (n, f) => window.addEventListener('w2s:' + n, f);
  on('speak', onSpeak); on('speakstart', onSpeakStart); on('timing', e => { D.timing = e.detail && e.detail.exact ? 'word boundaries' : 'estimated'; }); on('think', e => { thinking = !!(e.detail && e.detail.on); D.thinking = thinking; }); on('word', onWord); on('speakend', onSpeakEnd); on('mic', onMic); on('good', onGood); on('oops', onOops); on('help', onHelp); on('done', onDone);
  on('buddy', e => { touched = true; show(pick(e.detail && e.detail.id), false); });
  on('mute', e => { muted = !!(e.detail && e.detail.on); if (!muted) { touched = true; SFX.pop(); } });
  on('shown', run); on('layout', () => setTimeout(resize, 30)); on('start', () => { touched = true; });
  // hooks for the tests, the turnaround renders and the static pictures
  D.anchor = part => { if (!B) return null; const v = new THREE.Vector3(), n = B.chibi ? null : {face: B.bones.head, hair: B.bones.head, torso: B.bones.spine, arm: B.bones.rf || B.bones.ra, prop: B.prop || B.bones.lh, legs: B.bones.ll}[part];
    if (n) { n.getWorldPosition(v);
      if (part === 'face') { v.y += B.fw * 0.36; v.z += 0.1; } if (part === 'hair') v.y += B.fw * 0.93; if (part === 'torso') v.y += 0.22; if (part === 'legs') v.y -= 0.25; if (part === 'arm') v.y -= 0.1; }
    else {   // no skeleton (a generic model): aim at the body by height, on the front of the model
      const f = {face: [0, 0.66], hair: [0.78, 0.62], torso: [0, 0.4], arm: [0.44, 0.4], prop: [0.44, 0.27], legs: [0.12, 0.12]}[part]; if (!f) return null;
      const bx = new THREE.Box3().setFromObject(B.model), r = (bx.max.x - bx.min.x) / 2; v.set(f[0] * r, f[1] * B.H, 0);
      const rc = new THREE.Raycaster(new THREE.Vector3(v.x, v.y, 10), new THREE.Vector3(0, 0, -1)); if (B.hitBody) B.hitBody.matrixWorld.copy(B.spin.matrixWorld); const hit = rc.intersectObject(B.hitBody || B.model, !B.hitBody)[0]; if (hit) v.copy(hit.point); }
    v.project(camera); const r = canvas.getBoundingClientRect(), x = r.left + (v.x + 1) / 2 * r.width, y = r.top + (1 - v.y) / 2 * r.height; return {x, y, part: partAt(x, y)}; };
  D.face = () => (B && B.chibi) ? {integrated: !!B.face2, mouth: B.face2 ? B.faceU.uMouthA.value.x > 0.02 : !!(B.mouthCard && B.mouthCard.mesh.visible), lids: B.face2 ? [0, 1].map(() => B.faceU.uFaceEye.value.x > 0.5) : B.lids.map(c => c.mesh.visible), jaw: B.face2 ? +B.faceU.uMouthA.value.x.toFixed(3) : null, persona: B.persona === PERSONA.playful ? 'playful' : 'laidback', head: B.bones.head ? B.bones.head.rotation.toArray().slice(0, 3).map(v => +v.toFixed(4)) : null} : null;
  D.featurePts = () => { if (!B || !B.ex.face) return null; const r = canvas.getBoundingClientRect(), o = {}; B.model.updateMatrixWorld(true);
    for (const [k, e] of Object.entries(B.ex.face)) { const v = new THREE.Vector3(...e.c); (B.bones.head || B.model).updateWorldMatrix(true, false); v.applyMatrix4(B.model.matrixWorld); v.project(camera); o[k] = {x: r.left + (v.x + 1) / 2 * r.width, y: r.top + (1 - v.y) / 2 * r.height}; } return o; };
  D.faceDbg = v => { if (B && B.faceU) B.faceU.uFaceDbg.value = v; };
  D.cached = () => Object.keys(buddies); D.hitInfo = () => B ? {body: B.hitBody ? B.hitBody.geometry.attributes.position.count / 3 : 0, face: B.faceHit ? B.faceHit.geometry.attributes.position.count / 3 : 0, sphere: B.hitBody ? B.hitBody.geometry.boundingSphere.radius : 0} : null;
  D.say = (s, sec) => say(s, sec || 0.5); D.poke = p => poke(p); D.react = n => R[n] && R[n](); D.setQuality = setQuality;
  D.view = o => { o = o || {}; camForce = o.frame || null; D.hold = o.rot != null ? o.rot : null; if (o.pose) pose(o.pose); if (o.blink != null && B) B.hold = o.blink; frameCam(); };
  D.snap = () => { update(0.016, performance.now()); renderer.render(scene, camera); return canvas.toDataURL('image/png'); };
  show(pick(window.W2S_BUDDY), true);   // the other Buddies are only downloaded when the learner switches
  run();
}
start();
