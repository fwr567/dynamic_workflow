import frappe
from frappe import _
from frappe.utils import now_datetime


class ApprovalAction:
    """Handles individual approval actions on documents."""

    SUPPORTED_ACTIONS = [
        "Approve", "Reject", "Return", "Forward", "Countersign",
        "Delegate", "Terminate", "Recall",
    ]

    @staticmethod
    def perform_action(doc, action, **kwargs):
        """
        Execute an approval action on a document.

        Args:
            doc: The Frappe document.
            action: The action string (e.g. 'Approve', 'Reject').
            **kwargs: Additional parameters like comments, forward_to, delegate_to.

        Returns:
            dict: Result dict with status and message.
        """
        if action not in ApprovalAction.SUPPORTED_ACTIONS:
            frappe.throw(_(f"Unsupported action: {action}"))

        action_handler = {
            "Approve": ApprovalAction._approve,
            "Reject": ApprovalAction._reject,
            "Return": ApprovalAction._return,
            "Forward": ApprovalAction._forward,
            "Countersign": ApprovalAction._countersign,
            "Delegate": ApprovalAction._delegate,
            "Terminate": ApprovalAction._terminate,
            "Recall": ApprovalAction._recall,
        }

        handler = action_handler.get(action)
        return handler(doc, **kwargs)

    @staticmethod
    def _log_action(doc, action, **kwargs):
        """Create an Approval Log entry for the action."""
        log = frappe.get_doc({
            "doctype": "Approval Log",
            "document_type": doc.doctype,
            "document_name": doc.name,
            "approver": frappe.session.user,
            "action": action,
            "action_date": now_datetime(),
            "status": "Completed",
            "approval_node": doc.get("dw_current_node") or 0,
            "comments": kwargs.get("comments", ""),
            "forward_to": kwargs.get("forward_to", ""),
            "additional_approvers": kwargs.get("additional_approvers", ""),
        })
        log.insert(ignore_permissions=True)
        return log

    @staticmethod
    def _approve(doc, **kwargs):
        """Approve the current approval step."""
        ApprovalAction._log_action(doc, "Approve", **kwargs)

        approval_chain = frappe.parse_json(doc.get("dw_approval_chain") or "[]")
        current_node = doc.get("dw_current_node") or 0

        if current_node < len(approval_chain) - 1:
            doc.db_set("dw_current_node", current_node + 1)
            doc.db_set("dw_status", "In Progress")
        else:
            doc.db_set("dw_status", "Approved")

        return {"status": "success", "message": _("Document approved.")}

    @staticmethod
    def _reject(doc, **kwargs):
        """Reject the document."""
        ApprovalAction._log_action(doc, "Reject", **kwargs)
        doc.db_set("dw_status", "Rejected")
        return {"status": "success", "message": _("Document rejected.")}

    @staticmethod
    def _return(doc, **kwargs):
        """Return the document for modifications."""
        ApprovalAction._log_action(doc, "Return", **kwargs)
        doc.db_set("dw_status", "Returned")
        doc.db_set("dw_current_node", 0)
        return {"status": "success", "message": _("Document returned for modifications.")}

    @staticmethod
    def _forward(doc, **kwargs):
        """Forward the approval to another user."""
        forward_to = kwargs.get("forward_to")
        if not forward_to:
            frappe.throw(_("Forward target user is required."))

        ApprovalAction._log_action(doc, "Forward", **kwargs)
        return {"status": "success", "message": _(f"Document forwarded to {forward_to}.")}

    @staticmethod
    def _countersign(doc, **kwargs):
        """Add a countersign requirement."""
        ApprovalAction._log_action(doc, "Countersign", **kwargs)
        return {"status": "success", "message": _("Countersign added.")}

    @staticmethod
    def _delegate(doc, **kwargs):
        """Delegate approval authority to another user."""
        delegate_to = kwargs.get("delegate_to")
        if not delegate_to:
            frappe.throw(_("Delegation target user is required."))

        ApprovalAction._log_action(doc, "Delegate", **kwargs)
        return {"status": "success", "message": _(f"Approval delegated to {delegate_to}.")}

    @staticmethod
    def _terminate(doc, **kwargs):
        """Terminate the workflow."""
        ApprovalAction._log_action(doc, "Terminate", **kwargs)
        doc.db_set("dw_status", "Terminated")
        return {"status": "success", "message": _("Workflow terminated.")}

    @staticmethod
    def _recall(doc, **kwargs):
        """Recall a submitted document."""
        ApprovalAction._log_action(doc, "Recall", **kwargs)
        doc.db_set("dw_status", "Recalled")
        doc.db_set("dw_current_node", 0)
        return {"status": "success", "message": _("Document recalled.")}
