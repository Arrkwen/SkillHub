# Python Packaging — limits of uv_build

`uv_build` is the backend for pure-Python packages with one root module. These cases fall outside it.

## Native extensions

C, Cython, or Rust extension modules need a backend that compiles them. Do not switch the whole project to setuptools just to attach data files or scripts; those already work with `uv_build`.

## Namespace packages split across repositories

`uv_build` ships a single top-level module. A shared namespace such as `company.core` and `company.api` from two distributions is not this backend's layout. Prefer two independently named packages unless a namespace is an existing public API.

## Files installed outside the package

Small data stays inside the module. Directories that must install as scripts, headers, or environment data are declared separately and land in the wheel's `.data` directory:

```toml
[tool.uv.build-backend.data]
scripts = "bin"
headers = "include"
```
