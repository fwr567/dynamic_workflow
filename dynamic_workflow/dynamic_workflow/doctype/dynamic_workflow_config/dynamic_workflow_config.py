import frappe
from frappe import _
from frappe.model.document import Document


class DynamicWorkflowConfig(Document):
    def validate(self):
        self.validate_timeout_settings()
        self.validate_node_templates()

    def validate_timeout_settings(self):
        """Ensure second timeout is greater than first timeout."""
        if self.enable_timeout_escalation:
            if self.second_timeout_hours and self.first_timeout_hours:
                if self.second_timeout_hours <= self.first_timeout_hours:
                    frappe.throw(
                        _("Second timeout hours ({0}) must be greater than first timeout hours ({1}).").format(
                            self.second_timeout_hours, self.first_timeout_hours
                        )
                    )

    def validate_node_templates(self):
        """Ensure node templates have valid sequences."""
        if self.node_templates:
            sequences = [t.sequence for t in self.node_templates if t.sequence]
            if sequences and len(sequences) != len(set(sequences)):
                frappe.throw(_("Node template sequences must be unique."))
