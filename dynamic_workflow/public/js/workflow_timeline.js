frappe.provide("dynamic_workflow");

/**
 * WorkflowTimeline - Renders approval history in the document form sidebar.
 */
dynamic_workflow.WorkflowTimeline = class WorkflowTimeline {
    constructor(frm) {
        this.frm = frm;
    }

    render() {
        const me = this;
        if (!this.frm.doc.dw_workflow_config) {
            return;
        }

        frappe.call({
            method: "dynamic_workflow.api.approval_api.get_approval_logs",
            args: {
                document_type: me.frm.doc.doctype,
                document_name: me.frm.doc.name,
            },
            callback: function (r) {
                if (r.message && r.message.length > 0) {
                    me.build_timeline(r.message);
                }
            },
        });
    }

    build_timeline(logs) {
        const wrapper = this.frm.dashboard.wrapper || this.frm.layout.wrapper;
        if (!wrapper) return;

        let timeline_html = $(wrapper).find(".dw-workflow-timeline");
        if (!timeline_html.length) {
            timeline_html = $(`
                <div class="dw-workflow-timeline" style="margin-top: 10px; padding: 10px; border: 1px solid #d1d8dd; border-radius: 4px;">
                    <h6 style="margin-bottom: 10px;"><i class="fa fa-clock-o"></i> ${__("Approval Timeline")}</h6>
                    <div class="dw-timeline-items"></div>
                </div>
            `);
            $(wrapper).append(timeline_html);
        }

        const container = timeline_html.find(".dw-timeline-items");
        container.empty();

        logs.forEach(function (log) {
            const status_class = me._get_status_class(log.action);
            const item_html = `
                <div class="dw-timeline-item" style="padding: 5px 0; border-bottom: 1px solid #f0f0f0;">
                    <span class="dw-timeline-badge ${status_class}" style="display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;"></span>
                    <strong>${frappe.user.full_name(log.approver) || log.approver}</strong>
                    <span class="text-muted" style="font-size: 11px;"> - ${log.action}</span>
                    <br/>
                    <small class="text-muted">${frappe.datetime.str_to_user(log.action_date)}</small>
                    ${log.comments ? '<br/><small>' + frappe.utils.escape_html(log.comments) + '</small>' : ''}
                </div>
            `;
            container.append(item_html);
        });
    }

    _get_status_class(action) {
        const class_map = {
            "Approve": "bg-success",
            "Reject": "bg-danger",
            "Return": "bg-warning",
            "Forward": "bg-info",
            "Delegate": "bg-info",
            "Terminate": "bg-dark",
            "Recall": "bg-warning",
        };
        return class_map[action] || "bg-secondary";
    }
};
