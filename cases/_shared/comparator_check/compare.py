# -*- coding: utf-8 -*-
"""Shared anti-back-answer comparator (v3.1 R6).

Usage: each domain calls check(candidates, normal, tampered) where normal/
tampered are callables over a candidate. Every candidate that is *accepted*
under normal must flip to rejected under tampered; already-rejected
candidates must stay rejected (correct semantics). Returns ok + rows.
"""
import json


def check(candidates, normal, tampered, label="domain"):
    rows = []
    for c in candidates:
        n = normal(c)
        t = tampered(c)
        if n is True:
            ok = t is False  # accepted must flip
            note = "accepted->must flip"
        else:
            ok = t is False  # rejected stays rejected
            note = "rejected stays"
        rows.append({"input": c if isinstance(c, str) else repr(c),
                     "normal": n, "tampered": t, "ok": ok, "note": note})
    result = {"label": label, "ok": all(r["ok"] for r in rows), "rows": rows}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    # self-test
    r = check(["A", "B"], lambda s: s == "A", lambda s: False)
    assert r["ok"]