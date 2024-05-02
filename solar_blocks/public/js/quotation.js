frappe.ui.form.on('Quotation', {
	refresh(frm) {
        frm.add_custom_button(__("Go back to Opportunity"), function(){
            frappe.set_route('Form', 'Opportunity', frm.doc.opportunity)
        });	
	 }
})
