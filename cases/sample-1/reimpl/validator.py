# -*- coding: utf-8 -*-
"""Independent reimplementation of CrackMe.exe validation (sample 1).

Evidence: cases/sample-1/evidence/E-005-check.json
- input must be exactly 6 characters (strlen == 6)
- constants: 0x38, 0x27, 0x64, 0x66, 0x66, 0x62
- check: input[i] == constants[i] ^ 0x55 for all i
"""

KEY = 0x55
EXPECTED_XORED = [0x38, 0x27, 0x64, 0x66, 0x66, 0x62]


def expected_password() -> str:
    return "".join(chr(b ^ KEY) for b in EXPECTED_XORED)


def read_token(raw: str) -> str:
    """Model C++ `cin >> std::string`: skip leading whitespace, stop at the
    next whitespace. Evidence: E-008 cases B3/B6 accept trailing space/CR."""
    parts = raw.split()
    return parts[0] if parts else ""


def check(raw: str) -> bool:
    password = read_token(raw)
    if len(password) != 6:
        return False
    return all(ord(ch) == (b ^ KEY) for ch, b in zip(password, EXPECTED_XORED))


if __name__ == "__main__":
    import sys
    candidate = sys.argv[1] if len(sys.argv) > 1 else ""
    print("expected:", expected_password())
    print("input:", candidate)
    print("accepted" if check(candidate) else "denied")
