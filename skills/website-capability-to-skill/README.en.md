# Website capability to skill guide

[简体中文](./README.md) | English | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

This skill takes a website URL, learns what the site can do through browser
inspection, and converts those capabilities into a local API-first skill.

You do not need to map APIs manually or design the auth-recovery flow yourself.

## Author

- Author: `JasirVoriya`
- Team: `Infrastructure Storage Team`
- Email: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## Core rules (important)

To keep the generated skill reusable and automatable, the skill follows these
rules by default:

- Use the browser only for two tasks: capability discovery and auth recovery.
- Run business operations through APIs, not web-button automation.
- Save auth data under the user home directory as `~/.<site>-auth.yaml`.
- Read the auth file before every API session.
- If auth expires or fails, extract fresh auth from browser and write back.
- Keep auth file permission set to `0600`.

## What it can do

From a user perspective, this skill can:

- Discover capabilities exposed by the target website.
- Map UI capabilities to API methods, request shapes, and response shapes.
- Generate a runnable site-specific skill scaffold.
- Integrate auth lifecycle: read, validate, recover, and retry.
- Produce a verification report with supported and unsupported capabilities.

## Installation (`npx skills add`)

If you want to install this skill like `npx skills add openclaw/openclaw`,
install it directly from this GitHub repository.

### 1) List installable skills in the repository

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Install to Codex (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Install to Cursor (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Multi-skill repository scenario (optional)

If you later host multiple skills in one repository, install by skill name:

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

After installation, restart your AI client to load the new skill.

## Trigger words and scenarios

You can trigger this skill by naming the skill directly or by stating the
capability goal.

- Trigger words: `website-capability-to-skill`, `website to skill`,
  `API-first skill`
- Trigger scenarios: capability discovery, API mapping, skill scaffolding, auth
  recovery integration
- Minimum input: a target website URL, for example `https://example.com`
- Expected output: generated skill folder, capability map, auth flow, and
  verification result

## Prompt examples

You can copy these prompts directly.

### 1) Basic generation

```text
Use website-capability-to-skill to analyze https://example.com,
convert site capabilities into an API-first skill,
and output the complete directory.
```

### 2) Scoped generation

```text
Use website-capability-to-skill to analyze https://example.com,
cover only "post-login admin console + publishing flow",
and mark all other capabilities as unsupported-via-api.
```

### 3) Forced auth recovery

```text
Use website-capability-to-skill to generate the skill and validate APIs.
If auth fails, fetch cookie/token from browser,
write them to ~/.<site>-auth.yaml, then retry.
```

### 4) Verification report

```text
After generation with website-capability-to-skill,
provide a verification report with supported capabilities,
unsupported capabilities, failure causes, and next-step suggestions.
```

## Quick commands (scripts)

You can also run built-in scripts directly:

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Deliverables

At minimum, the output includes:

- Site-specific `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- A capability verification result (supported/unsupported/evidence)

## Prerequisites

Prepare the following:

- A reachable target website URL
- A browser session that can access and operate the target site
- A local Python 3 runtime

If the target site requires login, prepare a usable account in advance so auth
recovery can extract required data.
