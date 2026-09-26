---
name: python-packaging
description: Build and publish distributable Python packages. Use when writing package metadata, building a wheel or sdist, setting console scripts, choosing a version, or publishing to PyPI. Use python-project-structure for module layout, modern-python for uv/ruff/ty setup, and typer for CLI implementation.
---

# Python Packaging

Turn an existing Python project into something other people can install. This skill covers metadata, what goes into the distribution, build, version, and publish.

## When to Use This Skill

- Publishing a library or CLI to PyPI or a private index
- Deciding which files belong in the wheel and the sdist
- Declaring runtime dependencies, optional features, and console scripts
- Choosing and bumping a version
- Building `dist/*.whl` and `dist/*.tar.gz`

## When Not to Use This Skill

- Arranging modules, `__all__`, or test layout: [python-project-structure](../python-project-structure/SKILL.md)
- Creating the project, or configuring uv, ruff, and ty: [modern-python](../modern-python/SKILL.md)
- Writing the CLI commands themselves: [typer](../typer/SKILL.md)

## Core Concepts

### 1. Two artifacts

`uv build` writes both:

- **wheel** (`.whl`): what installers prefer
- **sdist** (`.tar.gz`): the source archive used to build a wheel

### 2. Metadata lives in `[project]`

Name, version, Python requirement, runtime dependencies, readme, and scripts are PEP 621 fields. Dev tools go in `[dependency-groups]`, not in the dependencies users install.

### 3. Build backend is `uv_build`

Pure-Python packages use `uv_build`. The version in `[project]` is a static string. Do not add setuptools, hatchling, flit, or poetry as the build backend.

### 4. One importable module

`uv_build` packages a single root module. Default location is `src/<package_name>/`. Files inside that module directory ship in the wheel, including non-Python data files next to the code.

## Quick Start

```bash
uv init --package my-package
cd my-package
uv build
uv publish --token "$UV_PUBLISH_TOKEN"
```

`uv init --package` creates `src/my_package/`. That directory is the module the backend packages. How to split code inside it belongs to `python-project-structure`.

Minimal metadata:

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
dependencies = ["requests"]

[project.optional-dependencies]
postgres = ["psycopg[binary]"]

[project.scripts]
my-tool = "my_package.cli:main"

[build-system]
requires = ["uv_build>=0.9,<1"]  # Use latest 0.x; check https://pypi.org/project/uv-build/
build-backend = "uv_build"
```

- `dependencies` are installed with the package.
- `optional-dependencies` are user-facing extras (`uv add "my-package[postgres]"`).
- Dev tools stay in `[dependency-groups]` and are not part of the published install.
- `[project.scripts]` only registers the command. Implement `main` with the typer skill.

Flat layout (module at the repository root, no `src/`) needs:

```toml
[tool.uv.build-backend]
module-root = ""
```

## Release

1. Set `[project].version` to the release version.
2. `uv build`
3. Confirm `dist/` contains one wheel and one sdist for that version.
4. Publish to TestPyPI, install the wheel in a clean environment, then publish to PyPI.

```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TEST_PYPI_TOKEN"
uv publish --token "$UV_PUBLISH_TOKEN"
```

Version meaning: MAJOR breaks users, MINOR adds backward-compatible behavior, PATCH fixes bugs.

## Detailed patterns

Metadata fields, entry points, package data, and the publish checklist are in `references/details.md`.

## Source

Adapted from [`wshobson/agents`](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-packaging). This copy may differ from upstream.
