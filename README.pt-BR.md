# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) |
[한국어](./README.ko.md) | Português (Brasil) | [Русский](./README.ru.md)

Este é um repositório com múltiplas skills. Cada skill fica em
`skills/<skill-name>/`, e cada diretório de skill contém seu próprio
`SKILL.md`.

## Skills atuais

- `website-capability-to-skill`

## Estrutura de diretórios

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

## Instalação (`npx skills`)

```bash
# Listar skills instaláveis
npx -y skills add JasirVoriya/voriya-skills --list

# Instalar no Codex (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Instalar no Cursor (global)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
