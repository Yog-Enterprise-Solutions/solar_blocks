frappe.query_reports["Procurement"] = {
	
    "formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "timeline" && data && data.timeline == 'Late') {
			value = "<span style='color:red'>" + value + "</span>";
		}
		else if (column.fieldname == "timeline" && data && data.timeline == 'On time') {
			value = "<span style='color:green'>" + value + "</span>";
		}
		else if (column.fieldname == "timeline" && data && data.timeline == 'Before time') {
			value = "<span style='color:yellow'>" + value + "</span>";
		}
		// Add hyperlink for first_name
        if (column.fieldname == "project_name"&& data.name) {
            const baseURL = window.location.origin + "/app/project/";
            const leadURL = baseURL + data.name;
            value = `<a href="${leadURL}" target="_blank">${value}</a>`;
        }


		return value;
	},

};
