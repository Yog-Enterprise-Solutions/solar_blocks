frappe.ui.form.on('Lead', {
    refresh(frm) {
        setTimeout(() => {
            $('.form-sidebar-stats').hide()
            $('.sidebar-image-wrapper').hide()
            $("[data-doctype='Quotation']").hide();
            $("[data-doctype='Prospect']").hide();
            $("[data-label='Create']").hide();
            $("[data-label='Action']").hide();
            $('.indicator-pill').hide()
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
        frm.set_value('reminder_date', null);
        frm.refresh_field('reminder_date');
        if (frm.doc.lead_sub_status === 'Appointment Setup' || frm.doc.lead_sub_status === 'Call at later Date') {

            frm.set_value('assign_user_groups', 'Sales closure')
        }
        if (frm.doc.lead_sub_status === 'Convert to Opportunity') {
            frm.set_value('assign_user_groups', 'Design Team')
        }
        if (frm.doc.status == "Lead" || frm.doc.lead_status == "Lead") {
            var today = frappe.datetime.get_today();
            if (frm.doc.lead_sub_status == "Pending additional information") {
                frm.set_value('pending_info_date', today)
            }
            if (frm.doc.lead_sub_status == "Tried to Call & no response") {
                frm.set_value('tried_to_call', today)
            }
            if (frm.doc.lead_sub_status == "Not Interested") {
                frm.set_value("lead_sub_status", "Lead Disqualified")
            }
        }

        let promise = new Promise(async (resolve, reject) => {

            if (frm.doc.lead_sub_status == "Convert to Opportunity") {
                await frm.save()
                cur_frm.refresh()
                frappe.dom.freeze();
                if (!cur_frm.doc.__islocal) {
                    frappe.db.insert({
                        "doctype": "Opportunity",
                        'party_name': frm.doc.name,
                        'source': frm.doc.source,
                        'city': frm.doc.city,
                        'state': frm.doc.state,
                        // 'contact_person': frm.doc.first_name,
                        // 'contact_email': frm.doc.email_id,
                        'contact_email': frm.doc.email,
                        'contact_mobile': frm.doc.mobile_no,
                        'phone_ext': frm.doc.phone_ext,
                        'phone': frm.doc.phone,
                        'custom_first_name': frm.doc.first_name,
                        'custom_last_name': frm.doc.last_name,
                        'custom_phone_number': frm.doc.phone_number,
                        'custom_email': frm.doc.email,
                        'custom_street': frm.doc.street,
                        'custom_city': frm.doc.city1,
                        'custom_state': frm.doc.state1,
                        'custom_country': frm.doc.country1,
                        'custom_postal_code': frm.doc.postal_code,
                        'custom_electrical_consumption': frm.doc.electrical_consumptions1,
                        'custom_assign_user_group': frm.doc.assign_user_groups,
                        'custom_lead_source': frm.doc.source,
                        'custom_install_pictures': frm.doc.custom_install_pictures,
                        'custom_site_visit_pictures': frm.doc.custom_site_visit_pictures

                    }).then(function (r) {
                        frappe.dom.unfreeze();
                        frm.save()
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
    custom_appointment_status: function (frm) {
        frm.set_value('custom_call_date_and_time', null);
        frm.refresh_field('custom_call_date_and_time');
    }
})
