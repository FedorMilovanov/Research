#!/usr/bin/env python3
"""Read-only, receipt-gated closure of bounded Charnock material collection.

Local validation cannot authenticate a remote service: the receipt records the
agent's separately observed Drive get_file SHA256 checksum. It is not a signature,
raw-byte download, publication approval, or a claim that all historical sources
behind the legacy dossiers have been obtained.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from audit_charnock_biographical_anchors import (
    audit_biographical_core, audit_reception_review, audit_research_handoff,
    audit_research_preparation, audit_publication_units,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path('data/charnock-biographical-anchors-v1.json')
MARKER = 'CHARNOCK-HANDOFF-V1 · wave40 · 2026-10-26'


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def observed_counts(registry):
    selection = registry['seriesSelection']
    plan = registry['researchPreparationReview']
    return dict(tcpAnchors=len(registry['anchors']), xmlObjects=len(registry['sources']),
                manualAnchors=len(registry['supportAnchors']),
                biographicalDecisions=len(registry['biographicalCoreReview']['items']),
                receptionCases=len(registry['receptionReview']['items']),
                selectionSlots=sum(len(s['refs']) for s in selection),
                selectionIds=len({r for s in selection for r in s['refs']}),
                plannedDocuments=len(selection), dossierOwners=len(registry['handoffContract']['dossierOwners']),
                textCandidates=sum(q['decision'] == 'TEXT_CANDIDATE' for q in plan['quotationPlan']),
                researchOnlyQuotes=sum(q['decision'] == 'RESEARCH_ONLY' for q in plan['quotationPlan']),
                illustrations=len(plan['illustrations']))


def safe_file(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Missing or unsafe handoff file: ' + name)
    return path


def audit_contract(registry, root=ROOT, packet_replay=False):
    contract = registry['handoffContract']
    if (contract.get('id') != 'CHARNOCK-HANDOFF-V1'
            or contract.get('authorityRole') != 'corpus-specific-supporting-only'
            or contract.get('closureMode') != 'RECEIPT_GATED_BOUNDED_RESEARCH'
            or contract.get('publicationState') != 'BLOCKED'
            or contract.get('holds') != ['PUBLICATION_HOLD']
            or contract.get('nextAction') != 'SEPARATE_USER_REQUEST_FOR_AUTHORING_OR_SCOPE_EXTENSION'
            or len(contract.get('essentialLimits', [])) < 7):
        raise ValueError('Handoff must remain bounded, non-root and publication-held')
    counts = observed_counts(registry)
    if counts != contract['expectedCounts'] or counts['plannedDocuments'] != 10 or counts['dossierOwners'] != 18:
        raise ValueError('Handoff count snapshot mismatch')
    owners = contract['dossierOwners']
    names = [o['path'] for o in owners]
    actual = sorted(str(p.relative_to(root)) for p in (root / 'БИОГРАФИИ/Стивен Чарнок').glob('*.md'))
    if len(set(names)) != 18 or sorted(names) != actual:
        raise ValueError('Handoff needs exactly eighteen distinct dossier owners')
    files = contract['requiredRepoFiles']
    if len(files) != len(set(files)) or not set(names) <= set(files):
        raise ValueError('Required files must include every dossier exactly once')
    for name in files:
        safe_file(root, name)
    receipt_path = (root / contract['receiptPath']).resolve()
    links = 0
    for owner in owners:
        text = safe_file(root, owner['path']).read_text()
        if MARKER not in text[:5000] or not owner.get('boundary') or ('Роль: ' + owner['role']) not in text[:5000]:
            raise ValueError('Dossier lacks current role/boundary marker')
        for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)', text):
            href = unquote(match.group(1).strip().split(' "')[0].split('#')[0])
            if not href or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', href):
                continue
            target = (root / owner['path']).parent / href
            target = target.resolve()
            external = str(target.relative_to(root.resolve())) if target.is_relative_to(root.resolve()) else None
            excluded_owner = packet_replay and external in contract.get('externalOwnerTargets', [])
            if not target.is_relative_to(root.resolve()) or (not target.exists() and target != receipt_path and not excluded_owner):
                raise ValueError('Missing or unsafe dossier link: ' + href)
            links += 1
    audit_publication_units(registry)
    audit_research_handoff(registry)
    audit_biographical_core(registry)
    audit_reception_review(registry, root)
    audit_research_preparation(registry, root)
    return dict(state='READY_FOR_CUSTODY', counts=counts, checkedLocalFileLinks=links,
                linkScope='Markdown file targets,not all heading fragments or external web availability')


def verify_receipt(registry, receipt, root=ROOT):
    contract = registry['handoffContract']
    policy = json.loads((root / 'data/artifact-custody-policy-v2.json').read_text())
    if any(field not in receipt for field in policy['durableReceiptRequiredFields']):
        raise ValueError('Missing durable receipt fields, including SHA256 readback')
    if (receipt.get('contractId') != contract['id'] or receipt.get('custodyState') != 'ACQUIRED_DURABLE'
            or receipt.get('publicationState') != 'BLOCKED'
            or receipt.get('holds') != ['PUBLICATION_HOLD']
            or receipt.get('destinationProvider') != 'Google Drive'
            or receipt.get('verificationMethod') != 'INDEPENDENT_DRIVE_GET_FILE_SHA256_CHECKSUM'
            or not receipt.get('destinationObjectId') or not receipt.get('destinationPath')
            or not receipt.get('verifiedBy') or receipt.get('destinationBytes', 0) <= 0
            or receipt.get('sourceArchiveBytes') != receipt.get('destinationBytes')
            or contract['destinationParentId'] not in receipt.get('destinationParentIds', [])
            or (receipt.get('sourceWorkflowRun') is None and not receipt.get('sourceWorkflowRunReason'))):
        raise ValueError('Receipt cannot invent custody, approval or verification method')
    digest = receipt.get('sourceArchiveSha256', '')
    if (not re.fullmatch('[0-9a-f]{64}', digest)
            or receipt['destinationSha256Readback'] != digest):
        raise ValueError('Destination SHA256 readback must match the archive SHA256;MD5 is insufficient')
    try:
        timestamp = datetime.fromisoformat(receipt['verifiedAtUtc'].replace('Z', '+00:00'))
        if timestamp.utcoffset() is None or timestamp.utcoffset().total_seconds() != 0:
            raise ValueError('not UTC')
    except (ValueError, TypeError) as exc:
        raise ValueError('Receipt timestamp must be UTC') from exc
    manifest = receipt['sourceManifest']
    if (hashlib.sha256(canonical_bytes(manifest)).hexdigest() != receipt['sourceManifestSha256']
            or manifest.get('contractId') != contract['id'] or manifest.get('counts') != observed_counts(registry)):
        raise ValueError('Receipt source manifest SHA/count mismatch')
    expected = set(contract['requiredRepoFiles']) | {'xml/' + k + '.xml' for k in registry['sources']}
    if set(manifest['files']) != expected:
        raise ValueError('Manifest must cover the exact research/source packet')
    for name, meta in manifest['files'].items():
        if name.startswith('xml/'):
            src = registry['sources'][Path(name).stem]
            if meta['sha256'] != src['sha256'] or meta['bytes'] != src['size']:
                raise ValueError('Manifest XML pin differs from registered source')
        else:
            raw = safe_file(root, name).read_bytes()
            if hashlib.sha256(raw).hexdigest() != meta['sha256'] or len(raw) != meta['bytes']:
                raise ValueError('Current research file differs from received packet: ' + name)
    return dict(state='BOUNDED_RESEARCH_COMPLETE', criteria=6, publicationState='BLOCKED',
                receiptObject=receipt['destinationObjectId'], counts=observed_counts(registry),
                nextAction=contract['nextAction'])


def inspect(registry, root=ROOT, require_receipt=False, packet_replay=False):
    status = audit_contract(registry, root, packet_replay)
    path = root / registry['handoffContract']['receiptPath']
    if not path.is_file():
        if require_receipt:
            raise ValueError('Receipt required: research completion remains unconfirmed')
        return status
    return verify_receipt(registry, json.loads(path.read_text()), root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--require-receipt', action='store_true')
    parser.add_argument('--packet-replay', action='store_true', help='Explicitly permit declared external-owner links,not other missing files')
    args = parser.parse_args()
    try:
        result = inspect(json.loads((args.root / REGISTRY).read_text()), args.root, args.require_receipt, args.packet_replay)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
