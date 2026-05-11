# {{app_title}}

Frappe/ERPNext custom app for {{client_name}} ({{region}}).

Built on [EnfonoTech/frappe-app-starter](https://github.com/EnfonoTech/frappe-app-starter).

## Quick Start

```bash
bench get-app https://github.com/EnfonoTech/{{repo_name}}
bench --site <site> install-app {{app_name}}
bench --site <site> migrate
```

## Dev Guide

See [TEAM.md](../TEAM.md) — setup, Claude Code usage, PR review, hard rules.

## Commands

```bash
bench --site <site> run-tests --app {{app_name}}
bench --site <site> export-fixtures --app {{app_name}}
bench --site <site> migrate
bench --site <site> clear-cache
```
