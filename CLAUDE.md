# {{app_name}} — Claude Code Instructions

## MANDATORY: Frappe Skill

**RULE:** Before writing ANY Frappe code, answering ANY Frappe question, or making ANY plan — invoke the `frappe-erpnext-expert` skill. No exceptions.

Trigger: any prompt containing frappe, erpnext, doctype, hooks, bench, custom field, print format, salary slip, sales invoice, purchase invoice, stock entry, workflow, fixtures, whitelist, server script, client script, patch, migration.

## Brain MCP Tools (use before guessing)

Always available in Claude Code sessions. Call these FIRST for any field/hook/pattern question:

- `mcp__frappe-brain__frappe_corpus_search` — ripgrep 615 Frappe repos
- `mcp__frappe-brain__frappe_find_doctype` — locate DocType JSON + controllers
- `mcp__frappe-brain__frappe_find_hook` — find hooks.py registrations
- `mcp__frappe-brain__frappe_knowledge_search` — semantic search (Voyage embeddings)
- `mcp__frappe-brain__frappe_get_print_format` — 481 Enfono print formats
- `mcp__frappe-brain__frappe_client_context` — per-client merged config

**Do NOT guess field names, hook signatures, or v15 API behavior. Brain corpus is ground truth.**

## Project Context

- **App:** `{{app_name}}`
- **Client:** `{{client_name}}`
- **Region:** `{{region}}` (KSA / UAE / India)
- **Frappe version:** v15 (default unless bench shows otherwise)
- **Bench root:** `/home/frappe/frappe-bench/` (or per-client path)

## Key Files — Read First on Any Task

```
apps/{{app_name}}/
├── hooks.py                          # Extension points — read before adding any
├── {{app_name}}/
│   ├── config/
│   │   └── desktop.py                # Module icons
│   ├── patches.txt                   # Migration order — add new patches here
│   ├── patches/                      # Patch scripts per version
│   ├── fixtures/                     # Exported Custom Fields, Property Setters, Workflows
│   └── <module>/
│       └── doctype/
│           └── <doctype>/
│               ├── <doctype>.json    # DocType definition — source of truth for fields
│               ├── <doctype>.py      # Controller — lifecycle hooks go here
│               ├── <doctype>.js      # Client script
│               └── test_<doctype>.py # Tests — required for accounting/stock DocTypes
```

## Hard Rules (non-negotiable)

### Database
- ❌ `frappe.db.sql(f"… {var} …")` — SQL injection blocker
- ✅ `frappe.qb` by default; raw SQL only parameterised: `frappe.db.sql("WHERE name = %s", (val,))`
- ✅ Right reader: `get_value` (one field), `get_list` (perms), `get_all` (no perms), `get_doc` (full), `get_cached_doc` (cached)

### Type Coercion
- ❌ `int(x)`, `float(x)`, `str(x)` on user input
- ✅ `cint(x)`, `flt(x)`, `cstr(x)` from `frappe.utils`

### Whitelisted Methods
- Every `@frappe.whitelist()` that touches a specific doc: call `frappe.has_permission(doctype, ptype, doc=name)`
- `allow_guest=True` requires code comment justification

### Errors
- User-facing: `frappe.throw(_("Message"))` — translatable, halts execution
- Diagnostic: `frappe.log_error(message, title)` — never interrupts
- Never `print()` in production. Never bare `raise Exception()` for user errors.

### Translations
- Every user-visible string: `_()` in Python, `__()` in JavaScript

### Hooks vs Controllers
- DocType lifecycle (`validate`, `on_submit`, etc.) → controller class in `.py`
- `hooks.py doc_events` → only for extending OTHER apps' DocTypes

### Customisations
- ❌ Never edit `apps/frappe/` or `apps/erpnext/` directly
- ✅ Custom Fields / Property Setters → fixtures, regenerated with `bench export-fixtures`
- ✅ Schema changes → patch in `patches/<version>/<name>.py` + `patches.txt`

### Performance
- N+1 in a loop = blocker. Use `filters={"name": ["in", [...]]}` batch fetch
- >30s operations → `frappe.enqueue(method, queue="long", enqueue_after_commit=True)`

## Regional Defaults

| Region | VAT | Currency | Compliance |
|--------|-----|----------|------------|
| KSA    | 15% | SAR      | ZATCA Phase 2, bilingual prints |
| UAE    | 5%  | AED      | VAT, bilingual prints |
| India  | GST | INR      | india-compliance app |

## Quick Reference

| Task | API |
|------|-----|
| Get one field | `frappe.db.get_value(dt, name, field)` |
| Get a doc | `frappe.get_doc(dt, name)` |
| Cached doc | `frappe.get_cached_doc(dt, name)` |
| Get many (perms) | `frappe.get_list(dt, filters, fields)` |
| Get many (no perms) | `frappe.get_all(dt, filters, fields)` |
| Insert | `doc = frappe.get_doc({...}); doc.insert()` |
| Translate | `_("text")` (Py) / `__("text")` (JS) |
| Throw user error | `frappe.throw(_("..."))` |
| Log error | `frappe.log_error(message, title)` |
| Background job | `frappe.enqueue(method, queue, enqueue_after_commit=True)` |
| Permission check | `frappe.has_permission(dt, ptype, doc)` |
| Coerce int/float/str | `cint`, `flt`, `cstr` from `frappe.utils` |

## Bench Commands

```bash
# Run tests for this app
bench --site <site> run-tests --app {{app_name}}

# Export fixtures after UI changes
bench --site <site> export-fixtures --app {{app_name}}

# Apply patches after migration changes
bench --site <site> migrate

# Clear cache after hooks.py change
bench --site <site> clear-cache

# Watch JS/CSS changes
bench watch
```

## Commit Standards

```
feat(doctype): add ZATCA QR to Sales Invoice print
fix(hooks): remove N+1 query in purchase receipt validate
chore(fixtures): export updated Custom Fields for Sales Invoice
patch(v1_0): rename field old_name → new_name in Customer
test(sales_invoice): add test for duplicate billing validation
```
