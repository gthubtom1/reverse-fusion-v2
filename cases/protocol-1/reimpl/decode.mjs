// decode.js - Custom-protocol decode (Stage 8 protocol reverse).
// Independent Node implementation that parses a captured frame hex
// (from the loopback pcap dump) into fields and checks the XOR checksum.
// Frame: 0xC0 0xD0 | ver(1) | type(1) | len(2 LE) | payload | checksum(1)
"use strict";

export function decodeFrame(hex) {
  const b = Buffer.from(hex, "hex");
  if (b.length < 7) return { ok: false, error: "short" };
  if (b[0] !== 0xc0 || b[1] !== 0xd0) return { ok: false, error: "bad_magic", raw: b.length };
  const ver = b[2];
  const type = b[3];
  const len = b[4] | (b[5] << 8);
  if (b.length < 6 + len + 1) return { ok: false, error: "short" };
  const payload = b.slice(6, 6 + len);
  let x = 0;
  for (const byte of payload) x ^= byte;
  const checksum = b[6 + len];
  return {
    ok: true,
    valid_checksum: x === checksum,
    version: ver,
    type,
    payload_len: len,
    payload: payload.toString("latin1"),
    payload_hex: payload.toString("hex"),
    checksum,
    expected_checksum: x,
  };
}

export function serverReplyFor(decoded) {
  // mirror of the Python server logic
  if (!decoded.ok) return decoded.error === "bad_magic" ? "ERR:magic" : "ERR:short";
  if (!decoded.valid_checksum) return "ERR:checksum";
  return `OK:${decoded.version}:${decoded.type}`;
}