#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "friend"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def create_bundle(base_dir: Path, name: str, slug: str) -> Path:
    profile_dir = base_dir / slug
    ensure_dir(profile_dir)

    meta_path = profile_dir / "meta.json"
    persona_path = profile_dir / "persona.md"
    memory_path = profile_dir / "memory.md"
    relationship_path = profile_dir / "relationship.md"
    skill_path = profile_dir / "SKILL.md"

    if not meta_path.exists():
        meta = {
            "name": name,
            "slug": slug,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "version": "v1",
            "source_summary": [],
            "notes": "",
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_if_missing(persona_path, f"# {name} — Persona\n\n- 待补充\n")
    write_if_missing(memory_path, f"# {name} — Memory\n\n- 待补充\n")
    write_if_missing(relationship_path, f"# {name} — Relationship\n\n- 待补充\n")
    write_if_missing(
        skill_path,
        f"---\nname: {slug}\ndescription: Speak and reason like {name} using persona, memory, relationship patterns, and known boundaries. Use when Codex needs to draft messages, simulate likely replies, or recall shared preferences in this friend's voice.\n---\n\n"
        f"# {name}\n\n"
        "Read `persona.md`, `memory.md`, and `relationship.md` before replying.\n\n"
        "## Rules\n\n"
        "- Mirror the friend's likely tone, not a caricature.\n"
        "- Prefer evidence-backed recall over invention.\n"
        "- Admit uncertainty when memory is incomplete.\n"
        "- Respect boundaries recorded in the profile files.\n",
    )

    return profile_dir


def list_bundles(base_dir: Path) -> list[dict]:
    rows = []
    if not base_dir.exists():
        return rows
    for child in sorted(base_dir.iterdir()):
        if not child.is_dir():
            continue
        meta_path = child / "meta.json"
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {"name": child.name, "version": "invalid-meta"}
        rows.append({
            "slug": child.name,
            "name": meta.get("name", child.name),
            "version": meta.get("version", "unknown"),
            "updated_at": meta.get("updated_at", "unknown"),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold and inspect distilled friend bundles.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new friend bundle skeleton")
    init_parser.add_argument("--base-dir", required=True)
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--slug")

    list_parser = subparsers.add_parser("list", help="List existing friend bundles")
    list_parser.add_argument("--base-dir", required=True)

    args = parser.parse_args()

    if args.action == "init":
        base_dir = Path(args.base_dir)
        ensure_dir(base_dir)
        slug = args.slug or slugify(args.name)
        profile_dir = create_bundle(base_dir, args.name, slug)
        print(profile_dir)
        return

    if args.action == "list":
        rows = list_bundles(Path(args.base_dir))
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
