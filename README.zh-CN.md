# voriya-skills

简体中文 | [English](./README.en.md) | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

`voriya-skills` 是一个面向 AI Agent 的实战 skill 仓库，当前重点解决：
把网站可见能力快速转换为可调用的 API-first skill。

适合人群：

- 需要把网页操作自动化为 API 工作流的工程师
- 需要复用技能并在 Codex/Cursor 中分发的团队
- 希望降低“手工梳理接口 + 鉴权恢复”成本的开发者

## 10 秒体验

下面的流程可以直接复制运行。

1. 安装 skill 到 Codex。

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

2. 把以下提示词发给 AI。

```text
用 website-capability-to-skill skill 分析 https://example.com，
把网站能力转换成 API-first skill，并输出完整目录。
```

## 当前 skills

- `website-capability-to-skill`
  - 从目标网站 URL 学习能力，并生成站点专用 skill
  - 坚持“浏览器学习 + API 执行”的 API-first 约束
  - 自动接入鉴权缓存与失效恢复（`~/.<site>-auth.yaml`）

## 安装（npx skills）

如果你需要先查看仓库中的可安装 skill，可先执行：

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

安装到 Cursor（全局）：

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

## 仓库结构

```text
voriya-skills/
  skills/
    website-capability-to-skill/
      SKILL.md
      README.md
      agents/
      scripts/
      references/
```

## 曝光增长执行模板

仓库运营模板（含 GitHub topics 清单与一周 Release 节奏）见：
[docs/repo-growth-playbook.md](./docs/repo-growth-playbook.md)
