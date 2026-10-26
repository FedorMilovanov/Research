#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Реестр доводов отдела «Искупление»: съём, сверка, пересъём.

Зачем этот файл существует. До круга 59 проверяемым и пересъёмным был только учёт
цитат: в главном реестре 493 датированных поля, а в четырёх содержательных под-ланах —
ноль (поле stampedFieldsPerRegistry). Спросить «сколько доводов закрыто» было не к чему,
и вердикт по объёму оставался открытым не от нехватки текстов, а от нехватки счётчика.

Что считается доводом. Раздел прозы уровня «## » — ровно тот блок, которым под-ланы уже
записывают свои утверждения (## AF-1. Климент, ## 2. Что не доказано, ## 6.3. Классы
для критики). Новой прозы этот круг не пишет: реестр обязан пересказать написанное и
отвечать за каждую строку локатором, который проверяется побайтово.

Откуда берётся класс. Не из заголовка и не из моей головы, а из маркеров внутри самой
секции: вердикт — это код в обратных кавычках (`EVIDENCE_HOLD`, `RESOLVED-BY-TEXT`).
Множества маркеров объявлены ниже, и словарь обязан покрывать весь измеренный словарь:
маркер, которому нет места в классах, — ошибка съёма, а не «прочее».

Приоритет осторожный: удержание > открыто > закрыто. Секция, где есть и закрытие, и HOLD,
идёт в удержание — так реестр физически не может слушать в пользу ланы.

Команды:
  --vocab          печать измеренного словаря маркеров с их классами
  --print [лан]    сводка по строкам, без записи
  --check [лан]    переснять и сравнить с записанным; код 1 при любом расхождении
  --write [лан]    записать блок в реестр лана (тогда, когда расхождение есть)

