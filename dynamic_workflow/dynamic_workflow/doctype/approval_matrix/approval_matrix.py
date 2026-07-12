import frappe
from frappe import _
from frappe.model.document import Document


class ApprovalMatrix(Document):
    def validate(self):
        self.validate_rules()

    def validate_rules(self):
        """Ensure each rule has at least one approval chain step."""
        if not self.rules:
            frappe.throw(_("At least one rule is required for the Approval Matrix."))
        for rule in self.rules:
            if not rule.approval_chain_desc:
                frappe.throw(
                    _("Row {0}: Each rule must have at least one Approval Chain Step.").format(rule.idx)
                )
