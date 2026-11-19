// Differential test: Node repro vs original browser baseline.
// 5 cases per family (TC1-TC5), plus a "new unseen input" anti-memorization probe.
"use strict";
import { sig1 } from "./sig1repro.mjs";
import { sig2 } from "./sig2repro.mjs";

// original baselines collected in browser (E-001)
const CASES = [
  // sig1: input -> baseline
  { fam: "sig1", input: "alice", expect: "14801cb2d5" },
  { fam: "sig1", input: "", expect: "f8881564" },
  { fam: "sig1", input: "abc", expect: "14b41064" },
  { fam: "sig1", input: "hello world", expect: "06be0641c1e0b1038331a7" },
  { fam: "sig1", input: "k3y!_x", expect: "0012fd2e2051" },
  // sig2: (msg, nonce) -> baseline
  { fam: "sig2", msg: "hello", nonce: 42, expect: "8698c417" },
  { fam: "sig2", msg: "", nonce: 0, expect: "811c9dc5" },
  { fam: "sig2", msg: "x", nonce: 7, expect: "783f0662" },
  { fam: "sig2", msg: "hello", nonce: 43, expect: "55fdcd57" },
  { fam: "sig2", msg: "hello world", nonce: 0, expect: "ac6e90b2" },
];

// anti-memorization: inputs never used to build the repro
const NEW = [
  { fam: "sig1", input: "fresh value 9!" },
  { fam: "sig2", msg: "fresh", nonce: 1234 },
];

const results = [];
let ok = true;
for (const c of CASES) {
  const got = c.fam === "sig1" ? sig1(c.input) : sig2(c.msg, c.nonce);
  const pass = got === c.expect;
  if (!pass) ok = false;
  results.push({ ...c, got, pass });
}
// new-input probes: we don't have browser baseline for these, so we verify
// determinism and that they differ from any memorized output (i.e. not stale).
for (const c of NEW) {
  const a = c.fam === "sig1" ? sig1(c.input) : sig2(c.msg, c.nonce);
  const b = c.fam === "sig1" ? sig1(c.input) : sig2(c.msg, c.nonce);
  const deterministic = a === b;
  // differs from empty/short known baselines -> not constant/back-answer
  const baselinePool = new Set(CASES.filter(x => x.fam === c.fam).map(x => x.expect));
  const notBackAnswer = !baselinePool.has(a);
  if (!deterministic || !notBackAnswer) ok = false;
  results.push({ ...c, got: a, pass: deterministic && notBackAnswer, note: "unseen-input probe" });
}
console.log(JSON.stringify({ ok, results }, null, 2));