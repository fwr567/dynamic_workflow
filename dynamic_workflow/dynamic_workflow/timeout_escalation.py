import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime, add_to_date


def check_and_escalate():
    """Scheduler entry point: check all pending approval logs and
    trigger reminders or escalations based on timeout configuration.

    Called by hooks.py scheduler_events (hourly).
    """
    pending_logs = frappe.get_all(
        "Approval Log",
        filters={"status": "Pending"},
        fields=["name", "document_type", "document_name", "approver", "action_date"],
    )

    for log in pending_logs:
        _process_log(log)


def _process_log(log):
    """Process a single pending approval log for timeout escalation."""
    config = _get_workflow_config(log.document_type, log.document_name)
    if not config or not config.enable_timeout_escalation:
        return

    escalation = _get_or_create_escalation(log, config)
    if not escalation:
        return

    now = get_datetime(now_datetime())
    action_time = get_datetime(log.action_date or log.get("creation"))
    if not action_time:
        return

    # Frappe v16: use add_to_date instead of add_hours
    first_timeout_limit = add_to_date(action_time, hours=escalation.first_timeout_hours)
    second_timeout_limit = add_to_date(action_time, hours=escalation.second_timeout_hours)

    if not escalation.first_executed and now >= first_timeout_limit:
        _execute_first_timeout(escalation, log)

    if not escalation.second_executed and now >= second_timeout_limit:
        _execute_second_timeout(escalation, log)


def _get_workflow_config(document_type, document_name):
    """Get the Dynamic Workflow Config for a document."""
    config_name = frappe.db.get_value(document_type, document_name, "dw_workflow_config")
    if config_name:
        return frappe.get_doc("Dynamic Workflow Config", config_name)
    return None


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


def _execute_first_timeout(escalation, log):
    """Send a reminder email on first timeout."""
    try:
        frappe.sendmail(
            recipients=[log.approver],
            subject=f"【提醒】待审批：{log.document_name}",
            message=(
                f"您的审批待处理：{log.document_type} {log.document_name}。"
                f"请及时审批。"
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


def _execute_second_timeout(escalation, log):
    """Escalate to manager or reassign on second timeout."""
    try:
        if escalation.second_timeout_action == "Notify Manager":
            _notify_manager(escalation, log)
        elif escalation.second_timeout_action == "Reassign":
            _reassign(escalation, log)

        escalation.db_set("second_executed", 1)
        escalation.db_set("second_timeout_time", now_datetime())
        escalation.db_set("status", "Escalated")
        escalation.db_set("escalation_time", now_datetime())
    except Exception as e:
        frappe.log_error(
            title="Timeout Escalation - Second Timeout Error",
            message=str(e),
        )


def _notify_manager(escalation, log):
    """Send escalation notification to the approver's manager."""
    manager_employee = frappe.db.get_value(
        "Employee", {"user_id": log.approver}, "reports_to"
    )
    if manager_employee:
        manager_email = frappe.db.get_value("Employee", manager_employee, "user_id")
        if manager_email:
            escalation.db_set("escalation_to", manager_email)
            frappe.sendmail(
                recipients=[manager_email],
                subject=f"【升级】{log.approver} 未及时审批：{log.document_name}",
                message=(
                    f"{log.approver} 对 {log.document_type} {log.document_name} "
                    f"的审批已超时，请您介入处理。"
                ),
                reference_doctype=log.document_type,
                reference_name=log.document_name,
            )


def _reassign(escalation, log):
    """Reassign the pending approval to the approver's manager."""
    manager_employee = frappe.db.get_value(
        "Employee", {"user_id": log.approver}, "reports_to"
    )
    if manager_employee:
        manager_email = frappe.db.get_value("Employee", manager_employee, "user_id")
        if manager_email:
            escalation.db_set("escalation_to", manager_email)
            frappe.db.set_value(
                "Approval Log", log.name, "approver", manager_email
            )
