# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import now, get_datetime
from datetime import datetime, timedelta


class TimeoutEscalationEngine:
    """
    Timeout Escalation Engine
    
    Handles:
    - 24 hour reminder
    - 48 hour escalation to manager
    - Automatic notifications
    """

    @staticmethod
    def check_and_escalate():
        """Background task to check and escalate pending approvals"""
        
        try:
            # Get pending approvals
            pending_approvals = frappe.get_all(
                'Approval Log',
                filters={'status': 'Pending'},
                fields=['name', 'document_type', 'document_name', 'creation', 'approver']
            )
            
            current_time = datetime.now()
            
            for approval in pending_approvals:
                try:
                    # Find or create escalation record
                    escalation = frappe.db.get_value(
                        'Workflow Timeout Escalation',
                        {'approval_log': approval['name']}
                    )
                    
                    if not escalation:
                        continue
                    
                    escalation_doc = frappe.get_doc('Workflow Timeout Escalation', escalation)
                    creation_time = get_datetime(approval['creation'])
                    hours_elapsed = (current_time - creation_time).total_seconds() / 3600
                    
                    # First timeout (24 hours)
                    if (hours_elapsed >= escalation_doc.first_timeout_hours and 
                        not escalation_doc.first_executed):
                        TimeoutEscalationEngine._execute_first_timeout(escalation_doc)
                    
                    # Second timeout (48 hours)
                    if (hours_elapsed >= escalation_doc.second_timeout_hours and 
                        not escalation_doc.second_executed):
                        TimeoutEscalationEngine._execute_second_timeout(escalation_doc)
                
                except Exception as e:
                    frappe.log_error(f"Error processing escalation for {approval.get('name')}: {str(e)}")
        
        except Exception as e:
            frappe.log_error(f"Error in check_and_escalate: {str(e)}")

    @staticmethod
    def _execute_first_timeout(escalation_doc):
        """Execute first timeout action"""
        try:
            if escalation_doc.first_timeout_action == 'Send Reminder':
                TimeoutEscalationEngine._send_reminder(
                    escalation_doc.approver,
                    escalation_doc.document_type,
                    escalation_doc.document_name
                )
            
            escalation_doc.db_set('first_executed', 1)
            escalation_doc.db_set('first_timeout_time', now())
            escalation_doc.db_set('status', 'Reminder Sent')
        except Exception as e:
            frappe.log_error(f"Error in first timeout: {str(e)}")

    @staticmethod
    def _execute_second_timeout(escalation_doc):
        """Execute second timeout action (escalation)"""
        try:
            if escalation_doc.second_timeout_action == 'Notify Manager':
                manager = TimeoutEscalationEngine._get_manager_user(escalation_doc.approver)
                if manager:
                    escalation_doc.escalation_to = manager
                    escalation_doc.escalation_time = now()
                    escalation_doc.save()
                    
                    TimeoutEscalationEngine._send_escalation_notification(
                        manager,
                        escalation_doc.approver,
                        escalation_doc.document_type,
                        escalation_doc.document_name
                    )
            
            escalation_doc.db_set('second_executed', 1)
            escalation_doc.db_set('second_timeout_time', now())
            escalation_doc.db_set('status', 'Escalated')
        except Exception as e:
            frappe.log_error(f"Error in second timeout: {str(e)}")

    @staticmethod
    def _send_reminder(approver, doc_type, doc_name):
        """Send reminder email"""
        try:
            doc = frappe.get_doc(doc_type, doc_name)
            
            frappe.sendmail(
                recipients=[approver],
                subject=f"【提醒】待审批：{doc_name}",
                template='workflow_reminder',
                args={
                    'doc_name': doc_name,
                    'doc_type': doc_type,
                    'doc_link': frappe.utils.get_link_to_form(doc_type, doc_name),
                    'amount': doc.get('grand_total', 0),
                    'approver': approver,
                }
            )
        except Exception as e:
            frappe.log_error(f"Failed to send reminder: {str(e)}")

    @staticmethod
    def _send_escalation_notification(manager, approver, doc_type, doc_name):
        """Send escalation notification"""
        try:
            doc = frappe.get_doc(doc_type, doc_name)
            frappe.sendmail(
                recipients=[manager],
                subject=f"【升级】{approver} 未及时审批：{doc_name}",
                template='workflow_escalation',
                args={
                    'doc_name': doc_name,
                    'doc_type': doc_type,
                    'original_approver': approver,
                    'doc_link': frappe.utils.get_link_to_form(doc_type, doc_name),
                    'amount': doc.get('grand_total', 0),
                }
            )
        except Exception as e:
            frappe.log_error(f"Failed to send escalation notification: {str(e)}")

    @staticmethod
    def _get_manager_user(approver):
        """Get manager of user"""
        try:
            employee = frappe.get_value('Employee', {'user_id': approver}, 'name')
            if employee:
                reports_to = frappe.get_value('Employee', employee, 'reports_to')
                if reports_to:
                    manager_user = frappe.get_value('Employee', reports_to, 'user_id')
                    return manager_user
        except Exception as e:
            frappe.log_error(f"Error getting manager user: {str(e)}")
        return None
