// sig1.js — easy web signature algorithm (self-hosted learning target)
// Algorithm: sign(input) = hex( (rot8(input bytes) + key byte) mod 256 ... )
// key constant K = "k3y!" (4 bytes). Deterministic, no randomness.
// Purpose: exercise locating a signature chain in page JS and reproducing it in Node.
"use strict";
const K = [0x6b, 0x33, 0x79, 0x21]; // "k3y!"

function sig1(s) {
  const bytes = [];
  for (let i = 0; i < s.length; i++) {
    bytes.push(s.charCodeAt(i) & 0xff);
  }
  let out = "";
  for (let i = 0; i < Math.max(bytes.length, 4); i++) {
    let b;
    if (i < bytes.length) {
      b = ((bytes[i] + i * 7) ^ K[i % K.length]) & 0xff;
    } else {
      b = (K[i % K.length] + 0x11) & 0xff;
    }
    // rotate left 1
    b = ((b << 1) | (b >> 7)) & 0xff;
    out += b.toString(16).padStart(2, "0");
  }
  return out;
}

window.sig1 = sig1;
document.getElementById("go").addEventListener("click", () => {
  const v = document.getElementById("inp").value;
  document.getElementById("out").textContent = sig1(v);
});