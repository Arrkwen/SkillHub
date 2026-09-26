#!/usr/bin/env python3
"""Rewrite skills-lock.json to Arrkwen/SkillHub and recompute folder hashes.

Scans skills/<collection>/<skill>/SKILL.md. Skill names must be unique
across collections.

Hashing matches vercel-labs/skills computeSkillFolderHash:
SHA-256 of each relative path plus file bytes, paths sorted, skipping .git and node_modules.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
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


def iter_skills() -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    if not SKILLS_ROOT.is_dir():
        return found
    for collection in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        for skill_dir in sorted(path for path in collection.iterdir() if path.is_dir()):
            if (skill_dir / "SKILL.md").is_file():
                found.append((skill_dir.name, skill_dir))
    return found


def main() -> None:
    skills: dict[str, dict[str, str]] = {}
    for name, skill_dir in iter_skills():
        if name in skills:
            previous = skills[name]["skillPath"]
            current = (skill_dir / "SKILL.md").relative_to(ROOT).as_posix()
            raise SystemExit(f"duplicate skill name {name!r}: {previous} and {current}")
        skill_md = skill_dir / "SKILL.md"
        skills[name] = {
            "source": SOURCE,
            "sourceType": "github",
            "skillPath": skill_md.relative_to(ROOT).as_posix(),
            "computedHash": skill_folder_hash(skill_dir),
        }
    LOCK_PATH.write_text(
        json.dumps({"version": 1, "skills": skills}, indent=2) + "\n",
        encoding="utf-8",
    )
    collections = sorted({entry["skillPath"].split("/")[1] for entry in skills.values()})
    print(
        f"wrote {len(skills)} skills in {len(collections)} collections "
        f"to {LOCK_PATH.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
