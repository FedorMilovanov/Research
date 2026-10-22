# -*- coding: utf-8 -*-
"""Renderer reproducing the mixed style of ИСКУПЛЕНИЕ/ot/data/ot-corpus-v1.json.

Rules (verified by round-tripping card 11):
  * dict / list -> multi-line, items at ind + 2
  * dict whose values are all scalars -> single line (as in cards[11].vocabularyAbsence
    and qaFullPass.totals)
  * dicts inside lists -> single line (as in cards[*].verses / .nt and sources)
  * scalars -> json.dumps(..., ensure_ascii=False)
"""
import json
import sys


def _scalar_only(v):
    return isinstance(v, dict) and v and all(
        not isinstance(x, (dict, list)) for x in v.values())


def _inline(v):
    return json.dumps(v, ensure_ascii=False)


def kv_block(key, value, ind):
    """`"key": value` where a multi-line value starts on the key line."""
    return ' ' * ind + json.dumps(key, ensure_ascii=False) + ': ' + render(value, ind)


def block(v, ind=0):
    """render() with the first line padded to `ind` (for insertion into a file)."""
    return ' ' * ind + render(v, ind)


def render(v, ind=0):
    pad = ' ' * ind
    if isinstance(v, dict):
        if _scalar_only(v):
            return _inline(v)
        out = ['{']
        items = list(v.items())
        for i, (k, val) in enumerate(items):
            out.append(' ' * (ind + 2) + json.dumps(k, ensure_ascii=False) + ': '
                       + render(val, ind + 2) + (',' if i < len(items) - 1 else ''))
        out.append(pad + '}')
        return '\n'.join(out)
    if isinstance(v, list):
        if not v:
            return '[]'
        out = ['[']
        for i, val in enumerate(v):
            txt = _inline(val) if isinstance(val, dict) else render(val, ind + 2)
            out.append(' ' * (ind + 2) + txt + (',' if i < len(v) - 1 else ''))
        out.append(pad + ']')
        return '\n'.join(out)
    return _inline(v)


if __name__ == '__main__':
    import io
    path = '/home/user/Research/ИСКУПЛЕНИЕ/ot/data/ot-corpus-v1.json'
    raw = io.open(path, encoding='utf-8').read()
    data = json.loads(raw)
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        lines = raw.split('\n')
        start = next(i for i, ln in enumerate(lines) if ln == '      "id": 11,') - 1
        end = next(i for i, ln in enumerate(lines[start:], start) if ln == '    }')
        want = '\n'.join(lines[start:end + 1])
        got = block(data['cards'][11], 4)
        print('card 11 round-trip:', 'IDENTICAL' if want == got else 'DIFF')
        if want != got:
            wl, gl = want.split('\n'), got.split('\n')
            for i in range(max(len(wl), len(gl))):
                a = wl[i] if i < len(wl) else '<none>'
                b = gl[i] if i < len(gl) else '<none>'
                if a != b:
                    print('line %d' % i)
                    print('  file:', a[:160])
                    print('  ours:', b[:160])
                    break
        # wave13 round-trip
        start = next(i for i, ln in enumerate(lines) if ln == '  "wave13": {')
        end = next(i for i, ln in enumerate(lines[start:], start) if ln == '  },')
        want = '\n'.join(lines[start:end + 1])
        got = kv_block('wave13', data['wave13'], 2)
        print('wave13 round-trip:', 'IDENTICAL' if want == got else 'DIFF')
        if want != got:
            wl, gl = want.split('\n'), got.split('\n')
            for i in range(max(len(wl), len(gl))):
                a = wl[i] if i < len(wl) else '<none>'
                b = gl[i] if i < len(gl) else '<none>'
                if a != b:
                    print('line %d\n  file: %s\n  ours: %s' % (i, a[:160], b[:160]))
                    break
