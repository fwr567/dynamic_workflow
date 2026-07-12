import frappe
from frappe import _
from frappe.model.document import Document


class ApprovalLog(Document):
    def validate(self):
        self.validate_action()

    def validate_action(self):
        """Ensure forward action has a target user."""
        if self.action == "Forward" and not self.forward_to:
            frappe.throw(_("Forward action requires a target user."))
