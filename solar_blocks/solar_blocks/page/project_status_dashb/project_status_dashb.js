frappe.pages['project-status-dashb'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Project Status Dashboard',
		single_column: true
	});

	getData(page)
	
}


function getData(page){frappe.call({
    method: 'solar_blocks.solar_blocks.page.project_status_dashb.project_status_dashb.get_project',
    args: {
    },
    // disable the button until the request is completed
    btn: $('.primary-action'),
    // freeze the screen until the request is completed
    freeze: true,
    callback: (r) => {
        // on success
		var records=r.message
		console.log("rr",records)
		// render template
	$(frappe.render_template('project_status_dashb', { data:records })).appendTo(page.body);
    },
    error: (r) => {
        // on error
    }
})}