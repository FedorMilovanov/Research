#!/usr/bin/env python3
"""Validate the completed I.1 entry citation pass."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
RECEIPT = ROOT / "data/heart-i1-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-i1-reader-assembly-2026-08-04.json"
CURRENT_V3 = ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/107_I1_CITATION_REVIEW_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

BLOBS = {
    ASSEMBLY: "e4b805585fbe9606efb5ed4c59861d52ec08c699",
    CURRENT_V3: "407c8d78baa966a3336e7bd60edfa51178b74f32",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    READER: "a5d35df1a87ab39abc8a85b1d84f1b1ab03da105",
}
PRODUCT_BLOB = "acc12804f5b2450efebbb6e0b2cabd31066ef48c"
PRODUCT_SHA = "50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07"
REFERENCE_SET_SHA = "054912d08830664a4f898ea326b47dd421986fe4dc80cad80f9061342d1013d5"
READER_REFERENCE_SET_SHA = "8a14e3cb29cc087963479ac9ae2e4e65ac7414615cb691233299d2eb520aedf4"
MANIFEST_SHA = "3464ce1118b5ae9cf829627346fc12850e2acb35e1e00448383bad61a7398a10"
EXPECTED_SECTION_SUMMARY = {'bog-trebuet-vsyo': {'surfaces': 3, 'withNearbyScripture': 3}, 'bog-vidit-serdce': {'surfaces': 6, 'withNearbyScripture': 6}, 'frontmatter-or-introduction': {'surfaces': 7, 'withNearbyScripture': 5}, 'hranit-serdce': {'surfaces': 3, 'withNearbyScripture': 3}, 'istochniki': {'surfaces': 3, 'withNearbyScripture': 3}, 'nepravilno-slyshim': {'surfaces': 10, 'withNearbyScripture': 10}, 'novoe-serdce': {'surfaces': 4, 'withNearbyScripture': 4}, 'padshee-serdce': {'surfaces': 4, 'withNearbyScripture': 4}, 'serdce-boga': {'surfaces': 6, 'withNearbyScripture': 5}, 'serdce-chuvstvuet': {'surfaces': 7, 'withNearbyScripture': 7}, 'serdce-dusha-duh': {'surfaces': 7, 'withNearbyScripture': 7}, 'serdce-govorit': {'surfaces': 3, 'withNearbyScripture': 3}, 'serdce-lyubit': {'surfaces': 6, 'withNearbyScripture': 5}, 'serdce-myslit': {'surfaces': 6, 'withNearbyScripture': 6}, 'serdce-reshaet': {'surfaces': 4, 'withNearbyScripture': 4}, 'serdce-sovest': {'surfaces': 5, 'withNearbyScripture': 5}, 'serdce-veruet': {'surfaces': 6, 'withNearbyScripture': 6}, 'tverdo-ne-dubinkoy': {'surfaces': 2, 'withNearbyScripture': 0}, 'vnutrenniy-chelovek': {'surfaces': 3, 'withNearbyScripture': 2}, 'vyhod': {'surfaces': 3, 'withNearbyScripture': 3}}
EXPECTED_LINKS = ['/articles/krajne-li-isporcheno-serdce/', '/articles/novoe-serdce/', '/articles/serdce-hrista-k-nemoshchnym/', '/articles/skrytye-idoly-serdca/']
EXPECTED_TARGETS = ['src/content/articles/krajne-li-isporcheno-serdce.mdx', 'src/content/articles/novoe-serdce.mdx', 'src/content/articles/serdce-hrista-k-nemoshchnym.mdx', 'src/content/articles/skrytye-idoly-serdca.mdx']
CLASS_HASHES = {
    'EDITORIAL_OR_COLLOQUIAL': ['1109d9b0fb9bf3efe86ffbb7f5a3ee3fcfd3e7615e0cc2b1d70f320e0bc07842', '1a2c601ce843221dfdb047ee5b76599e174b393829672c39e6b6639f5eb20b6f', '3242f85f2eb1d2c3b0bd56b44df583f5650c9b470d38a1985d347795610a2444', '444b75bc13260574b10f02f9a69b439d7795505d83286be29a1ae0ec72103c2c', '4f50119de597625bef47a20139697d7488df647efba64de02da0767bf25479a3', '59573d542001b9bff7823308515e8e5eb8b75eb4e841ba8a5cee11a668c5a322', '672e1b47a1fdbd45f5c99ef99638a6cb79cd7f2f90cb9b119d7958b0e950fd63', '69841218a09997fe6d46ed0e63dc7fd4f364285c7d7e71cd9e6b3aa2dd6931a2', '7ec6744d969e338013bf35ad0b815be87572681ab94c6db3a162187840848af9', '902767037a7756eb98484200bafeacc72b34061008afe674b42c1fabae593b59', '911a6fde6653ee59e779801598846295a5fcafe2640193f65dd84bba7c0ced50', '9a552d9b996bdf002d4307d0f5271de72b93d76b34a451d34197c4a97ddd9574', 'bfdb60a6533259b1fea87dbd5962fdc0f6d578c28c5e376c5a8e19c1bc8a00b3', 'c2b0e643eb67185553baec6ecc5448e2082432ecf27b34125366cbcfd22eb868', 'c41e8042b2e953e579114fd3a633bb4223cc012ed46a5345c463705ca0f6df54', 'dfa3b619426ee1682ac772797f3051a6e69096b07c05bb15370bb8a02b107c13', 'f6e8375d3fb8e64e016d60d5e0f3d9915d86ed3844285c0456d7e22a01127959'],
    'LEXICAL_OR_TRANSLATION': ['165ddb82c718490603f2a5892eed93b011c3c9bed940f1524eaf64ba3b2b1710', '6a250f5814c3c089ee79c6ba9ca23af950062507969a85a3f04fe1dcede81766', '8972c7ea393e7dd86f5f1704f6ed41d3892683ecd5c0fa393d25ea02001cac80', '9755233a9ac4811a21d99d93082727d8a73883916598c11df239f638e47d68a3', 'c09afa243fcec6bfcaf3e5bfe5e7ee302e5bda71d33e54c288faf9e81e97ec2f'],
    'SCRIPTURE_DIRECT_RUSSIAN_SYNODAL': ['02b2897c48863fd79f951019d2aeb6334b3e23e5338785c30b4fc55aee7164f2', '03f0afbf98a82fd37231e362af37716fafed1c975d8f00e3267d8ba968d2826f', '05ceba1cc6f2842f60929039c3e94adbf60596bcfd278122de17239aca399e97', '0d35e5a706b21ebc294577b4d119fb09190efabc6767db68272b7f978cca7a47', '1333fe688b3b0f4a6c4cb6d39ac9066102879afa64e7bf460cceca4552739eb3', '14ba5fdeff428610ad4bf3496b70ca334ea75f8a24f41fb4be6493c1443dfffd', '1812e25fcbefc78d250ee4c3718b629899186a346734111b22b4ddb09ababeb9', '190eb480b9e52f1e96f005cae95f528347740320b39aca268a57e138ee6f1d5b', '1991601d0d23775f2683ea86dc398fa9350863b9df29befce2a333151aa4adf0', '1ca8956af845e9356a083fbc9d73819401a134389a3b6fb2468d0623d8016566', '1e07d8dfeb219ebef2cb59f84f46de3f30130d33d758b8e023f429cc6895f758', '218ca94103b2d97ae29faaadbdaa444af6f22c75d6839737e5adf76f5901ccc1', '2bfeb4bf51c313191c3b8cf71e6eb238ff07e5040e32c504f49b734bcd92c90b', '2fbdbf08b78e2e484a641d8ea56d88d64d388e9f3a875cd3f2d5b1c63e4810da', '389a66e5cb8fbda71923f2bc5a29c1f40ee025e0bcc28da76fac8c713fbdcb27', '3a085e7f3a4cccb29d3bc348831bb91fa048b196cf01cba099ee3f7d87ea9aef', '3d7f3bf38a496579c902aa67f1c8aa8c0513df5732110b9992cd0bfd44c13787', '460cbbac852d84b0bbc9540b129439702d3378769dc9b316db1b5ad22ec06693', '4b847cb7596489a0295c132cc0ba922a258712294ca07149353a833178a7ac11', '4c4a4266416be8221147bfb71355466ac1763e61936694ce48e5f67789c90b34', '4dc5d9aa3c411916014365749d561769557cc885f7e1a6e20e569ff240a06184', '509a31fe42442b30acc0a66e536169ac6d1e28e0b7bb27cce0e655b9501a9eb1', '5b7e9fe70c5b82933781b0fa5e6df631f93f265818087c2f2b9e7eb480933486', '5b99eabe429fb77de0f3df3c3772c39bce5e85b9f9726fd5c50a7d38c300e20a', '5e39cf50bc5aa05598370a40af6b31a83aa0fe3e3a9051b3c442716c62c97402', '621a2b328a7e7e80e04686d601b06dadc8b41810a55c6b4c76f5038f4da18590', '641e08f0964521b02ba8140580a1fec328332d01d0d2396fab87a71cbcc436bb', '646006aea301f8e95ec0764552d072974ca1ce296989abc3be88f76ef1539d2c', '64eeadb959265981838fcebfd676a63fd0046853c18b72050d28c1e4a811eefc', '67d05322b0cc9c3ec28ad56d92ab93be0c4e2ea9b1661b4aade7458e6d84b47f', '685b0a80213031ce5bcb53d03b231e892ed60c20b3f6fa5fb300c6a76e5e8471', '718dde389a9a62a408c2e7e0c939120b24cef19a8a3f8b5c3c0c80e9a9c3f15c', '7731d1998fbbb521d8dba407b82d550c324d5fb2b404e3c448a2aff3c442073c', '7cc06f84d21f2fb9eac1206767f8ff898c312ce13c2b3bd2a1b0731b8065555f', '8168cfa9ed6189271f09e4dcb95c4a188a026ca58448bb86e9229217d220214a', '84224b67c8b8d7596fcad6cd78b24c911d7ee42c57ffd6d8bb942beb1cde143f', '864aaa39b3f1420afc4ade6e1fe36f7d1c27bbae1bc62d88aadd1ed222970df2', '922a175d1d44040cb4b17c40dc3f10de6fe19bbae46728f24a669b3c1f01663a', '947d6facd84d9ace2a86c585382899a7860c278c3486538d57aad864acdea9d5', '9a4b34748ed87c5f80d925de9bd27eae25ab149ea79a3b133a693c35bb52efb6', '9b6c74a954f1b17f2d9218067cb49f5dc2267ddef27952611512d24b70859602', '9d29f95dbb9b9e09385b6cbd62e6fcc473cb7ea04b11136163b3397023066966', 'a671e7be44fe9a932f8af92614131283bd0f45205459e1ee098525b44aed1b2b', 'a8a3389f3ca1b39a090f5e2a26f96810146b0e2b7a5f0258555eccbf1c3fad02', 'ae385f547d0b22bdc231a6b189a6c6f7c33c983529320e02ed8ce9efd8ab6a55', 'b0aa9b9257fdcd4f64a62eedcda9f750cb2f2904704d29f1e208f191bdd7acda', 'b16476a3938003ab9ea442d91f8242ec0e36274ede82150229bc8d077e47dd33', 'b6205bf9b67e0adcf5c2b5640a2cd2f0299ca0e7f52faf882b5aa5ab63a9d153', 'ba68629b7cb2f0d03e95d4c6754f05fab198205186d3e1373e77a42c80291f37', 'bea2cd3bc8676d1ae9186982bcdd4a8ec3805665d4df595b6f3dfd23e37eed77', 'bf0c9288f4cbc3582bf18d735945c6d04db2ef23284738807268195dfb2a7e63', 'bf78de27d204264f8155651173cd2ce2dfbfd18ece0a15ee96c4ddf32f9f0122', 'c0ff10d8b2b3c9ebeb71946ec5d8020654fcc264b3b80f35f9e3b0c3b427e693', 'c45da09c63b2b9f6fda4912dd17b78d52afb7e9b68a2a6048b34943a84830ba0', 'c56cb0e97903699eb5bf17b044a40cad379aec86b79c64eedf03477a163b3e01', 'c962ec6e28910b39d91ccaf1daccd3e3b83288a5fc30cc3b4aba726897f35cce', 'cd0ae80ef5f182e9dd73d66e14d30c9ab889cb44f95b0ddd6bc6b6197ae86bf0', 'd2610868879db347cdde85c5b91cb1b13b24f656fe6d990266414d41866ddf1f', 'd52945532d9ff85420d25cd66453d4d0fcfc45bae2c3c276192e82153194abb8', 'd9c1960ddb4c2cfacf69090349a96145e980dcd71a190131f0dc420396aa758a', 'd9d48c960e0b2db441a51238dc5dcf01446ca02f3a8fdd2f4d2c29996b6b8e44', 'da6da2a0cf6bc6df6c1996d5120c01469ba2660a4cff628cb778beef6204ab9f', 'dc1cd8ff0937504876220eae24bbdda4f8c83627172aba412be847eefdf3a673', 'de366a8a4fd3f5ad3538739a8b070a43e8d2c752d4174804b5f80ec1388f1330', 'eb69ccf908b2a22428067829369083ff1449d9ece5d59fd7feec283ef518f375', 'ef8c1eb2c620899706ae5528af36e2fc4fb3f785d10262293c04b0843b992c7a', 'f3e3460d3e133dbcdeccbd751252bcc8040fda63e54115a712e3b6bb0c672185', 'f3f2fa7f45cab4e17c410c4275b4bebbb99f1aa73422845b381fd8cfe0cd6b2b', 'f9006eb3146105de093633f5e4e0fd7b545a35559d64ddc0aa95b94a93883162'],
    'TITLE_OR_LINK_LABEL': ['01d036a6bd1e01c2c8f593b3916c2e74fda4794cce58cd37aecac67dc4b38cb3', '4d512decc7d5e4ba2f1005873ae93f6e998b32cf248c6c712f20e32d33f734c7', '64bc2bf3df3495ccab4536ad7da468b456ea7e1e8d6ddfe9ec2812dc0b2859d4', 'b3689a8ba926caeb3c4849c79b6c9db952c6cc84e27824e1ae94a6c13febdf6e', 'c5e3e7cdff66f7066e570e78d2a4605a97ac87c66a0156ee964fb4e1eb655370', 'dc0bcbf8fb34a30922b2557e4390002fb81f7776cdd0c0fc747887a6ae2a059c'],
}
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_sha(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[`*_#>\[\](){}]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def long_sentences(text: str, minimum: int = 120) -> set[str]:
    return {s.strip() for s in re.split(r"(?<=[.!?])\s+", normalize(text)) if len(s.strip()) >= minimum}


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def section_ranges(text: str) -> list[tuple[int, int, str]]:
    headings = [(m.start(), m.group(1)) for m in re.finditer(r'^##\s+[^\n]*\{#([^}]+)\}\s*$', text, flags=re.M)]
    ranges: list[tuple[int, int, str]] = []
    if headings and headings[0][0] > 0:
        ranges.append((0, headings[0][0], "frontmatter-or-introduction"))
    for idx, (start, section_id) in enumerate(headings):
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(text)
        ranges.append((start, end, section_id))
    return ranges


def section_for(ranges: list[tuple[int, int, str]], pos: int) -> tuple[str, str]:
    for start, end, section_id in ranges:
        if start <= pos < end:
            return section_id, product_text[start:end]
    return "frontmatter-or-introduction", product_text


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_file = product_root / PRODUCT_PATH
require(product_root.is_dir(), "exact Product checkout missing")
for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable Research blob drift: {path.relative_to(ROOT)}")
require(product_file.is_file(), "I.1 Product source missing")
if product_file.is_file():
    require(blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "I.1 Product blob drift")
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
require(sha(product_text) == PRODUCT_SHA, "I.1 Product SHA drift")

builder = import_builder()
full_scan = builder.scan_owner(builder.p(str(PRODUCT_PATH), "historical full I.1 owner"), product_root) if builder is not None else {}
reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "I.1 assembled reader"), product_root) if builder is not None else {}
require(len(full_scan.get("scriptureReferences", [])) == 142, "I.1 Product reference count drift")
require(full_scan.get("inlineQuotationSegments") == 98, "I.1 Product quotation count drift")
require(full_scan.get("markdownBlockquotes") == 0 and full_scan.get("htmlBlockquotes") == 0, "I.1 unexpected Product blockquote surfaces")
require(full_scan.get("externalLinks") == [], "I.1 Product external links introduced")
require(full_scan.get("internalArticleLinks") == EXPECTED_LINKS, "I.1 Product internal-link set drift")
require(canonical_sha(sorted(full_scan.get("scriptureReferences", []))) == REFERENCE_SET_SHA, "I.1 Product reference-set hash drift")

ranges = section_ranges(product_text)
surfaces: list[dict[str, Any]] = []
for match in re.finditer(r"«([^»\n]{8,})»", product_text):
    text = match.group(1)
    section_id, scoped = section_for(ranges, match.start())
    local_pos = match.start() - product_text.find(scoped) if scoped in product_text else 0
    refs: set[str] = set()
    if builder is not None:
        before = scoped[max(0, local_pos - 900):local_pos]
        after = scoped[local_pos:min(len(scoped), local_pos + len(match.group(0)) + 900)]
        for chunk in (before, after):
            refs.update(builder.normalize_ref(m.group(0)) for m in builder.SCRIPTURE_RE.finditer(chunk))
    surfaces.append({
        "type": "RUSSIAN_GUILLEMETS",
        "sectionId": section_id,
        "sha256": sha(normalize(text)),
        "characters": len(text),
        "nearbyScriptureReferences": sorted(refs, key=str.casefold),
    })
require(len(surfaces) == 98, "I.1 quotation extraction drift")
manifest = sorted(surfaces, key=lambda row: (row["sectionId"], row["sha256"], row["characters"], row["nearbyScriptureReferences"]))
require(canonical_sha(manifest) == MANIFEST_SHA, "I.1 quotation manifest hash drift")
all_hashes = [row["sha256"] for row in surfaces]
require(len(all_hashes) == 98 and len(set(all_hashes)) == 97, "I.1 expected one duplicate quotation occurrence")
flat_classes = [h for values in CLASS_HASHES.values() for h in values]
require(len(flat_classes) == 97 and len(set(flat_classes)) == 97, "I.1 class taxonomy must cover 97 unique hashes exactly once")
require(set(flat_classes) == set(all_hashes), "I.1 class taxonomy does not cover all Product quotation hashes")
class_counts = {name: sum(1 for h in all_hashes if h in set(values)) for name, values in sorted(CLASS_HASHES.items())}
require(class_counts == {'EDITORIAL_OR_COLLOQUIAL': 18, 'LEXICAL_OR_TRANSLATION': 5, 'SCRIPTURE_DIRECT_RUSSIAN_SYNODAL': 69, 'TITLE_OR_LINK_LABEL': 6}, "I.1 quotation class count drift")
section_summary: dict[str, dict[str, int]] = {}
for row in surfaces:
    bucket = section_summary.setdefault(row["sectionId"], {"surfaces": 0, "withNearbyScripture": 0})
    bucket["surfaces"] += 1
    bucket["withNearbyScripture"] += int(bool(row["nearbyScriptureReferences"]))
require(section_summary == EXPECTED_SECTION_SUMMARY, "I.1 section/proximity summary drift")
for marker in ("**Перевод Писания:** Синодальный", "## Источники", "Неточность заметили?"):
    require(marker in product_text, f"I.1 Product source marker missing: {marker}")
for target in EXPECTED_TARGETS:
    require((product_root / target).is_file(), f"I.1 Product internal target missing: {target}")

require(len(reader_scan.get("scriptureReferences", [])) == 20, "I.1 reader reference count drift")
require(canonical_sha(sorted(reader_scan.get("scriptureReferences", []))) == READER_REFERENCE_SET_SHA, "I.1 reader reference set drift")
for key in ("externalLinks", "internalArticleLinks"):
    require(reader_scan.get(key) == [], f"I.1 reader {key} must remain absent")
for key in ("footnoteDefinitions", "markdownBlockquotes", "htmlBlockquotes", "inlineQuotationSegments"):
    require(reader_scan.get(key) == 0, f"I.1 reader {key} must remain zero")
for match in re.finditer(r"«([^»\n]{8,})»", product_text):
    require(normalize(match.group(1)) not in normalize(reader_text), "I.1 reader copies a Product quotation surface")
require(long_sentences(product_text).isdisjoint(long_sentences(reader_text)), "I.1 reader contains a long exact Product sentence")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-I1-READER-ASSEMBLY-2026-08-04", "I.1 assembly authority drift")
require(assembly.get("reader", {}).get("gitBlob") == BLOBS[READER], "I.1 assembly reader blob drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 6, "I.1 assembly citation baseline drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 7, "I.1 assembly reader count drift")
current = read_json(CURRENT_V3)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04", "current V3 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 6, "current V3 citation count drift")
require("HEART-BOOK-I1" in current.get("openEntryIds", []), "I.1 absent from historical open set")
triage = read_json(TRIAGE)
rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I1"]
require(len(rows) == 1, "historical I.1 triage row missing")
if rows:
    require(rows[0].get("detected") == {"ownerSurfaces":1,"sourceHeadings":0,"scriptureReferences":142,"externalLinks":0,"internalArticleLinks":4,"quotationSurfaces":98}, "historical I.1 row drift")
    require(rows[0].get("disposition", {}).get("entryCitationPassComplete") is False, "historical triage was rewritten")

receipt = read_json(RECEIPT)
require(receipt.get("authorityId") == "HEART-I1-CITATION-REVIEW-2026-08-04", "I.1 citation receipt authority drift")
full = receipt.get("fullOwnerReview", {})
require(full.get("scriptureReferenceSetSha256") == REFERENCE_SET_SHA, "I.1 receipt reference hash drift")
require(full.get("quotationSurfaceManifestSha256") == MANIFEST_SHA, "I.1 receipt manifest hash drift")
require(full.get("surfaceClassHashSets") == {name: sorted(values) for name, values in sorted(CLASS_HASHES.items())}, "I.1 receipt class hash-set drift")
require(full.get("quotationClassCounts") == class_counts, "I.1 receipt class count drift")
require(full.get("internalArticleLinks") == EXPECTED_LINKS and full.get("internalTargetFiles") == EXPECTED_TARGETS, "I.1 receipt target disposition drift")
require(receipt.get("readerReview", {}).get("scriptureReferences") == 20, "I.1 receipt reader count drift")
require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.1 receipt direct quote boundary drift")
require(receipt.get("effectiveCounts") == {"finalBookEntries":18,"assembledReader":7,"missingStandaloneFinalReaders":11,"entryCitationPassComplete":7,"entryCitationPassOpen":11,"assembledReaderCitationReviewsComplete":7,"productSourceOnly":5,"researchDossierOnly":6,"newDirectQuotesApproved":0}, "I.1 receipt effective count drift")
boundary = receipt.get("publicationBoundary", {})
require(boundary.get("i1EntryCitationPassComplete") is True and boundary.get("allCurrentlyAssembledReadersCitationReviewed") is True, "I.1 completion boundary drift")
for key in ("wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete"):
    require(boundary.get(key) is False, f"I.1 falsely closes {key}")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I1-CITATION-REVIEW-2026-08-04", "I.1 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 7 / 18", "ASSEMBLED READER CITATION REVIEWS = 7 / 7",
    "PRODUCT SCRIPTURE REFERENCES GOVERNED = 142 / 142", "PRODUCT QUOTATION SURFACES CLASSIFIED = 98 / 98",
    "SCRIPTURE DIRECT / RUSSIAN SYNODAL = 69", "EDITORIAL / COLLOQUIAL = 18",
    "LEXICAL / TRANSLATION = 5", "TITLE / LINK LABEL = 6", "INTERNAL TARGETS RESOLVED = 4 / 4",
    "READER SCRIPTURE LOCATORS = 20", "READER QUOTATION / LINK SURFACES = 0",
    "NEW DIRECT QUOTES APPROVED = 0", MANIFEST_SHA, BLOBS[READER], PRODUCT_BLOB,
):
    require(marker in human, f"I.1 human authority marker missing: {marker}")
for forbidden in ("WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE","98 DIRECT QUOTES APPROVED","TODO","TBD"):
    require(forbidden not in human, f"I.1 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.1 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart I.1 entry citation pass: PASS — 142 references, 98 surfaces (69 Scripture / 18 editorial / 5 lexical / 6 titles), 4 internal targets, reader 20/0/0, whole-book 7/18")
