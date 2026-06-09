# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from datetime import datetime, timedelta
from frappe import _
from frappe.utils import now, get_datetime


class TimeoutEscalationEngine:
    """超时升级引擎
    
    处理审批超时和升级：
    - 24小时：发送催办
    - 48小时：升级至上级主管
    """

    @staticmethod
    def check_and_escalate():
        """后台定时任务：检查并执行超时升级"""
        
        # 查询所有未完成的审批记录
        pending_approvals = frappe.get_all(
            'Approval Log',
            filters={'status': 'Pending'},
            fields=['name', 'document_type', 'document_name', 'action_date', 'approver']
        )
        
        current_time = datetime.now()
        
        for approval in pending_approvals:
            # 查找或创建超时升级记录
            escalation = frappe.db.get_value(
                'Workflow Timeout Escalation',
                {'approval_log': approval.name}
            )
            
            if not escalation:
                continue
            
            escalation_doc = frappe.get_doc('Workflow Timeout Escalation', escalation)
            action_time = get_datetime(approval.action_date)
            hours_elapsed = (current_time - action_time).total_seconds() / 3600
            
            # 第一次超时（24小时）
            if (hours_elapsed >= escalation_doc.first_timeout_hours and 
                not escalation_doc.first_executed):
                TimeoutEscalationEngine._execute_first_timeout(escalation_doc)
            
            # 第二次超时（48小时）
            if (hours_elapsed >= escalation_doc.second_timeout_hours and 
                not escalation_doc.second_executed):
                TimeoutEscalationEngine._execute_second_timeout(escalation_doc)

    @staticmethod
    def _execute_first_timeout(escalation_doc):
        """执行第一次超时动作"""
        
        if escalation_doc.first_timeout_action == 'Send Reminder':
            TimeoutEscalationEngine._send_reminder(
                escalation_doc.approver,
                escalation_doc.document_type,
                escalation_doc.document_name
            )
        elif escalation_doc.first_timeout_action == 'Notify Manager':
            TimeoutEscalationEngine._notify_manager(
                escalation_doc.approver,
                escalation_doc.document_type,
                escalation_doc.document_name
            )
        
        escalation_doc.db_set('first_executed', 1)
        escalation_doc.db_set('first_timeout_time', now())
        escalation_doc.db_set('status', 'Reminder Sent')

    @staticmethod
    def _execute_second_timeout(escalation_doc):
        """执行第二次超时动作"""
        
        if escalation_doc.second_timeout_action == 'Notify Manager':
            # 升级给上级主管
            escalation_doc.escalation_to = TimeoutEscalationEngine._get_manager_user(escalation_doc.approver)
            escalation_doc.escalation_time = now()
            escalation_doc.save()
            
            TimeoutEscalationEngine._send_escalation_notification(
                escalation_doc.escalation_to,
                escalation_doc.approver,
                escalation_doc.document_type,
                escalation_doc.document_name
            )
        
        escalation_doc.db_set('second_executed', 1)
        escalation_doc.db_set('second_timeout_time', now())
        escalation_doc.db_set('status', 'Escalated')

    @staticmethod
    def _send_reminder(approver, doc_type, doc_name):
        """发送提醒邮件"""
        try:
            doc = frappe.get_doc(doc_type, doc_name)
            
            frappe.sendmail(
                recipients=[approver],
                subject=f'【提醒】待审批：{doc_name}',
                template='workflow_reminder',
                args={
                    'doc_name': doc_name,
                    'doc_type': doc_type,
                    'doc_link': frappe.utils.get_url_to_form(doc_type, doc_name),
                    'amount': doc.get('grand_total', 0),
                    'approver': approver,
                }
            )
        except Exception as e:
            frappe.log_error(f"Failed to send reminder: {str(e)}")

    @staticmethod
    def _notify_manager(approver, doc_type, doc_name):
        """通知主管（升级）"""
        try:
            manager = TimeoutEscalationEngine._get_manager_user(approver)
            
            if manager:
                doc = frappe.get_doc(doc_type, doc_name)
                frappe.sendmail(
                    recipients=[manager],
                    subject=f'【升级】待审批：{doc_name}',
                    template='workflow_escalation',
                    args={
                        'doc_name': doc_name,
                        'doc_type': doc_type,
                        'original_approver': approver,
                        'doc_link': frappe.utils.get_url_to_form(doc_type, doc_name),
                        'amount': doc.get('grand_total', 0),
                    }
                )
        except Exception as e:
            frappe.log_error(f"Failed to notify manager: {str(e)}")

    @staticmethod
    def _send_escalation_notification(manager, approver, doc_type, doc_name):
        """发送升级通知"""
        try:
            doc = frappe.get_doc(doc_type, doc_name)
            frappe.sendmail(
                recipients=[manager],
                subject=f'【升级】{approver} 未及时审批：{doc_name}',
                template='workflow_escalation',
                args={
                    'doc_name': doc_name,
                    'original_approver': approver,
                    'doc_link': frappe.utils.get_url_to_form(doc_type, doc_name),
                }
            )
        except Exception as e:
            frappe.log_error(f"Failed to send escalation notification: {str(e)}")

    @staticmethod
    def _get_manager_user(approver):
        """获取用户的上级主管"""
        try:
            employee = frappe.get_value('Employee', {'user_id': approver}, 'name')
            if employee:
                reports_to = frappe.get_value('Employee', employee, 'reports_to')
                if reports_to:
                    manager_user = frappe.get_value('Employee', reports_to, 'user_id')
                    return manager_user
        except:
            pass
        return None
