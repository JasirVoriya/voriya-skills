# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | Français | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Ce dépôt contient plusieurs skills. Chaque skill se trouve dans
`skills/<skill-name>/`, et chaque dossier de skill contient son propre
`SKILL.md`.

## Skills actuels

- `website-capability-to-skill`

## Structure du répertoire

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
# Lister les skills installables
npx -y skills add JasirVoriya/voriya-skills --list

# Installer dans Codex (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Installer dans Cursor (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
