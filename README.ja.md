# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | 日本語 | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

このリポジトリは複数の skill をまとめたものです。各 skill は
`skills/<skill-name>/` にあり、各 skill ディレクトリには専用の
`SKILL.md` が含まれます。

## 現在の skills

- `website-capability-to-skill`

## ディレクトリ構成

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

## インストール（`npx skills`）

```bash
# インストール可能な skills を表示
npx -y skills add JasirVoriya/voriya-skills --list

# Codex にインストール（グローバル）
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Cursor にインストール（グローバル）
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
