import frappe
from frappe import _


class OrganizationEngine:
    """
    Resolves approvers from organizational hierarchy based on assignment modes.
    Supports User, Role, Manager, Department Head, Business Line Head,
    Project Manager, Cost Center Head, Designation, and Custom Script modes.
    """

    @staticmethod
    def get_approvers(doc, assign_mode, step):
        """
        Return a list of approver user IDs based on the assignment mode.

        Args:
            doc: The Frappe document being routed.
            assign_mode: The assignment strategy string.
            step: The step object containing additional config (e.g. approver_user).

        Returns:
            list[str]: List of user email IDs who are approvers.
        """
        mode_map = {
            "User": OrganizationEngine._get_user_approver,
            "Role": OrganizationEngine._get_role_approvers,
            "Manager": OrganizationEngine._get_manager,
            "Department Head": OrganizationEngine._get_department_head,
            "Business Line Head": OrganizationEngine._get_business_line_head,
            "Project Manager": OrganizationEngine._get_project_manager,
            "Cost Center Head": OrganizationEngine._get_cost_center_head,
            "Designation": OrganizationEngine._get_designation_approvers,
            "Custom Script": OrganizationEngine._get_custom_script_approvers,
        }

        handler = mode_map.get(assign_mode)
        if not handler:
            frappe.log_error(
                title="Organization Engine Error",
                message=f"Unknown assign mode: {assign_mode}",
            )
            return []

        return handler(doc, step)

    @staticmethod
    def _get_user_approver(doc, step):
        """Return a specific user as approver."""
        if step.approver_user:
            return [step.approver_user]
        return []

    @staticmethod
    def _get_role_approvers(doc, step):
        """Return all users with a given role."""
        if not step.approver_role:
            return []
        users = frappe.get_all(
            "Has Role",
            filters={"role": step.approver_role, "parenttype": "User"},
            fields=["parent"],
        )
        return [u.parent for u in users if u.parent != "Administrator"]

    @staticmethod
    def _get_manager(doc, step):
        """Return the report-to manager of the document owner."""
        owner = doc.get("owner") or frappe.session.user
        reports_to = frappe.db.get_value("Employee", {"user_id": owner}, "reports_to")
        if reports_to:
            manager_user = frappe.db.get_value("Employee", reports_to, "user_id")
            if manager_user:
                return [manager_user]
        return []

    @staticmethod
    def _get_department_head(doc, step):
        """Return the head of the department associated with the document."""
        department = doc.get("department")
        if not department:
            return []
        head = frappe.db.get_value("Department", department, "department_head")
        if head:
            return [head]
        return []

    @staticmethod
    def _get_business_line_head(doc, step):
        """Return the head of the business line (custom field or department group)."""
        business_line = doc.get("business_line")
        if not business_line:
            return OrganizationEngine._get_department_head(doc, step)
        head = frappe.db.get_value("Department", business_line, "department_head")
        if head:
            return [head]
        return []

    @staticmethod
    def _get_project_manager(doc, step):
        """Return the project manager if a project is linked."""
        project = doc.get("project")
        if not project:
            return []
        pm = frappe.db.get_value("Project", project, "user")
        if pm:
            return [pm]
        return []

    @staticmethod
    def _get_cost_center_head(doc, step):
        """Return the cost center head / owner."""
        cost_center = doc.get("cost_center")
        if not cost_center:
            return []
        cc_owner = frappe.db.get_value("Cost Center", cost_center, "owner")
        if cc_owner:
            return [cc_owner]
        return []

    @staticmethod
    def _get_designation_approvers(doc, step):
        """Return all users with a given designation."""
        if not step.designation:
            return []
        employees = frappe.get_all(
            "Employee",
            filters={"designation": step.designation, "status": "Active"},
            fields=["user_id"],
        )
        return [e.user_id for e in employees if e.user_id]

    @staticmethod
    def _get_custom_script_approvers(doc, step):
        """Execute a custom Python script to determine approvers."""
        if not step.custom_script:
            return []
        try:
            result = frappe.safe_eval(step.custom_script, {"doc": doc, "frappe": frappe})
            if isinstance(result, str):
                return [result]
            if isinstance(result, (list, tuple)):
                return list(result)
            return []
        except Exception as e:
            frappe.log_error(
                title="Organization Engine - Custom Script Error",
                message=str(e),
            )
            return []
