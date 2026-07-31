from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path("БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED")
PROOF = ROOT / "data/PROOF_STATUS_LEDGER.csv"
SOURCES = ROOT / "data/SOURCE_ANCHORS.csv"
QUEUE = ROOT / "data/NEXT_MICROBATCH.csv"
GROUP = ROOT / "groups/06_DATA_AND_PROOF_LEDGERS.md"
MARKER = "## GOST v135 — первичное разрешение нумерации X–XI–XII"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise RuntimeError(f"Missing header: {path}")
        return list(reader.fieldnames), [dict(row) for row in reader]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\r\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


# 1. Replace the existing unresolved proof row; do not duplicate it.
fields, rows = read_csv(PROOF)
matches = [row for row in rows if row.get("item_id") == "GOST-130-003"]
if len(matches) != 1:
    raise RuntimeError(f"Expected one GOST-130-003 row, found {len(matches)}")
row = matches[0]
row.update(
    {
        "corpus": "Congress chronology",
        "issue": "Union congress sequence X (1935) — XI (1937) — XII (1939)",
        "status": "congress_numbering_resolved_primary_text_sequence_visual_pending",
        "pages": "1935 PDF p.7; 1936 PDF pp.9-10; 1937 no.2-3 p.13 target; 1939 pp.28,31",
        "holding": "JBC, Biblioteka Jagiellońska 7387 II czasop.",
        "source": "Primary JBC serial text layers + 1939 reproduced ministry notice; IPN ordinal superseded",
        "next_action": "Create visual page cards for 1935 X, 1937 no.2-3 p.13 and 1939 XI/XII pages; preserve screenshot cache-miss note",
        "year": "1935-1939",
        "source_url": "https://jbc.bj.uj.edu.pl/Content/680466/0004_NDIGCZAS039838_110491137.pdf",
        "verification_note": "Primary July 1935 issue explicitly calls Kowel 29 June–1 July the X Union Congress. May 1936 issue calls 15–19 May the II Congress of the interdenominational Committee and says Union delegates would participate, proving a separate numbering series. April 1939 text reproduces ministry notice calling May 1937 XI and announces XII for 1939. IPN 2023 wording 'jubilee 10th' for 1937 is superseded as a modern ordinal error. Text-layer use is safe; screenshots/facsimile quote cards remain pending.",
        "version": "v135",
    }
)
write_csv(PROOF, fields, rows)

# 2. Replace the queue item with a resolved row, retaining only visual work.
fields, rows = read_csv(QUEUE)
matches = [row for row in rows if row.get("item") == "Resolve May 1937 congress numbering"]
if len(matches) != 1:
    raise RuntimeError(f"Expected one congress queue row, found {len(matches)}")
row = matches[0]
row.update(
    {
        "priority": "RESOLVED-v135",
        "item": "Congress sequence X (1935) — XI (1937) — XII (1939)",
        "goal": "RESOLVED: primary serial sequence establishes the Union ordinals; IPN's 1937 '10th' is superseded. Remaining work is visual page-card capture only.",
        "blocker": "JBC/IPN screenshot calls return cache miss; parsed primary PDF text is available but facsimile and quote-ready status remain pending.",
    }
)
write_csv(QUEUE, fields, rows)

