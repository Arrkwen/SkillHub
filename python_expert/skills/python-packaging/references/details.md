# python-packaging — metadata, contents, and publish

## Metadata

```toml
[project]
name = "my-package"
version = "1.0.0"
description = "An awesome Python package"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [{ name = "Your Name", email = "you@example.com" }]
keywords = ["example", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "requests>=2.28,<3",
]

[project.optional-dependencies]
postgres = ["psycopg[binary]"]

[project.urls]
Homepage = "https://github.com/username/my-package"
Repository = "https://github.com/username/my-package"
Changelog = "https://github.com/username/my-package/blob/main/CHANGELOG.md"

[project.scripts]
my-tool = "my_package.cli:main"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins:plugin1"

[build-system]
requires = ["uv_build>=0.9,<1"]  # Use latest 0.x; check https://pypi.org/project/uv-build/
build-backend = "uv_build"
```

`name` on PyPI can contain hyphens. The importable module uses underscores (`my_package`).

Runtime dependencies and extras belong here. Add them with `uv add` and `uv add --optional postgres`. Dev tools use `uv add --group dev` and stay out of `[project]`.

## What the backend includes

Default module path: `src/<package_name>/`.

Included in the wheel:

- That module directory, Python and non-Python files
- `readme` and license files, stored as package metadata

Included in the sdist as well:

- `pyproject.toml`
- Files matched by `source-include`
- Directories listed under `[tool.uv.build-backend.data]`

Put small data files inside the module and read them from the installed package:

```python
from importlib.resources import files

def load_config() -> str:
    return files("my_package").joinpath("data/config.json").read_text()
```

Extra files that belong only in the sdist, such as a changelog:

```toml
[tool.uv.build-backend]
source-include = ["CHANGELOG.md"]
```

`uv_build` packages one root module. A flat layout sets `module-root = ""`. A module name that differs from the project name sets `module-name`.

## Version

Keep `version` as a literal in `[project]`. Bump it in the release commit. Do not derive it from git during the build.

Dependency bounds:

```toml
dependencies = [
    "requests>=2.28,<3",  # compatible range
    "click~=8.1.0",       # >=8.1.0,<8.2.0
]
```

## Publish checklist

- [ ] Tests pass
- [ ] `[project].version` matches the release
- [ ] Changelog notes the version
- [ ] `uv build` produces one wheel and one sdist
- [ ] Wheel imports in a clean environment
- [ ] Console script runs, if `[project.scripts]` is set
- [ ] Upload to TestPyPI first

```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TEST_PYPI_TOKEN"
uv publish --token "$UV_PUBLISH_TOKEN"
```

Private index: pass that index's upload URL to `--publish-url`.

Native extensions and split namespace packages are outside `uv_build`. See [advanced-patterns.md](advanced-patterns.md).
