# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) | Deutsch |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Dieses Repository enthält mehrere Skills. Jeder Skill liegt unter
`skills/<skill-name>/`, und jedes Skill-Verzeichnis enthält eine eigene
`SKILL.md`.

## Aktuelle skills

- `website-capability-to-skill`

## Verzeichnisstruktur

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
# Installierbare Skills auflisten
npx -y skills add JasirVoriya/voriya-skills --list

# In Codex installieren (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# In Cursor installieren (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
