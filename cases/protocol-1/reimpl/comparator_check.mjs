// Comparator self-check for protocol-1 (TC5 防背答案).
// 1) Correct frame decodes OK with valid checksum.
// 2) Flip a payload byte (corrupt) -> checksum now invalid, reply changes.
// 3) Flip the checksum byte -> invalid.
// This proves decode depends on actual bytes, not memorized output.
import { decodeFrame, serverReplyFor } from "./decode.mjs";

const good = "c0d00105050068656c6c6f62"; // T1 hello, checksum 0x62
const results = [];
let ok = true;

const cases = [
  ["good", good],
  ["corrupt_payload", "c0d00105050068656e6c6f62"], // 'h'->'n'
  ["corrupt_checksum", "c0d00105050068656c6c6f00"],
  ["corrupt_type", "c0d00107050068656c6c6f62"],
];
for (const [name, hex] of cases) {
  const d = decodeFrame(hex);
  const reply = serverReplyFor(d);
  results.push({ name, valid_checksum: d.ok ? d.valid_checksum : false,
                 decode_ok: d.ok, reply });
}
// good must be valid + OK; others must not be OK:1:5
const goodReply = results.find(r => r.name === "good").reply;
if (goodReply !== "OK:1:5") ok = false;
for (const r of results) {
  if (r.name !== "good" && r.reply === "OK:1:5") ok = false;
}
console.log(JSON.stringify({ ok, goodReply, results }, null, 2));