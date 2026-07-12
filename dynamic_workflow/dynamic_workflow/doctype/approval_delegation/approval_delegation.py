import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class ApprovalDelegation(Document):
    def validate(self):
        self.validate_dates()
        self.validate_users()

    def validate_dates(self):
        """Ensure date range is valid."""
        if getdate(self.from_date) > getdate(self.to_date):
            frappe.throw(_("From Date cannot be after To Date."))

    def validate_users(self):
        """Ensure delegator and delegatee are different users."""
        if self.delegator == self.delegatee:
            frappe.throw(_("Delegator and Delegatee cannot be the same user."))
