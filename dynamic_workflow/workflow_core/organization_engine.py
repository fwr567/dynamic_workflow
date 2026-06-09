# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


class OrganizationEngine:
    """组织关系引擎 - 第二层
    
    支持多种审批者分配模式：
    - 直属主管
    - 部门负责人
    - 条线负责人
    - 项目经理
    - 成本中心负责人
    - 职位
    - 角色
    - 自定义脚本
    """

    @staticmethod
    def get_approvers(doc, assign_mode, step):
        """根据分配模式获取审批者"""
        
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

    @staticmethod
    def _get_manager(doc):
        """获取提交者的直属主管"""
        try:
            employee = frappe.get_value('Employee', {'user_id': doc.owner}, 'name')
            if employee:
                reports_to = frappe.get_value('Employee', employee, 'reports_to')
                if reports_to:
                    manager = frappe.get_value('Employee', reports_to, 'user_id')
                    return [manager] if manager else []
        except:
            pass
        return []

    @staticmethod
    def _get_department_head(doc):
        """获取所在部门的部门负责人"""
        try:
            dept = doc.get('department')
            if dept:
                dept_head = frappe.get_value('Department', dept, 'manager')
                if dept_head:
                    user = frappe.get_value('Employee', dept_head, 'user_id')
                    return [user] if user else []
        except:
            pass
        return []

    @staticmethod
    def _get_business_line_head(doc):
        """获取业务线负责人"""
        try:
            business_line = doc.get('business_line')
            if business_line:
                # 假设有 Business Line 文档类型
                head = frappe.get_value('Business Line', business_line, 'manager')
                if head:
                    user = frappe.get_value('Employee', head, 'user_id')
                    return [user] if user else []
        except:
            pass
        return []

    @staticmethod
    def _get_project_manager(doc):
        """获取项目经理"""
        try:
            project = doc.get('project')
            if project:
                pm = frappe.get_value('Project', project, 'project_manager')
                return [pm] if pm else []
        except:
            pass
        return []

    @staticmethod
    def _get_cost_center_head(doc):
        """获取成本中心负责人"""
        try:
            cost_center = doc.get('cost_center')
            if cost_center:
                head = frappe.get_value('Cost Center', cost_center, 'manager')
                if head:
                    user = frappe.get_value('Employee', head, 'user_id')
                    return [user] if user else []
        except:
            pass
        return []

    @staticmethod
    def _get_users_by_role(role):
        """根据角色获取所有用户"""
        try:
            if role:
                users = frappe.db.sql("""
                    SELECT DISTINCT u.name
                    FROM `tabUser` u
                    JOIN `tabHas Role` hr ON u.name = hr.user
                    WHERE hr.role = %s AND u.enabled = 1
                """, (role,), as_dict=False)
                return [u[0] for u in users]
        except:
            pass
        return []

    @staticmethod
    def _get_by_designation(designation):
        """根据职位获取用户"""
        try:
            if designation:
                employees = frappe.get_all('Employee', 
                    filters={'designation': designation, 'status': 'Active'},
                    fields=['user_id'])
                return [e.user_id for e in employees if e.user_id]
        except:
            pass
        return []

    @staticmethod
    def _execute_custom_script(doc, script):
        """执行自定义脚本"""
        try:
            if script:
                context = {'doc': doc, 'frappe': frappe}
                exec(script, context)
                return context.get('approvers', [])
        except Exception as e:
            frappe.log_error(f"Custom script error: {str(e)}")
        return []
