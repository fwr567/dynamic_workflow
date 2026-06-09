# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


class BusinessActionEngine:
    """
    Business Action Engine - Layer 5
    
    Execute business operations after approval/rejection
    """

    @staticmethod
    def execute_on_approval(doc, workflow_config):
        """Execute actions on approval"""
        
        try:
            workflow = frappe.get_doc('Dynamic Workflow Config', workflow_config)
            
            for action in workflow.on_approval_actions:
                try:
                    BusinessActionEngine._execute_action(doc, action)
                
                except Exception as e:
                    frappe.log_error(f"Business action failed: {str(e)}")
        
        except Exception as e:
            frappe.log_error(f"Error in execute_on_approval: {str(e)}")

    @staticmethod
    def execute_on_rejection(doc, workflow_config):
        """Execute actions on rejection"""
        
        try:
            workflow = frappe.get_doc('Dynamic Workflow Config', workflow_config)
            
            for action in workflow.on_rejection_actions:
                try:
                    BusinessActionEngine._execute_action(doc, action)
                
                except Exception as e:
                    frappe.log_error(f"Business action on rejection failed: {str(e)}")
        
        except Exception as e:
            frappe.log_error(f"Error in execute_on_rejection: {str(e)}")

    @staticmethod
    def _execute_action(doc, action):
        """Execute specific action"""
        
        if action.action_type == 'Send Email':
            BusinessActionEngine._send_email(doc, action)
        
        elif action.action_type == 'Execute Script':
            BusinessActionEngine._execute_script(doc, action)

    @staticmethod
    def _send_email(doc, action):
        """Send email"""
        try:
            recipients = action.email_to.split(',') if action.email_to else []
            
            frappe.sendmail(
                recipients=recipients,
                subject=action.email_subject,
                message=action.email_body,
                reference_doctype=doc.doctype,
                reference_name=doc.name,
            )
        
        except Exception as e:
            frappe.log_error(f"Failed to send email: {str(e)}")

    @staticmethod
    def _execute_script(doc, action):
        """Execute custom script"""
        try:
            if action.python_script:
                context = {'doc': doc, 'frappe': frappe}
                frappe.safe_exec(action.python_script, context)
        
        except Exception as e:
            frappe.log_error(f"Failed to execute script: {str(e)}")
