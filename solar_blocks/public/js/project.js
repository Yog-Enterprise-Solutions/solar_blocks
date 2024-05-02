frappe.ui.form.on('Project', {
    onload(frm) {
        // Hide the collapsible section on load
       // Hide the element with the class "connections"
       $('.section-head.collapsible:contains("Connections")').hide();
       if(!frappe.user.has_role("System Manager")){
        frm.get_field('task_details').grid.cannot_add_rows = true;
// 	let status = frappe.meta.get_docfield("Task Detail","task_status", cur_frm.doc.name);
// 	let notes = frappe.meta.get_docfield("Task Detail","notes", cur_frm.doc.name);
// 	let actual_dates = frappe.meta.get_docfield("Task Detail","completion_date", cur_frm.doc.name);
    
    let assigned_to_team = frappe.meta.get_docfield("Task Detail","assigned_to_team", cur_frm.doc.name);
    let assigned_to_individual = frappe.meta.get_docfield("Task Detail","assigned_to_individual", cur_frm.doc.name);
    let created_by = frappe.meta.get_docfield("Task Detail","created_by", cur_frm.doc.name);
    let closed_by = frappe.meta.get_docfield("Task Detail","closed_by", cur_frm.doc.name);
    let started_on = frappe.meta.get_docfield("Task Detail","started_on", cur_frm.doc.name);
    let scheduled_close = frappe.meta.get_docfield("Task Detail","scheduled_close", cur_frm.doc.name);
// 	let attachement = frappe.meta.get_docfield("Task Detail","attachement", cur_frm.doc.name);
    let timeline = frappe.meta.get_docfield("Task Detail","timeline", cur_frm.doc.name);
    let priority = frappe.meta.get_docfield("Task Detail","priority", cur_frm.doc.name);
    let assign_date = frappe.meta.get_docfield("Task Detail","assign_date", cur_frm.doc.name);
    let is_notified = frappe.meta.get_docfield("Task Detail","is_notified", cur_frm.doc.name);
    
    assigned_to_team.disabled = 1;
    assigned_to_individual.disabled = 1;
    created_by.disabled = 1;
    closed_by.disabled = 1;
    started_on.disabled = 1;
    scheduled_close.disabled = 1;
// 	attachement.disabled = 1;
    timeline.disabled = 1;
    priority.disabled = 1;
    assign_date.disabled = 1;
    is_notified.disabled = 1;
    
    // status.disabled = 1;
    // notes.disabled = 1;
    // actual_dates.disabled = 1;
    
    // cur_frm.refresh_field('task_status');
    // cur_frm.refresh_field('notes');
    // cur_frm.refresh_field('completion_date');
    
    cur_frm.refresh_field('assigned_to_team');
    cur_frm.refresh_field('assigned_to_individual');
    cur_frm.refresh_field('created_by');
    cur_frm.refresh_field('closed_by');
    cur_frm.refresh_field('started_on');
    cur_frm.refresh_field('scheduled_close');
    // cur_frm.refresh_field('attachement');
    cur_frm.refresh_field('timeline');
    cur_frm.refresh_field('priority');
    cur_frm.refresh_field('assign_date');
    cur_frm.refresh_field('is_notified');
}
$('.section-head.collapsible:contains("Connections")').hide();

    },
    new_ticket(frm){
        let di = new frappe.ui.Dialog({
            title: 'Enter Details',
            fields: [
                {
                    label: 'Assigned to Group',
                    fieldname:'assign_user_group',
                    fieldtype: 'Link',
                    options:"User Group",
                },
                {
                    label: 'Assigned to Individual',
                    fieldname:'assign_user_individual',
                    fieldtype: 'Link',
                    options:"User",
                },
                //  {
                //     label: 'Completion Date',
                //     fieldname:'com_date',
                //     fieldtype: 'Date',
                // },
                 {
                    label: '',
                    fieldname:'col',
                    fieldtype: 'Column Break',
                },
                {
                    label: 'Notes',
                    fieldname:'notes',
                    fieldtype: 'Small Text',
                },
                 
                {
                    label: 'Add Attachment',
                    fieldname:'attach',
                    fieldtype: 'Attach',
                },
            ],
            primary_action_label: 'Submit',
            primary_action(r) {
                console.log(r)
        	   
        	   frappe.call({
                    method: 'get_data_from_user_group',
                    args:{'assign_to_user_group':r.assign_user_group},
                    callback: function(r) {
                        cur_frm.clear_table("task_user");
                        for(var i=0;i<=r.message.length;i++){
                            var childTable = cur_frm.add_child("task_user");
                            childTable.user=r.message[i].user
                            cur_frm.refresh_fields("task_user");
                        }
                        
                    }
        	    })
                	   
        	   
                var childTable = cur_frm.add_child("task_details");
                childTable.assigned_to_team=r.assign_user_group
                childTable.assigned_to_individual=r.assign_user_individual
                // childTable.completion_date=r.com_date
                childTable.notes=r.notes
                childTable.attachement=r.attach
                cur_frm.save()
                cur_frm.refresh_fields("task_details");
            di.hide()
          
            
        }
            
        })
        di.show()
        
    },
    refresh(frm) {

        frm.add_custom_button(__("Go back to Opportunity"), function(){
            frappe.set_route('Form', 'Opportunity', frm.doc.opportunity)
        });	
	    
        $('.indicator-pill').hide()

        // Hide the collapsible section on refresh
      // Hide the element with the class "connections"
    $('.section-head.collapsible:contains("Connections")').hide();


        // Make the two fields in the child table read-only
        frm.fields_dict['task_details'].grid.get_field('status').read_only = true;

        // Hide various elements
        setTimeout(() => {
            $('.form-link-title').hide();
            $('.form-sidebar-stats').hide();
            $('.sidebar-image-wrapper').hide();
            $("[data-doctype='Quotation']").hide();
            $("[data-doctype='Site Visit']").hide();
            $("[data-doctype='Lead']").hide();
            $("[data-doctype='Customer']").hide();
            $("[data-doctype='Zoho Sign Contracts']").hide();
            $("[data-doctype='Prospect']").hide();
            $("[data-label='Create']").hide();
            $("[data-label='Action']").hide();
            $('.indicator-pill').hide();
            $('.row.form-dashboard-section.form-heatmap').hide();
            $("[data-doctype='Material Request']").hide();
            $("[data-doctype='Sales Order']").hide();
            $("[data-doctype='Task']").hide();
            $("[data-doctype='BOM']").hide();
            $("[data-doctype='Stock Entry']").hide();
            $("[data-doctype='Delivery Note']").hide();
            $("[data-doctype='Timesheet']").hide();
            $("[data-doctype='Issue']").hide();
            $("[data-doctype='Project Update']").hide();
            $("[data-doctype='Purchase Order']").hide();
            $("[data-doctype='Sales Invoice']").hide();
            $("[data-doctype='Purchase Receipt']").hide();
            $("[data-doctype='Purchase Invoice']").hide();
        }, 10);
    },
    linked_lead(frm)
    {
             frappe.call({
             method: "frappe.client.get",
             args: {
                 doctype: "Opportunity",
                 name: frm.doc.opportunity,
             },
             callback(r) {
                 if(r.message) {
                     var doc_task = r.message;
                     frappe.set_route("List", "Lead", { "name": doc_task.party_name });
                 }
             }
         });
    },
    linked_site_visit(frm)
    {
        frappe.call({
             method: "frappe.client.get",
             args: {
                 doctype: "Opportunity",
                 name: frm.doc.opportunity,
             },
             callback(r) {
                 if(r.message) {
                     var doc_task = r.message;
                     frappe.set_route("List", "Site Visit", { "opportunity": doc_task.name});
                 }
             }
         });
    },
    linked_customer(frm)
    {
        frappe.call({
             method: "frappe.client.get",
             args: {
                 doctype: "Opportunity",
                 name: frm.doc.opportunity,
             },
             callback(r) {
                 if(r.message) {
                     var doc_task = r.message;
                     frappe.set_route("List", "Customer", { "opportunity_name": doc_task.name});
                 }
             }
         });
    },
    linked_zoho_sign_contract(frm)
    {
        frappe.call({
             method: "frappe.client.get",
             args: {
                 doctype: "Opportunity",
                 name: frm.doc.opportunity,
             },
             callback(r) {
                 if(r.message) {
                     var doc_task = r.message;
                     frappe.set_route("List", "Zoho Sign Contracts", { "opportunity": doc_task.name});
                 }
             }
         });
    },
	linked_tasks(frm) {
		    var project = frm.doc.name; 
            if (project) {
                frappe.set_route("List", "Task", { "project": project });
            } else {
                frappe.msgprint(__("Please select a project before opening linked tasks."));
            }
	},
	new_task(frm){
	         var project = frm.doc.name; 

            if (project) {
                var new_task = frappe.model.get_new_doc('Task');
                new_task.project = project;

                frappe.set_route('Form', 'Task', new_task.name);
            } else {
                frappe.msgprint(__("Please select a project before creating a new task."));
            }
	},
    before_save(frm) {
        cur_frm.clear_table('notify_users')
        frappe.call({
            method: 'get_data_from_user_group',
            args:{'assign_to_user_group':frm.doc.assign_to_user_group},
            callback: function(r) {
                cur_frm.clear_table("users");
                cur_frm.clear_table("notify_users");
                for(var i=0;i<=r.message.length;i++){
                    var childTable = cur_frm.add_child("users");
                    childTable.user=r.message[i].user
                    childTable.welcome_email_sent=1
                    
                    cur_frm.refresh_fields("users");
                }
                
            }
	   })

		var start_date = frm.doc.expected_start_date;

        if (start_date) {
           
            var end_date = frappe.datetime.add_months(start_date, 2);
            
            frm.set_value('expected_end_date', end_date);
        }
	}
});

