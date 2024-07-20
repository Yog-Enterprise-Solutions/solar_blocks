frappe.query_reports["Completed Tickets"] = {
    columns: [
        {
            'fieldname': 'task_status',
            'label': _('Status'),
            'fieldtype': 'Select',
            'options': ['', 'Open', 'Pending', 'In Progress', 'Cancelled', 'Completed']
        },
        {
            'fieldname': 'timeline',
            'label': _('Timeline'),
            'fieldtype': 'Select',
            'options': ['', 'On-Time', 'Before-Time', 'Delayed']
        }
    ],

    "formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "timeline" && data) {
            if (data.timeline === 'Delayed') {
                value = "<span style='color:red'>" + value + "</span>";
            } else if (data.timeline === 'On-Time') {
                value = "<span style='color:green'>" + value + "</span>";
            } else if (data.timeline === 'Before-Time') {
                value = "<span style='color:yellow'>" + value + "</span>";
            }
        }

        return value;
    }
};
