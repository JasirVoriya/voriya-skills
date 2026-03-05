# Руководство website capability to skill

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) |
[한국어](./README.ko.md) | [Português (Brasil)](./README.pt-BR.md) | Русский

Этот skill принимает URL сайта, изучает его возможности через браузер и
преобразует их в локальный skill в формате API-first.

Вам не нужно вручную разбирать API и проектировать поток восстановления
аутентификации.

## Автор

- Автор: `JasirVoriya`
- Команда: `Infrastructure Storage Team`
- Email: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## Основные правила (важно)

Чтобы сгенерированный skill был переиспользуемым и автоматизируемым:

- Браузер используется только для изучения возможностей и восстановления auth.
- Бизнес-операции выполняются через API, без зависимости от веб-кнопок.
- Auth-файл хранится в `~/.<site>-auth.yaml` в домашнем каталоге.
- Перед каждой API-сессией auth-файл читается.
- При ошибке/истечении auth данные заново извлекаются из браузера.
- Права файла фиксируются как `0600`.

## Что умеет skill

- Выявлять видимые возможности целевого сайта.
- Маппить UI-возможности на API-методы, структуру запроса и ответа.
- Генерировать рабочий scaffold skill для конкретного сайта.
- Встраивать жизненный цикл auth: чтение, проверка, восстановление, retry.
- Формировать отчёт о проверке (поддерживается/не поддерживается).

## Установка (`npx skills add`)

Если вы устанавливаете skills как `npx skills add openclaw/openclaw`, этот
skill также можно установить напрямую из этого GitHub-репозитория.

### 1) Показать устанавливаемые skills в репозитории

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Установить в Codex (глобально)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Установить в Cursor (глобально)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Сценарий multi-skill репозитория (опционально)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

После установки перезапустите AI-клиент.

## Примеры промптов

### 1) Базовая генерация

```text
Используй website-capability-to-skill для анализа https://example.com,
преобразуй возможности сайта в API-first skill,
и выведи полную структуру каталогов.
```

### 2) Генерация с ограничением области

```text
Используй website-capability-to-skill для анализа https://example.com,
покрой только "админ-консоль после входа + поток публикации",
остальное пометь как unsupported-via-api.
```

### 3) Принудительное восстановление auth

```text
Используй website-capability-to-skill для генерации skill и проверки API.
Если auth не проходит, забери cookie/token из браузера,
запиши в ~/.<site>-auth.yaml и повтори.
```

### 4) Отчёт о проверке

```text
После генерации через website-capability-to-skill
сформируй отчёт: поддержанные возможности,
неподдержанные, причины ошибок и следующие шаги.
```

## Быстрые команды (скрипты)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Артефакты

Минимальный набор:

- Site-specific `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- Результат проверки (поддерживается/не поддерживается/доказательства)

## Предварительные условия

- Доступный URL целевого сайта
- Сеанс браузера с доступом и возможностью работы на сайте
- Локальная среда Python 3

Если сайт требует логин, заранее подготовьте рабочий аккаунт.
