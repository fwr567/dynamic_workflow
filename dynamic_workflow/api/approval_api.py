# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from dynamic_workflow.workflow_core.approval_engine import ApprovalEngine
from dynamic_workflow.workflow_core.business_engine import BusinessActionEngine


@frappe.whitelist()
def submit_approval(document_type, document_name, action, comments='', attachments=None, **kwargs):
    """提交审批"""
    
    doc = frappe.get_doc(document_type, document_name)
    
    # 检查权限
    if not frappe.has_permission(document_type, 'write', doc=doc):
        frappe.throw(_("You do not have permission to approve this document"))
    
    # 创建审批记录
    approval_log = frappe.get_doc({
        'doctype': 'Approval Log',
        'document_type': document_type,
        'document_name': document_name,
        'approver': frappe.session.user,
        'action': action,
        'comments': comments,
        'status': 'Completed',
        'action_date': frappe.utils.now(),
        'additional_approvers': kwargs.get('additional_approvers', ''),
        'forward_to': kwargs.get('forward_to', ''),
    })
    
    approval_log.insert()
    
    # 根据动作类型处理
    if action == 'Approve':
        doc.dw_status = 'Approved'
        doc.dw_current_node = (doc.dw_current_node or 0) + 1
        
        # 执行业务动作
        if doc.dw_workflow_config:
            try:
                BusinessActionEngine.execute_on_approval(doc, doc.dw_workflow_config)
            except Exception as e:
                frappe.log_error(f"Business action execution failed: {str(e)}")
    
    elif action == 'Reject':
        doc.dw_status = 'Rejected'
        
        # 执行拒绝后的业务动作
        if doc.dw_workflow_config:
            try:
                BusinessActionEngine.execute_on_rejection(doc, doc.dw_workflow_config)
            except Exception as e:
                frappe.log_error(f"Business action execution failed: {str(e)}")
    
    elif action == 'Return':
        if doc.dw_current_node > 0:
            doc.dw_current_node -= 1
        doc.dw_status = 'Pending Approval'
    
    doc.save()
    
    frappe.publish_realtime(
        'approval_updated',
        {
            'document_type': document_type,
            'document_name': document_name,
            'action': action,
            'approver': frappe.session.user,
        }
    )
    
    return {'status': 'success', 'message': _(f'Approval {action} submitted')}


@frappe.whitelist()
def get_approval_logs(document_type, document_name):
    """获取审批记录"""
    
    logs = frappe.get_all(
        'Approval Log',
        filters={
            'document_type': document_type,
            'document_name': document_name,
        },
        fields=['*'],
        order_by='action_date desc'
    )
    
    return logs


@frappe.whitelist()
def get_pending_approvals():
    """获取当前用户的待审批列表"""
    
    pending = frappe.get_all(
        'Approval Log',
        filters={
            'approver': frappe.session.user,
            'status': 'Pending'
        },
        fields=['document_type', 'document_name', 'approval_node', 'action_date'],
        order_by='action_date asc'
    )
    
    return pending
