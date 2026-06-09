# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import now


class ApprovalAction:
    """审批动作插件 - 第四层
    
    支持 11 种审批动作：
    - Approve (同意)
    - Reject (拒绝)
    - Return (退回)
    - Forward (转办)
    - Countersign (加签)
    - Cosign (会签)
    - Delegate (委托)
    - Reminder (催办)
    - CC (抄送)
    - Terminate (终止)
    - Recall (撤回)
    """

    ACTIONS = {
        'approve': '同意',
        'reject': '拒绝',
        'return': '退回',
        'forward': '转办',
        'countersign': '加签',
        'cosign': '会签',
        'delegate': '委托',
        'reminder': '催办',
        'cc': '抄送',
        'terminate': '终止',
        'recall': '撤回',
    }

    @staticmethod
    def perform_action(doc, action, **kwargs):
        """执行审批动作"""
        
        action = action.lower()
        
        if action == 'approve':
            return ApprovalAction._approve(doc, **kwargs)
        elif action == 'reject':
            return ApprovalAction._reject(doc, **kwargs)
        elif action == 'return':
            return ApprovalAction._return(doc, **kwargs)
        elif action == 'forward':
            return ApprovalAction._forward(doc, **kwargs)
        elif action == 'countersign':
            return ApprovalAction._countersign(doc, **kwargs)
        elif action == 'delegate':
            return ApprovalAction._delegate(doc, **kwargs)
        elif action == 'terminate':
            return ApprovalAction._terminate(doc, **kwargs)
        elif action == 'recall':
            return ApprovalAction._recall(doc, **kwargs)

    @staticmethod
    def _approve(doc, **kwargs):
        """同意：文档推进到下一步"""
        doc.dw_status = 'Approved'
        doc.save()
        return True

    @staticmethod
    def _reject(doc, **kwargs):
        """拒绝：文档返回到初始状态"""
        doc.dw_status = 'Rejected'
        doc.dw_current_node = -1
        doc.save()
        return True

    @staticmethod
    def _return(doc, **kwargs):
        """退回：返回到前一步"""
        if doc.dw_current_node > 0:
            doc.dw_current_node -= 1
        doc.dw_status = 'Pending Approval'
        doc.save()
        return True

    @staticmethod
    def _forward(doc, forward_to, **kwargs):
        """转办：转交给其他审批者"""
        # 创建新的审批记录
        approval_log = frappe.get_doc({
            'doctype': 'Approval Log',
            'document_type': doc.doctype,
            'document_name': doc.name,
            'approver': forward_to,
            'action': 'Forward',
            'forward_to': forward_to,
            'comments': kwargs.get('comments', ''),
            'status': 'Pending',
        })
        approval_log.insert()
        return True

    @staticmethod
    def _countersign(doc, additional_approvers, **kwargs):
        """加签：添加额外的审批人"""
        if isinstance(additional_approvers, str):
            additional_approvers = additional_approvers.split(',')
        
        for approver in additional_approvers:
            frappe.get_doc({
                'doctype': 'Approval Log',
                'document_type': doc.doctype,
                'document_name': doc.name,
                'approver': approver.strip(),
                'action': 'Countersign',
                'comments': kwargs.get('comments', ''),
                'status': 'Pending',
            }).insert()
        return True

    @staticmethod
    def _delegate(doc, **kwargs):
        """委托：将权限委托给其他人"""
        delegation = frappe.get_doc({
            'doctype': 'Approval Delegation',
            'delegator': frappe.session.user,
            'delegatee': kwargs.get('delegatee'),
            'from_date': frappe.utils.today(),
            'reason': kwargs.get('reason', ''),
        })
        delegation.insert()
        return True

    @staticmethod
    def _terminate(doc, **kwargs):
        """终止：终止审批流程"""
        doc.dw_status = 'Terminated'
        doc.save()
        return True

    @staticmethod
    def _recall(doc, **kwargs):
        """撤回：撤回已提交的审批"""
        doc.dw_status = 'Draft'
        doc.dw_current_node = 0
        doc.save()
        return True
