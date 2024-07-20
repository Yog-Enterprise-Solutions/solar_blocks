frappe.query_reports["Opportunity Tickets"] = {
	"filters": [
		{
			"fieldname": "task_status",
			"label": __("Status"),
			"fieldtype": "Select",
			"default":"Open",
			"options": [
				{ "value": "", "label": __("") },
				{ "value": "Open", "label": __("Open") },
				{ "value": "Pending", "label": __("Pending") },
				{ "value": "In Progress", "label": __("In Progress") },
				{ "value": "Cancelled", "label": __("Cancelled") },
				{ "value": "Completed", "label": __("Completed") }
			]
		},
		{
			"fieldname": "timeline",
			"label": __("Timeline"),
			"fieldtype": "Select",
			"options": [
				{ "value": "", "label": __("") },
				{ "value": "On-Time", "label": __("On-Time") },
				{ "value": "Before Time", "label": __("Before Time") },
				{ "value": "Delayed", "label": __("Delayed") }
			]
		}
	],

	"formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "timeline" && data) {
            if (data.timeline === 'Delayed') {
                value = "<span style='color:red'>" + value + "</span>";
            } else if (data.timeline === 'On-Time') {
                value = "<span style='color:green'>" + value + "</span>";
            } else if (data.timeline === 'Before Time') {
                value = "<span style='color:yellow'>" + value + "</span>";
            }
        }

        return value;
    }
};
