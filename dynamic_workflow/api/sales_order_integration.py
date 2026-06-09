# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from dynamic_workflow.workflow_core.approval_engine import ApprovalEngine
from dynamic_workflow.workflow_core.business_engine import BusinessActionEngine


def attach_dynamic_workflow(doc, method):
    """Attach dynamic workflow"""
    try:
        workflow_config = frappe.db.get_value(
            'Dynamic Workflow Config',
            {'document_type': doc.doctype, 'is_active': 1},
            'name'
        )
        
        if not workflow_config:
            return
        
        engine = ApprovalEngine(doc, workflow_config)
        approval_chain = engine.get_approval_chain()
        
        if approval_chain:
            doc.dw_workflow_config = workflow_config
            doc.dw_approval_chain = frappe.as_json(approval_chain)
            doc.dw_current_node = 0
            doc.dw_status = 'Pending Approval'
    
    except Exception as e:
        frappe.log_error(f"Error attaching workflow: {str(e)}")


def validate_approval(doc, method):
    """Validate approval status"""
    try:
        if not doc.dw_workflow_config:
            return
        
        if doc.dw_status != 'Approved':
            frappe.throw(f"Document cannot be submitted. Current workflow status: {doc.dw_status}")
    
    except frappe.exceptions.ValidationError:
        raise
    except Exception as e:
        frappe.log_error(f"Error validating approval: {str(e)}")


def execute_business_actions(doc, method):
    """Execute business actions"""
    try:
        if doc.dw_workflow_config:
            BusinessActionEngine.execute_on_approval(doc, doc.dw_workflow_config)
    
    except Exception as e:
        frappe.log_error(f"Error executing business actions: {str(e)}")
