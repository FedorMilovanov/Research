#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Индекс библиотеки, круг 66: новый снимок получает свою строку, снимок круга 61 уходит в HOLD.

Та же процедура, что круг 63 восстановил после погибшего круга 62, только выверенная в одну деталь:
числа берутся не из транскрипции, а из соседнего скрипта круга 66, который сам выводит свой LISTING
из транскрипции круга 63. Строка индекса, переписанная руками с экрана, была бы вторым экземпляром
фактов о папке, а два экземпляра расходятся молча.

`rights` прежней записи обязан смениться с `mirror_of_git` на `HOLD_superseded`, потому что имя её
объекта на Drive теперь начинается с «УСТАРЕЛО», и `name` записи обязан стать этим новым именем:
правило 25 сверяет md5 и байт из имени с полями записи, а запись со старым именем осталась бы честной
для прошлого круга и молчаливой для настоящего.

Отдельно о `lagBehindGit` — единственное поле, в котором круг 66 не может написать «нет». В момент
заливки слепок был равен дереву с байта до байта (это и сверяет assert ниже), но файл, которому он
должен быть равен, изменился сразу после заливки: в него вписана сама эта запись. Ноль в момент
прогона и ненулевой разрыв в коммите — не расхождение учёта, а свойство зеркала, которое отражает
файл, описывающий зеркало.
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
CIRCLE = "66"
PREV_DRIVE_ID = "19-lyyyES9cCL_fNN3xVUNM5j8hV7ZFXh"
MIRROR_TOOL = "atonement_drive_mirror_round66.py"


