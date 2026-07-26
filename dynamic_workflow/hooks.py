app_name = "dynamic_workflow"
app_title = "Dynamic Workflow"
app_publisher = "fwr567"
app_description = "Advanced workflow engine for ERPNext V16 with approval matrix, dynamic nodes, and WeChat integration"
app_email = "fengweirui567@163.com"
app_license = "agpl-3.0"

# Frappe requirement
# required_apps = ["frappe", "erpnext"]

# Include JS and CSS
app_include_js = [
    "/assets/dynamic_workflow/js/approval_dialog.js",
    "/assets/dynamic_workflow/js/workflow_timeline.js",
    "/assets/dynamic_workflow/js/approval_utils.js",
]

app_include_css = [
    "/assets/dynamic_workflow/css/workflow.css",
    "/assets/dynamic_workflow/css/approval_timeline.css",
]

# Setup and Migration
after_install = "dynamic_workflow.setup.install.after_install"
after_migrate = "dynamic_workflow.setup.install.after_migrate"

# Document Event Handlers
doc_events = {
    "Material Request": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
        "on_cancel": "dynamic_workflow.api.document_integration.on_cancel_workflow",
    },
    "Purchase Order": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
        "on_cancel": "dynamic_workflow.api.document_integration.on_cancel_workflow",
    },
    "Sales Order": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
        "on_cancel": "dynamic_workflow.api.document_integration.on_cancel_workflow",
    },
    "Expense Claim": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    },
    "Leave Application": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    },
}

# Scheduler Events
scheduler_events = {
    "hourly": [
        "dynamic_workflow.dynamic_workflow.timeout_escalation.check_and_escalate",
        "dynamic_workflow.dynamic_workflow.delegation.sync_delegations",
    ],
    "daily": [
        "dynamic_workflow.dynamic_workflow.delegation.cleanup_expired_delegations",
        "dynamic_workflow.dynamic_workflow.approval_engine.cleanup_old_logs",
    ],
}

# Fixtures - Workspace and Custom Fields
fixtures = [
    {
        "doctype": "Workspace",
        "filters": [["name", "in", ["Dynamic Workflow"]]],
    },
    {
        "doctype": "Custom Field",
        "filters": [["dt", "in", [
            "Material Request",
            "Purchase Order", 
            "Sales Order",
            "Expense Claim",
            "Leave Application",
        ]]],
    }
]

# Website routes
website_route_rules = [
    {
        "route": "/approval/<approval_id>",
        "page_or_generator": "approval_detail"
    }
]

# Notification triggers
notification_config = {
    "Approval Log": {
        "after_insert": [
            "dynamic_workflow.integrations.notification.send_approval_notification",
        ]
    }
}

# Web form entries
web_form_entries = [
    {"name": "approval_form", "doctype": "Approval Log"}
]

# Sidebar menu items
app_logo_url = "/assets/dynamic_workflow/images/logo.png"

# Database indexes
db_indexes = [
    ("dynamic_workflow_config", ["doctype", "enabled"]),
    ("approval_log", ["document_type", "document_name", "status"]),
    ("approval_delegation", ["delegator", "delegatee", "status"]),
]
