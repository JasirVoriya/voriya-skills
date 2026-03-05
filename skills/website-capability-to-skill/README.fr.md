# Guide website capability to skill

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | Français | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Ce skill prend une URL de site web, analyse ses capacités via le navigateur,
et les transforme en skill local API-first.

Vous n'avez pas besoin de cartographier les APIs manuellement ni de concevoir
vous-même le flux de récupération d'authentification.

## Auteur

- Auteur : `JasirVoriya`
- Équipe : `Infrastructure Storage Team`
- E-mail : `jasirvoriya@gmail.com`
- GitHub : `https://github.com/JasirVoriya`

## Règles principales (important)

Pour garantir la réutilisation et l'automatisation du skill généré :

- Utiliser le navigateur seulement pour découverte et récupération d'auth.
- Exécuter les actions métier par API, sans automatisation par boutons web.
- Stocker l'auth dans `~/.<site>-auth.yaml` sous le répertoire utilisateur.
- Lire ce fichier avant chaque session API.
- En cas d'expiration ou d'échec, extraire l'auth depuis le navigateur.
- Conserver les permissions du fichier à `0600`.

## Ce que le skill peut faire

- Découvrir les capacités visibles du site cible.
- Mapper les capacités UI vers méthodes API, requêtes et réponses.
- Générer un scaffold de skill exécutable, spécifique au site.
- Intégrer le cycle d'auth : lecture, validation, récupération et retry.
- Produire un rapport de validation (supporté / non supporté).

## Installation (`npx skills add`)

Pour installer ce skill comme `npx skills add openclaw/openclaw`, installez-le
directement depuis ce dépôt GitHub.

### 1) Lister les skills installables du dépôt

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Installer dans Codex (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Installer dans Cursor (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Cas dépôt multi-skill (optionnel)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

Après installation, redémarrez le client IA pour charger le skill.

## Exemples de prompts

### 1) Génération de base

```text
Utilise website-capability-to-skill pour analyser https://example.com,
convertis les capacités du site en skill API-first,
et fournis l'arborescence complète.
```

### 2) Génération avec périmètre

```text
Utilise website-capability-to-skill pour analyser https://example.com,
couvre uniquement "console admin post-login + flux de publication",
et marque le reste en unsupported-via-api.
```

### 3) Récupération d'auth forcée

```text
Utilise website-capability-to-skill pour générer le skill et valider les APIs.
Si l'auth échoue, récupère cookie/token depuis le navigateur,
écris-les dans ~/.<site>-auth.yaml puis relance.
```

### 4) Rapport de validation

```text
Après génération avec website-capability-to-skill,
fournis un rapport : capacités validées, non supportées,
causes d'échec et recommandations de suite.
```

## Commandes rapides (scripts)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Livrables

Au minimum :

- `SKILL.md` spécifique au site
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- Résultat de validation (supporté / non supporté / preuve)

## Prérequis

- URL de site cible accessible
- Session navigateur capable d'ouvrir et d'opérer le site
- Environnement local Python 3

Si le site exige une connexion, préparez un compte valide à l'avance.
