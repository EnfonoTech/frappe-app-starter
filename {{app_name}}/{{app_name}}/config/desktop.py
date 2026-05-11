from frappe import _


def get_data():
    return [
        {
            "module_name": "{{app_title}}",
            "color": "blue",
            "icon": "octicon octicon-file-directory",
            "type": "module",
            "label": _("{{app_title}}"),
        }
    ]
