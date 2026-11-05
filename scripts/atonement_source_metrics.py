"""Label parsers, deliberately not reading/access/quote-safe classifiers.

A class label in Markdown cannot establish acquisition, context reading, locator
verification, rights or publication readiness. Legacy carrier labels are a
separate vocabulary retained for historical comparisons, NOT evidenceClass.
"""
from __future__ import annotations
import re

SOURCE_CLASSES = ("A1", "A2", "A3", "B1", "C", "D")
LEGACY_CARRIER_CODES = ("A1", "A2", "B1", "B2", "C")


def source_label_prefix(cell: str) -> str | None:
    """Recognize only an initial canonical label, not the truth of its grading."""
    match = re.match(r"(A[123]|B1|C|D)\b", cell.strip().lstrip("*` "))
    return match.group(1) if match else None


def legacy_carrier_code(row: str) -> str | None:
    """Find one explicitly labelled cell across the register's 5/6-column tables.

    Do not read a quoted grade halfway through a claim as the row's grade.
    A trailing explanation is allowed (FP-137 has one); two labelled cells are
    ambiguous and fail closed. This remains a legacy code, not a source class.
    """
    matches = [m.group(1) for cell in row.strip().strip("|").split("|")
               if (m := re.match(r"^`(A1|A2|B1|B2|C)`(?:\s|$)", cell.strip()))]
    return matches[0] if len(matches) == 1 else None
