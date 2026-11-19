#!/usr/bin/env python3
"""Validate the tracked router layout without invoking the router or a skill."""

import json
from pathlib import Path, PurePosixPath
import sys


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / 'core' / 'skills'
ROUTING = SKILLS / 'config' / 'routing.json'


def main():
    try:
        tables = sorted((ROOT / 'core').rglob('routing.json'))
        if tables != [ROUTING]:
            raise ValueError('expected exactly core/skills/config/routing.json under core/')
        config = json.loads(ROUTING.read_text(encoding='utf-8-sig'))
        routes = config['routes']
        priority = config['priority']
        if len(priority) != len(routes) or set(priority) != set(routes):
            raise ValueError('priority must contain each route ID exactly once')
        if config['meta']['fallbackId'] not in routes:
            raise ValueError('fallback must reference a defined route')
        for route_id, route in routes.items():
            value = route['skill']
            pointer = PurePosixPath(value)
            if (pointer.is_absolute() or '..' in pointer.parts or ':' in value or chr(92) in value
                    or pointer.name != 'SKILL.md'):
                raise ValueError(f'{route_id}: invalid relative skill pointer')
            target = (SKILLS / pointer).resolve()
            if not target.is_relative_to(SKILLS.resolve()) or not target.is_file():
                raise ValueError(f'{route_id}: missing or out-of-tree skill pointer')
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f'FAIL {exc}', file=sys.stderr)
        return 1
    print(f'OK one route table under core/, {len(routes)} skill pointers checked')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
