frappe.query_reports["Cancelled Tickets Project"] = {
	
    "formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "aging_timeline" && data && data.aging_timeline == 'Late') {
			value = "<span style='color:red'>" + value + "</span>";
		}
		else if (column.fieldname == "aging_timeline" && data && data.aging_timeline == 'On time') {
			value = "<span style='color:green'>" + value + "</span>";
		}
		else if (column.fieldname == "aging_timeline" && data && data.aging_timeline == 'Before time') {
			value = "<span style='color:yellow'>" + value + "</span>";
		}


		return value;
	},

};
