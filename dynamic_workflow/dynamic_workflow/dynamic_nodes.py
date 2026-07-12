import frappe
from frappe import _

from dynamic_workflow.dynamic_workflow.organization_engine import OrganizationEngine


class DynamicNodeEngine:
    """Builds dynamic workflow nodes from Dynamic Workflow Config templates."""

    @staticmethod
    def build_workflow_nodes(doc, config):
        """
        Build workflow nodes from the Dynamic Workflow Config node templates.

        Evaluates condition-based templates and resolves approvers via OrganizationEngine.

        Args:
            doc: The Frappe document being routed.
            config: Dynamic Workflow Config document.

        Returns:
            list[dict]: Ordered list of workflow node dicts.
        """
        if not config or not config.node_templates:
            return []

        nodes = []
        templates = sorted(config.node_templates, key=lambda t: t.sequence or 0)

        for template in templates:
            if DynamicNodeEngine._evaluate_condition(doc, template):
                node = DynamicNodeEngine._build_node(doc, template)
                if node and node.get("steps"):
                    nodes.append(node)

        return nodes

    @staticmethod
    def _evaluate_condition(doc, template):
        """
        Check whether a node template's condition matches the document.

        Args:
            doc: The Frappe document.
            template: Dynamic Node Template row.

        Returns:
            bool: True if the template should be included.
        """
        condition_type = template.condition_type

        if not condition_type:
            return True

        if condition_type == "Amount":
            amount = doc.get("grand_total") or doc.get("total") or 0
            amount = float(amount)
            if template.amount_from is not None and amount < float(template.amount_from):
                return False
            if template.amount_to is not None and amount > float(template.amount_to):
                return False
            return True

        if condition_type == "Custom":
            if not template.custom_condition:
                return True
            try:
                result = frappe.safe_eval(
                    template.custom_condition, {"doc": doc, "frappe": frappe}
                )
                return bool(result)
            except Exception as e:
                frappe.log_error(
                    title="Dynamic Node Engine - Condition Error",
                    message=f"Template {template.node_name}: {str(e)}",
                )
                return False

        return True

    @staticmethod
    def _build_node(doc, template):
        """
        Build a single workflow node dict from a template.

        Args:
            doc: The Frappe document.
            template: Dynamic Node Template row.

        Returns:
            dict: Node dict with name, type, sequence, and resolved steps.
        """
        steps = []
        if template.approval_steps:
            sorted_steps = sorted(template.approval_steps, key=lambda s: s.step_sequence or 0)
            for step in sorted_steps:
                approvers = DynamicNodeEngine._resolve_step_approvers(doc, step)
                if approvers:
                    steps.append({
                        "step_sequence": step.step_sequence,
                        "assign_mode": step.assign_mode,
                        "approvers": approvers,
                    })

        return {
            "node_name": template.node_name,
            "node_type": template.node_type or "Serial",
            "sequence": template.sequence or 0,
            "steps": steps,
        }

    @staticmethod
    def _resolve_step_approvers(doc, step):
        """
        Resolve approvers for a node approval step.

        Args:
            doc: The Frappe document.
            step: Node Approval Step row.

        Returns:
            list[str]: List of approver user IDs.
        """
        if step.assign_mode == "User" and step.approvers:
            return [a.strip() for a in step.approvers.split(",") if a.strip()]

        return OrganizationEngine.get_approvers(doc, step.assign_mode, step)