Ланы: root (ИСКУПЛЕНИЕ/*.md), ot, nt, fathers, synthesis; по умолчанию — все пять.
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "ИСКУПЛЕНИЕ"
MAIN_REGISTRY = CORPUS_DIR / "data" / "atonement-corpus-v1.json"
SUBLANES = ("ot", "nt", "fathers", "synthesis")
BLOCK_KEY = "claimRegister20261026"

TOKEN_RE = re.compile(r"`([A-Z][A-Z0-9 _./+-]{3,40})`")
HEADING_RE = re.compile(r"^## +(.+?)\s*$")
CODE_RE = re.compile(r"^([A-Z]{1,4}-\d+[a-z]?|\d+(?:[.\-]\d+)*[a-z]?)\.?\s")
STATUS_LINE_RE = re.compile(r"Статус|\*\*Status|\bverdict|\bВердикт|ВЫВОД|Итог")
SINGLE_WORD_VERDICTS = {
    "HOLD", "OPEN", "BLOCKED", "RESOLVED", "VERIFIED", "FORBIDDEN", "PASS", "PD", "READABLE", "ELIGIBLE",
}
# Форма маркера: не «любая капитель в кавычках», а disposition-вид: два и более
# алфавитных куска по две буквы и больше. Так из словаря сами выпадают шифры
# строк реестра (FP-160, C-24, L12113, GAP-B1), которые к вердиктам отношения не
# имеют, и счётчик не превращается в подсчёт всего капитального в отделе.
def is_marker_shape(tok: str) -> bool:
    parts = re.split(r"[ _./+-]+", tok.strip())
    return len(parts) >= 2 and all(re.fullmatch(r"[A-Z]{2,}", x) for x in parts)


HOLD_RE = re.compile(
    r"HOLD|BLOCKED|TENSION|RISK|UNAVAILABLE|UNKNOWN|UNCLEAR|PARTIAL|SECONDARY|FORBIDDEN|RESTRICTED|FALSE"
    r"|LAG|DISPUTED|QUOTE|PRIVATE_STUDY|SINGLE_ATTESTATION|NOT PUBLICATION|NOT PRODUCT"
)
OPEN_RE = re.compile(
    r"OPEN|PENDING|MISSING|TODO|NOT_YET|UNRESOLVED|SECOND_PASS|REQUEST|INTERRUPTED|ERROR|SCOPED_IN"
)
CLOSED_RE = re.compile(
    r"RESOLVED|VERIFIED|LOCATED|READABLE|READ$|ELIGIBLE|AVAILABLE|ACQUIRED|TRANSCRIBED|COLLATED|CONFIRMED"
    r"|NOT_IN_COPYRIGHT|FULL|SCOPED_OUT"
)

# Классификация обязана объяснять каждый маркер, но «объяснить» не значит «навесить
# вердикт»: служебные записи (PRIMARY TEXT, AGENT_RULES, README_FALLBACK) — не о том,
# закрыт ли довод. Они не тонут в «прочем», а стоят в блоке списком, который сверяется
# с обходом: новый жаргон обязан быть назван, иначе съём падает.
SERVICE_TOKENS = {
    "PRIMARY TEXT", "AGENT_RULES", "PRODUCT_REPO", "BIBLE_CORPUS", "README_FALLBACK", "FETCH_HEAD",
    "ATTRIBUTION_NOTE", "AUDIT / RECONCILIATION", "SECOND HEAD OF DOCTRINE", "PASS", "LICENSE",
    "MIRROR", "SSOT", "TODO", "LINK_ONLY", "STORAGE_ONLY", "LEGACY_NO_CLASSES", "PRECEDENT_OF_READING",
    "TEXT_CRIT_NOTE", "SUPERSEDED-BY-MIRROR", "OT-AUTH", "NT_CORPUS_HOME",
}
# Разошлось с первою версией списка намеренно: `CONTEXT_HOLD` — это удержание, а не
# служба, и оно попадает в HOLD_RE раньше, чем успевает быть названным здесь. Порядок
# проверок (сначала вердиктные множества, потом служебные) и есть контракт: в «службу»
# не ссылают то, что можно прочесть как удержание.
BUCKET_PRECEDENCE = ("УДЕРЖИВАЕТСЯ", "ОТКРЫТО", "ЗАКРЫТО", "СЛУЖЕБНОЕ")


def classify_token(tok: str) -> str:
    if HOLD_RE.search(tok):
        return "УДЕРЖИВАЕТСЯ"
    if OPEN_RE.search(tok):
        return "ОТКРЫТО"
    if CLOSED_RE.search(tok):
        return "ЗАКРЫТО"
    return "СЛУЖЕБНОЕ" if tok in SERVICE_TOKENS else "НЕ ОТНЕСЁН"


def row_class(buckets: list[str]) -> str:
    if not buckets:
        return "БЕЗ МАРКЕРА"
    for bucket in BUCKET_PRECEDENCE:
        if bucket in buckets:
            return bucket
    return "НЕ ОТНЕСЁН"


def files_for(lan: str) -> list[Path]:
    """Проза лана = все его .md, включая вложенные папки: черновики читательских статей в
    synthesis/drafts и заметки инструментов в ot/tools говорят ровно то же, что и
    карточки, и оставлять их вне счёта значило бы мерить лан по удобной ему части."""
    if lan == "root":
        return sorted(CORPUS_DIR.glob("*.md"))
    return sorted((CORPUS_DIR / lan).rglob("*.md"))


def registry_for(lan: str) -> Path:
    return MAIN_REGISTRY if lan == "root" else CORPUS_DIR / lan / "data" / f"{lan}-corpus-v1.json"


def machine_ids(lan: str) -> set[str]:
    """Идентификаторы, которые лан уже ведёт машинно: карточки, молчания, заявки.

    Нужно не для красоты, а чтобы учёт прозы и учёт данных нельзя было развести
    незаметно: покрытость измеряется обходом, а не заявляется словами.
    """
    path = registry_for(lan)
    out: set[str] = set()
    if not path.is_file():
        return out
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — нечитаемый реестр ловит гейт, здесь не дублируем
        return out
    id_shape = re.compile(r"^[A-Z]{1,4}-\d+[a-z]?$")

    def walk(node) -> None:
        if isinstance(node, dict):
            for val in node.values():
                if isinstance(val, str) and id_shape.match(val.strip()):
                    out.add(val.strip())
                walk(val)
        elif isinstance(node, list):
            for val in node:
                walk(val)

    walk(data)
    return out


def tokens_in(text: str) -> list[str]:
    """Маркеры секции: по форме, а одиночные капительные слова — только там, где проза
    сама называет их статусом (строка со «Статус:», «ВЫВОД», «verdict»)."""
    out: list[str] = []
    for line in text.splitlines():
        for tok in TOKEN_RE.findall(line):
            tok = tok.strip()
            if is_marker_shape(tok) or (tok in SINGLE_WORD_VERDICTS and STATUS_LINE_RE.search(line)):
                out.append(tok)
    return out


def scan_lan(lan: str) -> dict:
    """Строки и агрегаты одного лана. Детерминированно: обход по сортировке путей,
    внутри файла — по номеру строки. Никакой выборки: берётся весь ствол лана."""
    ids = machine_ids(lan)
    rows: list[dict] = []
    tokens_total: collections.Counter = collections.Counter()
    unmapped: collections.Counter = collections.Counter()
    per_file: collections.Counter = collections.Counter()
    seen: collections.Counter = collections.Counter()

    for path in files_for(lan):
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8").splitlines()
        starts = [(i, m.group(1)) for i, ln in enumerate(text, 1) if (m := HEADING_RE.match(ln))]
        for idx, (line, title) in enumerate(starts):
            end = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(text)
            body = "\n".join(text[line:end])
            buckets: list[str] = []
            for tok in tokens_in(body):
                tokens_total[tok] += 1
                bucket = classify_token(tok)
                if bucket == "НЕ ОТНЕСЁН":
                    unmapped[tok] += 1
                buckets.append(bucket)
            uniq = sorted(set(buckets))
            code_m = CODE_RE.match(title)
            base = f"{code_m.group(1) if code_m else 'СР'}@{path.stem}"
            seen[base] += 1
            code = base if seen[base] == 1 else f"{base}~{seen[base]}"
            rows.append(
                {
                    "код": code,
                    "лан": lan,
                    "файл": rel,
                    "строка": line,
                    "срез": title,
                    "класс": row_class(uniq),
                    "маркеров": len(uniq),
                    "машинно": code_m is not None and (code_m.group(1) in ids or base in ids),
                }
            )
            per_file[rel] += 1

    bad = resolve_rows(rows)
    classes = collections.Counter(r["класс"] for r in rows)
    return {
        "лан": lan,
        "rows": rows,
        "агрегаты": {
            "строк": len(rows),
            "файлов": len(per_file),
            "поКлассам": dict(sorted(classes.items(), key=lambda kv: (-kv[1], kv[0]))),
            "покрытоМашинно": sum(1 for r in rows if r["машинно"]),
            "разрешеноЛокаторов": len(rows) - len(bad),
            "неРазрешено": len(bad),
        },
        "маркеры": {
            "всего": sum(tokens_total.values()),
            "различных": len(tokens_total),
            "словарь": {t: classify_token(t) for t in sorted(tokens_total)},
            "частоты": dict(sorted(tokens_total.items(), key=lambda kv: (-kv[1], kv[0]))),
            "служебные": sorted(t for t in tokens_total if classify_token(t) == "СЛУЖЕБНОЕ"),
            "неОтнесено": dict(sorted(unmapped.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "плохо": bad,
    }


def resolve_rows(rows: list[dict]) -> list[str]:
    """Локатор обязан резолвиться: файл существует, и на названной строке лежит ровно
    тот срез, что записан. Непроверяемый локатор — украшение, а не ссылка."""
    bad: list[str] = []
    cache: dict[str, list[str] | None] = {}
    for row in rows:
        rel = row["файл"]
        if rel not in cache:
            path = ROOT / rel
            cache[rel] = path.read_text(encoding="utf-8").splitlines() if path.is_file() else None
        lines = cache[rel]
        if lines is None:
            bad.append(f"{row['код']}: файл не найден: {rel}")
        elif not (1 <= row["строка"] <= len(lines)):
            bad.append(f"{row['код']}: строки {row['строка']} нет в {rel}")
        elif lines[row["строка"] - 1].strip() != "## " + row["срез"].strip():
            bad.append(f"{row['код']}: срез не совпал со строкой {row['строка']} в {rel}")
    return bad


FIELDS_TO_MIRROR = ("строк", "файлов", "покрытоМашинно", "разрешеноЛокаторов", "неРазрешено")


def check_block(lan: str, fresh: dict) -> list[str]:
    """Сверка записанного блока с тем, что видит обход. Пустой список — значит сходится."""
    path = registry_for(lan)
    problems: list[str] = []
    if not path.is_file():
        return [f"{lan}: реестр {path.name} не найден"]
    block = json.loads(path.read_text(encoding="utf-8")).get(BLOCK_KEY)
    if not isinstance(block, dict):
        return [
            f"{lan}: в {path.name} нет блока {BLOCK_KEY} — счётчик доводов обязан быть записан, "
            "а не выводим из молчания"
        ]
    stored = block.get("строки") or []
    if len(stored) != fresh["агрегаты"]["строк"]:
        problems.append(
            f"{lan}: записано {len(stored)} строк, обход видит {fresh['агрегаты']['строк']} — "
            "проза изменилась, а реестр нет (или наоборот)"
        )
    by_code = {r["код"]: r for r in stored}
    fresh_codes = {r["код"] for r in fresh["rows"]}
    # Обратный ход обязателен: без него блоку достаточно «додать» строку и подвинуть
    # счётчик, и она будет жить в реестре, хотя в прозе её никогда не было. Сверка
    # в одну сторону — это учёт того, что удобно считать.
    for row in stored:
        if row.get("код") not in fresh_codes:
            problems.append(
                f"{lan}: строка {row.get('код')!r} есть в блоке, но обход прозы её не находит — "
                "локатор выдуман или устарел"
            )
    for line in resolve_rows(stored)[:4]:
        problems.append(f"{lan}: записанный локатор не разрешается — {line}")
    for row in fresh["rows"]:
        got = by_code.get(row["код"])
        if got is None:
            problems.append(f"{lan}: строки {row['код']} нет в записанном реестре")
            continue
        for field in ("файл", "строка", "срез", "класс", "маркеров", "машинно"):
            if got.get(field) != row[field]:
                problems.append(
                    f"{lan}: {row['код']}: поле «{field}» записано {got.get(field)!r}, обход даёт {row[field]!r}"
                )
    for field in FIELDS_TO_MIRROR:
        if block.get(field) != fresh["агрегаты"][field]:
            problems.append(
                f"{lan}: сводка «{field}» записана {block.get(field)!r}, обход даёт {fresh['агрегаты'][field]!r}"
            )
    if block.get("поКлассам") != fresh["агрегаты"]["поКлассам"]:
        problems.append(
            f"{lan}: распределение по классам разошлось: записано {block.get('поКлассам')!r}, "
            f"обход даёт {fresh['агрегаты']['поКлассам']!r}"
        )
    marks = block.get("маркеры") or {}
    for field in ("всего", "различных"):
        if marks.get(field) != fresh["маркеры"][field]:
            problems.append(
                f"{lan}: маркеров {field} записано {marks.get(field)!r}, обход видит {fresh['маркеры'][field]}"
            )
    if marks.get("служебные") != fresh["маркеры"]["служебные"]:
        problems.append(
            f"{lan}: список служебных маркеров разошёлся со съёмом: записано {marks.get('служебные')!r}, "
            f"обход даёт {fresh['маркеры']['служебные']!r}"
        )
    if marks.get("частоты") != fresh["маркеры"]["частоты"]:
        problems.append(f"{lan}: частоты маркеров разошлись со съёмом — переснимай блок целиком")
    if fresh["маркеры"]["неОтнесено"]:
        problems.append(
            f"{lan}: {len(fresh['маркеры']['неОтнесено'])} маркеров не отнесено ни к одному классу: "
            f"{list(fresh['маркеры']['неОтнесено'])[:6]} — классификация обязана объяснять каждый маркер"
        )
    for key in ("measuredAt", "checkedAt", "recheckCommand", "метод", "чтоСчитаетсяДоводом", "приоритет"):
        if not block.get(key):
            problems.append(f"{lan}: в блоке нет поля «{key}»")
    for line in fresh["плохо"][:6]:
        problems.append(f"{lan}: локатор не разрешается — {line}")
    return problems


def top_level_indent(raw: str) -> int:
    m = re.search(r"^([ ]+)\"", raw, re.M)
    return len(m.group(1)) if m else 1


def block_span(raw: str, key: str) -> tuple[int, int]:
    """Границы блока верхнего уровня вместе с запятой, которая к нему приклеена.
    Нужно, чтобы пересъём заменял блок, а не оставлял рядом второй: копия блока,
    которую круг 58 ловил в чужих записях (20 КБ duplicated-данных), начинается
    ровно с таких «вставил, а старое забыл снять» случаев."""
    i = raw.index(f'"{key}"')
    j = raw.index("{", i)
    depth, in_str, esc = 0, False, False
    for k in range(j, len(raw)):
        ch = raw[k]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                a, b = i, k + 1
                if raw[:i].rstrip().endswith(","):
                    a = raw.rfind(",", 0, i)  # запятая принадлежит предыдущему ключу
                elif raw[b:].lstrip().startswith(","):
                    b = raw.index(",", b) + 1
                return a, b
    raise SystemExit(f"блок {key} не закрыт — правь съёмщик, а не реестр")



def canonical_indent(raw: str) -> int | None:
    """Форма файла, в которой он записан: 1, 2 или 4 пробела, либо ничего. Съёмщик обязан
    возвращать реестр в той же форме, в какой взял: точечная вставка блока с собственным
    отступом оставляла бы в каноническом файле островок чужой вёрстки, и следующий дифф
    читался бы как порча данных, а не как добавление счёта."""
    try:
        data = json.loads(raw)
    except Exception:  # noqa: BLE001
        return None
    for ind in (1, 2, 4):
        if raw == json.dumps(data, ensure_ascii=False, indent=ind) + "\n":
            return ind
    return None


def insert_block(path: Path, block: dict) -> None:
    """Вставка без переформатирования реестра: остальной файл обязан остаться байт в
    байт — иначе сама правка сдвинет счётчики упоминаний, которые лана измеряет."""
    raw = path.read_text(encoding="utf-8")
    form = canonical_indent(raw)
    if f'"{BLOCK_KEY}"' in raw:
        a, b = block_span(raw, BLOCK_KEY)
        raw = raw[:a].rstrip() + "\n" + raw[b:].lstrip("\n")
    if form is not None:
        data_now = json.loads(raw)
        data_now[BLOCK_KEY] = block
        canon = json.dumps(data_now, ensure_ascii=False, indent=form) + "\n"
        probe = json.loads(canon)
        if probe[BLOCK_KEY] != json.loads(json.dumps(block, ensure_ascii=False)):
            raise SystemExit(f"{path.name}: каноническая форма исказила блок — правь съёмщик")
        for key in data_now:
            if key != BLOCK_KEY and json.dumps(probe[key], ensure_ascii=False, sort_keys=True) != json.dumps(
                data_now[key], ensure_ascii=False, sort_keys=True
            ):
                raise SystemExit(f"{path.name}: привидение к форме задело ключ {key!r}")
        path.write_text(canon, encoding="utf-8")
        return
    i = raw.rstrip().rfind("\n}")
    if i < 0:
        raise SystemExit(f"не нашёл закрывающую скобку верхнего уровня в {path.name}")
    width = top_level_indent(raw)
    pad = " " * width
    body = json.dumps(block, ensure_ascii=False, indent=width + 2)
    body = body.replace("\n", "\n" + pad)
    sep = "" if raw[:i].rstrip().endswith(",") else ","
    new = raw[:i] + sep + "\n" + pad + f'"{BLOCK_KEY}": ' + body + raw[i:]
    data = json.loads(new)
    if json.dumps(data[BLOCK_KEY], ensure_ascii=False, sort_keys=True) != json.dumps(
        block, ensure_ascii=False, sort_keys=True
    ):
        raise SystemExit(f"{path.name}: вставленный блок не равен исходному — правь вставку, не данные")
    before = json.loads(raw)
    for key in before:
        if key != BLOCK_KEY and json.dumps(before[key], ensure_ascii=False, sort_keys=True) != json.dumps(
            data[key], ensure_ascii=False, sort_keys=True
        ):
            raise SystemExit(f"{path.name}: вставка задела чужой ключ {key!r} — так нельзя")
    path.write_text(new, encoding="utf-8")


def build_block(lan: str, fresh: dict, previous: dict | None) -> dict:
    agg, marks = fresh["агрегаты"], fresh["маркеры"]
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "чтоЭто": f"реестр доводов лана «{lan}»: строка = раздел прозы уровня ## с локатором, "
        "классом из её собственных маркеров и отметкой съёма",
        "чтоСчитаетсяДоводом": "заголовок «## » в любом .md лана, включая вложенные папки "
        "(synthesis/drafts, ot/tools); тело секции — до следующего «## » или до конца файла",
        "приоритет": "УДЕРЖИВАЕТСЯ > ОТКРЫТО > ЗАКРЫТО; маркеров нет -> БЕЗ МАРКЕРА; маркер вне "
        "классификации -> ошибка съёма, а не «прочее»",
        "метод": "scripts/atonement_claim_register.py обходит прозу лана целиком (без выборки), "
        "разбирает маркеры вида `ВЕРДИКТ`, сверяет локатор побайтово (файл + номер строки + текст)",
        **{f: agg[f] for f in FIELDS_TO_MIRROR},
        "поКлассам": agg["поКлассам"],
        "маркеры": {
            "всего": marks["всего"],
            "различных": marks["различных"],
            "словарь": marks["словарь"],
            "частоты": marks["частоты"],
            "служебные": marks["служебные"],
            "неОтнесено": marks["неОтнесено"],
            "одиночныеСлова": sorted(SINGLE_WORD_VERDICTS),
        },
        "строки": fresh["rows"],
        "какЧитать": "покрытоМашинно — сколько кодов строк найдено в машинных списках того же "
        "реестра (карточки, молчания, заявки): сверка двух учётов лана, а не похвала сама себе",
        "recheckCommand": f"python3 -B scripts/atonement_claim_register.py --check {lan}",
        "measuredAt": now,
        "checkedAt": now,
        "предыдущийСъём": (previous or {}).get("measuredAt"),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--print", dest="show", action="store_true")
    ap.add_argument("--vocab", action="store_true")
    ap.add_argument("lans", nargs="*", default=["all"])
    args = ap.parse_args(argv)
    wanted = SUBLANES + ("root",) if (args.lans or ["all"]) == ["all"] else tuple(args.lans)
    rc = 0
    for lan in wanted:
        fresh = scan_lan(lan)
        if args.vocab:
            print(f"[{lan}] маркеров {fresh['маркеры']['всего']} / различных {fresh['маркеры']['различных']} "
                  f"/ не отнесено {len(fresh['маркеры']['неОтнесено'])}")
            for tok, cnt in fresh["маркеры"]["частоты"].items():
                flag = "!!!" if classify_token(tok) == "НЕ ОТНЕСЁН" else "   "
                print(f"  {flag} {tok:40s} {cnt:5d}  {classify_token(tok)}")
        if fresh["плохо"]:
            print(f"[{lan}] ЛОКАТОРЫ НЕ РЕЗОЛВЯТСЯ: {len(fresh['плохо'])}")
            for line in fresh["плохо"][:8]:
                print("   ", line)
            rc = 1
        if args.show:
            print(f"[{lan}] строк {fresh['агрегаты']['строк']} / файлов {fresh['агрегаты']['файлов']} / "
                  f"классы {fresh['агрегаты']['поКлассам']} / машинно {fresh['агрегаты']['покрытоМашинно']}")
        if args.check or args.write:
            problems = check_block(lan, fresh)
            if problems:
                rc = 1
                print(f"[{lan}] РАСХОЖДЕНИЕ РЕЕСТРА ДОВОДОВ: {len(problems)}")
                for line in problems[:10]:
                    print("   ", line)
            else:
                print(f"[{lan}] реестр доводов сходится: {fresh['агрегаты']['строк']} строк, "
                      f"{fresh['агрегаты']['разрешеноЛокаторов']} локаторов разрешено, "
                      f"{fresh['маркеры']['всего']} маркеров объяснено")
            if args.write:
                path = registry_for(lan)
                previous = json.loads(path.read_text(encoding="utf-8")).get(BLOCK_KEY) or {}
                insert_block(path, build_block(lan, fresh, previous))
                print(f"[{lan}] блок {BLOCK_KEY} записан в {path.name}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
