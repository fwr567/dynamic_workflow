import frappe
from frappe.utils import nowdate


def sync_delegations():
    """Scheduler entry point: expire outdated delegations daily.

    Called by hooks.py scheduler_events (daily).
    Sets status to 'Expired' for delegations whose to_date has passed.
    """
    today = nowdate()
    expired = frappe.get_all(
        "Approval Delegation",
        filters={
            "status": "Active",
            "to_date": ["<", today],
        },
        pluck="name",
    )

    for name in expired:
        frappe.db.set_value("Approval Delegation", name, "status", "Expired")
        frappe.db.set_value("Approval Delegation", name, "is_active", 0)

    if expired:
        frappe.db.commit()


def get_delegatee(approver, document_type=None):
    """Get the active delegatee for an approver.

    Args:
        approver: User email ID of the original approver.
        document_type: Optional DocType name to filter delegations.

    Returns:
        str or None: User email ID of the delegatee, or None if no active delegation.
    """
    today = nowdate()
    filters = {
        "delegator": approver,
        "is_active": 1,
        "status": "Active",
        "from_date": ["<=", today],
        "to_date": [">=", today],
    }

    delegations = frappe.get_all(
        "Approval Delegation",
        filters=filters,
        fields=["delegatee", "document_types"],
    )

    for delegation in delegations:
        if not delegation.document_types:
            return delegation.delegatee

        allowed_types = [
            dt.strip() for dt in delegation.document_types.split(",") if dt.strip()
        ]
        if document_type in allowed_types:
            return delegation.delegatee

    return None
