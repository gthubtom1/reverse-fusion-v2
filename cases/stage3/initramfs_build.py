# -*- coding: utf-8 -*-
"""Build a tiny gzipped newc cpio initramfs with an embedded sample.

Usage:
  python initramfs_build.py <out.cpio.gz> <src_dir>

Layout expected in src_dir: init (shell script), bin/busybox, sample, input.txt
"""
import gzip
import io
import os
import stat
import sys

out_path, src = sys.argv[1], sys.argv[2]

FILES = [
    ("init", "init", 0o100755),
    ("bin/busybox", "bin/busybox", 0o100755),
    ("sample", "sample", 0o100755),
    ("input.txt", "input.txt", 0o100644),
]

buf = io.BytesIO()
ino = 1


def pad4(b):
    return b + b"\x00" * ((4 - len(b) % 4) % 4)


def add(name, data, mode, rdev=(0, 0)):
    global ino
    namez = name.encode() + b"\x00"
    hdr = ("070701" + "".join("%08X" % v for v in [
        ino, mode, 0, 0, 1, 0, len(data), 0, 0, rdev[0], rdev[1],
        len(namez), 0]))
    buf.write(hdr.encode())
    buf.write(namez)
    buf.write(b"\x00" * ((4 - (110 + len(namez)) % 4) % 4))
    buf.write(data)
    buf.write(b"\x00" * ((4 - len(data) % 4) % 4))
    ino += 1


# explicit directories, then device nodes expected by an initramfs init
add("bin", b"", 0o040755)
add("dev", b"", 0o040755)
add("dev/console", b"", 0o020600, rdev=(5, 1))
add("dev/null", b"", 0o020666, rdev=(1, 3))

for src_rel, name, mode in FILES:
    path = os.path.join(src, src_rel)
    if not os.path.exists(path):
        sys.exit("missing " + path)
    with open(path, "rb") as f:
        data = f.read()
    add(name, data, mode)

# optional extra/ tree (paths preserved, directories created)
extra_root = os.path.join(src, "extra")
if os.path.isdir(extra_root):
    for dirpath, dirnames, filenames in os.walk(extra_root):
        rel_dir = os.path.relpath(dirpath, extra_root).replace("\\", "/")
        parts = [] if rel_dir == "." else rel_dir.split("/")
        acc = []
        for part in parts:
            acc.append(part)
            add("/".join(acc), b"", 0o040755)
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            with open(full, "rb") as f:
                data = f.read()
            add("/".join(parts + [fn]), data, 0o100644)

# trailer
hdr = ("070701" + "".join("%08X" % v for v in [
    ino, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 11, 0]))
buf.write(hdr.encode())
buf.write(b"TRAILER!!!\x00")
buf.write(b"\x00" * ((4 - (110 + 11) % 4) % 4))

with open(out_path, "wb") as raw:
    with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as g:
        g.write(buf.getvalue())
print("wrote", out_path, len(buf.getvalue()), "bytes")
