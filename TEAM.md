# Enfono Brain — Developer Guide

> AI-powered coding assistant for Frappe/ERPNext development. Searches 615 real Frappe repos before answering your questions.

---

## What Is It?

**Enfono Brain** is a VPS that stores every official Frappe/ERPNext repo + 600+ community apps as a searchable index. When you use Claude Code in any Enfono project, it automatically searches this corpus before answering — so you get answers based on actual Frappe source code, not guesses.

Two things it does for you:

1. **Smart code assistance** — Claude searches real Frappe patterns before suggesting code
2. **Automatic PR review** — every PR you open gets reviewed for Frappe anti-patterns (SQL injection, missing permissions, N+1 queries, etc.)

---

## Setup

### New Project

1. Go to **[frappe-app-starter](https://github.com/EnfonoTech/frappe-app-starter)** → click **"Use this template"** → create your repo under `EnfonoTech/`

2. Clone to your bench:
   ```bash
   bench get-app https://github.com/EnfonoTech/your-repo-name
   bench --site yoursite.localhost install-app your_app_name
   ```

3. Edit `CLAUDE.md` in the repo — fill in 4 lines:
   ```
   {{app_name}}    → your_app_name
   {{app_title}}   → Your App Title
   {{client_name}} → Client Name
   {{region}}      → KSA / UAE / India
   ```

4. Open Claude Code in the repo folder. Done.

### Existing Project

Ask Sayanth to run the deploy script — it opens a PR on your repo with `CLAUDE.md` + the review workflow. Merge it and brain is live.

---

## Using Claude Code Day-to-Day

### Junior Developers (Claude Code desktop / VS Code extension)

Open Claude Code in your Frappe app folder. Just ask normally:

```
"Add a custom button on Purchase Receipt to create a Purchase Invoice"
"Why is my Sales Invoice validate() running twice?"
"Write a whitelisted method to get customer outstanding"
```

Claude will **automatically search the brain corpus** before answering. You'll see it call tools like `frappe_corpus_search` or `frappe_find_doctype` — that means it's checking real Frappe source, not guessing.

**Tip:** If Claude answers without searching, say:
> "Search the brain corpus first, then answer"

### Senior Developers (Cursor)

The brain MCP is available via mTLS. Ask Sayanth for your client certificate (`your-email.p12`). Once configured, same corpus tools are available in Cursor.

---

## Automatic PR Review

Every PR you open on a repo that has `brain-pr-review.yml` gets an automatic review comment within ~30 seconds.

The bot checks for:

| Category | What it catches |
|---|---|
| ❌ **Blockers** | SQL injection, missing permission checks, N+1 queries, `print()` in production, secrets in plain fields |
| ⚠️ **Warnings** | Missing translations `_()`, no tests for submittable DocTypes, sync operations that should use `frappe.enqueue` |
| ✅ **Looks Good** | Correct patterns, good use of Frappe APIs |
| 💡 **Brain Insights** | Similar patterns found in the corpus that apply to your change |

**Blockers = request changes.** Fix before merging. Warnings = suggestions, use judgment.

---

## Hard Rules (Claude enforces these)

These come from Frappe's own semgrep rules. Breaking them causes production bugs.

```python
# ❌ SQL injection — never do this
frappe.db.sql(f"SELECT * FROM tabCustomer WHERE name = '{name}'")

# ✅ Always parameterise
frappe.db.sql("SELECT * FROM tabCustomer WHERE name = %s", (name,))

# ❌ Type coercion on user input
qty = int(frappe.form_dict.qty)

# ✅ Use Frappe utils
qty = frappe.utils.cint(frappe.form_dict.qty)

# ❌ No permission check
@frappe.whitelist()
def get_invoice(name):
    return frappe.get_doc("Sales Invoice", name)

# ✅ Check permission first
@frappe.whitelist()
def get_invoice(name):
    frappe.has_permission("Sales Invoice", "read", doc=name, throw=True)
    return frappe.get_doc("Sales Invoice", name)
```

---

## File Structure (in every app)

```
your_app/
├── CLAUDE.md                    ← AI instructions (edit placeholders once)
├── .github/
│   └── workflows/
│       └── brain-pr-review.yml  ← auto PR review (don't edit)
├── your_app/
│   ├── hooks.py                 ← read this before adding anything
│   ├── patches.txt              ← append migrations here (never reorder)
│   ├── fixtures/                ← run `bench export-fixtures` after UI changes
│   └── your_module/
│       └── doctype/
│           └── your_doctype/
│               ├── your_doctype.json   ← field definitions
│               ├── your_doctype.py     ← controller (lifecycle hooks here)
│               ├── your_doctype.js     ← client script
│               └── test_your_doctype.py
```

---

## Common Commands

```bash
# Run tests
bench --site yoursite run-tests --app your_app

# Export fixtures after changing Custom Fields in UI
bench --site yoursite export-fixtures --app your_app

# Apply patches after migrate changes
bench --site yoursite migrate

# Clear cache after hooks.py change
bench --site yoursite clear-cache

# Watch JS/CSS
bench watch
```

---

## Help

- **Can't find how something works in Frappe?** Ask Claude — it searches the source.
- **Bot flagged a blocker you disagree with?** Ask Claude to explain, or ping Sayanth.
- **Brain MCP not connecting?** Ask Sayanth for your mTLS cert.
- **Template repo:** https://github.com/EnfonoTech/frappe-app-starter
