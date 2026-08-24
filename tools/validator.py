"""CLI validator for security standards markdown structure and YAML frontmatter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_KEYS = ["doc_kind", "canonical_id", "purpose", "rank", "topics"]


def validate_standard_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append(f"{path.name}: missing YAML frontmatter opening '---'")
        return errors
    end = text.find("\n---", 3)
    if end == -1:
        errors.append(f"{path.name}: missing YAML frontmatter closing '---'")
        return errors
    frontmatter_raw = text[3:end]
    for k in REQUIRED_KEYS:
        if f"{k}:" not in frontmatter_raw:
            errors.append(f"{path.name}: missing required frontmatter key '{k}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate security standards")
    parser.add_argument("--all", action="store_true", help="Validate all standards")
    parser.add_argument("--path", type=str, default=None, help="Specific standard file to validate")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    standards_dir = root / "standards"
    all_errors = []

    if args.path:
        files = [Path(args.path)]
    else:
        files = [p for p in standards_dir.glob("*.md") if p.name != "README.md"]

    for f in files:
        errs = validate_standard_file(f)
        all_errors.extend(errs)

    if all_errors:
        print(f"Validation failed with {len(all_errors)} errors:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(files)} standards validated cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
