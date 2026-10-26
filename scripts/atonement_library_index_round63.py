#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Индекс библиотеки, круг 63: живой снимок получает свою строку, прежний — уходит в HOLD.

Ровно та процедура, что круг 61 завёл и круг 62 повторить не успел: слепок реестра в папке 05
с этой пары записей — строка индекса, и правило 25 считает его вместе с носителями цитат, а не
отдельным сужением «зеркало есть».

Записи не сочиняются: `bytes`, `md5` и имя берутся из `LISTING` скрипта
`atonement_drive_mirror_round63.py` (тот транскрибирован из ответа `list_files` этого часа),
`gitBytesAtUpload` / `gitMd5AtUpload` / `gitFileLinesAtUpload` — из `git show <upload-sha>`,
а сверка «закачанное равно дереву» — assert'ом. Без этого строка индекса была бы пересказом
имени файла, а имя файла написала та же рука, что его качала.

Отстаивание прежней записи — не только слово в `note`: `rights` обязан смениться с
`mirror_of_git` на `HOLD_superseded`, потому что имя объекта на Drive теперь начинается с
«УСТАРЕЛО», и поле `name` записи тоже обязано стать этим именем — правило 25 сверяет md5 и байт
из имени с полями записи, и запись, оставшаяся с прежним именем, осталась бы честной для
прошлого круга и молчаливой для настоящего.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-corpus-v1.json"
INDEX = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-library-index.json"
CORPUS_GIT_PATH = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
CIRCLE = "63"
PREV_DRIVE_ID = "1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn"


