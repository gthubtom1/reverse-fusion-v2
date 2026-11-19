// background.js — MV3 service worker for the extension learning target.
// getToken(pageUrl): deterministic token signed with an embedded secret.
// Exercise: locate the token/signature chain in the extension, reproduce in Node.
"use strict";

const SECRET = [0x5a, 0x67, 0x21, 0x4d, 0x59, 0x33]; // "Zg!MY3"

function rotl8(b, n) {
  return ((b << n) | (b >> (8 - n))) & 0xff;
}

function tokenFor(url) {
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
  // trailer: fold accumulator and length into 2 bytes
  const lo = acc;
  const hi = (acc ^ bytes.length) & 0xff;
  parts.push(rotl8(lo, 3), rotl8(hi, 5));
  return parts.map(x => x.toString(16).padStart(2, "0")).join("");
}

// chrome event listener (only for local test)
chrome.action.onClicked.addListener((tab) => {
  if (tab && tab.url) {
    console.log("token", tokenFor(tab.url));
  }
});