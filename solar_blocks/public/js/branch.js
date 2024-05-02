frappe.ui.form.on('Branch', {
	after_save(frm) {
		console.log("hhehe")
		frappe.db.get_list('User Group Member', {
    fields: '*',
    filters:{'parent':'Sales closure'}
}).then(records => {
    console.log(records);
})

	}
})