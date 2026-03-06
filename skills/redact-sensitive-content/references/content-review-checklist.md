# Content Review Checklist

Use this checklist before Markdown content is published, committed to a public repository, or shared outside a trusted environment.

## Goal

Preserve the technical value of the document while removing data that can identify people, customers, systems, environments, or credentials.

## Review Categories

### Personal Information

Redact or generalize:

- email addresses
- phone numbers
- ID numbers
- home or office addresses
- internal usernames, chat IDs, employee IDs
- real names when the identity is not important to the explanation

Preferred replacements:

- `someone@example.com`
- `138****5678`
- `用户 A`
- `工程师 B`

### Internal Infrastructure

Redact or generalize:

- private IP addresses such as `10.x.x.x`, `172.16.x.x`, `192.168.x.x`
- internal domains, VPN addresses, service discovery names
- hostnames, cluster names, namespace names, pod names
- local filesystem paths that expose real usernames or machine layout
- callback URLs, admin URLs, and dashboards that expose internal routes

Preferred replacements:

- `10.x.x.x`
- `internal.example.com`
- `cluster-a`
- `/path/to/project`

### Secrets and Credentials

Never publish:

- API keys
- bearer tokens
- JWTs
- cookies
- passwords
- webhook secrets
- private keys
- signed URLs that still work

Preferred replacements:

- `***REDACTED***`
- `YOUR_API_KEY`
- `YOUR_TOKEN`

### Business-Sensitive Content

Review carefully:

- customer names
- contract identifiers
- order or ticket numbers
- internal issue tracker URLs
- unpublished roadmap details
- screenshots showing dashboards, alerts, logs, or internal links

Preferred replacements:

- `某客户`
- `工单 12345`
- cropped or recreated screenshots

## Review Method

1. Read the document once for meaning.
2. Inspect code blocks, logs, stack traces, commands, and screenshots.
3. Run `scripts/scan_sensitive_content.py` on the file or directory.
4. Patch every unsafe finding.
5. Re-run the scanner.
6. Only then publish or share the content.

## Review Principle

When in doubt, prefer abstraction over realism. The public lesson matters more than the exact private context.
