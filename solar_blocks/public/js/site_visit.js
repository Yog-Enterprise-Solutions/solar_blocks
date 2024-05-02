frappe.ui.form.on('Site Visit', {
	refresh(frm) {
        frm.add_custom_button(__("Go back to Opportunity"), function(){
            frappe.set_route('Form', 'Opportunity', frm.doc.opportunity)
        });	
	 },
	 completion_status(frm){
	     if(frm.doc.completion_status=="Fully Completed"){
	        frappe.call({
            method: 'update_site_visit_status_on_opportunity',
                args:
                {
                    'opportunity':frm.doc.opportunity,
                    'visit_time':frm.doc.visit_time,
                    'visit_date':frm.doc.visit_date
                },
                callback: function(r) {
                }
            })
	         
	     }
	 }
})
