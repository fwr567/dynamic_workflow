import frappe
from frappe import _


class BusinessActionEngine:
    """Executes business actions configured on workflow approval or rejection."""

    @staticmethod
    def execute_on_approval(doc, config):
        """
        Execute all configured on-approval actions.

        Args:
            doc: The Frappe document.
            config: Dynamic Workflow Config document.
        """
        if not config or not config.on_approval_actions:
            return

        for action in config.on_approval_actions:
            BusinessActionEngine._execute_action(doc, action, "approval")

    @staticmethod
    def execute_on_rejection(doc, config):
        """
        Execute all configured on-rejection actions.

        Args:
            doc: The Frappe document.
            config: Dynamic Workflow Config document.
        """
        if not config or not config.on_rejection_actions:
            return

        for action in config.on_rejection_actions:
            BusinessActionEngine._execute_action(doc, action, "rejection")

    @staticmethod
    def _execute_action(doc, action, trigger_type):
        """
        Execute a single business action.

        Args:
            doc: The Frappe document.
            action: Business Action child row.
            trigger_type: 'approval' or 'rejection'.
        """
        try:
            if action.action_type == "Send Email":
                BusinessActionEngine._send_email(doc, action)
            elif action.action_type == "Execute Script":
                BusinessActionEngine._execute_script(doc, action)
            elif action.action_type == "Create Document":
                BusinessActionEngine._create_document(doc, action)
            elif action.action_type == "Call API":
                BusinessActionEngine._call_api(doc, action)
        except Exception as e:
            frappe.log_error(
                title=f"Business Action Error ({trigger_type})",
                message=f"Action: {action.action_type}\nError: {str(e)}",
            )

    @staticmethod
    def _send_email(doc, action):
        """Send an email notification as a business action."""
        if not action.email_to or not action.email_subject:
            return

        recipients = [r.strip() for r in action.email_to.split(",") if r.strip()]

        context = {
            "doc": doc,
            "doc_type": doc.doctype,
            "doc_name": doc.name,
            "doc_link": frappe.utils.get_url_to_form(doc.doctype, doc.name),
        }

        email_body = action.email_body or ""
        if "{{" in email_body:
            email_body = frappe.render_template(email_body, context)

        subject = action.email_subject
        if "{{" in subject:
            subject = frappe.render_template(subject, context)

        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=email_body,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
        )

    @staticmethod
    def _execute_script(doc, action):
        """Execute a Python script as a business action."""
        if not action.python_script:
            return
        frappe.safe_eval(action.python_script, {"doc": doc, "frappe": frappe})

    @staticmethod
    def _create_document(doc, action):
        """Placeholder for document creation action."""
        frappe.log_error(
            title="Business Action - Create Document",
            message="Create Document action is not yet implemented. Please use Execute Script instead.",
        )

    @staticmethod
    def _call_api(doc, action):
        """Placeholder for API call action."""
        frappe.log_error(
            title="Business Action - Call API",
            message="Call API action is not yet implemented. Please use Execute Script instead.",
        )
