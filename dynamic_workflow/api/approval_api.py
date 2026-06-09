# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import now


@frappe.whitelist()
def submit_approval(document_type, document_name, action, comments='', attachments=None, **kwargs):
    """
    Submit approval action
    
    Frappe v16 compatible API endpoint
    """
    
    try:
        # Check permission
        frappe.get_doc(document_type, document_name).check_permission('write')
        
        # Create approval log
        approval_log = frappe.get_doc({
            'doctype': 'Approval Log',
            'document_type': document_type,
            'document_name': document_name,
            'approver': frappe.session.user,
            'action': action,
            'comments': comments,
            'status': 'Completed',
            'action_date': now(),
            'additional_approvers': kwargs.get('additional_approvers', ''),
            'forward_to': kwargs.get('forward_to', ''),
        })
        
        approval_log.insert()
        
        # Get document and update status
        doc = frappe.get_doc(document_type, document_name)
        
        if action == 'Approve':
            doc.dw_status = 'Approved'
            doc.dw_current_node = (doc.dw_current_node or 0) + 1
        
        elif action == 'Reject':
            doc.dw_status = 'Rejected'
        
        elif action == 'Return':
            if doc.dw_current_node > 0:
                doc.dw_current_node -= 1
            doc.dw_status = 'Pending Approval'
        
        doc.save()
        
        # Publish realtime update
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
    
    except Exception as e:
        frappe.log_error(f"Error submitting approval: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@frappe.whitelist()
def get_approval_logs(document_type, document_name):
    """
    Get approval logs for document
    """
    
    try:
        logs = frappe.get_all(
            'Approval Log',
            filters={
                'document_type': document_type,
                'document_name': document_name,
            },
            fields=['name', 'approver', 'action', 'comments', 'action_date', 'duration_hours'],
            order_by='action_date desc'
        )
        
        return logs
    
    except Exception as e:
        frappe.log_error(f"Error getting approval logs: {str(e)}")
        return []


@frappe.whitelist()
def get_pending_approvals():
    """
    Get current user's pending approvals
    """
    
    try:
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
    
    except Exception as e:
        frappe.log_error(f"Error getting pending approvals: {str(e)}")
        return []
