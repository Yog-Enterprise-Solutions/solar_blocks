frappe.pages['photo-gallery'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Photo Gallery',
		single_column: true
	});
}