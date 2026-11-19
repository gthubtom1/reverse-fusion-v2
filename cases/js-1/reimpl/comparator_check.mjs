// Comparator self-check for js-1 (模式 3 算法抽取 TC5 防背答案).
// 1) Tamper a constant (sig1 key K[0]=0, sig2 LUT seed) -> output MUST change.
// 2) Regression: tampered variant rerun on TC1-TC4 inputs, all must differ from
//    their original baseline (= if we merely memorized answers, tampered==normal).
"use strict";
import { sig1 } from "./sig1repro.mjs";
import { sig2 } from "./sig2repro.mjs";

function sig1T(s) {
  const K = [0x00, 0x33, 0x79, 0x21]; // K[0] 0x6b -> 0x00
  const bytes = [];
  for (let i = 0; i < s.length; i++) bytes.push(s.charCodeAt(i) & 0xff);
  let out = "";
  const n = Math.max(bytes.length, 4);
  for (let i = 0; i < n; i++) {
    let b;
    if (i < bytes.length) b = ((bytes[i] + i * 7) ^ K[i % K.length]) & 0xff;
    else b = (K[i % K.length] + 0x11) & 0xff;
    b = ((b << 1) | (b >> 7)) & 0xff;
    out += b.toString(16).padStart(2, "0");
  }
  return out;
}

function sig2T(msg, nonce) {
  const n = (Number(nonce) >>> 0) & 0xffff;
  const lut = [];
  for (let i = 0; i < 256; i++) lut.push(i);
  let j = 0;
  for (let i = 0; i < 256; i++) {
    j = (j + lut[i] + ((n * 31 + 1 + i * 17) & 0xff)) & 0xff; // +1 tamper
    const t = lut[i]; lut[i] = lut[j]; lut[j] = t;
  }
  const bytes = [];
  for (let i = 0; i < msg.length; i++) bytes.push(msg.charCodeAt(i) & 0xff);
  const sc = bytes.map((b, i) => lut[(b + i) & 0xff]);
  let h = 0x811c9dc5;
  for (let i = 0; i < sc.length; i++) {
    h ^= sc[i];
    h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
  }
  return ((h ^ (bytes.length * 2654435761) ^ (n * 40503)) >>> 0).toString(16).padStart(8, "0");
}

// original baselines: input -> output
const B1 = { alice: "14801cb2d5", "": "f8881564", abc: "14b41064", "hello world": "06be0641c1e0b1038331a7", "k3y!_x": "0012fd2e2051" };
const B2 = [["hello", 42, "8698c417"], ["", 0, "811c9dc5"], ["x", 7, "783f0662"], ["hello", 43, "55fdcd57"], ["hello world", 0, "ac6e90b2"]];

const rows = [];
let ok = true;
// sig1 tamper vs normal
for (const k of Object.keys(B1)) {
  const normal = sig1(k);
  const tampered = sig1T(k);
  const changed = normal !== tampered && tampered !== B1[k];
  if (!changed) ok = false;
  rows.push({ fam: "sig1", input: k, normal, tampered, baseline: B1[k], changed });
}
// sig2 tamper vs normal
for (const [m, n, b] of B2) {
  const normal = sig2(m, n);
  const tampered = sig2T(m, n);
  const changed = normal !== tampered && tampered !== b;
  if (!changed) ok = false;
  rows.push({ fam: "sig2", input: `${m}/${n}`, normal, tampered, baseline: b, changed });
}
console.log(JSON.stringify({ ok, rows }, null, 2));