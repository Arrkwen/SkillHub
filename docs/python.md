# python

路径：[skills/python/](../skills/python/)

工具链以 `modern-python` 为准：`uv`、`ruff`、`ty`。设计原则见 `python-design-patterns`（含 `references/gof.md`）。

每个 skill 的 `SKILL.md` 末尾有来源链接。本地副本可以和上游不一致。

## Skill

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

## 上游协议

整仓是 [CC BY-SA 4.0](../LICENSE)。各 skill 原文在上游下的许可：

| 上游 | 原协议 | skill |
| --- | --- | --- |
| [trailofbits/skills](https://github.com/trailofbits/skills) | CC BY-SA 4.0 | modern-python |
| [openai/skills](https://github.com/openai/skills)（`security-best-practices/LICENSE.txt`） | Apache-2.0 | security-best-practices |
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Apache-2.0 | code-reviewer |
| [wshobson/agents](https://github.com/wshobson/agents) | MIT | python-*、async-python-patterns、sql-optimization-patterns |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | MIT | find-skills |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | MIT | fastapi |
| [fastapi/typer](https://github.com/fastapi/typer) | MIT | typer |
| [affaan-m/ecc](https://github.com/affaan-m/ecc) | MIT | django-patterns |
| [vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins) | MIT | django-expert |
| [wispbit-ai/skills](https://github.com/wispbit-ai/skills) | MIT（写在 skill 的 frontmatter，仓库无 LICENSE 文件） | sqlalchemy-alembic-expert-best-practices-code-review |
