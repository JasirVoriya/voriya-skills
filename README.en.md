# voriya-skills

[简体中文](./README.md) | English | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

This is a multi-skill repository. Each skill lives in
`skills/<skill-name>/`, and every skill directory contains its own
`SKILL.md`.

## Current skills

- `website-capability-to-skill`

## Directory structure

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

## Installation (`npx skills`)

```bash
# List installable skills
npx -y skills add JasirVoriya/voriya-skills --list

# Install to Codex (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Install to Cursor (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
