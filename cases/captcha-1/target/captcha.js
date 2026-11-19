// captcha.js — self-hosted learning captcha.
// Draws an arithmetic captcha and exposes a deterministic answer token
// generator. Exercise: locate the answer derivation (signature-like) and
// reproduce it, mirroring the DSL-VM captcha-reverse method (case->constant
// table->function tracing) but on our own target.
"use strict";

// constant table (obfuscated array)
const T = [
  7, 3, 5, 4, 2, 9, 1, 6, 8, 0,
  0x61, 0x62, 0x63, 0x64, 0x65,  // 'a'..'e'
];

function pick(a, b) {
  return T[(a * 7 + b * 3) % 10];
}

function draw(a, op, b) {
  const c = document.getElementById("c");
  const ctx = c.getContext("2d");
  ctx.clearRect(0, 0, 180, 60);
  ctx.font = "bold 28px monospace";
  ctx.fillText(`${a} ${op} ${b} = ?`, 10, 38);
  // noise dots (constant seed 0)
  for (let i = 0; i < 8; i++) {
    ctx.fillRect(T[i] * 4, (T[i + 1] % 6) * 8, 2, 2);
  }
}

// answer derivation: compute(a, op, b) -> int, and token(a,op,b) -> hex
function compute(a, op, b) {
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "%": return a % b;
    default: return -1;
  }
}

function token(a, op, b) {
  const ans = compute(a, op, b);
  const h = ((ans * 2654435761) ^ (a * 40503) ^ (b * 73)) >>> 0;
  return h.toString(16).padStart(8, "0");
}

// initial draw
draw(8, "+", 5);

// check handler
document.getElementById("go").addEventListener("click", () => {
  const inp = document.getElementById("a");
  const ok = token(8, "+", 5) === inp.value.trim();
  document.getElementById("out").textContent = ok ? "PASS" : "FAIL";
});