def _load_mirror():
    """LISTING и git-сторона — из соседнего скрипта, чтобы листинг папки не был переписан вручную."""
    spec = importlib.util.spec_from_file_location(
        "m63", ROOT / "scripts" / "atonement_drive_mirror_round63.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["m63"] = m
    spec.loader.exec_module(m)          # __main__-защита там есть, прогон непишущий
    return m


def git(*a):
    return subprocess.run(("git", "-c", "core.quotepath=off") + a, cwd=str(ROOT), capture_output=True,
                          text=True)


def main() -> int:
    write = "--write" in sys.argv
    m = _load_mirror()
    live, sup = m.LIVEOBJ, m.SUPERSEDED
    blob = git("show", f"{m.UPLOAD_SHA}:{CORPUS_GIT_PATH}")
    if blob.returncode != 0:
        raise SystemExit(f"blob {m.UPLOAD_SHA[:7]} не читается: в этом клоне такого дерева нет, а "
                         "строку индекса «на веру» круг 61 уже запретил писать")
    raw = blob.stdout.encode()
    gmd5 = hashlib.md5(raw).hexdigest()
    glines = raw.count(b"\n")
    assert len(raw) == live["size"] and gmd5 == live["md5Checksum"], " Drive ≠ git — запись не пишется"
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True,
                           text=True).stdout.strip()
    how = (f"scripts/atonement_library_index_round{CIRCLE}.py — LISTING скрипта "
           f"scripts/atonement_drive_mirror_round{CIRCLE}.py плюс git show {m.UPLOAD_SHA[:7]} "
           f"того же пути, равенство проверено assert'ом")
    rec = {
        "schema": "2026-10-26-drive-mirror-v1",
        "folder": "05",
        "driveId": live["id"],
        "kind": "file",
        "mime": "application/json",
        "bytes": live["size"],
        "name": live["name"],
        "gitFile": CORPUS_GIT_PATH,
        "role": "ssot-corpus-snapshot",
        "rights": "mirror_of_git",
        "readState": "registry_linked",
        "driveBytesClaimed": int(re.search(r"([\d ]{5,15}) B[,)]", live["name"]).group(1).replace(" ", "")),
        "driveMd5Claimed": re.search(r"md5 ([0-9a-f]{32})", live["name"]).group(1),
        "driveBytesVerified": live["size"],
        "driveMd5Verified": live["md5Checksum"],
        "gitBytesAtUpload": len(raw),
        "gitFileLinesAtUpload": glines,
        "gitMd5AtUpload": gmd5,
        "gitShaAtUpload": m.UPLOAD_SHA,
        "md5VerifiedFromDrive": True,
        "вытеснённыйОбъект": sup["id"],
        "съёмИзGit": (f"git show {m.UPLOAD_SHA[:7]}:{CORPUS_GIT_PATH} | md5sum — обязано дать md5, "
                      "вписанный в имя объекта; длина того же потока даёт bytes, число переводов строки — "
                      "gitFileLinesAtUpload"),
        "uploadedAt": "2026-10-26T20:01:00.082Z",
        "measuredAt": stamp,
        "checkedAt": stamp,
        "lagBehindGit": True,
        "lagОбъяснение": ("слепок снят с дерева круга 61; эта строка индекса и запись driveMirrors о нём "
                          "появились позже, поэтому md5 имени с md5 дерева разойдётся ровно на них — "
                          "правило 25 требует объявить это, а не подогнать число"),
        "почемуЭтоВажно": ("без строки индекса слепок не входит ни в один ценз: круг 20 лежал в папке 40 "
                           "кругов, и заметил это человек, перечитавший listing. Теперь это запись, у которой "
                           "есть права, состояние чтения и проверяемое имя"),
        "описаниеКруга63": ("заливал этот объект круг 62, чей коммит не дошёл до main (утрачен вместе с "
                            "рабочей веткой); запись ведёт круг 63, числа сняты заново этим часом, а не "
                            "унаследованы из потерянного прогона"),
        "aboutRows": [],
        "citedBy": [],
        "queueRows": [],
        "locator": "папка 05_SERIES_AND_REGISTRY, имя объекта несёт md5 дерева на момент заливки",
        "note": ("слепок SSOT-реестра, а не зеркало построчного реестра: bytes/md5 сняты с объекта "
                 f"get_file и сверены с деревом коммита {m.UPLOAD_SHA[:7]}; отстаёт на собственные записи — "
                 "lagBehindGit"),
    }
    retire = {
        "name": sup["name"],
        "rights": "HOLD_superseded",
        "supersededBy20261026r" + CIRCLE: {
            "driveId": live["id"],
            "кемЗаменёнВРеестре": f"driveMirrors.corpusSnapshotRound{CIRCLE}_20261026",
            "measuredAt": stamp, "checkedAt": stamp,
            "method": how,
            "recheckCommand": f"Drive get_file id={sup['id']} fields=name,trashed,md5Checksum",
            "почемуНеУдалён": ("идентификаторы опубликованы в записях круга 61 и в комментариях PR; "
                               "переименование оставляет ссылку живой и честной, удаление — нет"),
        },
        "noteRetired20261026r" + CIRCLE: ("объект на Drive переименован в «УСТАРЕЛО … заменён кругом 61» "
                                          "прогоном круга 62; права сняты с mirror_of_git, потому что байт и "
                                          "md5 этого объекта больше не равны дереву — они равны дереву круга 60"),
        "bytes": sup["size"],
        "driveMd5Verified": sup["md5Checksum"],
        "measuredAt": stamp,
        "checkedAt": stamp,
        "methodRetirement": ("name/bytes/md5 — из LISTING этого часа (транскрибирован в "
                             f"scripts/atonement_drive_mirror_round{CIRCLE}.py), не из памяти о круге 62"),
        "recheckCommand": f"Drive get_file id={sup['id']} fields=name,size,md5Checksum",
    }
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    prev = [r for r in idx["records"] if r.get("driveId") == PREV_DRIVE_ID]
    assert len(prev) == 1, f"прежняя запись о слепке должна быть одна, их {len(prev)}"
    before = {"записей": len(idx["records"]),
              "mirror_of_git": sum(1 for r in idx["records"] if r.get("rights") == "mirror_of_git"),
              "HOLD_superseded": sum(1 for r in idx["records"] if r.get("rights") == "HOLD_superseded"),
              "registry_linked": sum(1 for r in idx["records"] if r.get("readState") == "registry_linked")}
    print("ценз до:", json.dumps(before, ensure_ascii=False))
    print(f"новая запись: {live['id']}, {live['size']} B, md5 {gmd5}, строк дерева {glines}")
    if not write:
        print("пробный прогон — --write применит"); return 0
    prev[0].update(retire)
    idx["records"].append(rec)
    after = {"записей": len(idx["records"]),
             "mirror_of_git": sum(1 for r in idx["records"] if r.get("rights") == "mirror_of_git"),
             "HOLD_superseded": sum(1 for r in idx["records"] if r.get("rights") == "HOLD_superseded"),
             "registry_linked": sum(1 for r in idx["records"] if r.get("readState") == "registry_linked")}
    print("ценз после:", json.dumps(after, ensure_ascii=False))
    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    corp["libraryIndex20261023"][f"countsNote20261026r{CIRCLE}"] = (
        f"Круг {CIRCLE}: в индексе появился живой снимок реестра, а прежний перестал быть зеркалом дерева "
        f"(права mirror_of_git → HOLD_superseded, имя — то, что теперь лежит на Drive). Записей {before['записей']} "
        f"→ {after['записей']}, mirror_of_git {before['mirror_of_git']} → {after['mirror_of_git']} (прибыла одна, "
        f"ушла одна: счёт не льстят), HOLD_superseded {before['HOLD_superseded']} → {after['HOLD_superseded']}, "
        f"registry_linked {before['registry_linked']} → {after['registry_linked']}. Остальной ценз (файлы, байты, "
        "носители материала) переснят scripts/atonement_reshoot_state.py обходом правила 25, а не здесь."
    )
    corp["libraryIndex20261023"][f"методЗаписиР63"] = {
        "ктоПишет": f"scripts/atonement_library_index_round{CIRCLE}.py",
        "чтоПроверяетПрогон": ("assert равенства git-show и LISTING; без него строка индекса была бы "
                               "пересказом имени файла"),
        "measuredAt": stamp,
        "recheckCommand": f"python3 -B scripts/atonement_library_index_round{CIRCLE}.py",
        "метод": how,
    }
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    CORPUS.write_text(json.dumps(corp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("записано: индекс + countsNote в реестре")
    return 0


if __name__ == "__main__":
    sys.exit(main())
