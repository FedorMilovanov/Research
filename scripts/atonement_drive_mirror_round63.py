#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Запись круга 63 о слепке SSOT-реестра в папке 05 — и исправление бухгалтерии круга 61.

Почему запись отдельная, а не правка прежней: живой объект на Drive появился в 20:01:00Z руками
круга 62, но тот круг погиб вместе с незапушенным коммитом (проверяется локально:
`git cat-file -t fe3928` → «Not a valid object name»; удалённая ветка прошлой сессии
после мержа #250 с remote снята, `git ls-remote origin | grep -i ba50183d` пусто — эта половина
утверждения не переснимается офлайн и помечена как та, что есть). Дерево main получило слепок
круга 60, а Drive — круга 61: Registry называл «живым» объект, который там уже переименован в
«УСТАРЕЛО». Правило 25 такое молчание не ловит: оно сверяет поля записи между собой, а не с
 listing'ом папки. Значит, разрыв обязан описать круг, который его нашёл.

Что здесь число, а что перетасовка:
  • LISTING ниже — транскрипция ответа `list_files` этого часа (запрос: родитель 05 и подстрока
    имени `corpus-v1`, БЕЗ фильтра trashed — с фильтром ответ тот же минус 8 удалённых). Из него
    всё считается: и «живой» объект, и ценз папки, и старое определение ценза.
  • Байт, md5 и число строк зеркала берутся не из имени объекта и не из памяти, а из `git show
    2f2291c:ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` — и запись не состоится, если они не равны
    тому, что вернул Drive (`assert` ниже). Это ровно та проверка, из-за которой круг 18 и придумал
    naming-контракт «имя несёт md5».
  • `разрывСДеревом.байт` переснимается в момент записи (файл в рабочем дереве минус слепок) и
    помечается `снятПрогоном`: круг 62 обнаружил, что разрыв, вписанный один раз, врёт уже в
    следующем круге; здесь он число этого прогона, а не этого круга.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "ИСКУПЛЕНИЕ" / "data" / "atonement-corpus-v1.json"
UPLOAD_SHA = "2f2291c48629c4fd2d0ce2727453a8cc08beada5"   # main на момент заливки (мерж PR #250)
CORPUS_GIT_PATH = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
LOST_SHA = "fe39288"   # полное имя живёт только здесь и в §9.3 документа: в JSON-листьях
                       # семибитный префикс был бы «мёртвой sha-ссылкой» правила 20, а у неё
                       # единственный выход — пересъём через git show, которого для утраченного объекта нет
FOLDER_ID = "13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ"
CIRCLE = 63

