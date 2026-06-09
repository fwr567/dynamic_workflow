# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from dynamic_workflow.workflow_core.organization_engine import OrganizationEngine
from dynamic_workflow.workflow_core.dynamic_nodes import DynamicNodeEngine


class ApprovalEngine:
    """核心审批引擎 - 第一层和第二层"""

    def __init__(self, doc, workflow_config):
        self.doc = doc
        self.workflow_config = workflow_config
        self.approval_matrix = None
        self.approval_chain = []

    def get_approval_chain(self):
        """获取审批链"""
        workflow_config = frappe.get_doc('Dynamic Workflow Config', self.workflow_config)
        
        if not workflow_config.approval_matrix:
            return []
        
        approval_matrix = frappe.get_doc('Approval Matrix', workflow_config.approval_matrix)
        
        # 遍历规则，找到匹配的
        for rule in approval_matrix.rules:
            if self._match_conditions(rule):
                # 获取审批链步骤
                chain_steps = self._build_approval_chain(rule)
                return chain_steps
        
        return []

    def _match_conditions(self, rule):
        """判断条件是否匹配"""
        
        # 检查金额
        if rule.amount_from or rule.amount_to:
            amount_field = rule.amount_field or 'grand_total'
            amount = self.doc.get(amount_field) or 0
            
            if rule.amount_from and amount < rule.amount_from:
                return False
            if rule.amount_to and amount > rule.amount_to:
                return False
        
        # 检查部门
        if rule.department and self.doc.get('department') != rule.department:
            return False
        
        # 检查业务线
        if rule.business_line and self.doc.get('business_line') != rule.business_line:
            return False
        
        # 检查项目类型
        if rule.project_type and self.doc.get('project_type') != rule.project_type:
            return False
        
        # 检查供应商等级
        if rule.vendor_grade and self.doc.get('vendor_grade') != rule.vendor_grade:
            return False
        
        # 检查自定义条件
        if rule.custom_condition:
            try:
                result = eval(rule.custom_condition, {'doc': self.doc, 'frappe': frappe})
                if not result:
                    return False
            except Exception as e:
                frappe.log_error(f"Custom condition error: {str(e)}")
                return False
        
        return True

    def _build_approval_chain(self, rule):
        """构建审批链"""
        chain = []
        
        for step in rule.approval_chain_desc:
            approvers = OrganizationEngine.get_approvers(self.doc, step.assign_mode, step)
            
            chain.append({
                'step_sequence': step.step_sequence,
                'assign_mode': step.assign_mode,
                'approvers': approvers,
                'node_type': rule.approval_chain_type,  # Serial or Parallel
                'status': 'Pending'
            })
        
        return chain

    def submit_approval(self, action, **kwargs):
        """提交审批"""
        from dynamic_workflow.workflow_core.approval_actions import ApprovalAction
        
        approval_log = frappe.get_doc({
            'doctype': 'Approval Log',
            'document_type': self.doc.doctype,
            'document_name': self.doc.name,
            'approver': frappe.session.user,
            'action': action,
            'comments': kwargs.get('comments', ''),
            'status': 'Completed',
            'action_date': frappe.utils.now()
        })
        approval_log.insert()
        
        # 执行相应的审批动作
        ApprovalAction.perform_action(self.doc, action, **kwargs)
        
        return approval_log
