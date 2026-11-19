// Repro for ext-1 extension token algorithm (mode 3 algorithm extraction).
// Independent Node reimplementation written from static reading of the ext
// (manifest.json + background.js). Does NOT eval/require the extension files.
"use strict";

const SECRET = [0x5a, 0x67, 0x21, 0x4d, 0x59, 0x33];

function rotl8(b, n) {
  return ((b << n) | (b >> (8 - n))) & 0xff;
}

export function tokenFor(url) {
  const bytes = [];
  for (let i = 0; i < url.length; i++) bytes.push(url.charCodeAt(i) & 0xff);
  let acc = 0;
  const parts = [];
  for (let i = 0; i < bytes.length; i++) {
    const k = SECRET[i % SECRET.length];
    let b = rotl8((bytes[i] ^ k), (i % 7) + 1);
    acc = (acc + b) & 0xff;
    parts.push(b);
  }
  const lo = acc;
  const hi = (acc ^ bytes.length) & 0xff;
  parts.push(rotl8(lo, 3), rotl8(hi, 5));
  return parts.map(x => x.toString(16).padStart(2, "0")).join("");
}