# --- ответ google_drive list_files, снят этим часом (26.10.2026, после 20:44Z по песочнице). -----
# Поля оставлены как в ответе коннектора: id, name, size, md5Checksum, trashed. Ничего не добавлено.
LISTING = [
    {"id": "19-lyyyES9cCL_fNN3xVUNM5j8hV7ZFXh",
     "name": "atonement-corpus-v1 (слепок SSOT-реестра, круг 61, 1 121 533 B, "
             "md5 5dbb44a86dbf6e8a84c7aa1745e67a2d).json",
     "size": 1121533, "md5Checksum": "5dbb44a86dbf6e8a84c7aa1745e67a2d", "trashed": False},
    {"id": "1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn",
     "name": "УСТАРЕЛО (слепок SSOT-реестра круга 60: 1 113 528 B, md5 c50c742a9e38126ec6b7a4055baa5f2f, "
             "снят 26.10.2026 в 19:18Z) atonement-corpus-v1.json — заменён кругом 61 (26.10.2026, "
             "1 121 533 B)",
     "size": 1113528, "md5Checksum": "c50c742a9e38126ec6b7a4055baa5f2f", "trashed": False},
    {"id": "1u7fZCOatKh_MeUOqek_b_r8hKiZMKrf2",
     "name": "УСТАРЕЛО (слепок SSOT-реестра круга 20: 305 429 B, md5 1af98460184d0a3d6f4085041150a13d, "
             "снят 23.10.2026 в 17:59Z) atonement-corpus-v1.json — заменён кругом 60 (26.10.2026, "
             "1 113 528 B)",
     "size": 305429, "md5Checksum": "1af98460184d0a3d6f4085041150a13d", "trashed": False},
    {"id": "1dIMlITxk66OCSDF8sJ3nmrg14KaZtl5L",
     "name": "УСТАРЕЛО (слепок SSOT-реестра круга 18: 291 683 B, md5 f609f4552d089725657a2fcdefaeb925, "
             "съём 17:13Z) atonement-corpus-v1.json — заменён кругом 20",
     "size": 291683, "md5Checksum": "f609f4552d089725657a2fcdefaeb925", "trashed": False},
    {"id": "1BCDawvokh7NtPcS2pH_jIRAYJ96KM21W",
     "name": "УСТАРЕЛО (слепок SSOT-реестра круга 17: 297 064 B, 13:06Z; заменён слепком круга 18 17:13Z) "
             "atonement-corpus-v1.json",
     "size": 297064, "md5Checksum": "06f413605ba5e8a579368fb4b7b9195a", "trashed": False},
    {"id": "1VMyeLoOTfw73jUeOlShG0e1LqsN_QETO",
     "name": "УСТАРЕЛО (снимок 12:42Z, 287 913 B; заменено 2026-10-23 в 13:00Z) atonement-corpus-v1.json",
     "size": 287913, "md5Checksum": "14aee149fa01b1fcb1945f1041bf8fc5", "trashed": False},
    {"id": "1jzzN8PB92OdKjYBEbsHpyc3aeB76GQEV",
     "name": "УСТАРЕЛО (снимок круга 16, 276 905 B; заменено 2026-10-23 кругом 17) atonement-corpus-v1.json",
     "size": 276905, "md5Checksum": "2fc46aab68ed281b2251655ec65504e7", "trashed": False},
    {"id": "1kvWangNcv9DQOPoMi1k2k3Ussjf_EXwx",
     "name": "УСТАРЕЛО (снимок 2026-10-09) atonement-corpus-v1.json — заменено 2026-10-23",
     "size": 53098, "md5Checksum": "f0ef4fae5557bc0a9ce1f51267cc0832", "trashed": False},
    {"id": "19FcQjvf2zuDIfw2uGnrXhutGw6iXAr6-", "name": "atonement-corpus-v1.json", "size": 21814,
     "md5Checksum": "cc38e2c4da81f2f41e1103f13613713f", "trashed": True},
    {"id": "1unOnvjV1arj7DB80adcweN2MsQBwPlUs", "name": "atonement-corpus-v1.json", "size": 21814,
     "md5Checksum": "e4dab5f1da725dea5cf014ac0ed08209", "trashed": True},
    {"id": "13t1sEg1Vqb00dskwvL4DJbxSbIs8PD6V", "name": "atonement-corpus-v1.json", "size": 15955,
     "md5Checksum": "408e80a63f0d9b4703be439c567cb697", "trashed": True},
    {"id": "1dykOLwLQy8_WVYWMXyH1J5Nl0t1_4SOk", "name": "atonement-corpus-v1.json", "size": 10857,
     "md5Checksum": "68143545e21194273512d6378197595e", "trashed": True},
    {"id": "1tlyPq75eSLn7qecSkLSa9LnBLQk1EBUz", "name": "atonement-corpus-v1.json", "size": 10857,
     "md5Checksum": "748405c49fe06d8f2ee16d5ef3b3b9d8", "trashed": True},
    {"id": "13Pz_VKqa7iWYrnDdWjhqEmyGWignqasa", "name": "atonement-corpus-v1.json", "size": 10857,
     "md5Checksum": "0357abe0ce0688e38de228ccceb126bd", "trashed": True},
    {"id": "1C_LZQBGMFJV05V0M8rC67_hTvcEgD0v6", "name": "atonement-corpus-v1.json", "size": 9993,
     "md5Checksum": "e8347171b7d6ee3d4346a8ecf0e983cf", "trashed": True},
    {"id": "1d-wZvmGbfnD7U7YnQ6rKQ4mVMhQF7UL-", "name": "atonement-corpus-v1.json", "size": 8847,
     "md5Checksum": "9d472a296446e2d405f34dd38b9e368a", "trashed": True},
]

LIVE = [r for r in LISTING if not r["trashed"]]
STAMPED = [r for r in LIVE if r["name"].startswith("УСТАРЕЛО")]
CURRENT = [r for r in LIVE if not r["name"].startswith("УСТАРЕЛО")]
TRASHED = [r for r in LISTING if r["trashed"]]
assert len(CURRENT) == 1, "в папке обязан быть ровно один живой снимок — иначе нечего называть живым"
LIVEOBJ = CURRENT[0]
SUPERSEDED = next(r for r in STAMPED if r["id"] == "1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn")


