import frappe
from frappe import _
from frappe.utils import now_datetime, add_hours, get_datetime


class TimeoutEscalationEngine:
    """Handles automatic timeout reminders and escalation for pending approvals."""

    @staticmethod
    def check_and_escalate():
        """
        Scheduler entry point: check all pending approval logs and
        trigger reminders or escalations based on timeout configuration.
        """
        pending_logs = frappe.get_all(
            "Approval Log",
            filters={"status": "Pending"},
            fields=["name", "document_type", "document_name", "approver", "action_date"],
        )

        for log in pending_logs:
            TimeoutEscalationEngine._process_log(log)

    @staticmethod
    def _process_log(log):
        """
        Process a single pending approval log for timeout escalation.

        Args:
            log: Approval Log dict.
        """
        config = TimeoutEscalationEngine._get_workflow_config(
            log.document_type, log.document_name
        )
        if not config or not config.enable_timeout_escalation:
            return

        escalation = TimeoutEscalationEngine._get_or_create_escalation(log, config)
        if not escalation:
            return

        now = get_datetime(now_datetime())
        action_time = get_datetime(log.action_date)

        first_timeout_limit = add_hours(action_time, escalation.first_timeout_hours)
        second_timeout_limit = add_hours(action_time, escalation.second_timeout_hours)

        if not escalation.first_executed and now >= first_timeout_limit:
            TimeoutEscalationEngine._execute_first_timeout(escalation, log)

        if not escalation.second_executed and now >= second_timeout_limit:
            TimeoutEscalationEngine._execute_second_timeout(escalation, log)

    @staticmethod
    def _get_workflow_config(document_type, document_name):
        """Get the Dynamic Workflow Config for a document."""
        config_name = frappe.db.get_value(document_type, document_name, "dw_workflow_config")
        if config_name:
            return frappe.get_doc("Dynamic Workflow Config", config_name)
        return None

    @staticmethod
    def _get_or_create_escalation(log, config):
        """Get existing or create new Workflow Timeout Escalation record."""
        existing = frappe.db.get_value(
            "Workflow Timeout Escalation",
            {"approval_log": log.name},
            "name",
        )
        if existing:
            return frappe.get_doc("Workflow Timeout Escalation", existing)

        try:
            escalation = frappe.get_doc({
                "doctype": "Workflow Timeout Escalation",
                "approval_log": log.name,
                "document_type": log.document_type,
                "document_name": log.document_name,
                "approver": log.approver,
                "first_timeout_hours": config.first_timeout_hours or 24,
                "second_timeout_hours": config.second_timeout_hours or 48,
            })
            escalation.insert(ignore_permissions=True)
            return escalation
        except Exception as e:
            frappe.log_error(
                title="Timeout Escalation - Create Error",
                message=str(e),
            )
            return None

    @staticmethod
    def _execute_first_timeout(escalation, log):
        """Send a reminder email on first timeout."""
        try:
            frappe.sendmail(
                recipients=[log.approver],
                subject=_(f"Reminder: Pending Approval for {log.document_type} {log.document_name}"),
                message=_(
                    f"Your approval is pending for {log.document_type} {log.document_name}. "
                    f"Please review and take action."
                ),
                reference_doctype=log.document_type,
                reference_name=log.document_name,
            )
            escalation.db_set("first_executed", 1)
            escalation.db_set("first_timeout_time", now_datetime())
            escalation.db_set("status", "Reminder Sent")
        except Exception as e:
            frappe.log_error(
                title="Timeout Escalation - First Timeout Error",
                message=str(e),
            )

    @staticmethod
    def _execute_second_timeout(escalation, log):
        """Escalate to manager or reassign on second timeout."""
        try:
            if escalation.second_timeout_action == "Notify Manager":
                TimeoutEscalationEngine._notify_manager(escalation, log)
            elif escalation.second_timeout_action == "Reassign":
                TimeoutEscalationEngine._reassign(escalation, log)

            escalation.db_set("second_executed", 1)
            escalation.db_set("second_timeout_time", now_datetime())
            escalation.db_set("status", "Escalated")
            escalation.db_set("escalation_time", now_datetime())
        except Exception as e:
            frappe.log_error(
                title="Timeout Escalation - Second Timeout Error",
                message=str(e),
            )

    @staticmethod
    def _notify_manager(escalation, log):
        """Send escalation notification to the approver's manager."""
        manager_user = frappe.db.get_value(
            "Employee", {"user_id": log.approver}, "reports_to"
        )
        if manager_user:
            manager_email = frappe.db.get_value("Employee", manager_user, "user_id")
            if manager_email:
                escalation.db_set("escalation_to", manager_email)
                frappe.sendmail(
                    recipients=[manager_email],
                    subject=_(
                        f"ESCALATION: Overdue Approval for {log.document_type} {log.document_name}"
                    ),
                    message=_(
                        f"Approval by {log.approver} for {log.document_type} "
                        f"{log.document_name} is overdue. Please intervene."
                    ),
                    reference_doctype=log.document_type,
                    reference_name=log.document_name,
                )

    @staticmethod
    def _reassign(escalation, log):
        """Reassign the pending approval to the approver's manager."""
        manager_user = frappe.db.get_value(
            "Employee", {"user_id": log.approver}, "reports_to"
        )
        if manager_user:
            manager_email = frappe.db.get_value("Employee", manager_user, "user_id")
            if manager_email:
                escalation.db_set("escalation_to", manager_email)
                frappe.db.set_value(
                    "Approval Log", log.name, "approver", manager_email
                )
