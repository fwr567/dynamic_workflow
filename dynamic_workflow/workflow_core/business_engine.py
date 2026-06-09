# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
import requests
import json
from frappe import _


class BusinessActionEngine:
    """业务动作引擎 - 第五层
    
    审批通过后执行业务操作
    支持：创建采购订单、生成会计凭证、发送通知、调用第三方API等
    """

    @staticmethod
    def execute_on_approval(doc, workflow_config):
        """审批通过后执行业务动作"""
        
        workflow = frappe.get_doc('Dynamic Workflow Config', workflow_config)
        
        for action in workflow.on_approval_actions:
            try:
                BusinessActionEngine._execute_action(doc, action)
                
                # 记录执行结果
                frappe.get_doc({
                    'doctype': 'Business Action Log',
                    'document_type': doc.doctype,
                    'document_name': doc.name,
                    'action_type': action.action_type,
                    'status': 'Success',
                    'timestamp': frappe.utils.now()
                }).insert()
                
            except Exception as e:
                frappe.log_error(f"Business action failed: {str(e)}")
                frappe.get_doc({
                    'doctype': 'Business Action Log',
                    'document_type': doc.doctype,
                    'document_name': doc.name,
                    'action_type': action.action_type,
                    'status': 'Error',
                    'error_message': str(e),
                    'timestamp': frappe.utils.now()
                }).insert()

    @staticmethod
    def execute_on_rejection(doc, workflow_config):
        """拒绝后执行业务动作"""
        
        workflow = frappe.get_doc('Dynamic Workflow Config', workflow_config)
        
        for action in workflow.on_rejection_actions:
            try:
                BusinessActionEngine._execute_action(doc, action)
            except Exception as e:
                frappe.log_error(f"Business action on rejection failed: {str(e)}")

    @staticmethod
    def _execute_action(doc, action):
        """执行具体的业务动作"""
        
        if action.action_type == 'Create Document':
            BusinessActionEngine._create_document(doc, action)
        
        elif action.action_type == 'Send Email':
            BusinessActionEngine._send_email(doc, action)
        
        elif action.action_type == 'Call API':
            BusinessActionEngine._call_external_api(doc, action)
        
        elif action.action_type == 'Execute Script':
            BusinessActionEngine._execute_script(doc, action)
        
        elif action.action_type == 'Lock Inventory':
            BusinessActionEngine._lock_inventory(doc, action)
        
        elif action.action_type == 'Create Journal Entry':
            BusinessActionEngine._create_journal_entry(doc, action)

    @staticmethod
    def _create_document(doc, action):
        """创建文档（如采购订单）"""
        
        if not action.create_document_type:
            return
        
        new_doc = frappe.get_doc({
            'doctype': action.create_document_type,
            'source_document': f"{doc.doctype}:{doc.name}",
        })
        
        # 映射字段
        if action.map_fields:
            try:
                field_map = json.loads(action.map_fields)
                for src_field, dst_field in field_map.items():
                    if hasattr(doc, src_field):
                        setattr(new_doc, dst_field, doc.get(src_field))
            except:
                pass
        
        new_doc.insert()
        new_doc.submit()
        return new_doc.name

    @staticmethod
    def _send_email(doc, action):
        """发送邮件"""
        
        recipients = action.email_to.split(',') if action.email_to else []
        
        frappe.sendmail(
            recipients=recipients,
            subject=action.email_subject,
            message=action.email_body,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
        )

    @staticmethod
    def _call_external_api(doc, action):
        """调用第三方 API"""
        
        url = action.api_url
        method = action.api_method
        
        payload = {}
        if action.api_payload:
            try:
                payload = json.loads(action.api_payload)
            except:
                payload = {}
        
        # 替换变量
        payload = BusinessActionEngine._replace_variables(payload, doc)
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=payload, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=payload, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            
            return response.json()
        
        except Exception as e:
            frappe.log_error(f"API call failed: {str(e)}")
            raise

    @staticmethod
    def _execute_script(doc, action):
        """执行自定义脚本"""
        try:
            context = {'doc': doc, 'frappe': frappe}
            exec(action.python_script, context)
        except Exception as e:
            frappe.log_error(f"Script execution error: {str(e)}")
            raise

    @staticmethod
    def _lock_inventory(doc, action):
        """锁定库存"""
        # 实现库存锁定逻辑
        pass

    @staticmethod
    def _create_journal_entry(doc, action):
        """创建会计凭证"""
        # 实现会计凭证创建逻辑
        pass

    @staticmethod
    def _replace_variables(payload, doc):
        """替换 payload 中的变量"""
        import json
        payload_str = json.dumps(payload)
        
        # 替换 {{field_name}} 格式的变量
        for field in doc.meta.get_valid_columns():
            value = doc.get(field)
            payload_str = payload_str.replace(f"{{{{{field}}}}}", str(value))
        
        return json.loads(payload_str)
