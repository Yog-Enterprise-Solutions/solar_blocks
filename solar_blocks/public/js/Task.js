frappe.ui.form.on('Task', {
    refresh: function(frm) {
        // Check if the subject matches the specified values and the status is 'In Progress'
        if (['Engineering', 'Electrical Permit', 'Electrical Inspection', 'Installation Work'].includes(frm.doc.subject) && frm.doc.project_status === 'In Progress' && frm.doc.custom_sent===0) {
            // Add the custom button
            frm.add_custom_button(__('Send Mail'), function() {
                if (frm.doc.custom_receipient_email){
                        frappe.call({
                            method: 'solar_blocks.override.task.send_email_on_task',
                            args: {
                                recipient_email:frm.doc.custom_receipient_email,
                                custom_customer_name:frm.doc.custom_customer_name,
                                subject:frm.doc.subject,
                                custom_scheduled_on:frm.doc.custom_scheduled_on ||"",
                                project:frm.doc.project

                            },
                            freeze: true,
                            callback: (r) => {
                               frm.set_value('custom_sent',1)
                               cur_frm.save()
                            },
                            error: (r) => {
                                // on error
                            }
                        })}
                else{
                    frappe.throw("Please Give receipient email ID")
                }
            });
        }
    },
    custom_receipient_email:function(frm){
        frm.set_value('custom_sent',0)
    }
});
