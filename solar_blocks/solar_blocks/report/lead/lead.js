frappe.query_reports["Lead"] = {
	"filters": [
		{
			"fieldname": "lead_sub_status",
			"label": __("Status"),
			"fieldtype": "Select",
			"default":"Lead",
			"options": [
				{ "value": "", "label": __("") },
				{ "value": "Lead", "label": __("Lead") },
				{ "value": "Pending additional information", "label": __("Pending additional information") },
				{ "value": "Tried to Call & no response", "label": __("Tried to Call & no response") },
				{ "value": "Call at later Date", "label": __("Call at later Date") },
				{ "value": "Not Interested", "label": __("Not Interested") },
				{ "value": "Convert to Opportunity", "label": __("Convert to Opportunity") },
				{ "value": "Lead Disqualified", "label": __("Lead Disqualified") }
			]
		}
	]
};
