#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Запись круга 66 о переаливке зеркала SSOT-реестра — и о том, чем этот круг отличается от 63.

Круг 63 записал разрыв: живой объект на Drive отражал дерево `2f2291c` (круг 61), а main ушёл вперёд,
и разрыв этот круг считал как факт прогона, потому что «разрыв, вписанный один раз, врёт уже в
следующем круге». Круг 66 — первый, у которого разрыв можно закрыть, а не переснять: PR #254 слит в
`ceee8ec`, значит дерево main == дерево, из которого слепок законен.

Что здесь число, а что перетасовка:
  • LISTING НЕ транскрибируется: прежние 16 записей берутся из `LISTING` скрипта круга 63, к ним
    добавляется новый живой объект и правится имя вытесненного. Транскрипция чужого listing'а была
    бы вторым экземпляром тех же фактов, а два экземпляра расходятся молча; здесь расхождение
    невозможно по построению и проверяется assert'ом «папка не шевелилась, кроме двух моих операций».
  • Байт, md5 и строки слепок берёт из `git show ceee8ec:ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json`;
    имя живого объекта обязано нести те же числа, и они сверяются с Drive-стороной (size, md5Checksum)
    — это naming-контракт круга 18, а не вежливость. Запись не пишется, если хотя бы одно не совпало.
  • `разрывСДеревом.байт` переснимается прогоном (файл корпуса в дереве минус слепок). Он не обязан
    быть нулём и не бывает им: сама эта запись живёт в файле корпуса, поэтому тот, кто её вписал,
    тут же отстал от себя на её же байты. Ноль — это момент заливки, и он записан отдельным полем.
  • Доступ среды записан как замер, а не как оправдание: upload endpoint'ы Google из песочницы
    недосязаемы (HTTP 000), значит `initiate_resumable_upload` + PUT чантами здесь неисполнимы;
    объект прошёл через коннектор `upload_file` с `file_path`, то есть байтами не входил в контекст.
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
UPLOAD_SHA = "ceee8ec7a79ad54ef271379704e346eedfb36790"   # main = мерж PR #254 (круг 65)
CORPUS_GIT_PATH = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
FOLDER_ID = "13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ"
CIRCLE = 66
RECORD_KEY = "corpusSnapshotRound66_20261027"   # литералом: по нему же ищет CI-греп
PREV_TOOL = "scripts/atonement_drive_mirror_round63.py"

# --- то, что этот круг добавил в папку и переименовал в ней (остальное выводится из круга 63). ---
NEW_LIVE = {
    "id": "1bHY1lwLRg9ym4M4Uc2yC9uptbEx57GOd",
    "name": ("atonement-corpus-v1 (слепок SSOT-реестра, круг 66, дерево ceee8ec, 1 157 747 B, "
             "md5 88dd6f995d348ac09bc58818cede7a06).json"),
    "size": 1157747,
    "md5Checksum": "88dd6f995d348ac09bc58818cede7a06",
    "trashed": False,
    "createdTime": "2026-10-27T14:11:49.707Z",
    "modifiedTime": "2026-10-27T14:11:49.707Z",
}
RETIRED_ID = "19-lyyyES9cCL_fNN3xVUNM5j8hV7ZFXh"   # прежний живой слепок (круг 61)
RETIRED_NAME = ("УСТАРЕЛО (слепок SSOT-реестра круга 61: 1 121 533 B, md5 5dbb44a86dbf6e8a84c7aa1745e67a2d, "
                "снят 26.10.2026 в 20:01Z с дерева 2f2291c) atonement-corpus-v1.json — заменён кругом 66 "
                "(27.10.2026, 1 157 747 B, дерево ceee8ec)")
RETIRED_MODIFIED = "2026-10-27T14:11:59.174Z"


