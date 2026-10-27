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
    # имена констант пересъёмщика, которыми проза описывает способ съёма (круг 65): по форме —
    # маркеры, по смыслу — не вердикты; тот же разряд, что у FETCH_HEAD над ними
    "KEY_DATE", "PIPELINE_FILES",
    # ведра реестра стражей, которыми глава 11 описывает его устройство (круг 67): по форме —
    # маркеры, по смыслу — названия списков в исходнике; не вердикт и не удержание, и держаться
    # они обязаны списком, а не «прочим», ровно как константы пересъёмщика над ними
    "SCAN_EXEMPT", "PLANTED_GUARDS",
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


def card_index(lan: str) -> dict[str, list[dict]]:
    """Машинные записи лана, привязанные к файлу прозы: {относительный путь: [записи]}.

    Записью считается любой словарь реестра, у которого есть поле file|path|файл со
    значением *.md. Так в сверку попадают и карточки отцов (cardId + file), и карточки
    дел озаглавления (file + holds), и деливерали синтез-плана (path + status): ланы
    описывают своё машиночитаемое по-разному, и требовать от соседа моей схемы было бы
    тем же костылём, только с обратной стороны.
    """
    out: dict[str, list[dict]] = {}
    path = registry_for(lan)
    if not path.is_file():
        return out
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return out
    # корневой реестр лежит в ИСКУПЛЕНИЕ/data/, лановый — в ИСКУПЛЕНИЕ/<лан>/data/:
    # короткие ссылки вида «05_x.md» разрешаются относительно второго каталога сверху
    base_rel = str(path.relative_to(ROOT).parents[1])

    def own_file(node: dict) -> str | None:
        for key in ("file", "path", "файл", "markdownFile"):
            val = node.get(key)
            if isinstance(val, str) and val.endswith(".md"):
                return val if val.startswith("ИСКУПЛЕНИЕ/") else f"{base_rel}/{val}"
        return None

    def harvest(node) -> list[dict]:
        """Запись и всё, что внутри неё: поле состояния может стоять на ребёнке."""
        found = [node] if isinstance(node, dict) else []
        if isinstance(node, dict):
            for val in node.values():
                found += harvest(val)
        elif isinstance(node, list):
            for val in node:
                found += harvest(val)
        return found

    def walk(node) -> None:
        if isinstance(node, dict):
            rel = own_file(node)
            if rel:
                out.setdefault(rel, []).extend(harvest(node))
                return  # внутрь уже зашли; повторный спуск удвоил бы счёт
            for val in node.values():
                walk(val)
        elif isinstance(node, list):
            for val in node:
                walk(val)

    walk(data)
    return out


STATE_KEYS = ("status", "state", "holds", "publicationState", "rightsState", "accessState",
              "locatorState", "evidenceClass", "class")


def card_markers(card: dict) -> set[str]:
    """Маркеры, которыми запись описывает своё состояние: только поля состояния, а не
    весь текст записи. Иначе сверка меряла бы, как часто имя файла написано капителью."""
    out: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            for val in node.values():
                walk(val)
        elif isinstance(node, list):
            for val in node:
                walk(val)
        elif isinstance(node, str):
            for tok in re.findall(r"[A-Z][A-Z0-9 _./+-]{3,40}", node):
                if is_marker_shape(tok.strip()):
                    out.add(tok.strip())

    for key in STATE_KEYS:
        if key in card:
            walk(card[key])
    return out


def file_markers(rel: str) -> set[str]:
    """Маркеры всей прозы файла, а не только его разделов: статус шапки файла лежит над
    первым ## и в строки реестра по определению не входит — сверять карточку с частью
    файла было бы нечестно по отношению к файлу."""
    path = ROOT / rel
    if not path.is_file():
        return set()
    return {t.strip() for t in tokens_in(path.read_text(encoding="utf-8")) if is_marker_shape(t.strip()) or t in SINGLE_WORD_VERDICTS}


