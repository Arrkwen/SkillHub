# SkillHub

个人用的 Python Agent Skills 集合。从 [skills.sh](https://skills.sh/) 和上游仓库装进来之后，按现代 Python 约定改过一部分，并补了设计模式目录。

安装和恢复走官方 CLI：[`npx skills`](https://github.com/vercel-labs/skills)。本仓库是这些 skill 的发布源，不是再写一套包管理器。

## 安装

仓库公开后，在目标项目里按名字装：

```bash
npx skills add Arrkwen/SkillHub --skill python-design-patterns -y
```

一次装多份：

```bash
npx skills add Arrkwen/SkillHub \
  --skill modern-python \
  --skill python-design-patterns \
  --skill python-testing-patterns \
  -y
```

已经有这份 `skills-lock.json` 的项目，用 lock 恢复：

```bash
npx skills experimental_install
```

CLI 会按 lock 里的 `source` 拉 GitHub 默认分支上的当前文件，再按 `skillPath` 取出对应 skill。

## 目录

Skill 正文在 `python_expert/skills/<name>/`。

| Skill | 原始来源 |
| --- | --- |
| async-python-patterns | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/async-python-patterns) |
| code-reviewer | [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)（已从上游删除，本地改过） |
| django-expert | [vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins/tree/main/skills/django-expert) |
| django-patterns | [affaan-m/ecc](https://github.com/affaan-m/ecc/tree/main/skills/django-patterns) |
| fastapi | [fastapi/fastapi](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills/fastapi) |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) |
| modern-python | [trailofbits/skills](https://github.com/trailofbits/skills/tree/main/plugins/modern-python/skills/modern-python) |
| python-anti-patterns | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-anti-patterns) |
| python-background-jobs | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-background-jobs) |
| python-code-style | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-code-style) |
| python-configuration | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-configuration) |
| python-design-patterns | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-design-patterns) |
| python-error-handling | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-error-handling) |
| python-observability | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-observability) |
| python-packaging | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-packaging) |
| python-performance-optimization | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-performance-optimization) |
| python-project-structure | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-project-structure) |
| python-resilience | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-resilience) |
| python-resource-management | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-resource-management) |
| python-testing-patterns | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-testing-patterns) |
| python-type-safety | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-type-safety) |
| security-best-practices | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) |
| sql-optimization-patterns | [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/sql-optimization-patterns) |
| sqlalchemy-alembic-expert-best-practices-code-review | [wispbit-ai/skills](https://github.com/wispbit-ai/skills/tree/main/skills/sqlalchemy-alembic-expert-best-practices-code-review) |
| typer | [fastapi/typer](https://github.com/fastapi/typer/tree/master/typer/.agents/skills/typer) |

每个 skill 的 `SKILL.md` 末尾也有同样的来源链接。本地副本可以和上游不一致。

## 更新 `skills-lock.json`

lock 记录的是**从哪里装**，不是作者署名。发布到本仓库之后，`source` 应是 `Arrkwen/SkillHub`，`skillPath` 是本仓库里的 `SKILL.md` 路径，`computedHash` 是该 skill 目录下全部文件的 SHA-256（算法与 [vercel-labs/skills](https://github.com/vercel-labs/skills) 的 `computeSkillFolderHash` 相同）。

改完 skill 并 push 到默认分支后，用下面任一方式刷新索引。

在本仓库重算 hash：

```bash
python3 scripts/refresh-lock.py
```

在消费项目里让 CLI 重写 lock（仓库上线后）：

```bash
npx skills add Arrkwen/SkillHub --skill <name> -y
```

不要把 `source` 留在 `wshobson/agents` 这类上游上再跑 `experimental_install`：那会按上游默认分支覆盖本地改动。

## 约定

- 工具链以 `modern-python` 为准：`uv`、`ruff`、`ty`。
- 设计原则见 `python-design-patterns`：KISS、职责分离、组合优于继承、Rule of Three、Pythonic style。
- 23 个 Gang of Four 模式在 `python-design-patterns/references/gof.md`。

上游 skill 各自保留原许可。本仓库的改动按同样方式使用。