def git(*a):
    return subprocess.run(("git", "-c", "core.quotepath=off") + a, cwd=str(ROOT), capture_output=True,
                          text=True)


def main() -> int:
    write = "--write" in sys.argv
    # 1) git-сторона слепок: байт, md5, строки — из blob'а дерева, с которого его качали
    blob = git("show", f"{UPLOAD_SHA}:{CORPUS_GIT_PATH}")
    if blob.returncode != 0:
        raise SystemExit(f"blob {UPLOAD_SHA[:7]} не читается ({blob.stderr.strip()}) — в shallow-клоне "
                         "такого дерева нет, а врать про него запись не будет")
    raw = blob.stdout.encode()
    gmd5 = hashlib.md5(raw).hexdigest()
    glines = raw.count(b"\n")
    name_md5 = re.search(r"md5 ([0-9a-f]{32})", LIVEOBJ["name"]).group(1)
    name_bytes = int(re.search(r"([\d ]{5,15}) B[,)]", LIVEOBJ["name"]).group(1).replace(" ", ""))
    ok = [(f"blob {UPLOAD_SHA[:7]} весит {len(raw)} B, объект Drive — {LIVEOBJ['size']} B",
           len(raw) == LIVEOBJ["size"]),
          (f"md5 blob'а {gmd5}, md5 объекта {LIVEOBJ['md5Checksum']}", gmd5 == LIVEOBJ["md5Checksum"]),
          (f"имя объекта обещает {name_bytes} B, blob весит {len(raw)} B", name_bytes == len(raw)),
          (f"имя объекта обещает md5 {name_md5}, blob даёт {gmd5}", name_md5 == gmd5),
          ("утраченный коммит круга 62 так и не вернулся в дерево",
           git("cat-file", "-t", LOST_SHA).returncode != 0)]
    for msg, good in ok:
        print(("OK   " if good else "МЕЛО "), msg)
    if not all(g for _, g in ok):
        raise SystemExit("сверка не сошлась — запись не пишется")

    gap_now = CORPUS.stat().st_size - len(raw)
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True,
                           text=True).stdout.strip()
    rec = {
        "что": (f"переаливка зеркала SSOT-реестра кругом {CIRCLE}: в папке 05 живым лежит объект, снятый с "
                f"дерева {UPLOAD_SHA[:7]} (мерж PR #250, круг 61) и названный «круг 61» — по дереву, а не по "
                "кругу, который его описывает. Запись о нём ведёт круг 63, потому что заливал его круг 62, чей "
                "коммит в main не попал: он остался на ветке, снятой после мержа #250. Прежний живой снимок "
                "(круг 60, 1 113 528 B) переименован в «УСТАРЕЛО» и оставлен на месте — идентификаторы, "
                "опубликованные в записях, не отзываются"),
        "зачем": ("реестр называл живым объект, который на Drive уже был помечен устаревшим: правило 25 "
                  "сверяет поля записи между собой и расхождения с listing'ом папки не видит вовсе. Эта запись "
                  "нужна, чтобы проверка «что лежит в папке» стала пересъёмной, а не устной"),
        "папка": {"id": FOLDER_ID, "имя": "05 — SOURCE REGISTRY AND ACQUISITION QUEUE"},
        "живойСлепок": {
            "driveId": LIVEOBJ["id"],
            "имя": LIVEOBJ["name"],
            "байт": LIVEOBJ["size"],
            "md5Drive": LIVEOBJ["md5Checksum"],
            "md5Git": gmd5,
            "zalitoAt": "2026-10-26T20:01:00.082Z",
            "oписаниюОбъекта": "createdTime и size/md5 — из get_file и list_files этого часа; description "
                               "объекта круг 63 не перечитывал, поэтому о нём здесь ничего не сказано",
            "gitShaAtUpload": UPLOAD_SHA,
            "gitFileBytesAtUpload": len(raw),
            "gitFileLinesAtUpload": glines,
            "съёмИзGit": (f"git show {UPLOAD_SHA[:7]}:{CORPUS_GIT_PATH} — поток обязан дать ровно те {len(raw)} "
                          f"байт и md5 {gmd5}, что вписаны в имя объекта; длина потока = байт, число переводов "
                          "строки = строки"),
            "recheckCommand": (f"md5sum <(git show {UPLOAD_SHA}:{CORPUS_GIT_PATH}); Drive get_file "
                               f"id={LIVEOBJ['id']} fields=md5Checksum,size"),
            "measuredAt": stamp, "checkedAt": stamp,
            "method": ("scripts/atonement_drive_mirror_round63.py — LISTING, транскрипция list_files этого часа, "
                       "git-сторона — из blob'а, совпадение проверено assert'ом, а не глазами"),
        },
        "вытесненный": {
            "driveId": SUPERSEDED["id"],
            "байт": SUPERSEDED["size"],
            "md5Drive": SUPERSEDED["md5Checksum"],
            "былСнят": "круг 60, 2026-10-26T19:18Z (запись driveMirrors.corpusSnapshotRound61_20261026)",
            "переименованВ": SUPERSEDED["name"],
            "переименованКругом": 62,
            "переименованAt": "не измерено кругом 63: событие залило и подписало прошлое прогон-описание, "
                              "которое не дошло до main; время правки имени — modifiedTime объекта (20:01:25Z "
                              "по get_file круга 63)",
            "measuredAt": stamp,
            "method": "name и size/md5 — из того же list_files; время — modifiedTime из get_file этого часа",
            "recheckCommand": f"Drive get_file id={SUPERSEDED['id']} fields=name,modifiedTime",
        },
        "перечислениеПапки": {
            "объектовСИменемCorpusV1": len(LISTING),
            "живых": len(LIVE),
            "живыхБезПометкиУСТАРЕЛО": len(CURRENT),
            "помеченоУСТАРЕЛО": len(STAMPED),
            "вКорзине": len(TRASHED),
            "запрос": ("list_files: \"'13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ' in parents and name contains "
                       "'corpus-v1'\" — без фильтра trashed; фильтр trashed=false даёт те же 8 живых и "
                       "молчит про 8 удалённых, чем круг 61 и воспользовался"),
            "составКорзины": ("8 объектов с коротким именем atonement-corpus-v1.json, от 8 847 до 21 814 B — "
                              "ранние копии до круга 16; удалены не этим кругом, состав перечислен, а не "
                              "оценён"),
            "measuredAt": stamp, "checkedAt": stamp,
            "method": "счёт выведен из LISTING этого скрипта (trashed/name), а не вписан словами",
            "recheckCommand": ("python3 -B scripts/atonement_drive_mirror_round63.py   # сверит LISTING с "
                               "git-стороной; сам listing переснимается командой из поля запрос"),
        },
        "утраченныйПредшественник": {
            "коммит": LOST_SHA[:6] + "… (полный id не восстановим: объекта нет ни в одном.refs песочницы)",
            "чтоСталоСКоммитом": ("рабочая ветка круга 62 была запушена, но PR для неё не открыт; после мержа "
                                  "#250 доступ к ветке на remote закрылся, а при возобновлении сессии песочница "
                                  "вернулась глубины 1 без этого объекта — значит ни скрипты, ни записи круга 62 "
                                  "в канон не попали"),
            "какПроверено": ("git cat-file -t fe3928 → «fatal: Not a valid object name fe3928» (префикс "
                             "достаточный: git разрешает префиксы, а отсутствующий объект не разрешает ни в "
                             "какой длине); git ls-remote origin с фильтром по имени прошлой ветки → пусто "
                             "(вторая команда требует сети и в прогоне не повторяется)"),
            "recheckCommand": f"git cat-file -t {LOST_SHA[:6]}",
            "measuredAt": stamp,
            "method": "assert в этом скрипте: запись не пишется, если утраченный коммит внезапно нашёлся",
        },
        "lagBehindGit": ("имя снимка несёт байт и md5 дерева 2f2291c, то есть круга 61; разрыв — собственные "
                         "записи об этом слепке (запись в driveMirrors, запись индекса, переснятые счётчики) и "
                         "текст раздела 9.3 аудита. Это единственный вид отставания, который зеркалу разрешён"),
        "разрывСДеревом": {
            "байт": gap_now,
            "чтоВходит": ("файл корпуса в рабочем дереве минус слепок: эта запись, запись индекса, счётчики "
                          "из scripts/atonement_reshoot_state.py и проза §9.3"),
            "байтБылоНаМоментЗаливки": 0,
            "почемуЧислоПересъёмное": ("круг 62 вписал разрыв как факт круга, и он тут же устарел на байты "
                                       "собственной правки; здесь это поле переснимает каждый прогон скрипта, и "
                                       "значение принадлежит прогону, а не кругу"),
            "снятПрогоном": stamp,
            "measuredAt": stamp,
            "method": "len(git show <upload-sha>) вычитается из размера файла корпуса в рабочем дереве",
            "recheckCommand": "python3 -B scripts/atonement_drive_mirror_round63.py",
        },
        "междуСнимками": {
            "кругов": 1,
            "байтБыло": SUPERSEDED["size"],
            "байтСтало": LIVEOBJ["size"],
            "delta": LIVEOBJ["size"] - SUPERSEDED["size"],
            "почемуТакМало": ("между кругом 60 и кругом 61 лёг один мерж: реестр доводов, ценз индекса и "
                              "раздел 9.2; между кругом 61 и этим слепком — только записи, которые не успели "
                              "в канон. Прежний разрыв в 40 кругов был аварией учёта, а не нормой"),
        },
        "метод": ("LISTING (транскрипция list_files этого часа) → git show blob → assert равенства → "
                  "запись в driveMirrors; индексную половину записывает scripts/atonement_library_index_round63.py, "
                  "счётчики — scripts/atonement_reshoot_state.py"),
        "recheckCommand": ("python3 -B scripts/atonement_drive_mirror_round63.py && python3 -B "
                           "scripts/validate_atonement_corpus_integrity.py"),
        "measuredAt": stamp,
        "checkedAt": stamp,
    }

    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    prev = corp["driveMirrors"]["corpusSnapshotRound61_20261026"]
    print("\n--- что изменится в записи круга 61 ---")
    correction = {
        "какиеЦифрыБыли": dict(prev.get("перечислениеПапки") or {}),
        "чтоЗначилНоль": ("поле «корзин: 0» было снято запросом с trashed=false и не могло увидеть корзину: "
                          "в папке 8 удалённых объектов с тем же именем. Формулировка круга 61 не врала про "
                          "выборку, но читалась как «корзина пуста» — поэтому поле переименовано"),
        "какНазваноТеперь": "`корзинВВыборкеTrashedFalse`, плюс `корзинПолноеПеречисление` с числом этого часа",
        "measuredAt": stamp, "checkedAt": stamp,
        "method": "тот же LISTING скрипта круга 63",
        "recheckCommand": "python3 -B scripts/atonement_drive_mirror_round63.py",
    }
    print(json.dumps(correction, ensure_ascii=False, indent=1)[:600])
    if not write:
        print(f"\nпробный прогон: живой {LIVEOBJ['id']}, {LIVEOBJ['size']} B, md5 {gmd5}, строк blob'а "
              f"{glines}; ценз {len(LISTING)}/{len(LIVE)}/{len(CURRENT)}/{len(STAMPED)}/{len(TRASHED)}; "
              f"разрыв с деревом {gap_now} B. Ключи для записи: "
              f"driveMirrors.corpusSnapshotRound{CIRCLE}_20261026; --write — применить")
        return 0
    corp["driveMirrors"][f"corpusSnapshotRound{CIRCLE}_20261026"] = rec
    prev["перечислениеПапки"] = {
        "объектовСИменемCorpusV1": (prev.get("перечислениеПапки") or {}).get("объектовСИменемCorpusV1"),
        "живых": (prev.get("перечислениеПапки") or {}).get("живых"),
        "помеченоУСТАРЕЛО": (prev.get("перечислениеПапки") or {}).get("помеченоУСТАРЕЛО"),
        "корзинВВыборкеTrashedFalse": 0,
        "корзинПолноеПеречисление": len(TRASHED),
        "пометкаКруга63": correction,
    }
    prev["вытесненКругом63"] = {
        "кем": f"driveMirrors.corpusSnapshotRound{CIRCLE}_20261026",
        "объект": SUPERSEDED["id"],
        "имяНаDrive": SUPERSEDED["name"],
        "measuredAt": stamp, "checkedAt": stamp,
        "method": "list_files этого часа (см. живойСлепок.вытесненный того же круга)",
        "recheckCommand": "Drive get_file id=1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn fields=name,size",
        "чтоЭтоЗначит": ("объект, который круг 61 назвал живым, больше не жив: его место занял снимок, "
                         "залитый кругом 62 и записанный только сейчас"),
    }
    CORPUS.write_text(json.dumps(corp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\nзаписано: driveMirrors.corpusSnapshotRound{CIRCLE}_20261026; поправка в "
          "corpusSnapshotRound61_20261026.перечислениеПапки")
    return 0


if __name__ == "__main__":
    sys.exit(main())
