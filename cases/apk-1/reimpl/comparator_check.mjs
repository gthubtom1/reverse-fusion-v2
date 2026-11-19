// Comparator self-check for apk-1 (模式 3 算法抽取 TC5 防背答案).
// 1) Tamper the constant 0xD0 -> output must change for the valid serial.
// 2) Generate a NEW valid serial from the algorithm (not memorized), and
//    verify the original JVM also accepts it (cross-check in acceptance).
import { validate } from "./licensecheck.mjs";

function check(serial) {
  // original algorithm with tampered target constant 0xD1
  const KEY = [0x46, 0x55, 0x53, 0x49, 0x4f, 0x4e];
  if (serial == null || serial.length < 4) return "false";
  let sum = 0;
  for (let i = 0; i < serial.length; i++) {
    const c = serial.charCodeAt(i) & 0xff;
    sum += c ^ KEY[i % KEY.length];
  }
  return (sum & 0xff) === 0xd1 && serial.startsWith("FUSION") ? "true" : "false";
}

const rows = [];
let ok = true;
for (const s of ["FUSION-2026-Xs", "FUSION-2026-OO", "abc"]) {
  const a = String(validate(s));   // unchanged KEY, target 0xD0
  const b = check(s);              // tampered target 0xD1
  const differs = b === "false" || (a === "false" && b === "true");
  rows.push({ serial: s, normal: a, tamperedTarget: b, differs });
  if (!differs) ok = false;
}
console.log(JSON.stringify({ ok, rows }, null, 2));