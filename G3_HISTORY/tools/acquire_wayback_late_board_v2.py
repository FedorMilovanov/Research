#!/usr/bin/env python3
"""Acquire and decode late-2026 archived G3 Who-We-Are pages.

Read-only research helper. The CDX query deliberately preserves every capture
timestamp (no digest collapse) so late-board continuity is not accidentally hidden
when several snapshots have identical content. Exact archive bytes and decoded HTML
are kept separately with hashes. Nothing is publication-authorized.

Exit contract:
- 0: acquisition completed without semantic or transport defects;
- 2: parse/schema/decode/invariant or other non-transport defect (fail closed);
- 3: only bounded retryable transport failures were exhausted (TRANSPORT_HOLD).

A known archived timestamp may be used as a recovery locator for object acquisition,
but it is never counted as a CDX result and never converts a failed continuity query
into successful archive coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

TARGET = 'http://g3min.org/about/who-we-are/'
CDX_TARGET = 'g3min.org/about/who-we-are/'
KNOWN = '20260721102641'
NAMES = ['Buck Braswell', 'Matt Broome', 'Jon Norton', 'Matt Sikes', 'Dylan Joyner', 'Ron Mooney']
UA = 'FedorMilovanov-Research-G3-Wayback-Acquisition/3.1 (research-only)'
ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
RETRY_DELAYS = (2, 6)


class TransportHold(RuntimeError):
    """A bounded retry budget was exhausted for an external transport failure."""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def writej(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = ' '.join(data.split())
        if value:
            self.parts.append(value)


def txt(data: bytes) -> str:
    parser = Text()
    parser.feed(data.decode('utf-8', 'replace'))
    return '\n'.join(parser.parts)


def get(url: str, timeout: int = 90, attempts: int = 3):
    """Fetch with bounded retries; classify exhausted retryable failures separately."""
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                return data, {
                    'requested_url': url,
                    'final_url': response.geturl(),
                    'status': getattr(response, 'status', None),
                    'content_type': response.headers.get('Content-Type'),
                    'content_encoding': response.headers.get('Content-Encoding'),
                    'bytes': len(data),
                    'sha256': sha(data),
                    'elapsed_seconds': round(time.time() - started, 3),
                    'attempt': attempt,
                    'max_attempts': attempts,
                }
        except urllib.error.HTTPError as exc:
            body = exc.read()
            message = (
                f'HTTP {exc.code} {exc.reason} url={url} '
                f'body_sha256={sha(body)} bytes={len(body)} attempt={attempt}/{attempts}'
            )
            if exc.code not in RETRYABLE_HTTP:
                raise RuntimeError(message) from exc
            if attempt >= attempts:
                raise TransportHold(message) from exc
        except urllib.error.URLError as exc:
            message = f'URL error {exc.reason} url={url} attempt={attempt}/{attempts}'
            if attempt >= attempts:
                raise TransportHold(message) from exc
        except TimeoutError as exc:
            message = f'Timeout url={url} attempt={attempt}/{attempts}'
            if attempt >= attempts:
                raise TransportHold(message) from exc

        delay = RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)]
        print('TRANSIENT_RETRY', f'attempt={attempt}/{attempts}', f'sleep={delay}s', url, file=sys.stderr)
        time.sleep(delay)

    raise RuntimeError(f'fetch exhausted unexpectedly url={url}')


def decode_archived_payload(raw: bytes):
    if raw.startswith(ZSTD_MAGIC):
        zstd = shutil.which('zstd')
        if not zstd:
            raise RuntimeError('Zstandard payload detected but zstd CLI is unavailable')
        proc = subprocess.run(
            [zstd, '-d', '-q', '-c'],
            input=raw,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode:
            raise RuntimeError('zstd decode failed: ' + proc.stderr.decode('utf-8', 'replace')[:500])
        return proc.stdout, 'zstd-cli'
    return raw, 'identity'


def parse_cdx(data: bytes) -> tuple[list[dict], str]:
    rows = json.loads(data.decode('utf-8'))
    if not isinstance(rows, list):
        raise RuntimeError('CDX JSON root is not a list')
    if not rows:
        return [], 'VALID_EMPTY_CDX'
    header = rows[0]
    if not isinstance(header, list) or 'timestamp' not in header:
        raise RuntimeError('CDX response has an invalid header row')
    captures = [
        dict(zip(header, row))
        for row in rows[1:]
        if isinstance(row, list) and len(row) == len(header)
    ]
    return captures, 'CAPTURES_PRESENT' if captures else 'VALID_HEADER_ZERO_ROWS'


def selected_captures(captures: list[dict]) -> list[dict]:
    """Known snapshot if indexed + every chronological digest change + latest capture."""
    rows = sorted(captures, key=lambda item: item.get('timestamp', ''))
    out: list[dict] = []
    seen_ts: set[str] = set()
    previous_digest = object()

    def add(item: dict) -> None:
        timestamp = item.get('timestamp', '')
        if timestamp and timestamp not in seen_ts:
            out.append(item)
            seen_ts.add(timestamp)

    known = next((item for item in rows if item.get('timestamp') == KNOWN), None)
    if known:
        add(known)
    for item in rows:
        digest = item.get('digest')
        if digest != previous_digest:
            add(item)
            previous_digest = digest
    if rows:
        add(rows[-1])
    return sorted(out, key=lambda item: item.get('timestamp', ''))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='g3-wayback-late-board-output')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    cdx_url = 'https://web.archive.org/cdx/search/cdx?' + urllib.parse.urlencode({
        'url': CDX_TARGET,
        'from': '20260721',
        'to': '20260831',
        'output': 'json',
        'fl': 'timestamp,original,statuscode,mimetype,digest,length',
        'filter': 'statuscode:200',
    })

    summary = {
        'target': TARGET,
        'known_snapshot': KNOWN,
        'state': 'EPHEMERAL_ACTION_ARTIFACT',
        'publication_eligible': False,
        'negative_result_boundary': (
            'Archive coverage or transport failure is not evidence of board continuity, absence, resignation, or non-resignation.'
        ),
        'errors': [],
        'transport_holds': [],
        'captures': [],
    }

    cdx_captures: list[dict] = []
    try:
        raw_cdx, fetch_meta = get(cdx_url, 45)
        (out / 'CDX.json').write_bytes(raw_cdx)
        writej(out / 'CDX_FETCH.json', fetch_meta)
        cdx_captures, cdx_state = parse_cdx(raw_cdx)
        summary['cdx_query_state'] = cdx_state
    except TransportHold as exc:
        summary['cdx_query_state'] = 'TRANSPORT_HOLD'
        summary['transport_holds'].append('CDX: ' + str(exc))
    except Exception as exc:
        summary['cdx_query_state'] = 'ERROR'
        summary['errors'].append('CDX: ' + str(exc))

    by_timestamp: dict[str, dict] = {}
    for item in cdx_captures:
        timestamp = item.get('timestamp', '')
        if timestamp:
            by_timestamp.setdefault(timestamp, item)
    cdx_captures = sorted(by_timestamp.values(), key=lambda item: item.get('timestamp', ''))

    summary['cdx_capture_count'] = len(cdx_captures)
    summary['cdx_timestamps'] = [item.get('timestamp') for item in cdx_captures]
    summary['distinct_digests'] = len({item.get('digest') for item in cdx_captures if item.get('digest')})
    summary['latest_cdx_capture'] = cdx_captures[-1] if cdx_captures else None

    chosen = selected_captures(cdx_captures)
    if not any(item.get('timestamp') == KNOWN for item in chosen):
        chosen.append({
            'timestamp': KNOWN,
            'original': TARGET,
            'fallback_known_locator': True,
            'digest': 'unknown',
        })
        chosen = sorted(chosen, key=lambda item: item.get('timestamp', ''))

    summary['selected_capture_timestamps'] = [item.get('timestamp') for item in chosen]
    summary['fallback_locator_used'] = any(item.get('fallback_known_locator') for item in chosen)

    for item in chosen[:50]:
        timestamp = item.get('timestamp', '')
        original = item.get('original') or TARGET
        if not timestamp:
            continue
        snapshot_url = f'https://web.archive.org/web/{timestamp}id_/{original}'
        record = {'cdx': item, 'snapshot_url': snapshot_url}
        try:
            raw, fetch_meta = get(snapshot_url, 120)
            raw_name = f'{timestamp}_who-we-are.raw'
            (out / raw_name).write_bytes(raw)
            decoded, method = decode_archived_payload(raw)
            html_name = f'{timestamp}_who-we-are.html'
            (out / html_name).write_bytes(decoded)
            text = txt(decoded)
            text_name = f'{timestamp}_who-we-are.txt'
            (out / text_name).write_text(text, encoding='utf-8')
            hits = {name: (name.casefold() in text.casefold()) for name in NAMES}
            record.update({
                'fetch': fetch_meta,
                'raw_file': raw_name,
                'raw_sha256': sha(raw),
                'raw_bytes': len(raw),
                'decoded_file': html_name,
                'decoded_sha256': sha(decoded),
                'decoded_bytes': len(decoded),
                'decode_method': method,
                'text_file': text_name,
                'text_sha256': sha(text.encode()),
                'name_hits': hits,
                'all_six_names_present': all(hits.values()),
            })
        except TransportHold as exc:
            record['transport_hold'] = str(exc)
            summary['transport_holds'].append(f'snapshot {timestamp}: {exc}')
        except Exception as exc:
            record['error'] = str(exc)
            summary['errors'].append(f'snapshot {timestamp}: {exc}')
        summary['captures'].append(record)

    successful = [
        item for item in summary['captures']
        if item.get('fetch') and item.get('decoded_file')
    ]
    summary['successful_capture_count'] = len(successful)

    writej(out / 'SUMMARY.json', summary)

    print('CDX_QUERY_STATE', summary.get('cdx_query_state'))
    print('CDX_CAPTURE_COUNT', summary['cdx_capture_count'])
    print('CDX_TIMESTAMPS', ','.join(item or '' for item in summary['cdx_timestamps']))
    print('DISTINCT_DIGESTS', summary['distinct_digests'])
    latest = summary.get('latest_cdx_capture') or {}
    print('LATEST_CDX', latest.get('timestamp'), latest.get('digest'))
    print('FALLBACK_LOCATOR_USED', summary['fallback_locator_used'])

    for item in successful:
        print(
            'ACQUIRED',
            item['cdx'].get('timestamp'),
            'digest=', item['cdx'].get('digest'),
            'fallback=', bool(item['cdx'].get('fallback_known_locator')),
            'all6=', item.get('all_six_names_present'),
            'decode=', item.get('decode_method'),
        )

    if summary['errors']:
        for error in summary['errors']:
            print('ERROR', error, file=sys.stderr)
        return 2
    if summary['transport_holds']:
        for hold in summary['transport_holds']:
            print('TRANSPORT_HOLD', hold, file=sys.stderr)
        return 3
    if not successful:
        print('ERROR no archived snapshot could be acquired despite a clean transport state', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
