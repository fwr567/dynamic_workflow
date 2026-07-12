import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    """Create custom fields on supported DocTypes after app installation."""
    create_dw_custom_fields()
    frappe.db.commit()


def after_migrate():
    """Ensure custom fields are up to date after bench migrate."""
    create_dw_custom_fields()
    frappe.db.commit()


def create_dw_custom_fields():
    """Create Dynamic Workflow custom fields on ERPNext transaction DocTypes.

    Only creates fields on DocTypes that actually exist in the current site.
    Each DocType is processed independently so a validation error on one
    DocType (e.g. broken links from a removed third-party app) does not
    block the others.
    """
    target_doctypes = [
        "Material Request",
        "Purchase Order",
        "Sales Order",
    ]

    fields = _get_custom_fields()

    for doctype in target_doctypes:
        if not frappe.db.table_exists(doctype):
            continue

        try:
            create_custom_fields({doctype: fields}, update=True)
        except Exception as e:
            frappe.log_error(
                title=f"Dynamic Workflow - Custom Field Error ({doctype})",
                message=str(e),
            )
            frappe.clear_last_message()


def _get_custom_fields():
    """Return the list of custom field definitions for Dynamic Workflow."""
    return [
        {
            "fieldname": "dw_workflow_section",
            "label": "Dynamic Workflow",
            "fieldtype": "Section Break",
            "insert_after": "",
            "collapsible": 1,
            "translatable": 0,
        },
        {
            "fieldname": "dw_workflow_config",
            "label": "Workflow Config",
            "fieldtype": "Link",
            "options": "Dynamic Workflow Config",
            "insert_after": "dw_workflow_section",
            "translatable": 0,
        },
        {
            "fieldname": "dw_status",
            "label": "Approval Status",
            "fieldtype": "Select",
            "options": "\nPending\nIn Progress\nApproved\nRejected\nReturned\nTerminated\nRecalled",
            "insert_after": "dw_workflow_config",
            "default": "",
            "read_only": 1,
            "translatable": 0,
        },
        {
            "fieldname": "dw_approval_chain",
            "label": "Approval Chain",
            "fieldtype": "JSON",
            "insert_after": "dw_status",
            "read_only": 1,
            "hidden": 1,
            "translatable": 0,
        },
        {
            "fieldname": "dw_current_node",
            "label": "Current Node",
            "fieldtype": "Int",
            "insert_after": "dw_approval_chain",
            "default": "0",
            "read_only": 1,
            "hidden": 1,
            "translatable": 0,
        },
    ]
