# -*- coding: utf-8 -*-
"""Boot a sample as initramfs /sample in QEMU and capture its console output.

Usage:
  python qemu_run.py <sample> <input_file> <out_log>

Requires:
  QEMU at C:/Program Files/qemu/qemu-system-x86_64.exe
  kernel D:/tmp/alpine/vmlinuz-virt
  busybox D:/tmp/alpine/busybox
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
BUILDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initramfs_build.py")

sample, input_file, out_log = sys.argv[1:4]

work = tempfile.mkdtemp(prefix="qrun-", dir=r"D:\tmp")
os.makedirs(os.path.join(work, "bin"), exist_ok=True)
shutil.copyfile(BUSYBOX, os.path.join(work, "bin", "busybox"))
shutil.copyfile(sample, os.path.join(work, "sample"))
shutil.copyfile(input_file, os.path.join(work, "input.txt"))

with open(os.path.join(work, "init"), "w", newline="\n") as f:
    f.write("""#!/bin/busybox sh
/bin/busybox --install -s 2>/dev/null
mount -t proc proc /proc 2>/dev/null
mount -t sysfs sys /sys 2>/dev/null
mount -t devtmpfs dev /dev 2>/dev/null
echo "INIT-READY"
/sample < /input.txt
echo "SAMPLE-RC=$?"
echo "INIT-DONE"
/bin/busybox poweroff -f
""")

initrd = os.path.join(work, "initrd.gz")
subprocess.run([sys.executable, "-I", BUILDER, initrd, work], check=True,
               stdout=subprocess.DEVNULL)

cmd = [QEMU, "-m", "256", "-kernel", KERNEL, "-initrd", initrd,
       "-append", "console=ttyS0 rdinit=/init loglevel=4",
       "-nographic", "-no-reboot"]
try:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=120)
    raw = proc.stdout.decode("utf-8", "replace")
except subprocess.TimeoutExpired as exc:
    raw = (exc.stdout or b"").decode("utf-8", "replace") + "\n[TIMEOUT]\n"

with open(out_log, "w", encoding="utf-8") as f:
    f.write(raw)

clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", raw)
m = re.search(r"INIT-READY(.*?)INIT-DONE", clean, re.S)
body = m.group(1) if m else clean
with open(out_log + ".body.txt", "w", encoding="utf-8") as f:
    f.write(body)

print(body[-800:])
