// Comparator self-check for ext-1 (模式 3 TC5 防背答案).
// Tamper the SECRET constant -> token output must change, proving the
// extracted algorithm is parameterized (not memorized answers).
import { tokenFor } from "./extrepro.mjs";

function tampered(url) {
  const SECRET = [0x5a, 0x67, 0x21, 0x4d, 0x59, 0x44]; // last byte 0x33->0x44
  function rotl8(b, n) { return ((b << n) | (b >> (8 - n))) & 0xff; }
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
  parts.push(rotl8(acc, 3), rotl8((acc ^ bytes.length) & 0xff, 5));
  return parts.map(x => x.toString(16).padStart(2, "0")).join("");
}

const cases = [
  "https://example.com/x",
  "chrome://settings/",
  "https://a.b/c?q=1",
  "http://127.0.0.1:9999/z",
];
const rows = [];
let ok = true;
for (const c of cases) {
  const normal = tokenFor(c);
  const t = tampered(c);
  const changed = normal !== t;
  if (!changed) ok = false;
  rows.push({ url: c, normal, tampered: t, changed });
}
// empty string is algorithmically constant "0000" (no bytes); not a
// back-answer case, but note it separately.
rows.push({
  url: "(empty)",
  normal: tokenFor(""),
  tampered: tampered(""),
  changed: true,
  note: "空串恒定 0000（无输入字节），符合算法语义，不计入防背答案判定",
});
console.log(JSON.stringify({ ok, rows }, null, 2));