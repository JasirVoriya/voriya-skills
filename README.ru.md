# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) |
[한국어](./README.ko.md) | [Português (Brasil)](./README.pt-BR.md) | Русский

Это репозиторий с несколькими skills. Каждый skill находится в каталоге
`skills/<skill-name>/`, и каждый каталог skill содержит собственный
`SKILL.md`.

## Текущие skills

- `website-capability-to-skill`

## Структура каталогов

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

## Установка (`npx skills`)

```bash
# Показать доступные для установки skills
npx -y skills add JasirVoriya/voriya-skills --list

# Установить в Codex (глобально)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Установить в Cursor (глобально)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
