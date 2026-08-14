#!/usr/bin/env python3
"""CI entrypoint for the canonical Chapter 4–5 handoff validator.

All evidence, source-owner, HOLD-history, prototype-risk, and ranking semantics live
in validate_product_handoff.py. CI must not silently patch a stricter or looser
meaning than a direct local invocation of the canonical validator.
"""
import sys

import validate_product_handoff as core


if __name__ == "__main__":
    try:
        core.main()
    except core.AuditError as exc:
        print(f"HANDOFF_AUDIT_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
