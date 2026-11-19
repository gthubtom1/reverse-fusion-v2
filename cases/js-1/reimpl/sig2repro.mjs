// Repro for js-1 medium target: sig2.
// Independent Node reimplementation, written from static reading only;
// does NOT eval or require the page script.
"use strict";

function fnv1a(bytes) {
  let h = 0x811c9dc5;
  for (let i = 0; i < bytes.length; i++) {
    h ^= bytes[i];
    h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
  }
  return h >>> 0;
}

function makeLut(nonce) {
  const lut = [];
  for (let i = 0; i < 256; i++) lut.push(i);
  let j = 0;
  for (let i = 0; i < 256; i++) {
    j = (j + lut[i] + ((nonce * 31 + i * 17) & 0xff)) & 0xff;
    const t = lut[i]; lut[i] = lut[j]; lut[j] = t;
  }
  return lut;
}

export function sig2(msg, nonce) {
  const n = (Number(nonce) >>> 0) & 0xffff;
  const lut = makeLut(n);
  const bytes = [];
  for (let i = 0; i < msg.length; i++) bytes.push(msg.charCodeAt(i) & 0xff);
  const sc = bytes.map((b, i) => lut[(b + i) & 0xff]);
  const h = fnv1a(sc);
  const h2 = (h ^ (bytes.length * 2654435761) ^ (n * 40503)) >>> 0;
  return h2.toString(16).padStart(8, "0");
}