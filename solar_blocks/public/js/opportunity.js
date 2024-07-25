frappe.ui.form.on('Opportunity', {
    before_save(frm){
        frm.doc.created_by=frm.doc.owner
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
   
	proposal_sub_status(frm){
	    if(frm.doc.proposal_sub_status=="Client not interested"){
	        frm.set_value("opportunity_status","Client Lost")
	        
	    }
	},
    // change maxfit status on lead
    opportunity_status: (frm) => {
        if (frm.doc.opportunity_status === 'Maxfit Completed'){
            frm.set_value('custom_assign_user_group','Sales closure')
             var user=frappe.session.user
	       frappe.db.get_value('User',user,'full_name')
    .then(r => {
        // console.log("kkk",r.message.full_name)
       frm.set_value("custom_maxfit_completed_by",r.message.full_name)
    })
        }
        if (frm.doc.opportunity_status === 'Appointment Scheduled'){
            frm.set_value('custom_assign_user_group','Design Team')
        }
        if (frm.doc.opportunity_status === 'Contract Sent'){
            var user=frappe.session.user
	       frappe.db.get_value('User',user,'full_name')
        .then(r => {
            // console.log("kkk",r.message.full_name)
           frm.set_value("custom_contract_sent_by",r.message.full_name)
        })
            
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
                        "custom_project_stage":"Welcome Call",
                        "project_status":"In Progress",
                        // "custom_acp5_report":frm.doc.custom_acp5_report,
                        // "custom_property_survey":frm.doc.custom_property_survey,
                        // "custom_fz_survey":frm.doc.custom_fz_survey,
                        // "custom_lift_required":frm.doc.custom_lift_required,
                        // "custom_historical_building":frm.doc.custom_historical_building,
                        // "custom_stop_work_order":frm.doc.custom_stop_work_order,
                        // "custom_utility_bills":frm.doc.custom_utility_bills,
                        // "custom_property_tax":frm.doc.custom_property_tax,
                        // "custom_property_deed":frm.doc.custom_property_deed,
                        //  "custom_acp5_report1":frm.doc.custom_acp5_report1,
                        // "custom_property_survey1":frm.doc.custom_property_survey1,
                        // "custom_fz_survey1":frm.doc.custom_fz_survey1,
                        // "custom_lift_required1":frm.doc.custom_lift_required1,
                        // "custom_historical_building1":frm.doc.custom_historical_building1,
                        // "custom_stop_work_order1":frm.doc.custom_stop_work_order1,
                        // "custom_utility_bills1":frm.doc.custom_utility_bills1,
                        // "custom_property_tax1":frm.doc.custom_property_tax1,
                        // "custom_property_deed1":frm.doc.custom_property_deed1,
                        "custom_document_status":frm.doc.custom_document_status,
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
                        "custom_dob_username":frm.doc.custom_dob_username,
                        "custom_dob_password":frm.doc.custom_dob_password,
                        "assign_to_user_group":frm.doc.custom_assign_user_group,
                        'custom_document_attachments':frm.doc.custom_document_attachments,
                        'custom_pre_install_pictures':frm.doc.custom_pre_install_pictures,
                        'custom_post_install_pictures':frm.doc.custom_post_install_pictures,
                        'custom_roof_area':frm.doc.custom_roof_area,
                        'custom_proposals':frm.doc.custom_proposals,
                        'custom_lead':frm.doc.party_name
                        // 'custom_dob_link':frm.doc.custom_dob_link
                    }).then(function(r) {
                        frappe.dom.unfreeze();
                        // console.log(r,"ooooooooooooooooooooooooooooooo");
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
        const required_roles = [
            'Solarblocks Sales Head',
            'Solarblocks Operations Head',
            'Solarblocks Management',
            'Administrator'
        ];
        // / Check if the user has any of the required roles
        const has_required_role = required_roles.some(role => frappe.user.has_role(role));

        // Hide the field if the user does not have any of the required roles
        if (!has_required_role) {
            frm.set_df_property('custom_assign_team', 'hidden', 1);
        }
                const roles = [
            'Sales Closure', 
            'Customer Success', 
            'Sales Head', 
            'Operations Head', 
            'Design Team'
        ];
        
        const hasRelevantRole = roles.some(role => frappe.user_roles.includes(role));
        const isNotAdmin = !frappe.user_roles.includes('Administrator');
        
        if (hasRelevantRole && isNotAdmin) {
            if (!frm.is_new()) {

               
                setTimeout(() => {
                    console.log("INNNN")
                    frm.set_df_property('custom_first_name', 'read_only', 1);
                    frm.set_df_property('custom_last_name', 'read_only', 1);
                    frm.set_df_property('custom_phone_number', 'read_only', 1);
                    frm.set_df_property('custom_email', 'read_only', 1);
                    frm.$wrapper.find('.delete-note-btn').hide();
                }, 100);
            }
        }

        setTimeout(() => {
        // $('.text-muted').hide()
            // Assuming frm.$wrapper is the context wrapper
            var wrapper = frm.$wrapper;
            
            // Show specific elements within the wrapper context
            wrapper.find('.icon-btn').show();
            wrapper.find('.document-link-badge').show();
            wrapper.find('.document-link').show();
            
            // Hide specific elements within the wrapper context
            wrapper.find('.indicator-pill').hide();
            wrapper.find('.form-sidebar-stats').hide();
            wrapper.find('.ql-toolbar').hide();
            wrapper.find("[data-label='Create']").hide();
            wrapper.find("[data-doctype='Request for Quotation']").hide();
            wrapper.find("[data-doctype='Supplier Quotation']").hide();
            wrapper.find("[data-doctype='Quotation']").hide();
            
            	    },10)
        
        
        
        if(frm.doc.opportunity_status=="Client Lost"){
            frm.set_df_property('client_lost_reason','read_only',0)
        }
        frm.get_field('task_details').grid.cannot_add_rows = true;
        
       
    },
    task_details_on_form_rendered: function(frm, grid_row, cdt, cdn) {
         const roles = [
            'Sales Closure', 
            'Customer Success', 
            'Sales Head', 
            'Operations Head', 
            'Solarblocks Sales Head', 
            'Solarblocks Management', 
            'Solarblocks Operations Head',
            'Design Team'
        ];
        
        const hasRelevantRole = roles.some(role => frappe.user_roles.includes(role));
        const isNotAdmin = !frappe.user_roles.includes('Administrator');
        
        if (hasRelevantRole && isNotAdmin) {
       frm.$wrapper.find(".grid-delete-row").hide();}
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
                
                cur_frm.save();
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



// -------------------------------------------change-------------------------------------
frappe.ui.form.on('Opportunity', {
    refresh: function(frm, cdt, cdn) {
        frm.$wrapper.find('.form-attachments').hide(); 
        
        
    //     $(document).ready(function(){
    //     $(".pill-label.ellipsis.explore-link").hide();
    // });
// $(document).ready(function(){
//         $(".form-sidebar-items").hide();
//     });
    
    
    
    
        // Check if the opportunity status is one of the specified values
        if (["Client Won", "Client Lost", "Client Disqualified"].includes(frm.doc.opportunity_status)) {
            // Check if the user is not a System Manager
            if (!frappe.user.has_role("System Manager")) {
                // Iterate over all fields
                frm.fields.forEach(function(field) {
                    // Exclude Opportunity Status field
                    if (field.df.fieldname !== 'opportunity_status') {
                        // Set the field to read-only
                        frm.set_df_property(field.df.fieldname, 'read_only', 1);
                    }
                });
                // Disable the Opportunity Status field
                frm.set_df_property('opportunity_status', 'disabled', 1);
            } else {
                // If the user is a System Manager, make all fields editable
                frm.set_df_property('opportunity_status', 'disabled', 0);
                frm.fields.forEach(function(field) {
                    if (field.df.fieldname !== 'opportunity_status') {
                        frm.set_df_property(field.df.fieldname, 'read_only', 0);
                    }
                });
            }
        } else {
            // If the opportunity status is not one of the specified values, make all fields editable
            frm.fields.forEach(function(field) {
                frm.set_df_property(field.df.fieldname, 'read_only', 0);
            });
            // Enable the Opportunity Status field
            frm.set_df_property('opportunity_status', 'disabled', 0);
        }
    }
});

// ---------------------------------------change---------------------------------------

function checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn) {
    frappe.call({
        method: 'get_role_for_delete_permission',
        callback: function(r) {
            let roles = r.message;
            if (Array.isArray(roles)) {
                console.log("Roles fetched:", roles);

                // Check if user has any of the roles
                let hasRole = roles.some(role => frappe.user.has_role(role));

                if (hasRole) {
                    // User has at least one of the allowed roles, show the delete button
                    console.log("User has at least one of the allowed roles.");
                   frm.$wrapper.find(".grid-delete-row").show();
                } else {
                    // User does not have any of the allowed roles, hide the delete button
                    console.log("User does not have any of the allowed roles.");
                     frm.$wrapper.find(".grid-delete-row").hide();
                }
            } else {
                console.error("Roles is not an array:", roles);
            }
        },
        error: function(r) {
            // Handle error
            console.error("Error fetching roles:", r);
        }
    });
}




frappe.ui.form.on('Opportunity', {
    custom_proposals_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Opportunity', {
    custom_document_attachments_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Opportunity', {
    custom_pre_install_pictures_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Opportunity', {
    custom_post_install_pictures_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});


// ---------------------------------change-------------------------------------------
frappe.ui.form.on('Opportunity', {
	date_and_time_of_appointment:function(frm) {
        console.log(";;;;;;")
	frm.set_value('custom_is_proposed',0)
	}
})

frappe.ui.form.on('Opportunity', {
	date_and_time:function(frm) {
        console.log("oooooo")
	frm.set_value('custom_is_later',0)
	}
})


frappe.ui.form.on('Task Detail', {
	save(frm,cdt,cdn) {
		frm.save()
	}
})



// --------------------------------change---------------------------
frappe.ui.form.on('Opportunity', {
	onload(frm) {
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
	}
})