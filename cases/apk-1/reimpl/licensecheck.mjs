// Repro for apk-1 license validation (extracted via jadx from MainActivity).
// Independent Node reimplementation of the Java validate() semantics.
// Original: cases/apk-1/target/MainActivity.class (jadx-out gives the source
// reading; we DO NOT load/eval the class, we re-implement the algorithm).
"use strict";

const KEY = [0x46, 0x55, 0x53, 0x49, 0x4f, 0x4e]; // "FUSION"

export function validate(serial) {
  if (serial == null || serial.length < 4) return false;
  let sum = 0;
  for (let i = 0; i < serial.length; i++) {
    const c = serial.charCodeAt(i) & 0xff;
    const k = KEY[i % KEY.length];
    sum += (c ^ k);
  }
  return (sum & 0xff) === 0xd0 && serial.startsWith("FUSION");
}

// derive a valid serial for given prefix by adjusting last char
export function makeValid(prefix) {
  if (!prefix.startsWith("FUSION")) prefix = "FUSION" + prefix;
  const base = prefix + "A";
  let s = base;
  // adjust last char until sum&0xFF == 0xD0
  for (let c = 0; c < 256; c++) {
    s = prefix + String.fromCharCode(c);
    if (validate(s)) return s;
  }
  return null;
}