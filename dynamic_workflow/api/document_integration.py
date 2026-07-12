import json

import frappe
from frappe import _

from dynamic_workflow.dynamic_workflow.approval_engine import ApprovalEngine
from dynamic_workflow.dynamic_workflow.business_engine import BusinessActionEngine
from dynamic_workflow.dynamic_workflow.dynamic_nodes import DynamicNodeEngine
from dynamic_workflow.dynamic_workflow.delegation import DelegationEngine


def attach_dynamic_workflow(doc, method=None):
    """
    Doc event hook (before_insert): Attach workflow config to a document
    if an active Dynamic Workflow Config exists for its DocType.

    Args:
        doc: The Frappe document being inserted.
        method: Doc event method name.
    """
    if doc.get("dw_workflow_config"):
        return

    config = _get_active_config(doc.doctype)
    if not config:
        return

    doc.dw_workflow_config = config.name
    doc.dw_status = "Pending"

    approval_chain = ApprovalEngine.get_approval_chain(doc, config)
    dynamic_nodes = DynamicNodeEngine.build_workflow_nodes(doc, config)

    chain_data = {
        "matrix_chain": approval_chain,
        "dynamic_nodes": dynamic_nodes,
    }
    doc.dw_approval_chain = json.dumps(chain_data)
    doc.dw_current_node = 0


def validate_approval(doc, method=None):
    """
    Doc event hook (before_submit): Validate that the document has been
    fully approved before allowing submission.

    Args:
        doc: The Frappe document being submitted.
        method: Doc event method name.
    """
    if not doc.get("dw_workflow_config"):
        return

    status = doc.get("dw_status")
    if status and status not in ("Approved", ""):
        frappe.throw(
            _(f"Document cannot be submitted. Current approval status: {status}")
        )


def execute_business_actions(doc, method=None):
    """
    Doc event hook (on_submit): Execute business actions after document submission.

    Args:
        doc: The Frappe document that was submitted.
        method: Doc event method name.
    """
    if not doc.get("dw_workflow_config"):
        return

    config_name = doc.get("dw_workflow_config")
    config = frappe.get_doc("Dynamic Workflow Config", config_name)

    status = doc.get("dw_status")
    if status == "Approved":
        BusinessActionEngine.execute_on_approval(doc, config)
    elif status == "Rejected":
        BusinessActionEngine.execute_on_rejection(doc, config)


def _get_active_config(doctype):
    """
    Find an active Dynamic Workflow Config for the given DocType.

    Args:
        doctype: The DocType name.

    Returns:
        Dynamic Workflow Config document or None.
    """
    config_name = frappe.db.get_value(
        "Dynamic Workflow Config",
        {"document_type": doctype, "is_active": 1},
        "name",
    )
    if config_name:
        return frappe.get_doc("Dynamic Workflow Config", config_name)
    return None
