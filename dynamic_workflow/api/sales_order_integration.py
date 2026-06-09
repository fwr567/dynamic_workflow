# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from dynamic_workflow.workflow_core.approval_engine import ApprovalEngine
from dynamic_workflow.workflow_core.business_engine import BusinessActionEngine


def attach_dynamic_workflow(doc, method):
    """在保存前检查并附加工作流"""
    
    workflow_config = frappe.get_value(
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


def validate_approval(doc, method):
    """在提交前验证审批状态"""
    
    if not doc.dw_workflow_config:
        return
    
    if doc.dw_status != 'Approved':
        frappe.throw(f"Document cannot be submitted. Current workflow status: {doc.dw_status}")


def execute_business_actions(doc, method):
    """在提交后执行业务动作"""
    
    if doc.dw_workflow_config:
        try:
            BusinessActionEngine.execute_on_approval(doc, doc.dw_workflow_config)
        except Exception as e:
            frappe.log_error(f"Business action execution failed: {str(e)}")
