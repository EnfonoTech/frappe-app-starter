# apps/{{app_name}}/{{app_name}}/hooks.py
"""
hooks.py — extension points for this app.

RULE: DocType lifecycle events (validate, on_submit, etc.) go in the
controller class. Use doc_events here ONLY when extending another app's DocType.

See brain corpus: frappe_find_hook("doc_events") for patterns.
"""

from . import __version__ as app_version

# ─── App metadata ──────────────────────────────────────────────────────────
app_name = "{{app_name}}"
app_title = "{{app_title}}"
app_publisher = "Enfono Technologies"
app_description = ""
app_email = "team@enfono.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

# ─── DocType JS / List JS overrides ───────────────────────────────────────
# doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}
# doctype_list_js = {"Sales Invoice": "public/js/sales_invoice_list.js"}

# ─── Document Events (extending OTHER apps' DocTypes only) ────────────────
doc_events = {
    # "Sales Invoice": {
    #     "on_submit": "{{app_name}}.overrides.sales_invoice.on_submit",
    # },
}

# ─── Scheduled Tasks ──────────────────────────────────────────────────────
scheduler_events = {
    # "daily": ["{{app_name}}.tasks.daily"],
    # "cron": {"0 9 * * 1-5": ["{{app_name}}.tasks.weekday_morning"]},
}

# ─── Fixtures ─────────────────────────────────────────────────────────────
# Run: bench --site <site> export-fixtures --app {{app_name}}
fixtures = [
    # {"dt": "Custom Field", "filters": [["dt", "in", ["Sales Invoice"]]]},
    # {"dt": "Property Setter", "filters": [["doc_type", "in", ["Sales Invoice"]]]},
    # {"dt": "Print Format", "filters": [["module", "=", "{{app_title}}"]]}
]

# ─── Override DocType class (last resort — try doc_events first) ───────────
# override_doctype_class = {
#     "Sales Invoice": "{{app_name}}.overrides.sales_invoice.CustomSalesInvoice",
# }

# ─── Install / Migrate lifecycle ──────────────────────────────────────────
# after_install = "{{app_name}}.install.after_install"
# after_migrate = ["{{app_name}}.migrate.after_migrate"]
