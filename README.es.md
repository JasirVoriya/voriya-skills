# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) | Español |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Este es un repositorio con múltiples skills. Cada skill se encuentra en
`skills/<skill-name>/`, y cada directorio de skill incluye su propio
`SKILL.md`.

## Skills actuales

- `website-capability-to-skill`

## Estructura del directorio

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

## Instalación (`npx skills`)

```bash
# Listar skills instalables
npx -y skills add JasirVoriya/voriya-skills --list

# Instalar en Codex (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Instalar en Cursor (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
