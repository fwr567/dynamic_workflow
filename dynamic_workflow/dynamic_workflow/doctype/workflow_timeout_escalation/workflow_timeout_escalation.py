import frappe
from frappe import _
from frappe.model.document import Document


class WorkflowTimeoutEscalation(Document):
    def validate(self):
        self.validate_timeout_hours()

    def validate_timeout_hours(self):
        """Ensure second timeout is greater than first timeout."""
        if self.second_timeout_hours and self.first_timeout_hours:
            if self.second_timeout_hours <= self.first_timeout_hours:
                frappe.throw(
                    _("Second timeout hours must be greater than first timeout hours.")
                )
