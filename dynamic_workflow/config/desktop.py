# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

from frappe import _


def get_data():
    return [
        {
            "module_name": "Dynamic Workflow",
            "color": "#FF6B6B",
            "icon": "octicon octicon-git-branch",
            "type": "module",
            "label": _("Dynamic Workflow 3.0"),
            "description": _("Advanced workflow engine with approval matrix, dynamic nodes, and business actions"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Approval Matrix",
                    "label": _("Approval Matrix"),
                    "description": _("Define approval rules based on amount, department, business line, etc.")
                },
                {
                    "type": "doctype",
                    "name": "Dynamic Workflow Config",
                    "label": _("Workflow Configuration"),
                    "description": _("Configure dynamic workflow with nodes and business actions")
                },
                {
                    "type": "doctype",
                    "name": "Approval Log",
                    "label": _("Approval Timeline"),
                    "description": _("View approval records with comments and attachments")
                },
                {
                    "type": "doctype",
                    "name": "Approval Delegation",
                    "label": _("Approval Delegation"),
                    "description": _("Delegate approvals to other users")
                },
                {
                    "type": "doctype",
                    "name": "Workflow Timeout Escalation",
                    "label": _("Timeout Escalation"),
                    "description": _("Manage approval timeouts and escalations")
                },
                {
                    "type": "report",
                    "name": "Workflow Analytics",
                    "label": _("Workflow Analytics"),
                    "description": _("Analyze approval metrics and performance")
                },
            ]
        }
    ]