def _load_mirror():
    spec = importlib.util.spec_from_file_location("m66", ROOT / "scripts" / MIRROR_TOOL)
    m = importlib.util.module_from_spec(spec)
    sys.modules["m66"] = m
    spec.loader.exec_module(m)          # __main__-защита есть, прогон непишущий
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
    assert len(raw) == live["size"] and gmd5 == live["md5Checksum"], "Drive ≠ git — запись не пишется"
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True,
                           text=True).stdout.strip()
    how = (f"scripts/atonement_library_index_round{CIRCLE}.py — LISTING скрипта scripts/{MIRROR_TOOL} "
           f"(тот выводит его из транскрипции круга 63) плюс git show {m.UPLOAD_SHA[:7]} того же пути, "
           "равенство проверено assert'ом")
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
        "uploadedAt": live["createdTime"],
        "measuredAt": stamp,
        "checkedAt": stamp,
        "lagBehindGit": True,
        "lagОбъяснение": ("в момент заливки разрыв был нулём (assert выше и есть та сверка), но нулём он "
                           "остаться не может: в файл, которому обязан равняться слепок, тут же вписаны эта "
                           "запись, запись driveMirrors и проза главы 10 аудита. Число переснимает прогон "
                           "scripts/atonement_drive_mirror_round66.py, а не это поле"),
        "почемуЭтоВажно": ("без строки индекса слепок не входит ни в один ценз; с этой строкой он носитель, "
                           "у которого есть права, состояние чтения и проверяемое имя — ровно то, чего не "
                           "хватило в круге 62, где заливать успели, а учесть — нет"),
        "описаниеКруга66": (f"заливку и запись сделал один и тот же круг {CIRCLE}: у кругов 62 (залил, "
                            "погиб вместе с веткой) и 63 (записал чужую заливку) эти две половины "
                            "разъехались по кругам. Дерево-источник — main на момент заливки "
                            f"({m.UPLOAD_SHA[:7]}, мерж PR #254), разрыв в момент заливки 0 B"),
        "aboutRows": [],
        "citedBy": [],
        "queueRows": [],
        "locator": "папка 05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE, имя объекта несёт байт и md5 дерева на момент заливки",
        "note": ("слепок SSOT-реестра, а не зеркало построчного реестра: bytes/md5 сняты с объекта list_files "
                 f"и сверены с деревом коммита {m.UPLOAD_SHA[:7]}; отстаёт на собственные записи — lagBehindGit"),
    }
    retire = {
        "name": sup["name"],
        "rights": "HOLD_superseded",
        "supersededBy20261027r" + CIRCLE: {
            "driveId": live["id"],
            "кемЗаменёнВРеестре": f"driveMirrors.corpusSnapshotRound{CIRCLE}_20261027",
            "measuredAt": stamp, "checkedAt": stamp,
            "method": how,
            "recheckCommand": f"Drive get_file id={sup['id']} fields=name,trashed,md5Checksum",
            "почемуНеУдалён": ("идентификаторы опубликованы в записях driveMirrors и в комментариях PR #254; "
                               "переименование оставляет ссылку живой и честной, удаление — нет"),
        },
        "noteRetired20261027r" + CIRCLE: ("объект на Drive переименован в «УСТАРЕЛО … заменён кругом 66» "
                                          f"прогоном круга {CIRCLE} в {live['modifiedTime'][:19]}Z; права сняты "
                                          "с mirror_of_git, потому что его байт и md5 равны дереву круга 61, а "
                                          "не нынешнему — ровно та формулировка, из-за которой круг 63 и "
                                          "завёл это поле"),
        "bytes": sup["size"],
        "driveMd5Verified": sup["md5Checksum"],
        "measuredAt": stamp,
        "checkedAt": stamp,
        "methodRetirement": ("name/bytes/md5 — из LISTING скрипта "
                             f"scripts/{MIRROR_TOOL}, выведенного из транскрипции круга 63, а не из памяти"),
        "recheckCommand": f"Drive get_file id={sup['id']} fields=name,size,md5Checksum",
    }
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    prev = [r for r in idx["records"] if r.get("driveId") == PREV_DRIVE_ID]
    assert len(prev) == 1, f"прежняя запись о слепке должна быть одна, их {len(prev)}"
    already = [r for r in idx["records"] if r.get("driveId") == live["id"]]
    note_key = f"countsNote20261027r{CIRCLE}"
    note_present = note_key in (json.loads(CORPUS.read_text(encoding="utf-8"))
                                .get("libraryIndex20261023") or {})
    if already:
        # Повторный прогон — не повод падать и не повод заводить дубль: строка либо уже есть и
        # числами совпадает с тем, что даёт дерево сейчас, либо прошлый прогон записал другие
        # числа — это называется словами, а не пересъёмом переписывается.
        assert len(already) == 1, f"строк об этом объекте {len(already)} — двойной учёт носителя"
        a = already[0]
        for fld, want in (("bytes", live["size"]), ("driveMd5Verified", live["md5Checksum"]),
                          ("gitShaAtUpload", m.UPLOAD_SHA), ("gitMd5AtUpload", gmd5),
                          ("gitBytesAtUpload", len(raw))):
            assert a.get(fld) == want, (
                f"строка уже в индексе, но {fld} = {a.get(fld)!r} ≠ {want!r} — прошлый прогон записал "
                "другие числа; чинить руками, а не пересъёмом молча")
        if not note_present:
            if write:
                raise SystemExit(
                    "строка индекса уже есть, а счётчика countsNote нет — прошлый прогон оборвался "
                    "между двумя записями. Догадочное «before» здесь недопустимо: восстановите файл "
                    "из git и запустите заново")
            print("строка уже записана, счётчика нет — и пробный прогон, и --write останавливаются: "
                  "полузапись чинится из git, а не догадкой")
            return 0
        print("уже записано: строка и счётчик на месте, повторный прогон ничего не меняет")
        return 0

    def census(rows):
        return {"записей": len(rows),
                "mirror_of_git": sum(1 for r in rows if r.get("rights") == "mirror_of_git"),
                "HOLD_superseded": sum(1 for r in rows if r.get("rights") == "HOLD_superseded"),
                "registry_linked": sum(1 for r in rows if r.get("readState") == "registry_linked")}

    before = census(idx["records"])
    print("ценз до:", json.dumps(before, ensure_ascii=False))
    print(f"новая запись: {live['id']}, {live['size']} B, md5 {gmd5}, строк дерева {glines}")
    if not write:
        print("пробный прогон — --write применит")
        return 0
    prev[0].update(retire)
    idx["records"].append(rec)
    after = census(idx["records"])
    print("ценз после:", json.dumps(after, ensure_ascii=False))
    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    corp["libraryIndex20261023"][f"countsNote20261027r{CIRCLE}"] = (
        f"Круг {CIRCLE}: слепок реестра переалит, и в индексе это две строки — новая с правами mirror_of_git "
        f"и прежняя, у которой права сняты на HOLD_superseded (имя — то, что теперь лежит на Drive). Записей "
        f"{before['записей']} → {after['записей']}, mirror_of_git {before['mirror_of_git']} → "
        f"{after['mirror_of_git']} (прибыла одна, ушла одна: счёт не льстят), HOLD_superseded "
        f"{before['HOLD_superseded']} → {after['HOLD_superseded']}, registry_linked {before['registry_linked']} "
        f"→ {after['registry_linked']}. Остальной ценз (файлы, байты, носители материала) переснят "
        "scripts/atonement_reshoot_state.py обходом правила 25, а не здесь."
    )
    corp["libraryIndex20261023"][f"методЗаписиР{CIRCLE}"] = {
        "ктоПишет": f"scripts/atonement_library_index_round{CIRCLE}.py",
        "чтоПроверяетПрогон": ("assert равенства git-show и LISTING + assert отсутствия строки об этом "
                               "объекте в индексе (второй прогон не должен заводить дубль)"),
        "measuredAt": stamp,
        "recheckCommand": f"python3 -B scripts/atonement_library_index_round{CIRCLE}.py",
        "метод": how,
    }
    CORPUS.write_text(json.dumps(corp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"записано: строка индекса о {live['id']}, вытеснение {PREV_DRIVE_ID}, "
          f"countsNote20261027r{CIRCLE} в реестре")
    return 0


if __name__ == "__main__":
    sys.exit(main())
