# SkillHub

个人用的 Agent Skills 集合。按工程 / 项目分目录存放，用官方 CLI [`npx skills`](https://github.com/vercel-labs/skills) 安装和恢复。

## 目录

```text
skills/<collection>/<skill-name>/SKILL.md
docs/<collection>.md
```

`collection` 是一个工程或项目。`skill-name` 全局唯一。集合说明写在 `docs/`，不要堆进本文件。

| 集合 | 路径 | 说明 |
| --- | --- | --- |
| python | [`skills/python/`](skills/python/) | [文档](docs/python.md)：应用、Django、FastAPI、SQL、安全与 code review |

## 安装

```bash
npx skills add Arrkwen/SkillHub --skill <name> -y
npx skills experimental_install
```

`experimental_install` 按 `skills-lock.json` 的 `source` 和 `skillPath` 恢复。

## 增加集合

1. 建 `skills/<collection>/<skill-name>/SKILL.md`，名字不要和现有 skill 重复。
2. 写 `docs/<collection>.md`（清单、约定、上游来源），并在上表加一行。
3. `python3 scripts/refresh-lock.py`

## 协议

整仓采用上游中最严的一份：**[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**，全文见 [LICENSE](LICENSE)。再分发须署名，改编后仍用同一协议。各 skill 的原协议见对应集合文档。
