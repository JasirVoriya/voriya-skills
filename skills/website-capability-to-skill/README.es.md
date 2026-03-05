# Guía de website capability to skill

[简体中文](./README.md) | [English](./README.en.md) | Español |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

Este skill toma una URL de sitio web, estudia sus capacidades mediante el
navegador y las convierte en un skill local con enfoque API-first.

No necesitas mapear APIs manualmente ni diseñar por tu cuenta el flujo de
recuperación de autenticación.

## Autor

- Autor: `JasirVoriya`
- Equipo: `Infrastructure Storage Team`
- Correo: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## Reglas clave (importante)

Para que el skill generado sea reutilizable y automatizable, se aplican estas
reglas por defecto:

- Usa el navegador solo para descubrir capacidades y recuperar autenticación.
- Ejecuta operaciones de negocio por API, no por clics de la web.
- Guarda la autenticación en `~/.<site>-auth.yaml` en el directorio home.
- Lee el archivo de autenticación antes de cada sesión API.
- Si falla o expira la autenticación, extrae datos del navegador y reescribe.
- Mantén permisos del archivo en `0600`.

## Qué puede hacer

- Descubrir capacidades visibles del sitio objetivo.
- Mapear capacidades de UI a métodos API, requests y responses.
- Generar un scaffold ejecutable de skill específico para el sitio.
- Integrar ciclo de autenticación: leer, validar, recuperar y reintentar.
- Entregar un informe de validación con capacidades soportadas y no soportadas.

## Instalación (`npx skills add`)

Si quieres instalar este skill como `npx skills add openclaw/openclaw`, puedes
instalarlo directamente desde este repositorio de GitHub.

### 1) Ver skills instalables en el repositorio

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Instalar en Codex (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Instalar en Cursor (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Escenario de repositorio multi-skill (opcional)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

Después de instalar, reinicia tu cliente de IA para cargar el skill.

## Ejemplos de prompt

### 1) Generación básica

```text
Usa website-capability-to-skill para analizar https://example.com,
convierte capacidades del sitio en un skill API-first,
y entrega el directorio completo.
```

### 2) Generación con alcance acotado

```text
Usa website-capability-to-skill para analizar https://example.com,
cubre solo "consola admin tras login + flujo de publicación",
y marca el resto como unsupported-via-api.
```

### 3) Recuperación forzada de autenticación

```text
Usa website-capability-to-skill para generar el skill y validar APIs.
Si falla la autenticación, toma cookie/token del navegador,
guárdalos en ~/.<site>-auth.yaml y reintenta.
```

### 4) Informe de validación

```text
Tras generar con website-capability-to-skill,
entrega un informe con capacidades soportadas,
capacidades no soportadas, causas de fallo y siguientes pasos.
```

## Comandos rápidos (scripts)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Entregables

Como mínimo incluye:

- `SKILL.md` específico del sitio
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- Resultado de validación (soportado/no soportado/evidencia)

## Requisitos previos

- URL del sitio objetivo accesible
- Sesión de navegador con acceso y capacidad de operar el sitio
- Entorno local con Python 3

Si el sitio requiere login, prepara una cuenta válida para facilitar la
extracción de datos en la recuperación de autenticación.
