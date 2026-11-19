// Repro for captcha-1 answer token (mode 3 algorithm extraction).
// Independent Node reimplementation of compute()+token() from the captcha
// page analysis (does NOT eval/require captcha.js).
"use strict";

export function compute(a, op, b) {
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "%": return a % b;
    default: return -1;
  }
}

export function token(a, op, b) {
  const ans = compute(a, op, b);
  const h = ((ans * 2654435761) ^ (a * 40503) ^ (b * 73)) >>> 0;
  return h.toString(16).padStart(8, "0");
}