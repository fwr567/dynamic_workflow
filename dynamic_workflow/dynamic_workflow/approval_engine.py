import frappe
from frappe import _

from dynamic_workflow.dynamic_workflow.organization_engine import OrganizationEngine


class ApprovalEngine:
    """Core engine for building approval chains from Approval Matrix rules."""

    @staticmethod
    def get_approval_chain(doc, workflow_config):
        """
        Build the full approval chain for a document based on the workflow config.

        Args:
            doc: The Frappe document being routed.
            workflow_config: Dynamic Workflow Config document.

        Returns:
            list: Ordered list of approval step dicts.
        """
        if not workflow_config or not workflow_config.approval_matrix:
            frappe.log_error(
                title="Approval Engine Error",
                message=f"No approval matrix configured for {workflow_config.name}",
            )
            return []

        matrix = frappe.get_doc("Approval Matrix", workflow_config.approval_matrix)
        if not matrix.enabled:
            frappe.log_error(
                title="Approval Engine Error",
                message=f"Approval Matrix {matrix.name} is disabled.",
            )
            return []

        matched_chain = ApprovalEngine._match_rules(doc, matrix)
        return matched_chain

    @staticmethod
    def _match_rules(doc, matrix):
        """
        Evaluate matrix rules against the document and return the first matching chain.

        Args:
            doc: The Frappe document.
            matrix: Approval Matrix document.

        Returns:
            list: Approval chain steps from the matched rule.
        """
        for rule in matrix.rules:
            if ApprovalEngine._evaluate_rule(doc, rule):
                return ApprovalEngine._build_chain_from_rule(doc, rule, matrix.approval_chain_type)

        frappe.log_error(
            title="Approval Engine Warning",
            message=f"No matching rule found in matrix {matrix.name} for {doc.doctype} {doc.name}",
        )
        return []

    @staticmethod
    def _evaluate_rule(doc, rule):
        """
        Check whether a single matrix rule matches the document.

        Args:
            doc: The Frappe document.
            rule: Approval Matrix Rule row.

        Returns:
            bool: True if the rule matches.
        """
        amount_field = rule.amount_field or "grand_total"
        doc_amount = doc.get(amount_field)

        if doc_amount is not None:
            if rule.amount_from and float(doc_amount) < float(rule.amount_from):
                return False
            if rule.amount_to and float(doc_amount) > float(rule.amount_to):
                return False

        if rule.department and doc.get("department") != rule.department:
            return False

        if rule.business_line and doc.get("business_line") != rule.business_line:
            return False

        if rule.project_type and doc.get("project_type") != rule.project_type:
            return False

        if rule.custom_condition:
            try:
                result = frappe.safe_eval(rule.custom_condition, {"doc": doc})
                if not result:
                    return False
            except Exception as e:
                frappe.log_error(
                    title="Approval Engine - Custom Condition Error",
                    message=f"Rule {rule.idx}: {str(e)}",
                )
                return False

        return True

    @staticmethod
    def _build_chain_from_rule(doc, rule, chain_type):
        """
        Convert a matched rule's approval chain steps into executable approval steps.

        Args:
            doc: The Frappe document.
            rule: The matched Approval Matrix Rule.
            chain_type: 'Serial' or 'Parallel'.

        Returns:
            list[dict]: List of approval step dicts with approver info.
        """
        chain = []
        steps = sorted(rule.approval_chain_desc, key=lambda s: s.step_sequence)

        for step in steps:
            approvers = OrganizationEngine.get_approvers(doc, step.assign_mode, step)
            if approvers:
                chain.append({
                    "step_sequence": step.step_sequence,
                    "assign_mode": step.assign_mode,
                    "approvers": approvers,
                    "chain_type": chain_type,
                })

        return chain