# 3. Add only new, stable source anchors.
fields, rows = read_csv(SOURCES)
existing = {row.get("source_id") for row in rows}
new_rows = [
    {
        "source_id": "GOST-135-SRC-JBC-X-1935",
        "url": "https://jbc.bj.uj.edu.pl/Content/680466/0004_NDIGCZAS039838_110491137.pdf",
        "confirms": "Primary July 1935 issue explicitly identifies the Kowel meeting of 29 June–1 July 1935 as the X Congress of the Union.",
        "source": "Ewangeliczny Chrześcijanin R.2 no.6, July 1935",
        "authority_level": "A primary periodical text layer; visual screenshot pending",
        "used_for": "Union congress ordinal X and chronology",
        "version": "v135",
        "source_key": "GOST-135-SRC-JBC-X-1935",
        "use": "supersede 1937-as-10th chronology",
        "label": "X Union Congress — Kowel 1935",
        "type": "primary periodical PDF",
        "trust_note": "Parsed PDF text is explicit; screenshot failed with cache miss, so no facsimile quotation claim.",
        "source_type": "official digital-library primary source",
        "note": "Also distinguishes the first interdenominational congress of 1935 from the Union's own X Congress.",
    },
    {
        "source_id": "GOST-135-SRC-JBC-II-1936",
        "url": "https://jbc.bj.uj.edu.pl/Content/680469/0002_NDIGCZAS039838_110491157.pdf",
        "confirms": "Primary May 1936 issue announces the II Congress of the Committee for the Union of Evangelical Christians for 15–19 May and separately says Union delegates would participate.",
        "source": "Ewangeliczny Chrześcijanin R.3 no.2, May 1936",
        "authority_level": "A primary periodical text layer; visual screenshot pending",
        "used_for": "separation of interdenominational and Union congress numbering",
        "version": "v135",
        "source_key": "GOST-135-SRC-JBC-II-1936",
        "use": "prevent false insertion of 1936 into Union ordinal sequence",
        "label": "II interdenominational Congress — Warsaw 1936",
        "type": "primary periodical PDF",
        "trust_note": "The organizing committee and participation wording are explicit; screenshot failed with cache miss.",
        "source_type": "official digital-library primary source",
        "note": "This is a different numbering series from X/XI/XII Union congresses.",
    },
    {
        "source_id": "GOST-135-SRC-JBC-XI-1937-OBJECT",
        "url": "https://jbc.bj.uj.edu.pl/dlibra/publication/718051/edition/680473",
        "confirms": "Official JBC object identity for R.4 no.2/3, September 1937; IPN footnote targets p.13 for the May 1937 meeting and pp.24–27 for the confession of faith.",
        "source": "JBC edition 680473 / IPN exact page locators",
        "authority_level": "A official object identity; target pages not directly rendered",
        "used_for": "exact visual-control target for the XI Congress report",
        "version": "v135",
        "source_key": "GOST-135-SRC-JBC-XI-1937-OBJECT",
        "use": "targeted page acquisition only",
        "label": "1937 no.2/3 exact JBC object",
        "type": "official digital-library object record",
        "trust_note": "Object and page targets are exact; the direct PDF filename and visual page have not been recovered in current tooling.",
        "source_type": "official metadata plus scholarly page locator",
        "note": "Do not quote p.13 until facsimile is obtained. Ordinal XI is resolved independently by the primary 1935 and 1939 sequence.",
    },
]
for new in new_rows:
    if new["source_id"] not in existing:
        rows.append(new)
write_csv(SOURCES, fields, rows)

# 4. Append one consolidated supersession block to the grouped master.
text = GROUP.read_text(encoding="utf-8")
if MARKER not in text:
    block = f"""

{MARKER}

**Статус:** `CONGRESS NUMBERING RESOLVED — PRIMARY TEXT SEQUENCE / VISUAL PAGES PENDING`.

- Июльский выпуск `Ewangeliczny Chrześcijanin` за 1935 год прямо называет собрание в Ковеле 29 июня — 1 июля **X съездом Союза славянских общин евангельских христиан в Польше**.
- Майский выпуск 1936 года объявляет на 15–19 мая **II съезд Комитета объединения евангельских христиан в Польше** и отдельно сообщает, что Союз направит на него своих представителей. Это другая, межконфессиональная нумерационная серия, а не XI союзный съезд.
- Апрельский выпуск 1939 года воспроизводит министерское сообщение о правлении, избранном на **XI съезде** в мае 1937 года, и объявляет **XII съезд** на май 1939 года.
- Поэтому формула современной статьи IPN `юбилейный 10-й съезд` для варшавского собрания 15–19 мая 1937 года **superseded** как ошибочный ordinal. Событие, даты, координационный комитет и автономия организаций оцениваются отдельно и этой поправкой не отменяются.
- Каноническая последовательность: **X — Ковель, 29.06–01.07.1935; XI — Варшава, 15–19.05.1937; XII — объявлен на май 1939**.
- Визуальный барьер сохранён: screenshot страниц JBC/IPN снова завершился `cache miss`. Допустим пересказ первичного text layer с точной атрибуцией; facsimile/quote-ready формулировки пока запрещены.

**Первичные маршруты:**
- 1935 X: https://jbc.bj.uj.edu.pl/Content/680466/0004_NDIGCZAS039838_110491137.pdf
- 1936 II межконфессиональный: https://jbc.bj.uj.edu.pl/Content/680469/0002_NDIGCZAS039838_110491157.pdf
- 1937 №2/3 exact object: https://jbc.bj.uj.edu.pl/dlibra/publication/718051/edition/680473
- 1939 XI/XII control: https://jbc.bj.uj.edu.pl/Content/680480/0001_NDIGCZAS039838_110491233.pdf
"""
    text = text.rstrip() + block.rstrip() + "\n"
    GROUP.write_text(text, encoding="utf-8")
else:
    GROUP.write_text(text.rstrip() + "\n", encoding="utf-8")

print("Gost v135 congress supersession prepared successfully")
