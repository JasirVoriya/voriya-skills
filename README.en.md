# voriya-skills

[简体中文](./README.md) | English | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

`voriya-skills` is a practical skill repository for AI agents. The current
focus is converting visible website capabilities into callable API-first
skills.

This repo is for you if you:

- want to turn browser workflows into reusable API workflows,
- need to distribute skills in Codex or Cursor, and
- want to avoid manual auth-recovery glue code.

## 10-second quick start

Run the command below to install the skill into Codex.

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

Then send this prompt to your AI assistant.

```text
Use the website-capability-to-skill skill to analyze https://example.com,
convert the website capabilities into an API-first skill, and output the full
folder.
```

## Current skill

- `website-capability-to-skill`
  - learns capabilities from a target website URL,
  - enforces "discover by browser, execute by API," and
  - wires auth cache and refresh via `~/.<site>-auth.yaml`.

## Installation (`npx skills`)

List all installable skills in this repository:

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

Install to Cursor (global):

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

## Repository structure

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

## Growth playbook

For GitHub topic recommendations and a weekly release cadence template, see
[docs/repo-growth-playbook.md](./docs/repo-growth-playbook.md).