def in_walk_scope(lan: str, rel: str) -> bool:
    """Относится ли ссылка к обходу этого лана: корень видит только свои .md в ИСКУПЛЕНИЕ/,
    лан — всё под своим каталогом. Ссылки чужих отделений в реестре корня — не висячие
    пути, а указания на соседей и на объекты Drive: их существование полирует холодный
    замер, а не эта сверка, и требовать от них совпадения со строками корня было бы
    приписыванием дефекта там, где его нет."""
    parts = rel.split("/")
    if lan == "root":
        return len(parts) == 2 and parts[0] == "ИСКУПЛЕНИЕ"
    return rel.startswith(f"ИСКУПЛЕНИЕ/{lan}/")


def cross_check(lan: str, rows: list[dict]) -> dict:
    """Сверка двух учётов лана: проза (строки реестра со своими маркерами) и машинные
    карточки, ссылающиеся на те же файлы. Ни одна из сторон не правит другую; расхождение
    — это то, что надо заметить, а не то, что надо замазать."""
    by_file = card_index(lan)
    prose_by_file: dict[str, set[str]] = {}
    for row in rows:
        prose_by_file.setdefault(row["файл"], set()).update(row["токены"])
    # сверяем только вердикты: карточка, написанная источниками («MT + LXX»), а не
    # приговорами, не обязана совпадать с прозой, и считать это расхождением — портить число
    out_of_scope = sorted(f for f in by_file if not in_walk_scope(lan, f))
    all_files = {r["файл"] for r in rows} | {f for f in by_file if in_walk_scope(lan, f)}
    markers_by_file = {rel: file_markers(rel) for rel in sorted(all_files)}
    lane_prose = {t for fs in markers_by_file.values() for t in fs if classify_token(t) is not None}
    res = {
        "файловПрозы": len(prose_by_file),
        "файловСКарточкой": len(set(prose_by_file) & set(by_file)),
        "файловБезКарточки": len(set(prose_by_file) - set(by_file)),
        "ссылокНаНесуществующийФайл": 0,
        "ссылокВнеОбходаЛана": len(out_of_scope),
        "записейВнеСтрокЛана": 0,
        "файловБезКарточкиСостояния": 0,
        "маркеровВПрозеНеОтражённыхВКарточке": 0,
        "маркеровВКарточкеНеИзПрозыЛана": 0,
        "детально": {},
    }
    for rel in sorted(all_files):
        assert in_walk_scope(lan, rel) or rel in prose_by_file
        state_cards = [c for c in by_file.get(rel, []) if card_markers(c)]
        if by_file.get(rel) and not state_cards:
            res["файловБезКарточкиСостояния"] += 1
        if not (ROOT / rel).is_file():
            res["ссылокНаНесуществующийФайл"] += 1
        if rel not in prose_by_file and (ROOT / rel).is_file():
            res["записейВнеСтрокЛана"] += 1  # в каталоге лана есть, в обход не попало
        pm = markers_by_file[rel]
        cm = set().union(*[card_markers(c) for c in state_cards]) if state_cards else set()
        held_in_prose = {t for t in pm if classify_token(t) == "УДЕРЖИВАЕТСЯ"}
        not_in_card = held_in_prose - cm
        not_from_prose = {t for t in cm if classify_token(t) is not None and t not in lane_prose}
        res["маркеровВПрозеНеОтражённыхВКарточке"] += len(not_in_card)
        res["маркеровВКарточкеНеИзПрозыЛана"] += len(not_from_prose)
        if not_in_card or not_from_prose or (rel not in by_file) or (rel not in prose_by_file):
            res["детально"][Path(rel).name] = {
                "проза": len(pm),
                "карточка": len(cm),
                "вПрозеНеВКарточке": sorted(not_in_card),
                "вКарточкеНеИзПрозы": sorted(not_from_prose),
                "естьКарточка": rel in by_file,
            }
    return res


