#!/usr/bin/env python3
from pathlib import Path
import json

# Configuration
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"}
BEFORE_SUFFIX = "_before"
AFTER_SUFFIX = "_after"

def main():
    repo_root = Path(__file__).resolve().parent
    images_dir = repo_root / "images"
    output_file = images_dir / "sets.json"

    if not images_dir.is_dir():
        raise SystemExit(f"Images directory not found: {images_dir}")

    # id -> {"before": str|None, "after": str|None}
    sets = {}

    for path in images_dir.iterdir():
        if not path.is_file():
            continue

        ext = path.suffix
        if ext not in IMAGE_EXTENSIONS:
            continue

        stem = path.stem  # filename without extension
        if stem.endswith(BEFORE_SUFFIX):
            base_id = stem[: -len(BEFORE_SUFFIX)]
            sets.setdefault(base_id, {})["before"] = f"images/{path.name}"
        elif stem.endswith(AFTER_SUFFIX):
            base_id = stem[: -len(AFTER_SUFFIX)]
            sets.setdefault(base_id, {})["after"] = f"images/{path.name}"
        else:
            # Doesn't match the XXXX_before / XXXX_after pattern, ignore
            continue

    # Only keep complete pairs
    output_sets = []
    for base_id, data in sets.items():
        before = data.get("before")
        after = data.get("after")
        if before and after:
            output_sets.append(
                {
                    "id": base_id,
                    "before": before,
                    "after": after,
                }
            )

    # Sort for stable ordering by id
    output_sets.sort(key=lambda s: s["id"])

    output = {"sets": output_sets}

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote {len(output_sets)} sets to {output_file}")

if __name__ == "__main__":
    main()
