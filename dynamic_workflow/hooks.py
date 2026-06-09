# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

app_name = "dynamic_workflow"
app_title = "Dynamic Workflow 3.0"
app_publisher = "Your Company"
app_description = "Advanced workflow engine with approval matrix, dynamic nodes, and WeChat integration"
app_email = "your-email@example.com"
app_license = "GNU General Public License v3"
app_version = "1.0.0"

# Fixtures
fixtures = []

# Document Events
doc_events = {
    "Purchase Request": {
        "before_insert": "dynamic_workflow.api.purchase_order_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.purchase_order_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.purchase_order_integration.execute_business_actions",
    },
    "Purchase Order": {
        "before_insert": "dynamic_workflow.api.purchase_order_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.purchase_order_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.purchase_order_integration.execute_business_actions",
    },
    "Sales Order": {
        "before_insert": "dynamic_workflow.api.sales_order_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.sales_order_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.sales_order_integration.execute_business_actions",
    },
}

# Scheduler Events
scheduler_events = {
    "hourly": [
        "dynamic_workflow.workflow_core.timeout_escalation.TimeoutEscalationEngine.check_and_escalate"
    ],
    "daily": [
        "dynamic_workflow.workflow_core.delegation.DelegationEngine.sync_delegations"
    ]
}

# Asset Includes
app_include_js = [
    "assets/dynamic_workflow/js/approval_dialog.js",
    "assets/dynamic_workflow/js/workflow_timeline.js",
]

app_include_css = [
    "assets/dynamic_workflow/css/workflow.css",
]

# Custom Fields
custom_fields = {
    "Purchase Request": [
        {
            "fieldname": "dw_workflow_section",
            "fieldtype": "Section Break",
            "label": "Dynamic Workflow",
            "insert_after": "company"
        },
        {
            "fieldname": "dw_workflow_config",
            "fieldtype": "Link",
            "label": "Workflow Config",
            "options": "Dynamic Workflow Config",
            "hidden": 1,
            "insert_after": "dw_workflow_section"
        },
        {
            "fieldname": "dw_status",
            "fieldtype": "Select",
            "label": "Workflow Status",
            "options": "Draft\nPending Approval\nApproved\nRejected\nCompleted",
            "read_only": 1,
            "insert_after": "dw_workflow_config"
        },
        {
            "fieldname": "dw_approval_chain",
            "fieldtype": "JSON",
            "label": "Approval Chain",
            "hidden": 1,
            "insert_after": "dw_status"
        },
        {
            "fieldname": "dw_current_node",
            "fieldtype": "Int",
            "label": "Current Approval Node",
            "hidden": 1,
            "insert_after": "dw_approval_chain"
        },
    ],
    "Purchase Order": [
        {
            "fieldname": "dw_workflow_section",
            "fieldtype": "Section Break",
            "label": "Dynamic Workflow",
            "insert_after": "company"
        },
        {
            "fieldname": "dw_workflow_config",
            "fieldtype": "Link",
            "label": "Workflow Config",
            "options": "Dynamic Workflow Config",
            "hidden": 1,
            "insert_after": "dw_workflow_section"
        },
        {
            "fieldname": "dw_status",
            "fieldtype": "Select",
            "label": "Workflow Status",
            "options": "Draft\nPending Approval\nApproved\nRejected\nCompleted",
            "read_only": 1,
            "insert_after": "dw_workflow_config"
        },
    ],
}

# Page routing
page_length = 500

# Jinja2 Settings
template_apps = ["dynamic_workflow"]

# Error Log
ignored_exceptions_in_hook_logs = []