frappe.ui.form.on('Task Detail', {
	task_status(frm, cdt,cdn) {
	    let row = frappe.get_doc(cdt, cdn);
// 		console.log("validation of task details...", row.task_status, cdn);
		if (row.task_status == "Completed"){
		  //  console.log("Current user", frappe.session.user);
		    row.closed_by = frappe.session.user;
		    
		  //  console.log("Current date", frappe.datetime.nowdate());
		  //  console.log("close date", row.scheduled_close);
		    row.completion_date = frappe.datetime.nowdate();
		    
		    var date1 = new Date(frappe.datetime.nowdate());
            var date2 = new Date(row.scheduled_close);
            
            if (date1 < date2) {
                // console.log("completed before"); // dateString1 is earlier than dateString2
                row.timeline = "Before Time";
            } else if (date1 > date2) {
                // console.log("completed after, late");; // dateString1 is later than dateString2
                row.timeline = "Delayed";
            } else {
                // console.log("completed on time"); // dateString1 and dateString2 are equal
                row.timeline = "On-Time";
            }
            
            frm.refresh_fields("task_details");
            let escapeEvent = new KeyboardEvent('keydown', {
                keyCode: 27,  // Key code for the escape key
                key: 'Escape' // Key name for the escape key
            });
            
            // Dispatch the event on the document
            console.log("escape");
            document.dispatchEvent(escapeEvent);
            console.log("escape after");
		}
	},
    assign_to_user_group(frm) {
        frappe.call({
             method: 'get_data_from_user_group',
             args:{'assign_to_user_group':frm.doc.assign_to_user_group},
             callback: function(r) {
                 cur_frm.clear_table("users");
                 for(var i=0;i<=r.message.length;i++){
                     var childTable = cur_frm.add_child("users");
                     childTable.user=r.message[i].user
                     childTable.welcome_email_sent=1
                     
                     cur_frm.refresh_fields("users");
                 }
                 
             }
        })                   
     }
});