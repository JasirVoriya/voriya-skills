# Guia de website capability to skill

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) |
[한국어](./README.ko.md) | Português (Brasil) | [Русский](./README.ru.md)

Este skill recebe uma URL de site, aprende as capacidades via navegador e
converte essas capacidades em um skill local API-first.

Você não precisa mapear APIs manualmente nem desenhar o fluxo de recuperação
de autenticação por conta própria.

## Autor

- Autor: `JasirVoriya`
- Equipe: `Infrastructure Storage Team`
- E-mail: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## Regras centrais (importante)

Para manter o skill gerado reutilizável e automatizável:

- Use o navegador apenas para descoberta de capacidades e recuperação de auth.
- Execute operações de negócio via API, sem depender de botões da web.
- Salve auth em `~/.<site>-auth.yaml` no diretório home do usuário.
- Leia o arquivo de auth antes de cada sessão de API.
- Se auth expirar ou falhar, extraia do navegador e grave novamente.
- Mantenha permissão do arquivo como `0600`.

## O que ele faz

- Descobre capacidades visíveis do site alvo.
- Mapeia capacidades de UI para métodos API, request e response.
- Gera scaffold executável de skill específico por site.
- Integra ciclo de auth: leitura, validação, recuperação e retry.
- Entrega relatório de validação com capacidades suportadas e não suportadas.

## Instalação (`npx skills add`)

Se você instala skills com `npx skills add openclaw/openclaw`, pode instalar
este skill diretamente deste repositório GitHub.

### 1) Listar skills instaláveis no repositório

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Instalar no Codex (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Instalar no Cursor (global)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) Cenário de repositório multi-skill (opcional)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

Após instalar, reinicie o cliente de IA para carregar o novo skill.

## Exemplos de prompt

### 1) Geração básica

```text
Use website-capability-to-skill para analisar https://example.com,
converta as capacidades do site em um skill API-first,
e mostre a estrutura completa de diretórios.
```

### 2) Geração com escopo

```text
Use website-capability-to-skill para analisar https://example.com,
cubra apenas "console admin pós-login + fluxo de publicação",
e marque o restante como unsupported-via-api.
```

### 3) Recuperação forçada de auth

```text
Use website-capability-to-skill para gerar o skill e validar APIs.
Se auth falhar, extraia cookie/token do navegador,
salve em ~/.<site>-auth.yaml e tente novamente.
```

### 4) Relatório de validação

```text
Depois de gerar com website-capability-to-skill,
forneça um relatório com capacidades suportadas,
não suportadas, causas de falha e próximos passos.
```

## Comandos rápidos (scripts)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## Entregáveis

No mínimo, inclua:

- `SKILL.md` específico do site
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- Resultado de validação (suportado/não suportado/evidência)

## Pré-requisitos

- URL de site alvo acessível
- Sessão de navegador capaz de acessar e operar o site alvo
- Ambiente local com Python 3

Se o site exigir login, prepare uma conta válida com antecedência.
