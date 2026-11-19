#!/usr/bin/env python3
"""Check a committed handoff checkpoint, without writing to STATE.yaml."""

import argparse
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
STATE = 'lifecycle/STATE.yaml'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.PIPE)


def check(require_origin_main):
    head = git('rev-parse', '--verify', 'HEAD^{commit}').decode().strip()
    committed = git('show', f'{head}:{STATE}')
    local = (ROOT / STATE).read_bytes()
    if local.replace(b'\r\n', b'\n') != committed.replace(b'\r\n', b'\n'):
        raise ValueError(f'{STATE} has uncommitted content')

    # The checkpoint format uses these two one-line top-level scalar values.
    text = committed.decode('utf-8-sig')
    for key in ('current_stage', 'next_step'):
        values = re.findall(rf'(?m)^{key}:[ \t]*([^\r\n]*)', text)
        if len(values) != 1 or not values[0].strip().strip('\"\'').strip() or values[0].startswith('#'):
            raise ValueError(f'{STATE} requires one nonempty {key} value')

    checkpoint = git('log', '-1', '--first-parent', '--format=%H', head, '--', STATE).decode().strip()
    if checkpoint != head:
        raise ValueError(f'HEAD {head} has no state checkpoint. Last checkpoint: {checkpoint}')
    if require_origin_main:
        origin_main = git('rev-parse', '--verify', 'refs/remotes/origin/main^{commit}').decode().strip()
        if origin_main != head:
            raise ValueError(f'HEAD {head} differs from fetched origin/main {origin_main}')
    return head


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-origin-main', action='store_true',
                        help='compare HEAD with the cached origin/main ref after git fetch')
    args = parser.parse_args()
    try:
        head = check(args.require_origin_main)
    except subprocess.CalledProcessError as exc:
        print(f'FAIL Git: {exc.stderr.decode("utf-8", errors="replace").strip()}')
        return 1
    except (OSError, ValueError) as exc:
        print(f'FAIL {exc}')
        return 1
    print(f'OK STATE checkpoint {head}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