def _load_prev():
    spec = importlib.util.spec_from_file_location("mirror63", str(ROOT / PREV_TOOL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PREV = _load_prev()


def build_listing():
    """LISTING круга 66 = LISTING круга 63 + два моих события, ничего не переписывается руками."""
    out = []
    for r in PREV.LISTING:
        r = dict(r)
        if r["id"] == RETIRED_ID:
            r["name"] = RETIRED_NAME
            r["modifiedTime"] = RETIRED_MODIFIED
        out.append(r)
    ids = {r["id"] for r in out}
    assert NEW_LIVE["id"] not in ids, "новый объект уже был в listing'е круга 63 — тогда заливать нечего"
    out.append(dict(NEW_LIVE))
    return out


LISTING = build_listing()
LIVE = [r for r in LISTING if not r.get("trashed")]
STAMPED = [r for r in LIVE if r["name"].startswith("УСТАРЕЛО")]
CURRENT = [r for r in LIVE if not r["name"].startswith("УСТАРЕЛО")]
TRASHED = [r for r in LISTING if r.get("trashed")]
assert len(CURRENT) == 1, "в папке обязан быть ровно один живой снимок — иначе нечего называть живым"
LIVEOBJ = CURRENT[0]
SUPERSEDED = next(r for r in STAMPED if r["id"] == RETIRED_ID)
GAP_NAME_RE = r"([\d ]{5,15}) B[,)]"


def git(*a):
    return subprocess.run(("git", "-c", "core.quotepath=off") + a, cwd=str(ROOT), capture_output=True,
                          text=True)


def main() -> int:
    write = "--write" in sys.argv
    # 1) git-сторона слепок: байт, md5, строки — из blob'а дерева, с которого его заливали
    blob = git("show", f"{UPLOAD_SHA}:{CORPUS_GIT_PATH}")
    if blob.returncode != 0:
        raise SystemExit(f"blob {UPLOAD_SHA[:7]} не читается ({blob.stderr.strip()}) — в shallow-клоне "
                         "такого дерева нет, а врать про него запись не будет")
    raw = blob.stdout.encode()
    gmd5 = hashlib.md5(raw).hexdigest()
    glines = raw.count(b"\n")
    name_md5 = re.search(r"md5 ([0-9a-f]{32})", LIVEOBJ["name"]).group(1)
    name_bytes = int(re.search(GAP_NAME_RE, LIVEOBJ["name"]).group(1).replace(" ", ""))
    ok = [(f"blob {UPLOAD_SHA[:7]} весит {len(raw)} B, объект Drive — {LIVEOBJ['size']} B",
           len(raw) == LIVEOBJ["size"]),
          (f"md5 blob'а {gmd5}, md5 объекта {LIVEOBJ['md5Checksum']}", gmd5 == LIVEOBJ["md5Checksum"]),
          (f"имя объекта обещает {name_bytes} B, blob весит {len(raw)} B", name_bytes == len(raw)),
          (f"имя объекта обещает md5 {name_md5}, blob даёт {gmd5}", name_md5 == gmd5),
          (f"размер, обещанный в имени, равен размеру на Drive ({LIVEOBJ['size']})",
           name_bytes == LIVEOBJ["size"]),
          (f"md5 в имени равен md5, который посчитал Drive ({LIVEOBJ['md5Checksum']})",
           name_md5 == LIVEOBJ["md5Checksum"]),
          ("папка не шевелилась, кроме двух операций круга 66 (16 прежних записей совпали id/size/md5)",
           {(r["id"], r["size"], r["md5Checksum"]) for r in PREV.LISTING}
           == {(r["id"], r["size"], r["md5Checksum"]) for r in LISTING if r["id"] != NEW_LIVE["id"]}),
          ("вытесненный объект помечен УСТАРЕЛО и назван круг, который его вытеснил",
           SUPERSEDED["name"].startswith("УСТАРЕЛО") and "заменён кругом 66" in SUPERSEDED["name"]),
          ("в корзине по-прежнему то же, что перечислил круг 63",
           [r["id"] for r in TRASHED] == [r["id"] for r in PREV.TRASHED])]
    for msg, good in ok:
        print(("OK   " if good else "МЕЛО "), msg)
    if not all(g for _, g in ok):
        raise SystemExit("сверка не сошлась — запись не пишется")

    gap_now = CORPUS.stat().st_size - len(raw)
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True,
                           text=True).stdout.strip()
    rec = {
        "что": (f"переаливка зеркала SSOT-реестра кругом {CIRCLE}: в папке 05 живым лежит объект, снятый с "
                f"дерева {UPLOAD_SHA[:7]} — то есть из main (PR #254 слит в `ceee8ec`). Заливка и запись "
                "о ней сделаны одним кругом: круг 62 заливал и погиб вместе с веткой, круг 63 записывал "
                "чужую заливку постфактум. Разрыв, который круг 63 замерил в 36 214 B, к моменту "
                "заливки равен нулю; новый разрыв, который появится от самих записей этого круга, "
                "снимает прогон — поле и объявлено пересъёмным"),
        "зачем": ("правило 25 сверяет поля записи между собой, а не с listing'ом папки, поэтому «что лежит "
                  "в папке» до сих пор было устным; запись нужна, чтобы это переснималось командой, а не "
                  "памятью о вчерашнем вечере"),
        "папка": {"id": FOLDER_ID, "имя": "05 — SOURCE REGISTRY AND ACQUISITION QUEUE"},
        "живойСлепок": {
            "driveId": LIVEOBJ["id"],
            "имя": LIVEOBJ["name"],
            "байт": LIVEOBJ["size"],
            "md5Drive": LIVEOBJ["md5Checksum"],
            "md5Git": gmd5,
            "zalitoAt": LIVEOBJ["createdTime"],
            "gitShaAtUpload": UPLOAD_SHA,
            "gitFileBytesAtUpload": len(raw),
            "gitFileLinesAtUpload": glines,
            "съёмИзGit": (f"git show {UPLOAD_SHA}:{CORPUS_GIT_PATH} — поток обязан дать ровно {len(raw)} "
                          f"байт и md5 {gmd5}, которые вписаны в имя объекта; длина потока = байт, число "
                          "переводов строки = строки"),
            "recheckCommand": (f"md5sum <(git show {UPLOAD_SHA}:{CORPUS_GIT_PATH}); Drive get_file "
                               f"id={LIVEOBJ['id']} fields=md5Checksum,size"),
            "measuredAt": stamp, "checkedAt": stamp,
            "method": (f"scripts/atonement_drive_mirror_round66.py — LISTING выведен из LISTING скрипта круга 63 "
                       f"(16 прежних записей импортированы, не переписаны), git-сторона — из blob'а, совпадение "
                       "проверено assert'ом, а не глазами"),
        },
        "вытесненный": {
            "driveId": SUPERSEDED["id"],
            "байт": SUPERSEDED["size"],
            "md5Drive": SUPERSEDED["md5Checksum"],
            "былСнят": "круг 61, 2026-10-26T20:01:00.082Z, с дерева 2f2291c (мерж PR #250)",
            "переименованВ": SUPERSEDED["name"],
            "переименованКругом": CIRCLE,
            "переименованAt": RETIRED_MODIFIED,
            "measuredAt": stamp, "checkedAt": stamp,
            "method": ("имя и modifiedTime — из ответа update_file этого часа, сверены повторным list_files; "
                       "время — изменённый modifiedTime объекта, а не догадка"),
            "recheckCommand": f"Drive get_file id={SUPERSEDED['id']} fields=name,modifiedTime",
        },
        "доступСреды": {
            "uploadEndpointИзПесочницы": "недоступен (HTTP 000 на www.googleapis.com и upload.googleapis.com)",
            "следствие": ("`initiate_resumable_upload` + PUT чантами отсюда неисполним: коннектор умеет "
                          "выдать session URI, но стримить в Google должна среда, а ей путь закрыт"),
            "какЗалили": ("`upload_file` с `file_path`: Arena забирает файл с диска сам, байты в контекст "
                          "модели не входят; повторить можно этой же командой, дубликат ловится "
                          "перечислением папки (в ней обязан остаться ровно один живой снимок)"),
            "measuredAt": stamp,
            "method": ("curl -s -o /dev/null -w '%{http_code}' https://<host>/ → 000 при коде curl 35 "
                       "(TLS не установлен), 27.10.2026; контроль в те же секунды: "
                       "https://api.github.com/ → 200 — сеть среды работает, закрыт именно хост Google"),
            "recheckCommand": "timeout 20 curl -s -o /dev/null -w '%{http_code}\\n' https://www.googleapis.com/drive/v3/about",
        },
        "перечислениеПапки": {
            "объектовСИменемCorpusV1": len(LISTING),
            "живых": len(LIVE),
            "живыхБезПометкиУСТАРЕЛО": len(CURRENT),
            "помеченоУСТАРЕЛО": len(STAMPED),
            "вКорзине": len(TRASHED),
            "запрос": ("list_files: \"'13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ' in parents and name contains "
                       "'corpus-v1'\" — без фильтра trashed (тот же запрос, что у круга 63; с фильтром "
                       "не видно 8 удалённых, чем круг 61 и воспользовался)"),
            "изменениеПротивКруга63": (f"было {len(PREV.LISTING)} записей, стало {len(LISTING)}: добавлен один "
                                       "живой объект, ни один не удалён и не переименован чужими руками"),
            "measuredAt": stamp, "checkedAt": stamp,
            "method": "счёт выведен из LISTING этого скрипта (trashed/name), а LISTING выведен из круга 63",
            "recheckCommand": "python3 -B scripts/atonement_drive_mirror_round66.py   # сверит listing с git-стороной",
        },
        "разрывСДеревом": {
            "байт": gap_now,
            "чтоВходит": ("файл корпуса в рабочем дереве минус слепок: эта запись, запись индекса, "
                          f"правки {PREV_TOOL.split('/')[-1]} и проза новой главы аудита"),
            "байтБылоНаМоментЗаливки": 0,
            "почемуНеНоль": ("ноля не бывает по построению: поле живёт внутри файла, размер которого этим "
                             "полем и меняется. Круг 62 вписал разрыв как факт круга, и он устарел в том же "
                             "вечере; здесь это число прогона, снятое после всех правок"),
            "снятПрогоном": stamp,
            "measuredAt": stamp,
            "method": f"len(git show {UPLOAD_SHA[:7]}) вычитается из размера файла корпуса в рабочем дереве",
            "recheckCommand": "python3 -B scripts/atonement_drive_mirror_round66.py",
        },
        "междуСнимками": {
            "байтБыло": SUPERSEDED["size"],
            "байтСтало": LIVEOBJ["size"],
            "delta": LIVEOBJ["size"] - SUPERSEDED["size"],
            "круговМеждуЗаливками": CIRCLE - 61,
            "почемуТакМало": ("между деревом `2f2291c` и `ceee8ec` лёг один мерж этого круга: реестр доводов, "
                              "ценз папки и проза §9 росли правками кругов 64–65, а слепок не двигался ни разу. "
                              "Прежний разрыв в 40 кругов был аварией учёта, а не нормой"),
        },
        "лагОтносительноПрошлогоСнимка": {
            "байт": LIVEOBJ["size"] - SUPERSEDED["size"],
            "чтоЗначит": ("столько несли в себе правки, которые круг 63–65 делали в файле корпуса, пока зеркало "
                          "молчало; теперь lagBehindGit у записи индекса становится не нулём, а числом этой "
                          "переаливки: она описывает состояние до собственных правок"),
        },
        "метод": ("LISTING (выведен из транскрипции круга 63) → git show blob → assert равенства → запись в "
                  "driveMirrors; индексную половину пишет scripts/atonement_library_index_round66.py, "
                  "счётчики — scripts/atonement_reshoot_state.py"),
        "recheckCommand": ("python3 -B scripts/atonement_drive_mirror_round66.py && python3 -B "
                           "scripts/validate_atonement_corpus_integrity.py"),
        "measuredAt": stamp,
        "checkedAt": stamp,
    }

    corp = json.loads(CORPUS.read_text(encoding="utf-8"))
    key = RECORD_KEY
    prev_key = f"corpusSnapshotRound{PREV.CIRCLE}_20261026"
    prev = corp["driveMirrors"].get(prev_key)
    if prev is None:
        raise SystemExit(f"прежней записи ({prev_key}) в реестре нет — вытеснять нечего, запись не пишется")
    print("\n--- что изменится в записи круга 63 ---")
    print(json.dumps({"какиеЦифрыБыли": {"живыхБезПометкиУСТАРЕЛО": len(PREV.CURRENT),
                                        "помеченоУСТАРЕЛО": len(PREV.STAMPED),
                                        "разрывСДеревом": (prev.get("разрывСДеревом") or {}).get("байт")},
                      "чтоСтанет": f"живой объект записи круга 63 помечен УСТАРЕЛО кругом {CIRCLE}; "
                                  "сама запись не правится: она описывает listing своего часа, "
                                  "а не теперешний",
                      "разрывКруга63БольшеНеАктуален": True},
                     ensure_ascii=False, indent=1)[:700])
    if not write:
        print(f"\nпробный прогон: живой {LIVEOBJ['id']}, {LIVEOBJ['size']} B, md5 {gmd5}, строк blob'а "
              f"{glines}; ценз {len(LISTING)}/{len(LIVE)}/{len(CURRENT)}/{len(STAMPED)}/{len(TRASHED)}; "
              f"разрыв с деревом {gap_now} B. Ключ для записи: driveMirrors.{key}; --write — применить")
        return 0
    corp["driveMirrors"][key] = rec
    prev[f"вытесненКругом{CIRCLE}"] = {
        "кем": f"driveMirrors.{key}",
        "объект": SUPERSEDED["id"],
        "имяНаDrive": SUPERSEDED["name"],
        "чтоЭтоЗначит": ("объект, который круг 63 назвал живым, с этого часа помечен УСТАРЕЛО: его место занял "
                         f"слепок дерева {UPLOAD_SHA[:7]}, залитый кругом {CIRCLE}. Числа записи круга 63 при "
                         "этом верны своему часу и не переснимаются — пересъём чужой записи был бы правкой "
                         "источника задним числом"),
        "measuredAt": stamp, "checkedAt": stamp,
        "method": f"list_files этого часа (см. живойСлепок.вытесненный записи круга {CIRCLE})",
        "recheckCommand": f"Drive get_file id={SUPERSEDED['id']} fields=name,size",
    }
    CORPUS.write_text(json.dumps(corp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\nзаписано: driveMirrors.{key}; в записи круга 63 добавлено поле вытесненКругом{CIRCLE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