def scan_lan(lan: str) -> dict:
    """Строки и агрегаты одного лана. Детерминированно: обход по сортировке путей,
    внутри файла — по номеру строки. Никакой выборки: берётся весь ствол лана."""
    ids = machine_ids(lan)
    byFile = card_index(lan)
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
                    "токены": sorted(set(t for t in tokens_in(body))),
                    "машинно": code_m is not None and (code_m.group(1) in ids or base in ids),
                    "машинноПоФайлу": rel in byFile,
                }
            )
            per_file[rel] += 1

    bad = resolve_rows(rows)
    classes = collections.Counter(r["класс"] for r in rows)
    cross = cross_check(lan, rows)
    return {
        "лан": lan,
        "rows": rows,
        "агрегаты": {
            "строк": len(rows),
            "файлов": len(per_file),
            "поКлассам": dict(sorted(classes.items(), key=lambda kv: (-kv[1], kv[0]))),
            "покрытоМашинно": sum(1 for r in rows if r["машинно"]),
            "покрытоПоФайлу": sum(1 for r in rows if r["машинноПоФайлу"]),
            "файловПрозы": len(per_file),
            "файловБезКарточки": len(set(per_file) - set(card_index(lan))),
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
        "сверка": cross,
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


FIELDS_TO_MIRROR = ("строк", "файлов", "покрытоМашинно", "покрытоПоФайлу", "файловПрозы",
                    "файловБезКарточки", "разрешеноЛокаторов", "неРазрешено")


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
    if block.get("сверкаСКарточками") != fresh["сверка"]:
        problems.append(
            f"{lan}: сверка с машинными карточками разошлась со съёмом: записано "
            f"{ {k: v for k, v in (block.get('сверкаСКарточками') or {}).items() if k != 'детально'}!r}, "
            f"обход даёт { {k: v for k, v in fresh['сверка'].items() if k != 'детально'}!r}"
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


AGG_FIELDS_A = ("сВердиктом", "удерживается", "открыто", "закрыто", "служебное", "покрытоМашинно",
                "маркеров", "неОтнесено", "неРазрешено")
AGG_FIELDS_B = ("покрытоПоФайлу", "файловПрозы", "файловБезКарточки", "ссылокНаНесуществующийФайл",
                "ссылокВнеОбходаЛана", "записейВнеСтрокЛана", "файловБезКарточкиСостояния",
                "маркеровВПрозеНеОтражённыхВКарточке", "маркеровВКарточкеНеИзПрозыЛана")
CROSS_KEYS = ("строк", "покрытоПоФайлу", "файлов", "файловБезКарточки", "висящихСсылок",
              "ссылокВнеОбходаЛана", "карточекБезСостояния", "неОтраженоВКарточке",
              "терминовКарточкиВнеПрозы")


def rollup() -> dict:
    """Сводка `integrityGate.scopeOfMeasurementRules.claimsPerRegistry`, снятая теми же съёмами,
    которыми её сверяет правило 27 и 28 гейта.

    До круга 65 у этой сводки не было производителя: гейт её сравнивал с обходом, пересъёмщик
    чисел её явно не трогал (в его отчёте стояло «ими заведует atonement_claim_register.py», где
    «заведует» означало «когда-нибудь»), а правили её рукой. Первый же прогон круга
    это и поймал: проза назвала два новых служебных маркера, живой счётчик двинулся, а записанный
    остался — и единственный доступный способ починить красное правило 27 был «вписать число с
    экрана», то есть ровно тот жест, против которого круг 63 и затевал пересъёмщик. Копия
    агрегации гейта здесь осознанна: два счёта одного определения обязаны разойтись громко, а не
    договориться; поле `метод` сводки называет эту команду именно потому, что пересъёмность —
    способ, а не обещание."""
    roll: dict = {}
    agg_a = {k: 0 for k in AGG_FIELDS_A}
    agg_b = {k: 0 for k in AGG_FIELDS_B}
    cross: dict = {}
    for lan in SUBLANES + ("root",):
        fresh = scan_lan(lan)
        if fresh["плохо"]:
            raise SystemExit(f"сводка не снимается: лан {lan} имеет {len(fresh['плохо'])} неразрешённых "
                             f"локаторов — сначала чини локаторы, потом переснимай сводку")
        name = "корпус" if lan == "root" else lan
        a, cr = fresh["агрегаты"], fresh["сверка"]
        cls = a["поКлассам"]
        roll[name] = a["строк"]
        agg_a["сВердиктом"] += a["строк"] - cls.get("БЕЗ МАРКЕРА", 0)
        agg_a["удерживается"] += cls.get("УДЕРЖИВАЕТСЯ", 0)
        agg_a["открыто"] += cls.get("ОТКРЫТО", 0)
        agg_a["закрыто"] += cls.get("ЗАКРЫТО", 0)
        agg_a["служебное"] += cls.get("СЛУЖЕБНОЕ", 0)
        agg_a["покрытоМашинно"] += a["покрытоМашинно"]
        agg_a["маркеров"] += fresh["маркеры"]["всего"]
        agg_a["неОтнесено"] += sum(fresh["маркеры"]["неОтнесено"].values())
        agg_a["неРазрешено"] += a["неРазрешено"]
        # покрытоПоФайлу/файловПрозы/файловБезКарточки лежат в агрегатах лана, остальное — в
        # сверке; разделение взято ровно из правил 27/28, потому что сводка обязана сходиться с ними
        agg_b["покрытоПоФайлу"] += a["покрытоПоФайлу"]
        agg_b["файловПрозы"] += a["файловПрозы"]
        agg_b["файловБезКарточки"] += a["файловБезКарточки"]
        for k in AGG_FIELDS_B[3:]:
            agg_b[k] += cr[k]
        cross[name] = {"строк": a["строк"], "покрытоПоФайлу": a["покрытоПоФайлу"],
                       "файлов": a["файловПрозы"], "файловБезКарточки": a["файловБезКарточки"],
                       "висящихСсылок": cr["ссылокНаНесуществующийФайл"],
                       "ссылокВнеОбходаЛана": cr["ссылокВнеОбходаЛана"],
                       "карточекБезСостояния": cr["файловБезКарточкиСостояния"],
                       "неОтраженоВКарточке": cr["маркеровВПрозеНеОтражённыхВКарточке"],
                       "терминовКарточкиВнеПрозы": cr["маркеровВКарточкеНеИзПрозыЛана"]}
        assert all(k in cross[name] for k in CROSS_KEYS)
    return {"всего": sum(roll.values()), "поЛанам": roll, "детально": {**agg_a, **agg_b},
            "сверкаСКарточками": cross}


def rollup_diff(fresh: dict) -> list:
    """Что сводка скажет после записи: сравнение с тем, что записано, — по сверяемым полям."""
    data = json.loads(MAIN_REGISTRY.read_text(encoding="utf-8"))
    stored = ((data.get("integrityGate") or {}).get("scopeOfMeasurementRules") or {}).get(
        "claimsPerRegistry") or {}
    bad = []
    for k, v in sorted(fresh["поЛанам"].items()):
        if int(stored.get(k, -1)) != v:
            bad.append(f"{k}: записано {stored.get(k)!r}, обход даёт {v}")
    if int(stored.get("всего", -1)) != fresh["всего"]:
        bad.append(f"всего: записано {stored.get('всего')!r}, обход даёт {fresh['всего']}")
    for k, v in sorted(fresh["детально"].items()):
        if int((stored.get("детально") or {}).get(k, -1)) != v:
            bad.append(f"детально.{k}: записано {(stored.get('детально') or {}).get(k)!r}, обход даёт {v}")
    for lan, cells in sorted(fresh["сверкаСКарточками"].items()):
        for k, v in sorted(cells.items()):
            if int(((stored.get("сверкаСКарточками") or {}).get(lan) or {}).get(k, -1)) != v:
                bad.append(f"сверкаСКарточками.{lan}.{k}: записано "
                           f"{((stored.get('сверкаСКарточками') or {}).get(lan) or {}).get(k)!r}, "
                           f"обход даёт {v}")
    return bad


def write_rollup(fresh: dict) -> list:
    """Запись снятой сводки: только числа и `measuredAt`; проза блока (`метод`, `чтоЗначит`,
    `зачем`, поправки прежних кругов) остаётся нетронутой — сводка переснимается, а не переписывается."""
    path = MAIN_REGISTRY
    raw = path.read_text(encoding="utf-8")
    form = canonical_indent(raw)
    data = json.loads(raw)
    scope = data["integrityGate"]["scopeOfMeasurementRules"]
    cpr = scope["claimsPerRegistry"]
    cpr.update(fresh["поЛанам"])
    cpr["всего"] = fresh["всего"]
    cpr["детально"].update(fresh["детально"])
    for lan, cells in fresh["сверкаСКарточками"].items():
        (cpr["сверкаСКарточками"].setdefault(lan, {})).update(cells)
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cpr["measuredAt"] = now
    out = json.dumps(data, ensure_ascii=False, indent=form if form is not None else 1) + "\n"
    back = json.loads(out)
    bp, ap_ = json.loads(raw), back
    for key in bp:
        if key != "integrityGate" and json.dumps(bp[key], ensure_ascii=False, sort_keys=True) != json.dumps(
                ap_[key], ensure_ascii=False, sort_keys=True):
            raise SystemExit(f"запись сводки задела чужой ключ верхнего уровня {key!r} — так нельзя")
    # стража «не задень чужое» обязана сравнивать одно с другим: до и после, а не до и саму себя;
    # первая версия индексировала после-словарь ключом из integrityGate и падала KeyError'ом
    gate_b, gate_a = bp["integrityGate"], ap_["integrityGate"]
    for key in gate_b:
        if key != "scopeOfMeasurementRules" and json.dumps(gate_b[key], ensure_ascii=False,
                                                           sort_keys=True) != json.dumps(
                gate_a[key], ensure_ascii=False, sort_keys=True):
            raise SystemExit(f"запись сводки задела чужой ключ integrityGate.{key!r} — так нельзя")
    path.write_text(out, encoding="utf-8")
    return [l for l in rollup_diff(fresh)]


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
        "сверкаСКарточками": fresh["сверка"],
        "правилоСверки": "запись лана считается относящейся к файлу, если в ней есть file|path|файл на этот .md; "
        " HOLD-маркеры секций файла обязаны встретиться в маркерах его записей, а маркеры записи обязаны "
        "встречаться в прозе лана — так оба учёта проверяют друг друга, а не дополняются до совпадения",
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
    ap.add_argument("--cross", action="store_true")
    ap.add_argument("--rollup", dest="rollup_only", action="store_true",
                    help="сверить сводку claimsPerRegistry со съёмом всех ланов, ничего не записывая; "
                         "сводка глобальна, поэтому лан в командной строке на неё не влияет")
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
        if args.cross:
            cr = fresh["сверка"]
            print(f"[{lan}] сверка: файлов прозы {cr['файловПрозы']}, с карточкой {cr['файловСКарточкой']}, "
                  f"без карточки {cr['файловБезКарточки']}, висящих ссылок {cr['ссылокНаНесуществующийФайл']}, "
                  f"записей вне строк лана {cr['записейВнеСтрокЛана']}, "
f"ссылок вне обхода лана {cr['ссылокВнеОбходаЛана']}, "
                                    f"карточек без поля состояния {cr['файловБезКарточкиСостояния']}; "
                  f"маркеров в прозе, не отражённых в карточке: {cr['маркеровВПрозеНеОтражённыхВКарточке']}; "
                  f"маркеров в карточке, не известных прозе лана: {cr['маркеровВКарточкеНеИзПрозыЛана']}")
            for name, det in list(cr["детально"].items())[:14]:
                print(f"    {name[:46]:46s} проза {det['проза']:3d} карточка {det['карточка']:3d} "
                      f"не в карточке {det['вПрозеНеВКарточке']} не из прозы {det['вКарточкеНеИзПрозы'][:3]}")
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
    # сводка глобальна: её снимают по всем пяти ланам, даже если в команду занесён один, — иначе
    # «переснял root» оставило бы в реестре сумму, сочинённую по четырём чужим ланам на глаз
    if args.rollup_only or args.check:
        fresh_roll = rollup()
        bad = rollup_diff(fresh_roll)
        if bad:
            rc = 1
            print(f"сводка claimsPerRegistry отстала от обхода: {len(bad)}")
            for line in bad[:12]:
                print("   ", line)
        else:
            # число берётся из того же съёма, которым сверяли; пересчитывать его вторым вызовом —
            # значит иметь два ответа на один вопрос и удивляться, если они разойдутся
            print(f"сводка claimsPerRegistry совпадает с обходом: всего {fresh_roll['всего']} доводов, "
                  f"полей {len(fresh_roll['детально'])}, ланов сверки "
                  f"{len(fresh_roll['сверкаСКарточками'])}")
    if args.write:
        left = write_rollup(rollup())
        if left:
            rc = 1
            print(f"сводка записана, но сверка не молчит: {left[:3]}")
        else:
            print("сводка claimsPerRegistry переснята этим же съёмом, что её сверяет (правила 27/28)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
