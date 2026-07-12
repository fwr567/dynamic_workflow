frappe.provide("dynamic_workflow");

/**
 * ApprovalDialog - Provides an approval action dialog for documents
 * configured with Dynamic Workflow.
 */
dynamic_workflow.ApprovalDialog = class ApprovalDialog {
    constructor(frm) {
        this.frm = frm;
    }

    show() {
        const me = this;
        const status = this.frm.doc.dw_status;

        if (!status || status === "Approved" || status === "Terminated" || status === "Recalled") {
            return;
        }

        const dialog = new frappe.ui.Dialog({
            title: __("Approval Action"),
            fields: [
                {
                    fieldname: "action",
                    label: __("Action"),
                    fieldtype: "Select",
                    options: "Approve\nReject\nReturn\nForward\nCountersign\nDelegate\nTerminate",
                    reqd: 1,
                },
                {
                    fieldname: "comments",
                    label: __("Comments"),
                    fieldtype: "Text",
                },
                {
                    fieldname: "forward_to",
                    label: __("Forward To"),
                    fieldtype: "Link",
                    options: "User",
                    depends_on: "eval:doc.action=='Forward'",
                },
                {
                    fieldname: "delegate_to",
                    label: __("Delegate To"),
                    fieldtype: "Link",
                    options: "User",
                    depends_on: "eval:doc.action=='Delegate'",
                },
            ],
            primary_action_label: __("Submit"),
            primary_action: function (values) {
                me.submit_action(values);
                dialog.hide();
            },
        });

        dialog.show();
    }

    submit_action(values) {
        const me = this;
        frappe.call({
            method: "dynamic_workflow.api.approval_api.submit_approval",
            args: {
                document_type: me.frm.doc.doctype,
                document_name: me.frm.doc.name,
                action: values.action,
                comments: values.comments || "",
                forward_to: values.forward_to || "",
                delegate_to: values.delegate_to || "",
            },
            callback: function (r) {
                if (r.message && r.message.status === "success") {
                    frappe.show_alert({
                        message: r.message.message,
                        indicator: "green",
                    });
                    me.frm.reload_doc();
                }
            },
            error: function () {
                frappe.show_alert({
                    message: __("Failed to submit approval action."),
                    indicator: "red",
                });
            },
        });
    }
};

/**
 * Attach an approval button to the form toolbar if the document
 * has a Dynamic Workflow configuration.
 */
dynamic_workflow.attach_approval_button = function (frm) {
    if (frm.doc.dw_workflow_config && frm.doc.dw_status &&
        frm.doc.dw_status !== "Approved" &&
        frm.doc.dw_status !== "Terminated" &&
        frm.doc.dw_status !== "Recalled") {
        frm.add_custom_button(__("Approval Action"), function () {
            const dialog = new dynamic_workflow.ApprovalDialog(frm);
            dialog.show();
        }, __("Dynamic Workflow"));
    }
};
