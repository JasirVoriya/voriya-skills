# voriya-skills

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) | 한국어 |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

이 저장소는 여러 skill을 포함한 저장소입니다. 각 skill은
`skills/<skill-name>/` 경로에 있으며, 각 skill 디렉터리에는 자체
`SKILL.md`가 포함됩니다.

## 현재 skills

- `website-capability-to-skill`

## 디렉터리 구조

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

## 설치 (`npx skills`)

```bash
# 설치 가능한 skills 목록 보기
npx -y skills add JasirVoriya/voriya-skills --list

# Codex에 설치 (전역)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y

# Cursor에 설치 (전역)
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```
