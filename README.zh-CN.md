# voriya-skills

简体中文 | [English](./README.en.md) | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

这是一个多 skill 仓库。每个 skill 放在 `skills/<skill-name>/` 目录下，且每个
skill 目录都包含自己的 `SKILL.md`。

## 当前 skills

- `website-capability-to-skill`

## 目录结构

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

## 安装（npx skills）

```bash
# 查看可安装 skills
npx -y skills add JasirVoriya/voriya-skills --list

# 安装到 Codex（全局）
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# 安装到 Cursor（全局）
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
