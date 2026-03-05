# Website capability to skill Anleitung

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) | Deutsch |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Dieses Skill nimmt eine Website-URL, analysiert die Fähigkeiten über den
Browser und wandelt sie in ein lokales API-first Skill um.

Du musst APIs nicht manuell zuordnen und keinen eigenen Auth-Recovery-Flow
entwerfen.

## Autor

- Autor: `JasirVoriya`
- Team: `Infrastructure Storage Team`
- E-Mail: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## Kernregeln (wichtig)

Damit das generierte Skill automatisierbar und wiederverwendbar bleibt:

- Browser nur für Capability-Discovery und Auth-Recovery verwenden.
- Fachliche Aktionen über APIs ausführen, nicht über Web-Buttons.
- Auth-Daten in `~/.<site>-auth.yaml` im Home-Verzeichnis speichern.
- Auth-Datei vor jeder API-Sitzung einlesen.
- Bei Ablauf/Fehler Auth aus Browser extrahieren und zurückschreiben.
- Dateiberechtigung auf `0600` setzen.

## Was das Skill kann

- Sichtbare Fähigkeiten der Zielwebsite erkennen.
- UI-Fähigkeiten auf API-Methoden, Request- und Response-Formen mappen.
- Ein lauffähiges, websitespezifisches Skill-Scaffold erzeugen.
- Auth-Lebenszyklus integrieren: lesen, prüfen, wiederherstellen, retry.
- Verifizierungsbericht zu unterstützten/nicht unterstützten Fähigkeiten liefern.

## Installation (`npx skills add`)

Du kannst dieses Skill wie `npx skills add openclaw/openclaw` direkt aus diesem
GitHub-Repository installieren.

### 1) Installierbare Skills im Repository anzeigen

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) In Codex installieren (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) In Cursor installieren (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Multi-Skill-Repository (optional)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

Nach der Installation den AI-Client neu starten.

## Prompt-Beispiele

### 1) Basis-Generierung

```text
Nutze website-capability-to-skill für https://example.com,
wandle Website-Fähigkeiten in ein API-first Skill um,
und gib die vollständige Verzeichnisstruktur aus.
```

### 2) Generierung mit Umfang

```text
Nutze website-capability-to-skill für https://example.com,
decke nur "Admin-Konsole nach Login + Publish-Flow" ab,
und markiere den Rest als unsupported-via-api.
```

### 3) Erzwinge Auth-Recovery

```text
Nutze website-capability-to-skill, generiere das Skill und validiere APIs.
Wenn Auth fehlschlägt, hole Cookie/Token aus dem Browser,
schreibe nach ~/.<site>-auth.yaml und wiederhole.
```

### 4) Verifizierungsbericht

```text
Nach der Generierung mit website-capability-to-skill,
erstelle einen Bericht mit unterstützten Fähigkeiten,
nicht unterstützten Fähigkeiten, Fehlerursachen und nächsten Schritten.
```

## Schnellbefehle (Skripte)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Artefakte

Mindestens enthalten:

- Website-spezifische `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- Verifizierungsergebnis (unterstützt/nicht unterstützt/Evidenz)

## Voraussetzungen

- Erreichbare Ziel-Website-URL
- Browser-Sitzung mit Zugriff und Bedienmöglichkeit der Website
- Lokale Python-3-Umgebung

Wenn Login erforderlich ist, vorher ein gültiges Konto vorbereiten.
