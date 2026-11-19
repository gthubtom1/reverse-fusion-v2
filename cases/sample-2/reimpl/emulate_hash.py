# -*- coding: utf-8 -*-
"""Emulate FUN_00401d80 (the custom 256-byte hash) with Unicorn.

Usage: python emulate_hash.py <elf> <hex-input>
Prints the 256-byte result as hex.
"""
import struct
import sys

from elftools.elf.elffile import ELFFile
from unicorn import (UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_64, Uc, UcError)
from unicorn.x86_const import (UC_X86_REG_FS_BASE, UC_X86_REG_RDI,
                               UC_X86_REG_RIP, UC_X86_REG_RSI,
                               UC_X86_REG_RSP, UC_X86_REG_RAX,
                               UC_X86_REG_RCX, UC_X86_REG_RDX,
                               UC_X86_REG_R8, UC_X86_REG_R9)

FUNC = 0x401D80
MALLOC = 0x41B7D0
FREE = 0x41BB10
MEMCPY_GOT = 0x4C5038
RET_MAGIC = 0x11111111
STACK = 0x70000000
STACK_SIZE = 0x40000
HEAP = 0x60000000
HEAP_SIZE = 0x1000000
TLS = 0x50000000
STUB = 0x4D0000

elf_path, hex_input = sys.argv[1], sys.argv[2]
data_in = bytes.fromhex(hex_input)

mu = Uc(UC_ARCH_X86, UC_MODE_64)

with open(elf_path, "rb") as f:
    elf = ELFFile(f)
    for seg in elf.iter_segments():
        if seg["p_type"] != "PT_LOAD":
            continue
        vaddr = seg["p_vaddr"]
        memsz = seg["p_memsz"]
        filesz = seg["p_filesz"]
        base = vaddr & ~0xFFF
        end = (vaddr + memsz + 0xFFF) & ~0xFFF
        mu.mem_map(base, max(end - base, 0x1000))
        mu.mem_write(vaddr, seg.data()[:filesz])

mu.mem_map(STACK, STACK_SIZE)
mu.mem_map(HEAP, HEAP_SIZE)
mu.mem_map(TLS, 0x4000)
mu.mem_map(STUB, 0x1000)
mu.mem_write(TLS + 0x28, b"\x11\x22\x33\x44\x55\x66\x77\x88")

heap_ptr = HEAP + 0x1000
input_ptr = HEAP + 0x800000
mu.mem_write(input_ptr, data_in)
mu.mem_write(MEMCPY_GOT, struct.pack("<Q", STUB))

# stub: memcpy(dst, src, n) -> handled in hook, then ret
mu.mem_write(STUB, b"\xC3")


def hook_code(uc, address, size, user):
    global heap_ptr
    if address == MALLOC:
        size = uc.reg_read(UC_X86_REG_RDI)
        ptr = heap_ptr
        heap_ptr = (heap_ptr + size + 0x3F) & ~0x3F
        uc.reg_write(UC_X86_REG_RAX, ptr)
        ret = struct.unpack("<Q", uc.mem_read(
            uc.reg_read(UC_X86_REG_RSP), 8))[0]
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)
        return
    if address == FREE:
        ret = struct.unpack("<Q", uc.mem_read(
            uc.reg_read(UC_X86_REG_RSP), 8))[0]
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)
        return
    if address == STUB:
        dst = uc.reg_read(UC_X86_REG_RDI)
        src = uc.reg_read(UC_X86_REG_RSI)
        n = uc.reg_read(UC_X86_REG_RDX)
        if n:
            uc.mem_write(dst, bytes(uc.mem_read(src, n)))
        uc.reg_write(UC_X86_REG_RAX, dst)
        ret = struct.unpack("<Q", uc.mem_read(
            uc.reg_read(UC_X86_REG_RSP), 8))[0]
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)


mu.hook_add(UC_HOOK_CODE, hook_code)

rsp = STACK + STACK_SIZE - 0x1000
mu.mem_write(rsp, struct.pack("<Q", RET_MAGIC))
mu.reg_write(UC_X86_REG_RSP, rsp)
mu.reg_write(UC_X86_REG_RDI, input_ptr)
mu.reg_write(UC_X86_REG_RSI, len(data_in))
mu.reg_write(UC_X86_REG_FS_BASE, TLS)

try:
    mu.emu_start(FUNC, RET_MAGIC, timeout=60 * 1000 * 1000, count=200000000)
except UcError as exc:
    print("EMU ERROR", exc, "pc", hex(mu.reg_read(UC_X86_REG_RIP)))
    sys.exit(1)

ptr = mu.reg_read(UC_X86_REG_RAX)
out = bytes(mu.mem_read(ptr, 256))
print(out.hex())
