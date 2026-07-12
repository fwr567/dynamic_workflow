app_name = "dynamic_workflow"
app_title = "Dynamic Workflow"
app_publisher = "fwr567"
app_description = "Advanced workflow engine for ERPNext V16 with approval matrix, dynamic nodes, and WeChat integration"
app_email = "fengweirui567@163.com"
app_license = "gpl-3.0"

# required_apps = ["frappe", "erpnext"]

app_include_js = [
    "/assets/dynamic_workflow/js/approval_dialog.js",
    "/assets/dynamic_workflow/js/workflow_timeline.js",
]

app_include_css = [
    "/assets/dynamic_workflow/css/workflow.css",
]

after_install = "dynamic_workflow.setup.install.after_install"
after_migrate = "dynamic_workflow.setup.install.after_migrate"

doc_events = {
    "Purchase Request": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    },
    "Purchase Order": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    },
    "Sales Order": {
        "before_insert": "dynamic_workflow.api.document_integration.attach_dynamic_workflow",
        "before_submit": "dynamic_workflow.api.document_integration.validate_approval",
        "on_submit": "dynamic_workflow.api.document_integration.execute_business_actions",
    },
}

scheduler_events = {
    "hourly": [
        "dynamic_workflow.dynamic_workflow.timeout_escalation.check_and_escalate",
    ],
    "daily": [
        "dynamic_workflow.dynamic_workflow.delegation.sync_delegations",
    ],
}

fixtures = [
    {
        "doctype": "Workspace",
        "filters": [["name", "in", ["Dynamic Workflow"]]],
    }
]
