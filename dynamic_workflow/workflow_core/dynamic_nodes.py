# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


class DynamicNodeEngine:
    """动态节点引擎 - 第三层
    
    支持运行时动态插入审批节点
    不是预定义流程，而是根据条件动态生成
    """

    @staticmethod
    def build_workflow_nodes(doc, workflow_config):
        """动态构建工作流节点"""
        nodes = []
        
        workflow = frappe.get_doc('Dynamic Workflow Config', workflow_config)
        
        for node_template in workflow.node_templates:
            # 评估是否应该包含此节点
            if DynamicNodeEngine._should_include_node(doc, node_template):
                node = DynamicNodeEngine._create_node(doc, node_template)
                nodes.append(node)
        
        return nodes

    @staticmethod
    def _should_include_node(doc, node_template):
        """根据条件判断是否包含节点"""
        
        # 金额条件
        if node_template.condition_type == 'Amount':
            amount_field = 'grand_total'
            amount = doc.get(amount_field) or 0
            
            if node_template.amount_from and amount < node_template.amount_from:
                return False
            if node_template.amount_to and amount > node_template.amount_to:
                return False
        
        # 自定义条件
        if node_template.custom_condition:
            try:
                result = eval(node_template.custom_condition, {'doc': doc, 'frappe': frappe})
                if not result:
                    return False
            except Exception as e:
                frappe.log_error(f"Node condition error: {str(e)}")
                return False
        
        return True

    @staticmethod
    def _create_node(doc, node_template):
        """创建工作流节点"""
        return {
            'node_id': node_template.name,
            'node_name': node_template.node_name,
            'node_type': node_template.node_type,  # serial / parallel
            'sequence': node_template.sequence,
            'approval_steps': [
                {
                    'step_sequence': step.step_sequence,
                    'assign_mode': step.assign_mode,
                    'approvers': step.approvers,
                } for step in node_template.approval_steps
            ]
        }
