// Comparator self-check for captcha-1 (TC5 防背答案).
// Tamper the token mixing constant (40503 -> 40504) or the op handling;
// output must change, proving the extracted algorithm is parameterized.
import { token } from "./captcharepro.mjs";

function tampered(a, op, b) {
  const ans = (
    op === "+" ? a + b :
    op === "-" ? a - b :
    op === "*" ? a * b :
    op === "%" ? a % b : -1);
  const h = ((ans * 2654435761) ^ (a * 40504) ^ (b * 73)) >>> 0; // 40503->40504
  return h.toString(16).padStart(8, "0");
}

const cases = [[8, "+", 5], [3, "*", 7], [10, "-", 4], [7, "%", 3], [0, "+", 0]];
const rows = [];
let ok = true;
for (const [a, op, b] of cases) {
  const n = token(a, op, b);
  const t = tampered(a, op, b);
  // 全零输入 (a=0,b=0,ans=0) 时 a*40504 与 b*73 均为 0，token 恒为 00000000，属算法语义
  const zeroCase = a === 0 && op === "+" && b === 0 && n === "00000000";
  const changed = n !== t || zeroCase;
  if (!changed) ok = false;
  rows.push({ expr: `${a}${op}${b}`, normal: n, tampered: t, changed,
              note: zeroCase ? "全零输入恒 00000000（语义）" : "" });
}
console.log(JSON.stringify({ ok, rows }, null, 2));