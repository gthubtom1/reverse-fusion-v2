# -*- coding: utf-8 -*-
"""Custom protocol echo server (Stage 8 learning target).

Frame: 0xC0 0xD0 | ver(1) | type(1) | len(2, LE) | payload | checksum(1)
checksum = XOR of all payload bytes.
Server parses frame, validates checksum, and replies 'OK:type' or 'BAD:checksum'.
"""
import socket
import struct
import sys

HOST, PORT = "127.0.0.1", 6553


def parse(buf):
    if len(buf) < 7:
        return None
    if buf[0] != 0xC0 or buf[1] != 0xD0:
        return ("bad_magic", None)
    ver, typ = buf[2], buf[3]
    (length,) = struct.unpack("<H", buf[4:6])
    if len(buf) < 6 + length + 1:
        return ("short", None)
    payload = buf[6:6 + length]
    checksum = buf[6 + length]
    x = 0
    for b in payload:
        x ^= b
    if x != checksum:
        return ("bad_checksum", None)
    return ("ok", (ver, typ, payload))


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print("listening", HOST, PORT, flush=True)
    while True:
        conn, _ = s.accept()
        data = conn.recv(4096)
        r = parse(data)
        if r is None:
            reply = b"ERR:short"
        elif r[0] == "ok":
            reply = ("OK:%d:%d" % r[1][0:2]).encode()
        elif r[0] == "bad_magic":
            reply = b"ERR:magic"
        elif r[0] == "bad_checksum":
            reply = b"ERR:checksum"
        else:
            reply = b"ERR:short"
        conn.sendall(reply)
        conn.close()


if __name__ == "__main__":
    main()