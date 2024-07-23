frappe.ui.form.on('Lead', {
    
	refresh(frm) {
	    const relevantRoles = [
            'Sales Field Agent',
            'Sales Closure',
            'Tellecallers',
            'Sales Head',
            'Solarblocks Sales Head',
            'Solarblocks Management'
        ];
        const hasRelevantRole = relevantRoles.some(role => frappe.user_roles.includes(role));
        const isNotAdmin = !frappe.user_roles.includes('Administrator');
	      // Check if the current user has the role 'Sales Agent'
        if (hasRelevantRole && isNotAdmin) {
            // Check if the lead is saved
            if (!frm.is_new()) {
                // Make the email field read-only
                frm.set_df_property('first_name', 'read_only', 1);
                frm.set_df_property('last_name', 'read_only', 1);
                frm.set_df_property('phone_number', 'read_only', 1);
                frm.set_df_property('email', 'read_only', 1);
                 setTimeout(function() {
                    // $('.delete-note-btn').hide();
                    frm.$wrapper.find('.delete-note-btn').hide();
                }, 100);
            }
        }

frm.refresh_field('items');

	    frm.$wrapper.find('.form-attachments').hide(); 
	    setTimeout(() => {
	       // Assuming frm.$wrapper is the context wrapper
            var wrapper = frm.$wrapper;
            
            // Hide specific elements within the wrapper context
            wrapper.find('.form-sidebar-stats').hide();
            wrapper.find('.sidebar-image-wrapper').hide();
            wrapper.find("[data-doctype='Quotation']").hide();
            wrapper.find("[data-doctype='Prospect']").hide();
            wrapper.find("[data-label='Create']").hide();
            wrapper.find("[data-label='Action']").hide();
            wrapper.find('.indicator-pill').hide();

        }, 10);
	   // if(!frappe.user.has_role("System Manager")){
    // 	    if(frm.doc.lead_sub_status=="Client Disqualified" || frm.doc.lead_sub_status=="Convert to Opportunity"){
    //             frm.set_df_property('lead_sub_status','read_only',1)
    //         }
	   // }
       
	},
	lead_sub_status: async (frm) => {
	    frm.set_value('custom_call_date_and_time', null);
	    frm.refresh_field('custom_call_date_and_time');
	    frm.set_value('custom_appointment_status', null);
	    frm.refresh_field('custom_appointment_status');
	    frm.set_value('reminder_date1', null);
	    frm.refresh_field('reminder_date1');
	    if(frm.doc.lead_sub_status==='Appointment Setup' || frm.doc.lead_sub_status==='Call at later Date' ){
	       
	       frm.set_value('assign_user_groups','Sales closure')
	    }
	    if (frm.doc.lead_sub_status==='Convert to Opportunity'){
	        frm.set_value('assign_user_groups','Sales Closure')
	    }
	    if(frm.doc.status=="Lead" || frm.doc.lead_status=="Lead"){
    	    var today = frappe.datetime.get_today();
    	    if(frm.doc.lead_sub_status=="Pending additional information"){
    	        frm.set_value('pending_info_date',today)
    	    }
    	   	if(frm.doc.lead_sub_status=="Tried to Call & no response"){
    	        frm.set_value('tried_to_call',today)
    	   	}
    	   	if(frm.doc.lead_sub_status=="Not Interested"){
    	   	    frm.set_value("lead_sub_status","Lead Disqualified")
    	   	}
	    }
	    
	   let promise = new Promise(async(resolve, reject) => {
        
	   if (frm.doc.lead_sub_status == "Convert to Opportunity") {
	 
            await cur_frm.save()
            cur_frm.refresh()
            // frappe.dom.freeze();
            if (frm.doc.lead_sub_status === "Convert to Opportunity") {
    	       frappe.db.insert({
                    "doctype": "Opportunity",
                    'party_name':frm.doc.name,
                    'source': frm.doc.source,
                    'city':frm.doc.city,
                    'state': frm.doc.state,
                    // 'contact_person': frm.doc.first_name,
                    // 'contact_email': frm.doc.email_id,    //for test of conversion
                    'contact_email': frm.doc.email,
                    'contact_mobile': frm.doc.mobile_no,
                    'phone_ext': frm.doc.phone_ext,
                    'phone': frm.doc.phone,
                    'custom_first_name':frm.doc.first_name,
                    'custom_last_name':frm.doc.last_name,
                    'custom_phone_number':frm.doc.phone_number,
                    'custom_email':frm.doc.email,
                    'custom_street':frm.doc.street,
                    'custom_city':frm.doc.city1,
                    'custom_state':frm.doc.state1,
                    'custom_country':frm.doc.country1,
                    'custom_postal_code':frm.doc.postal_code,
                    'custom_electrical_consumption':frm.doc.electrical_consumptions1,
                    'custom_assign_user_group':frm.doc.assign_user_groups,
                    'custom_lead_source':frm.doc.source,
                    'custom_customer_availability':frm.doc.custom_customer_availability,
                    'custom_document_attachments':frm.doc.custom_document_attachments,
                    'custom_pre_install_pictures':frm.doc.custom_pre_install_pictures,
                    'custom_post_install_pictures':frm.doc.custom_post_install_pictures,
                    'custom_proposals':frm.doc.custom_proposals
                    }).then(function(r) {
                         frappe.dom.unfreeze();
                        // frm.save()
                        cur_frm.refresh()
                        resolve()
                        frappe.msgprint("Opportunity created successfully")
                        frappe.set_route('Form', 'Opportunity', r.name)
                        
                        });
                    }
    
                }

        });
        await promise.catch(() => frappe.throw());
	    
    },
})



// ------------------------------------------------------------------------change-------------------------


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




frappe.ui.form.on('Lead', {
    custom_proposals_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Lead', {
    custom_document_attachments_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Lead', {
    custom_pre_install_pictures_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});

frappe.ui.form.on('Lead', {
    custom_post_install_pictures_on_form_rendered: function(frm, grid_row, cdt, cdn) {
       checkUserRoleAndToggleDeleteButton(frm, grid_row, cdt, cdn)
    }
});


// ------------------------------------------------------------------------change-------------------------
frappe.ui.form.on('Lead', {
	custom_appointment_status :function(frm) {
		frm.set_value('custom_call_date_and_time', null);
	    frm.refresh_field('custom_call_date_and_time');
	}
})


// ------------------------------------------------------------------------change-------------------------
frappe.listview_settings['Lead'] = {
    hide_name_column: true,
}
