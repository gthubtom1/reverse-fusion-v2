// Repro for js-1 easy target: sig1.
// Independent Node reimplementation written from static reading of the
// page analysis (we do NOT eval or require the page script). Deterministic.
//
// Original page: cases/js-1/target/sig1.js  (SHA-256 in E-000)
// Original browser baseline: E-001 (5 cases)
"use strict";

const K = [0x6b, 0x33, 0x79, 0x21];

export function sig1(s) {
  const bytes = [];
  for (let i = 0; i < s.length; i++) bytes.push(s.charCodeAt(i) & 0xff);
  let out = "";
  const n = Math.max(bytes.length, 4);
  for (let i = 0; i < n; i++) {
    let b;
    if (i < bytes.length) {
      b = ((bytes[i] + i * 7) ^ K[i % K.length]) & 0xff;
    } else {
      b = (K[i % K.length] + 0x11) & 0xff;
    }
    b = ((b << 1) | (b >> 7)) & 0xff;
    out += b.toString(16).padStart(2, "0");
  }
  return out;
}