# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from dynamic_workflow.workflow_core.organization_engine import OrganizationEngine


class ApprovalEngine:
    """
    Core Approval Engine - Layer 1 & 2
    
    Implements:
    - Approval Matrix evaluation
    - Organization Relationship Engine
    """

    def __init__(self, doc, workflow_config):
        self.doc = doc
        self.workflow_config = workflow_config
        self.approval_chain = []

    def get_approval_chain(self):
        """Get approval chain based on approval matrix"""
        try:
            workflow_config = frappe.get_doc('Dynamic Workflow Config', self.workflow_config)
            
            if not workflow_config.approval_matrix:
                return []
            
            approval_matrix = frappe.get_doc('Approval Matrix', workflow_config.approval_matrix)
            
            # Iterate through rules and find matching one
            for rule in approval_matrix.rules:
                if self._match_conditions(rule):
                    chain_steps = self._build_approval_chain(rule)
                    return chain_steps
            
            return []
        except Exception as e:
            frappe.log_error(f"Error getting approval chain: {str(e)}")
            return []

    def _match_conditions(self, rule):
        """Check if rule conditions match"""
        try:
            # Check amount
            if rule.amount_from or rule.amount_to:
                amount_field = rule.amount_field or 'grand_total'
                amount = self.doc.get(amount_field) or 0
                
                if rule.amount_from and amount < rule.amount_from:
                    return False
                if rule.amount_to and amount > rule.amount_to:
                    return False
            
            # Check department
            if rule.department and self.doc.get('department') != rule.department:
                return False
            
            # Check business line
            if rule.business_line and self.doc.get('business_line') != rule.business_line:
                return False
            
            # Check project type
            if rule.project_type and self.doc.get('project_type') != rule.project_type:
                return False
            
            # Check custom condition
            if rule.custom_condition:
                try:
                    result = frappe.safe_eval(rule.custom_condition, {"doc": self.doc, "frappe": frappe})
                    if not result:
                        return False
                except Exception as e:
                    frappe.log_error(f"Custom condition error: {str(e)}")
                    return False
            
            return True
        except Exception as e:
            frappe.log_error(f"Error matching conditions: {str(e)}")
            return False

    def _build_approval_chain(self, rule):
        """Build approval chain from rule"""
        chain = []
        
        try:
            for step in rule.approval_chain_desc:
                approvers = OrganizationEngine.get_approvers(self.doc, step.assign_mode, step)
                
                chain.append({
                    'step_sequence': step.step_sequence,
                    'assign_mode': step.assign_mode,
                    'approvers': approvers,
                    'node_type': rule.approval_chain_type,
                    'status': 'Pending'
                })
            
            return chain
        except Exception as e:
            frappe.log_error(f"Error building approval chain: {str(e)}")
            return []
