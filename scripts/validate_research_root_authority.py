#!/usr/bin/env python3
"""Fail-closed, read-only validation of the Research root authority graph."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/research-authority-registry-v1.json"
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read(rel: str) -> str:
    path = ROOT / rel
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {rel}: {exc}")
        return ""


def safe_rel(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{field} must be a non-empty repository-relative path")
        return ""
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{field} must stay inside the repository: {value}")
        return ""
    return value


try:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    print(f"Research root authority: FAIL (registry unreadable: {exc})", file=sys.stderr)
    raise SystemExit(1)

if not isinstance(registry, dict):
    fail("registry must contain a JSON object")

if registry.get("schemaVersion") != 1:
    fail("schemaVersion must be 1")
if registry.get("authorityId") != "RESEARCH-ROOT-AUTHORITY-REGISTRY-V1":
    fail("authorityId drift")

path_fields = (
    "stableEntrypoint",
    "rootAuthority",
    "controlPlaneAuthority",
    "evidencePolicy",
    "publicProjectionAuthority",
    "artifactCustodyPolicy",
)
paths = {field: safe_rel(registry.get(field), field) for field in path_fields}
for field, rel in paths.items():
    if rel and not (ROOT / rel).is_file():
        fail(f"{field} target missing: {rel}")

former = registry.get("formerRootAuthorities", [])
if not isinstance(former, list):
    fail("formerRootAuthorities must be an array")
    former = []
former_paths: set[str] = set()
for index, item in enumerate(former):
    if not isinstance(item, dict):
        fail(f"formerRootAuthorities[{index}] must be an object")
        continue
    rel = safe_rel(item.get("path"), f"formerRootAuthorities[{index}].path")
    if rel:
        former_paths.add(rel)
        if not (ROOT / rel).is_file():
            fail(f"former root target missing: {rel}")
    if item.get("rootStatus") != "superseded-as-root":
        fail(f"formerRootAuthorities[{index}] must be superseded-as-root")
    if not item.get("currentRole"):
        fail(f"formerRootAuthorities[{index}] must declare currentRole")

root_authority = paths.get("rootAuthority", "")
if root_authority in former_paths:
    fail("current root authority cannot also be a former root")

policy = registry.get("policy")
if not isinstance(policy, dict):
    fail("policy must be an object")
else:
    for flag in (
        "exactlyOneRootAuthority",
        "datedAuthorityMustNotBeOperationalEntrypoint",
        "formerRootMayRemainSupportingEvidence",
        "researchClosureIsNotPublicationApproval",
        "validatorMustBeReadOnly",
    ):
        if policy.get(flag) is not True:
            fail(f"policy.{flag} must be true")

stable = read(paths.get("stableEntrypoint", "")) if paths.get("stableEntrypoint") else ""
if root_authority and f"]({root_authority})" not in stable:
    fail("stable entrypoint does not link the registry rootAuthority")
if "data/research-authority-registry-v1.json" not in stable:
    fail("stable entrypoint must link the machine registry")

root_text = read(root_authority) if root_authority else ""
if "CURRENT" not in root_text or "FAIL-CLOSED" not in root_text:
    fail("root authority does not declare CURRENT / FAIL-CLOSED status")

control_text = read(paths.get("controlPlaneAuthority", "")) if paths.get("controlPlaneAuthority") else ""
if "RESEARCH-CONTROL-PLANE-2026-08-02" not in control_text:
    fail("control-plane authority identity marker missing")

for rel in ("README.md", "AGENT_RULES.md"):
    text = read(rel)
    if "CURRENT_AUTHORITY.md" not in text:
        fail(f"{rel} must use stable CURRENT_AUTHORITY.md entrypoint")
    dated = re.findall(r"00_RESEARCH_CURRENT_AUTHORITY_\d{4}-\d{2}-\d{2}\.md", text)
    if dated:
        fail(f"{rel} must not directly select a dated root authority: {sorted(set(dated))}")

if "Research closure" not in read("README.md") or "publication" not in read("README.md"):
    fail("README must preserve Research-to-publication boundary")

if errors:
    print(f"Research root authority: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Research root authority: PASS ({root_authority})")
