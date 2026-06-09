# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


class OrganizationEngine:
    """
    Organization Relationship Engine - Layer 2
    
    Supports multiple approval assignment modes:
    - User (direct assignment)
    - Role (by user role)
    - Manager (direct manager)
    - Department Head
    - Business Line Head
    - Project Manager
    - Cost Center Head
    - Designation
    - Custom Script
    """

    @staticmethod
    def get_approvers(doc, assign_mode, step):
        """Get approvers based on assignment mode"""
        
        try:
            if assign_mode == "User":
                return [step.approver_user] if step.approver_user else []
            
            elif assign_mode == "Role":
                return OrganizationEngine._get_users_by_role(step.approver_role)
            
            elif assign_mode == "Manager":
                return OrganizationEngine._get_manager(doc)
            
            elif assign_mode == "Department Head":
                return OrganizationEngine._get_department_head(doc)
            
            elif assign_mode == "Business Line Head":
                return OrganizationEngine._get_business_line_head(doc)
            
            elif assign_mode == "Project Manager":
                return OrganizationEngine._get_project_manager(doc)
            
            elif assign_mode == "Cost Center Head":
                return OrganizationEngine._get_cost_center_head(doc)
            
            elif assign_mode == "Designation":
                return OrganizationEngine._get_by_designation(step.designation)
            
            elif assign_mode == "Custom Script":
                return OrganizationEngine._execute_custom_script(doc, step.custom_script)
            
            return []
        except Exception as e:
            frappe.log_error(f"Error getting approvers: {str(e)}")
            return []

    @staticmethod
    def _get_manager(doc):
        """Get direct manager of document owner"""
        try:
            employee = frappe.get_value('Employee', {'user_id': doc.owner}, 'name')
            if employee:
                reports_to = frappe.get_value('Employee', employee, 'reports_to')
                if reports_to:
                    manager = frappe.get_value('Employee', reports_to, 'user_id')
                    return [manager] if manager else []
        except Exception as e:
            frappe.log_error(f"Error getting manager: {str(e)}")
        return []

    @staticmethod
    def _get_department_head(doc):
        """Get department head"""
        try:
            dept = doc.get('department')
            if dept:
                dept_head = frappe.get_value('Department', dept, 'manager')
                if dept_head:
                    user = frappe.get_value('Employee', dept_head, 'user_id')
                    return [user] if user else []
        except Exception as e:
            frappe.log_error(f"Error getting department head: {str(e)}")
        return []

    @staticmethod
    def _get_business_line_head(doc):
        """Get business line head"""
        try:
            business_line = doc.get('business_line')
            if business_line:
                head = frappe.get_value('Business Line', business_line, 'manager')
                if head:
                    user = frappe.get_value('Employee', head, 'user_id')
                    return [user] if user else []
        except Exception as e:
            frappe.log_error(f"Error getting business line head: {str(e)}")
        return []

    @staticmethod
    def _get_project_manager(doc):
        """Get project manager"""
        try:
            project = doc.get('project')
            if project:
                pm = frappe.get_value('Project', project, 'project_manager')
                return [pm] if pm else []
        except Exception as e:
            frappe.log_error(f"Error getting project manager: {str(e)}")
        return []

    @staticmethod
    def _get_cost_center_head(doc):
        """Get cost center head"""
        try:
            cost_center = doc.get('cost_center')
            if cost_center:
                head = frappe.get_value('Cost Center', cost_center, 'manager')
                if head:
                    user = frappe.get_value('Employee', head, 'user_id')
                    return [user] if user else []
        except Exception as e:
            frappe.log_error(f"Error getting cost center head: {str(e)}")
        return []

    @staticmethod
    def _get_users_by_role(role):
        """Get all users with specific role"""
        try:
            if role:
                users = frappe.get_all('User',
                    filters={'enabled': 1},
                    fields=['name'])
                # Filter users with the role
                approved_users = []
                for u in users:
                    if frappe.get_all('Has Role',
                        filters={'user': u['name'], 'role': role}):
                        approved_users.append(u['name'])
                return approved_users
        except Exception as e:
            frappe.log_error(f"Error getting users by role: {str(e)}")
        return []

    @staticmethod
    def _get_by_designation(designation):
        """Get users by designation"""
        try:
            if designation:
                employees = frappe.get_all('Employee',
                    filters={'designation': designation, 'status': 'Active'},
                    fields=['user_id'])
                return [e['user_id'] for e in employees if e['user_id']]
        except Exception as e:
            frappe.log_error(f"Error getting users by designation: {str(e)}")
        return []

    @staticmethod
    def _execute_custom_script(doc, script):
        """Execute custom script to get approvers"""
        try:
            if script:
                context = {'doc': doc, 'frappe': frappe}
                frappe.safe_exec(script, context)
                return context.get('approvers', [])
        except Exception as e:
            frappe.log_error(f"Error executing custom script: {str(e)}")
        return []
