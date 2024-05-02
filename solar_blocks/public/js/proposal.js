frappe.ui.form.on('Proposal', {
    before_save(frm) {
         frappe.call({
            method: 'zohosign.api.generateAPIToken',
            args: {
                "client_id":"1000.KEBX6XAN6ZLHX734ALY4NQ8378X9AO",
                "refresh_token":"1000.fd5ff1cf53c84f20e6ba9e0b4306d522.00994a550c4450e80e596e2671981ef5",
                "client_secret":"33451dcffc5dbb2e02787789928069dda01b284b5d"
             }, 
            callback: function (r) {
               var responseArray = JSON.parse(r._server_messages);
               const messageObject = JSON.parse(responseArray[0]);
               const at= JSON.parse(messageObject.message);
               console.log(at.access_token)
        


                  
                
            },
        });
        
        // frappe.call({
        //     method: 'zohosign.api.docsign',
        //      args: { 
        //      'file_url': frm.doc.attach, 
        //      'request_name': "Contracts", 
        //      'recipient_name': frm.doc.name, 
        //      'recipient_email': frm.doc.email, 
        //      }, 
        //     callback: function (r) {
        //         frappe.msgprint(r);
        //         console.log(r.message)
        //         // action_id
        //     },
        // });
       
    }


    // refresh(frm){
    //     // create quotation button and redirect to quotation
    //     if(frm.doc.workflow_state=="Proposal Approved"){
    //         frm.add_custom_button(__('Create Quotation'), function(){
    //             frappe.route_options = {
    //                 'quotation_to': "Lead",
    //                 'party_name':frm.doc.lead_id,
    //             };
    //             frappe.new_doc("Quotation");
    
    //         }).addClass("btn-primary");
    //     }
        
    //     if(frm.doc.workflow_state!="Proposal Created"){

    //         frm.set_df_property('schedule_appointment','read_only',1)
    //         frm.set_df_property('meeting_and_negotiations','read_only',1)
    //         frm.set_df_property('schedule_at_later_day','read_only',1)
    //         frm.set_df_property('basic_site_review','read_only',1)
    //         frm.set_df_property('date_and_time_of_appoinment','read_only',1)
    //         frm.set_df_property('meeting_done','read_only',1)
    //         frm.set_df_property('notes','read_only',1)
    //         frm.set_df_property('date_and_time','read_only',1)
    //         frm.set_df_property('note_2','read_only',1)
    //     }
    //     if(frm.doc.workflow_state=="Proposal Created"){
    //         if(frm.doc.schedule_appointment==1){
    //             frm.set_df_property('meeting_and_negotiations','read_only',0)
    //         }else{
    //             frm.set_df_property('meeting_and_negotiations','read_only',1)
    //         }
    //         if(frm.doc.meeting_and_negotiations==1){
    //             frm.set_df_property('schedule_appointment','read_only',1)
    //             // cur_frm.set_df_property('date_and_time_of_appoinment','read_only',1)
    //             // frm.set_df_property('date_and_time_of_appoinment','hidden',0)
    //             frm.set_df_property('schedule_at_later_day','read_only',0)
    //         }else{
    //             frm.set_df_property('schedule_at_later_day','read_only',1)
    //         }
    //         if(frm.doc.schedule_at_later_day==1){
    //             frm.set_df_property('meeting_and_negotiations','read_only',1)
    //             frm.set_df_property('notes','read_only',1)
    //             frm.set_df_property('meeting_done','read_only',1)
    //             frm.set_df_property('basic_site_review','read_only',0)
    //         }else{
    //             frm.set_df_property('basic_site_review','read_only',1)
    //         }
    //         if(frm.doc.basic_site_review==1){
    //             frm.set_df_property('schedule_at_later_day','read_only',1)
    //             // frm.set_df_property('date_and_time','read_only',1)
    //             // frm.set_df_property('note_2','read_only',1)
    //         }
    //     }
    // },
    // meeting_and_negotiations(frm){
	//     var today = frappe.datetime.get_today();
    //     if(frm.doc.meeting_and_negotiations==1){
    //         frm.set_value('meeting_date',today)
    //     }
    // },
    // after_workflow_action: (frm) => {
    //     // update status on lead and opportunity
    //     frappe.call({
    //         method: 'update_remaining_status_from_proposal',
    //         args:{
    //             lead_id:frm.doc.lead_id,
    //             opportunity_id:frm.doc.opportunity_id,
    //             workflow_state:frm.doc.workflow_state,
    //             full_name:frm.doc.full_name
    //         },
    //         callback: function(d) {
    //             console.log(d,"lead")
    //         }
    //     })
	
    // },
    // before_workflow_action: async (frm) => {
    //     if ((cur_frm.selected_workflow_action === 'Finance Approve')){
    //         frappe.db.set_value('Proposal',  cur_frm.doc.name, {
    //             finance_approved:  "Yes",
    //         })
    //         cur_frm.refresh()
    //     }
    //     if ((cur_frm.selected_workflow_action === 'Client Approve')){
    //         frappe.db.set_value('Proposal',  cur_frm.doc.name, {
    //             client_approved:  "Yes",
    //         })
    //         cur_frm.refresh()
    //     }
        

    //     // create customer automatically
    //     if (cur_frm.selected_workflow_action === 'Client Won'){
    //         frappe.db.insert({
    //             "doctype": "Customer",
    //             "lead_name": frm.doc.lead_id,
    //             "opportunity_name": frm.doc.opportunity_id,
    //             "customer_name": frm.doc.full_name,
    //             "customer_group":"All Customer Groups",
    //         }).then(function(r) {
    //             console.log(r.name,"check");
    //             frappe.msgprint("Customer created successfully")
    //             // create project automatically
                           
    //             frappe.db.get_list("Project Template", {
    //                 fields: ['*']
    //             }).then(pro_temp => {
    //                 console.log(pro_temp)
                
    //                 frappe.db.insert({
    //                     "doctype": "Project",
    //                     "project_name": r.name,
    //                     "project_template": pro_temp[0]['name'],
    //                     "customer": r.name,
    //                     'opportunity':frm.doc.opportunity_id
    //                 }).then(function(r) {
    //                     console.log(r);
    //                     frappe.msgprint("Project created successfully")
    //                     frappe.set_route('Form', 'Project', r.name)
    //                 });
    //             })
    //         });
    //         cur_frm.refresh()
    //     }

    //     let promise = new Promise((resolve, reject) => {

    //         if ((cur_frm.selected_workflow_action === 'Contract Sign')){
    //             frappe.dom.unfreeze()

    //             let di = new frappe.ui.Dialog({
    //                 title: 'Enter Details',
    //                 fields: [
    //                     {
    //                         label: 'Attach Contract',
    //                         fieldname:'con',
    //                         fieldtype: 'Attach',
    //                         reqd:1
    //                     },
    //                     {
    //                     label: 'Any Addtional Notes',
    //                     fieldname:'notes',
    //                     fieldtype: 'Small Text',
    //                     },
    //                 ],
    //                 primary_action_label: 'Submit',
    //                 primary_action(r) {
    //                     if(r.con){
    //                         var status="Yes"
    //                     }else{
    //                         var status="No"
    //                     }
    //                 frappe.db.set_value('Proposal',  cur_frm.doc.name, {
    //                     contract_attach:  r.con,
    //                     contract_notes: r.notes,
    //                     contract_signed:status
    //                 })
                    
    //                 .then(r => {
    //                     resolve()
    //                     di.hide();
    //                 })
    //             }
    //             })
    //             di.show()
    //         }
    //         else{
    //             resolve()
    //         }

    //         });
    //         await promise.catch(() => frappe.throw());
    //         // console.log(promise,"rrrrrrrrrrrrrr")
              
              
              
    //     let promise2 = new Promise((resolve, reject) => {
    //         if ((cur_frm.selected_workflow_action === 'Client Lost')){
    //             frappe.dom.unfreeze()

    //             let di = new frappe.ui.Dialog({
    //                 title: 'Enter Reason',
    //                 fields: [
    //                     {
    //                         label: 'Select Reason',
    //                         fieldname:'res',
    //                         fieldtype: 'Select',
    //                         options:['Client Cancel the contract',"Finance not approved"]
    //                     },
    //                 ],
    //             primary_action_label: 'Submit',
    //             primary_action(r) {
    //             frappe.db.set_value('Proposal',  cur_frm.doc.name, {
    //                 reason_for_client_lost:  r.res,
    //             })
    //             .then(r => {
    //                 resolve()
    //                 di.hide();
    //             })
    //         }
    //         })
    //         di.show()
    //     }
    //      else{
    //         resolve()
    //                   }
    //             });
    //           await promise2.catch(() => frappe.throw());
              
        
    //     let promise3 = new Promise((resolve, reject) => {
    //     if ((cur_frm.selected_workflow_action === 'Proposal Approve')){
    //         frappe.dom.unfreeze()
    //         console.log(frm.doc.schedule_appointment)
    //         if(frm.doc.schedule_appointment!="1" || frm.doc.meeting_and_negotiations!="1" || frm.doc.schedule_at_later_day!="1" || frm.doc.basic_site_review!="1"){
    //             console.log("kkkk")
    //             frappe.throw("Pending basic site review")
    //         }
    //         else{
                
    //             resolve()
    //         }
            
    //     }
    //     else{
    //             resolve()
    //         }

    //         });
    //         await promise3.catch(() => frappe.throw());
              
              
              
    
    // }
});
