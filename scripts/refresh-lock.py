#!/usr/bin/env python3
"""Rewrite skills-lock.json to Arrkwen/SkillHub and recompute folder hashes.

Hashing matches vercel-labs/skills computeSkillFolderHash:
SHA-256 of each relative path plus file bytes, paths sorted, skipping .git and node_modules.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "python_expert" / "skills"
LOCK_PATH = ROOT / "skills-lock.json"
SOURCE = "Arrkwen/SkillHub"


def skill_folder_hash(skill_dir: Path) -> str:
    files: list[tuple[str, bytes]] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue
        relative = path.relative_to(skill_dir).as_posix()
        files.append((relative, path.read_bytes()))
    files.sort(key=lambda item: item[0])
    digest = hashlib.sha256()
    for relative, content in files:
        digest.update(relative.encode())
        digest.update(content)
    return digest.hexdigest()


def main() -> None:
    skills: dict[str, dict[str, str]] = {}
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        name = skill_dir.name
        skill_path = skill_md.relative_to(ROOT).as_posix()
        skills[name] = {
            "source": SOURCE,
            "sourceType": "github",
            "skillPath": skill_path,
            "computedHash": skill_folder_hash(skill_dir),
        }
    LOCK_PATH.write_text(
        json.dumps({"version": 1, "skills": skills}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(skills)} skills to {LOCK_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
