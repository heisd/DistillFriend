#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

TRACKED_FILES = ["meta.json", "persona.md", "memory.md", "relationship.md", "SKILL.md"]


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def versions_dir(profile_dir: Path) -> Path:
    path = profile_dir / ".versions"
    path.mkdir(parents=True, exist_ok=True)
    return path


def backup(profile_dir: Path) -> Path:
    dest = versions_dir(profile_dir) / now_tag()
    dest.mkdir(parents=True, exist_ok=False)
    copied = []
    for name in TRACKED_FILES:
        src = profile_dir / name
        if src.exists():
            shutil.copy2(src, dest / name)
            copied.append(name)
    manifest = {"copied": copied, "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()}
    (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def list_versions(profile_dir: Path) -> list[str]:
    root = versions_dir(profile_dir)
    return [p.name for p in sorted(root.iterdir()) if p.is_dir()]


def restore(profile_dir: Path, version: str) -> None:
    source = versions_dir(profile_dir) / version
    if not source.exists():
        raise FileNotFoundError(f"Version not found: {version}")
    for name in TRACKED_FILES:
        src = source / name
        if src.exists():
            shutil.copy2(src, profile_dir / name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Backup and restore distilled friend bundles.")
    sub = parser.add_subparsers(dest="action", required=True)

    backup_parser = sub.add_parser("backup")
    backup_parser.add_argument("--profile-dir", required=True)

    list_parser = sub.add_parser("list")
    list_parser.add_argument("--profile-dir", required=True)

    restore_parser = sub.add_parser("restore")
    restore_parser.add_argument("--profile-dir", required=True)
    restore_parser.add_argument("--version", required=True)

    args = parser.parse_args()
    profile_dir = Path(args.profile_dir)

    if args.action == "backup":
        print(backup(profile_dir))
    elif args.action == "list":
        print(json.dumps(list_versions(profile_dir), ensure_ascii=False, indent=2))
    elif args.action == "restore":
        restore(profile_dir, args.version)
        print(profile_dir)


if __name__ == "__main__":
    main()
