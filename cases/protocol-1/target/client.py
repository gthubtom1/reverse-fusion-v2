# -*- coding: utf-8 -*-
"""Client that sends 5 protocol frames and prints server replies."""
import socket
import struct

HOST, PORT = "127.0.0.1", 6553


def build(ver, typ, payload):
    length = len(payload)
    x = 0
    for b in payload:
        x ^= b
    return bytes([0xC0, 0xD0, ver, typ]) + struct.pack("<H", length) + payload + bytes([x])


def run(cases):
    out = []
    for name, pkt in cases:
        s = socket.create_connection((HOST, PORT), timeout=3)
        s.sendall(pkt)
        reply = s.recv(64)
        s.close()
        out.append((name, pkt.hex(), reply.decode("latin-1")))
    return out


if __name__ == "__main__":
    cases = [
        ("T1-good", build(1, 5, b"hello")),
        ("T2-good", build(2, 9, b"world!")),
        ("T3-empty", build(1, 0, b"")),          # valid, empty payload
        ("T4-bad_checksum", build(1, 5, b"hello")[:-1] + bytes([0x00])),  # corrupt cs
        ("T5-bad_magic", bytes([0x00, 0x00, 1, 5, 6, 0]) + b"hello" + bytes([0x00])),
    ]
    for row in run(cases):
        print("%s %s -> %s" % row)