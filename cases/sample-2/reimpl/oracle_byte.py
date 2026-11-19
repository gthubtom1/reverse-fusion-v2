# -*- coding: utf-8 -*-
"""Oracle scan: find a serial byte accepted by the original.

Check loop at index i (i = 0,3,6,9,12,15):
  A: serial[(i+1)%17] + serial[i]  OP  serial[(i+2)%17]*8     (OP = "eq" or "ne")
  B: serial[(i+3)%17] == (signed char)table[i] * 4

Usage: python oracle_byte.py <sample> <i> <eq|ne>
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

QEMU = r"C:\Program Files\qemu\qemu-system-x86_64.exe"
KERNEL = r"D:\tmp\alpine\vmlinuz-virt"
BUSYBOX = r"D:\tmp\alpine\busybox"
BUILDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "stage3", "initramfs_build.py")

sample, i, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
name = sys.argv[4] if len(sys.argv) > 4 else "alice"
email = sys.argv[5] if len(sys.argv) > 5 else "bob@example.com"
pos = (i + 3) % 17
a, b, c = i % 17, (i + 1) % 17, (i + 2) % 17
if max(pos, a, b) > 16:
    sys.exit("index %d is out of range" % i)

work = tempfile.mkdtemp(prefix="oracle-", dir=r"D:\tmp")
os.makedirs(os.path.join(work, "bin"))
os.makedirs(os.path.join(work, "extra", "cases"))
shutil.copyfile(BUSYBOX, os.path.join(work, "bin", "busybox"))
shutil.copyfile(sample, os.path.join(work, "sample"))
open(os.path.join(work, "input.txt"), "wb").write(b"\n\n\n")


def base_serial():
    s = bytearray(b"ABCDEFGHIJKLMNOP")
    if mode == "eq":
        # 1 + 127 == 16 * 8
        if a <= 15:
            s[a] = 1
        if b <= 15:
            s[b] = 127
        if c <= 15:
            s[c] = 16
    else:
        if get(s, b) + get(s, a) == get(s, c) * 8 and c <= 15:
            s[c] = (s[c] + 1) & 0xFF or 1
    return s


def get(s, idx):
    return s[idx] if idx < 16 else 0


for v in range(1, 256):
    s = base_serial()
    s[pos] = v
    if mode == "ne" and get(s, b) + get(s, a) == get(s, c) * 8 and c <= 15:
        s[c] = (s[c] + 1) & 0xFF or 1
    payload = name.encode() + b"\n" + email.encode() + b"\n" + bytes(s) + b"\n"
    with open(os.path.join(work, "extra", "cases", "b%03d.in" % v), "wb") as f:
        f.write(payload)

with open(os.path.join(work, "init"), "w", newline="\n") as f:
    f.write("""#!/bin/busybox sh
/bin/busybox --install -s 2>/dev/null
mount -t proc proc /proc 2>/dev/null
echo "INIT-READY"
for f in /extra/cases/*; do
  /sample < "$f" >/dev/null 2>&1
  echo "CASE:$f:$?"
done
echo "INIT-DONE"
/bin/busybox poweroff -f
""")

initrd = os.path.join(work, "initrd.gz")
subprocess.run([sys.executable, "-I", BUILDER, initrd, work], check=True,
               stdout=subprocess.DEVNULL)
proc = subprocess.run([QEMU, "-m", "256", "-kernel", KERNEL, "-initrd", initrd,
                       "-append", "console=ttyS0 rdinit=/init loglevel=4",
                       "-nographic", "-no-reboot"],
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                      timeout=300)
clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", proc.stdout.decode("utf-8", "replace"))
hits = re.findall(r"CASE:/extra/cases/(b\d+)\.in:0", clean)
print("i=%d pos=%d mode=%s hits=%s" % (i, pos, mode, hits))
if hits:
    v = int(hits[0][1:])
    s = base_serial()
    s[pos] = v
    open(r"D:\tmp\s2-valid-%d-%s.txt" % (i, mode), "wb").write(bytes(s))
    print("serial_hex", bytes(s).hex())
