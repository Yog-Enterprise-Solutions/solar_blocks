frappe.pages['opportunity-dashboar'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Opportunity Dashboard',
		single_column: true
	});

	getData(page)
	
}


function getData(page){frappe.call({
    method: 'solar_blocks.solar_blocks.page.opportunity_dashboar.opportunity_dashboar.get_opportunity',
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
	$(frappe.render_template('opportunity_dashboar', { data:records })).appendTo(page.body);
    },
    error: (r) => {
        // on error
    }
})}