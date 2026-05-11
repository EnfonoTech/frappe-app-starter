# {{app_title}}

Frappe custom app for {{client_name}} — {{region}}.

## Setup

```bash
bench get-app https://github.com/EnfonoTech/{{repo_name}}
bench --site <site> install-app {{app_name}}
bench --site <site> migrate
```

## Development

```bash
# Run tests
bench --site <site> run-tests --app {{app_name}}

# Export fixtures after UI changes
bench --site <site> export-fixtures --app {{app_name}}

# Watch assets
bench watch
```

## AI Assistance

This repo has `CLAUDE.md` — Claude Code auto-loads Enfono's brain corpus (615 Frappe repos) before answering any question. Every PR is automatically reviewed by the brain bot.

Edit `CLAUDE.md` → update `{{app_name}}`, `{{client_name}}`, `{{region}}` placeholders.
