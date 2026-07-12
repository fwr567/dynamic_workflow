import json

import frappe
from frappe import _

from dynamic_workflow.dynamic_workflow.approval_actions import ApprovalAction
from dynamic_workflow.dynamic_workflow.approval_engine import ApprovalEngine
from dynamic_workflow.dynamic_workflow.dynamic_nodes import DynamicNodeEngine
from dynamic_workflow.dynamic_workflow.delegation import DelegationEngine


@frappe.whitelist()
def submit_approval(document_type, document_name, action, comments=None, forward_to=None, delegate_to=None):
    """
    Submit an approval action for a document.

    Args:
        document_type: DocType of the document.
        document_name: Name of the document.
        action: Approval action (Approve, Reject, Return, Forward, etc.).
        comments: Optional comments for the action.
        forward_to: User to forward to (for Forward action).
        delegate_to: User to delegate to (for Delegate action).

    Returns:
        dict: Result with status and message.
    """
    doc = frappe.get_doc(document_type, document_name)

    kwargs = {}
    if comments:
        kwargs["comments"] = comments
    if forward_to:
        kwargs["forward_to"] = forward_to
    if delegate_to:
        kwargs["delegate_to"] = delegate_to

    result = ApprovalAction.perform_action(doc, action, **kwargs)

    if action == "Approve" and doc.get("dw_status") == "Approved":
        _trigger_approval_actions(doc)

    return result


@frappe.whitelist()
def get_approval_logs(document_type, document_name, limit=50):
    """
    Get approval logs for a document.

    Args:
        document_type: DocType of the document.
        document_name: Name of the document.
        limit: Maximum number of logs to return.

    Returns:
        list[dict]: Approval log entries.
    """
    logs = frappe.get_all(
        "Approval Log",
        filters={
            "document_type": document_type,
            "document_name": document_name,
        },
        fields=[
            "name", "approver", "action", "action_date",
            "status", "approval_node", "comments",
            "forward_to", "additional_approvers", "duration_hours",
        ],
        order_by="action_date desc",
        limit_page_length=limit,
    )
    return logs


@frappe.whitelist()
def get_pending_approvals(user=None):
    """
    Get all pending approvals for a user.

    Args:
        user: User email ID. Defaults to current user.

    Returns:
        list[dict]: Pending approval entries.
    """
    if not user:
        user = frappe.session.user

    delegatee = DelegationEngine.get_delegatee(user)
    effective_user = delegatee or user

    logs = frappe.get_all(
        "Approval Log",
        filters={
            "approver": effective_user,
            "status": "Pending",
        },
        fields=[
            "name", "document_type", "document_name",
            "action", "action_date", "approval_node",
        ],
        order_by="action_date asc",
    )
    return logs


@frappe.whitelist()
def get_workflow_status(document_type, document_name):
    """
    Get the current workflow status for a document.

    Args:
        document_type: DocType of the document.
        document_name: Name of the document.

    Returns:
        dict: Workflow status information.
    """
    doc = frappe.get_doc(document_type, document_name)

    approval_chain = []
    if doc.get("dw_approval_chain"):
        try:
            approval_chain = frappe.parse_json(doc.get("dw_approval_chain"))
        except (json.JSONDecodeError, TypeError):
            approval_chain = []

    return {
        "status": doc.get("dw_status") or "",
        "current_node": doc.get("dw_current_node") or 0,
        "workflow_config": doc.get("dw_workflow_config") or "",
        "approval_chain": approval_chain,
    }


def _trigger_approval_actions(doc):
    """Trigger post-approval business actions."""
    from dynamic_workflow.dynamic_workflow.business_engine import BusinessActionEngine

    config_name = doc.get("dw_workflow_config")
    if not config_name:
        return

    config = frappe.get_doc("Dynamic Workflow Config", config_name)
    BusinessActionEngine.execute_on_approval(doc, config)
