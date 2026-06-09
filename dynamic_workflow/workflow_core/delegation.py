# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import today, get_datetime
from datetime import datetime


class DelegationEngine:
    """审批代理引擎
    
    管理用户的审批权限委托
    """

    @staticmethod
    def sync_delegations():
        """定时同步代理状态"""
        
        current_date = today()
        
        # 查找过期的代理
        expired_delegations = frappe.get_all(
            'Approval Delegation',
            filters=[
                ['to_date', '<', current_date],
                ['status', '=', 'Active']
            ]
        )
        
        for delegation in expired_delegations:
            delegation_doc = frappe.get_doc('Approval Delegation', delegation.name)
            delegation_doc.status = 'Expired'
            delegation_doc.save()

    @staticmethod
    def get_delegatee(approver, doc_type=None):
        """获取代理人
        
        如果审批人设置了代理，返回代理人，否则返回审批人本身
        """
        
        current_date = today()
        
        # 查找有效的代理
        delegations = frappe.get_all(
            'Approval Delegation',
            filters=[
                ['delegator', '=', approver],
                ['from_date', '<=', current_date],
                ['to_date', '>=', current_date],
                ['is_active', '=', 1],
                ['status', '=', 'Active']
            ]
        )
        
        for delegation in delegations:
            delegation_doc = frappe.get_doc('Approval Delegation', delegation.name)
            
            # 检查文档类型限制
            if delegation_doc.document_types:
                doc_types = [dt.strip() for dt in delegation_doc.document_types.split(',')]
                if doc_type not in doc_types:
                    continue
            
            # 检查部门限制
            # 这里需要根据实际情况处理
            
            return delegation_doc.delegatee
        
        return approver

    @staticmethod
    def create_delegation(delegator, delegatee, from_date, to_date, reason='', doc_types=''):
        """创建代理记录"""
        
        delegation = frappe.get_doc({
            'doctype': 'Approval Delegation',
            'delegator': delegator,
            'delegatee': delegatee,
            'from_date': from_date,
            'to_date': to_date,
            'reason': reason,
            'document_types': doc_types,
            'is_active': 1,
            'status': 'Active'
        })
        
        delegation.insert()
        return delegation.name
