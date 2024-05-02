frappe.ui.form.on('Opportunity', {
    before_save(frm) {
        frm.doc.created_by = frm.doc.owner
        // cur_frm.clear_table("users");
        // cur_frm.clear_table("notify_users");
    },
    //     if(frm.doc.assign_user_group){
    //     frappe.call({
    //         method: 'get_data_from_user_group',
    //         args:{'assign_to_user_group':frm.doc.assign_user_group},
    //         callback: function(r) {
    //             cur_frm.clear_table("users");
    //             for(var i=0;i<=r.message.length;i++){
    //                 var childTable = cur_frm.add_child("users");
    //                 childTable.user=r.message[i].user
    //                 cur_frm.refresh_fields("users");
    //             }

    //         }
    // })
    //     }
    // },
    date_and_time_of_appointment:function(frm) {
        frm.set_value('custom_is_proposed',0)
    },
    date_and_time:function(frm) {
        frm.set_value('custom_is_later',0)
    },
    proposal_sub_status(frm) {
        if (frm.doc.proposal_sub_status == "Client not interested") {
            frm.set_value("opportunity_status", "Client Lost")
        }
    },
    // change maxfit status on lead
    opportunity_status: (frm) => {
        if (frm.doc.opportunity_status === 'Maxfit Completed'){
            frm.set_value('custom_assign_user_group','Sales closure')
        }
        if (frm.doc.opportunity_status === 'Client Won'){
            frm.set_value('custom_assign_user_group','Customer Success')
            frm.save()
            frappe.db.insert({
                "doctype": "Customer",
                "lead_name": frm.doc.party_name,
                "opportunity_name": frm.doc.name,
                "customer_name": frm.doc.title,
                "customer_group":"All Customer Groups",
            }).then(function(r) {
                console.log(r.name,"check");
                frappe.msgprint("Customer created successfully")
                // create project automatically
                console.log("jjjjjj")
                           
                frappe.db.get_list("Project Template", {
                    fields: ['*']
                }).then(pro_temp => {
                    console.log(pro_temp)
                    let end_date = new Date(frappe.datetime.nowdate());
                    
                    end_date.setDate(end_date.getDate()+60);
                    let year = end_date.getFullYear();
                    let month = (end_date.getMonth() + 1).toString().padStart(2, '0');
                    let day = end_date.getDate().toString().padStart(2, '0');
                    
                    let expected_end_date = year + "-" + month + "-" + day;
                    console.log("vvvvvvvvvv")
                    // let expected_end_date = ""
                    frappe.dom.freeze();
                    frappe.db.insert({
                        "doctype": "Project",
                        "project_name": r.name,
                        "project_template": pro_temp[0]['name'],
                        "expected_start_date":frappe.datetime.nowdate(),
                        "expected_end_date": expected_end_date,
                        "customer": r.name,
                        'opportunity':frm.doc.name,
                        "custom_stage":"Welcome Call",
                        "project_status":"In Progress",
                        "custom_property_survey":frm.doc.custom_property_survey,
                        "custom_fz_survey":frm.doc.custom_fz_survey,
                        "custom_lift_required":frm.doc.custom_lift_required,
                        "custom_historical_building":frm.doc.custom_historical_building,
                        "custom_stop_work_order":frm.doc.custom_stop_work_order,
                        "custom_utility_bills":frm.doc.custom_utility_bills,
                        "custom_property_tax":frm.doc.custom_property_tax,
                        "custom_property_deed":frm.doc.custom_property_deed,
                        "custom_electrical_works":frm.doc.custom_electrical_works,
                        "custom_electrical_works_description":frm.doc.custom_electrical_works_description,
                        "custom_service_upgrade":frm.doc.custom_service_upgrade,
                        "custom_service_upgrade_description":frm.doc.custom_service_upgrade_description,
                        "custom_reroof":frm.doc.custom_reroof,
                        "custom_reroof_description":frm.doc.custom_reroof_description,
                        "custom_trenching":frm.doc.custom_trenching,
                        "custom_trenching_description":frm.doc.custom_trenching_description,
                        "custom_tree_cut":frm.doc.custom_tree_cut,
                        "custom_tree_cut_description":frm.doc.custom_tree_cut_description,
                        "custom_structural_upgrade":frm.doc.custom_structural_upgrade,
                        "custom_structural_upgrade_description":frm.doc.custom_structural_upgrade_description,
                        "custom_first_name":frm.doc.custom_first_name,
                        "custom_last_name":frm.doc.custom_last_name,
                        "custom_phone_number":frm.doc.custom_phone_number,
                        "custom_email":frm.doc.custom_email,
                        "custom_street":frm.doc.custom_street,
                        "custom_city":frm.doc.custom_city,
                        "custom_state":frm.doc.custom_state,
                        "country":frm.doc.custom_country,
                        "custom_postal_code":frm.doc.custom_postal_code,
                        "custom_electrical_consumption":frm.doc.custom_electrical_consumption,
                        'custom_install_pictures':frm.doc.custom_install_pictures,
                        'custom_site_visit_pictures':frm.doc.custom_site_visit_pictures,
                        "assign_to_user_group":frm.doc.custom_assign_user_group
                    }).then(function(r) {
                        frappe.dom.unfreeze();
                        console.log(r,"ooooooooooooooooooooooooooooooo");
                        frm.save()
                        // frappe.db.set_value('Project',r.name, 'assign_to_user_group', 'Customer Success')
                        cur_frm.refresh()
                        frappe.msgprint("Project created successfully")
                        frappe.set_route('Form', 'Project', r.name)
                    });
                })
            });
            cur_frm.refresh()
        }
        
	},

    refresh(frm){
        setTimeout(() => {
        // $('.text-muted').hide()
            $('.icon-btn').show()
            $('.document-link-badge').show()
            $('.document-link').show()
            $('.indicator-pill').hide()
            $('.form-sidebar-stats').hide()
            $('.ql-toolbar').hide()
            $("[data-label='Create']").hide();
            $("[data-doctype='Request for Quotation']").hide();
            $("[data-doctype='Supplier Quotation']").hide();
            $("[data-doctype='Quotation']").hide();
	    },10)
        
        
        
        if(frm.doc.opportunity_status=="Client Lost"){
            frm.set_df_property('client_lost_reason','read_only',0)
        }
        frm.get_field('task_details').grid.cannot_add_rows = true;
        
       
    },

    assign_user_group(frm) {
	    frappe.call({
            method: 'get_data_from_user_group',
            args:{'assign_to_user_group':frm.doc.assign_user_group},
            callback: function(r) {
                cur_frm.clear_table("users");
                for(var i=0;i<=r.message.length;i++){
                    var childTable = cur_frm.add_child("users");
                    childTable.user=r.message[i].user
                    cur_frm.refresh_fields("users");
                }
            }
	    })
	     frappe.call({
                method: 'assign_and_share_from_opportunity',
                args:
                {
                    'assign_to_user_group':frm.doc.assign_user_group,
                    'name':frm.doc.name
                    
                },
                callback: function(r) {
                    console.log(r,"jjjjjjjjjjjjjjjj")
            }
            })
            frm.save()
	    
    },

    // onload(frm){
    //     frm.get_field('task_details').grid.cannot_add_rows = true;
    //     setTimeout(() => {
    //         $("[data-doctype='Request for Quotation']").hide();
    //         $("[data-doctype='Supplier Quotation']").hide();
    //         $("[data-doctype='Quotation']").hide();
    //     }, 10);
    // },
    onload(frm) {
        if (!frappe.user.has_role("System Manager")) {
            // frm.get_field('task_details').grid.cannot_add_rows = true;
            // 	let status = frappe.meta.get_docfield("Task Detail","task_status", cur_frm.doc.name);
            // 	let notes = frappe.meta.get_docfield("Task Detail","notes", cur_frm.doc.name);
            // 	let actual_dates = frappe.meta.get_docfield("Task Detail","completion_date", cur_frm.doc.name);

            let assigned_to_team = frappe.meta.get_docfield("Task Detail", "assigned_to_team", cur_frm.doc.name);
            let assigned_to_individual = frappe.meta.get_docfield("Task Detail", "assigned_to_individual", cur_frm.doc.name);
            let created_by = frappe.meta.get_docfield("Task Detail", "created_by", cur_frm.doc.name);
            let closed_by = frappe.meta.get_docfield("Task Detail", "closed_by", cur_frm.doc.name);
            let started_on = frappe.meta.get_docfield("Task Detail", "started_on", cur_frm.doc.name);
            let scheduled_close = frappe.meta.get_docfield("Task Detail", "scheduled_close", cur_frm.doc.name);
            // 	let attachement = frappe.meta.get_docfield("Task Detail","attachement", cur_frm.doc.name);
            let timeline = frappe.meta.get_docfield("Task Detail", "timeline", cur_frm.doc.name);
            let priority = frappe.meta.get_docfield("Task Detail", "priority", cur_frm.doc.name);
            let assign_date = frappe.meta.get_docfield("Task Detail", "assign_date", cur_frm.doc.name);
            let is_notified = frappe.meta.get_docfield("Task Detail", "is_notified", cur_frm.doc.name);

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
    },
    new_task(frm){
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
                
                let close_date = new Date(frappe.datetime.nowdate());
                close_date.setDate(close_date.getDate()+3);
                let year = close_date.getFullYear();
                let month = (close_date.getMonth() + 1).toString().padStart(2, '0');
                let day = close_date.getDate().toString().padStart(2, '0');
                
                let scheduled_close_date = year + "-" + month + "-" + day;
                childTable.scheduled_close = scheduled_close_date;
                
                // cur_frm.save(ignore_permissions=true);
                cur_frm.refresh_fields("task_details");
            di.hide();
            
        }
            
        })
        di.show();
        // let di = new frappe.ui.Dialog({
        //     title: 'Enter Details',
        //     fields: [
        //         {
        //             label: 'Assigned to user group',
        //             fieldname:'assign_user_group',
        //             fieldtype: 'Link',
        //             options:"User Group",
        //             reqd:1
        //         },
                
               
        //         {
        //             label: 'Assign Date',
        //             fieldname:'ass_date',
        //             fieldtype: 'Date',
        //         },
        //          {
        //             label: 'Completion Date',
        //             fieldname:'com_date',
        //             fieldtype: 'Date',
        //         },
        //          {
        //             label: '',
        //             fieldname:'col',
        //             fieldtype: 'Column Break',
        //         },
        //         {
        //             label: 'Notes',
        //             fieldname:'notes',
        //             fieldtype: 'Small Text',
        //         },
                 
        //         {
        //             label: 'Add Attachment',
        //             fieldname:'attach',
        //             fieldtype: 'Attach',
        //         },
        //     ],
        //     primary_action_label: 'Submit',
        //     primary_action(r) {
        //         console.log(r)
        	   
        // 	   frappe.call({
        //             method: 'get_data_from_user_group',
        //             args:{'assign_to_user_group':r.assign_user_group},
        //             callback: function(r) {
        //                 cur_frm.clear_table("task_user");
        //                 for(var i=0;i<=r.message.length;i++){
        //                     var childTable = cur_frm.add_child("task_user");
        //                     childTable.user=r.message[i].user
        //                     cur_frm.refresh_fields("task_user");
        //                 }
                        
        //             }
        // 	    })
                	   
        	   
        //         var childTable = cur_frm.add_child("task_details");
        //         childTable.assigned_to_team=r.assign_user_group
        //         childTable.assign_date=r.ass_date
        //         childTable.completion_date=r.com_date
        //         childTable.notes=r.notes
        //         childTable.attachement=r.attach
        //         cur_frm.save()
        //         cur_frm.refresh_fields("task_details");
        //     di.hide()
            
        // }
            
        // })
        // di.show()
        
    },

})


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
	}
});