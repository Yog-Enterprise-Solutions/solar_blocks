// Copyright (c) 2024, yes@tranqwality.com and contributors
// For license information, please see license.txt

frappe.query_reports["Opportunity"] = {
	"filters":  [
		{
			"fieldname": "opportunity_status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": [
				{ "value": "", "label": __("") },
				{ "value": "Opportunity", "label": __("Opportunity") },
				{ "value": "Maxfit Completed", "label": __("Maxfit Completed") },
				{ "value": "Proposal", "label": __("Proposal") },
				{ "value": "Contract Signed", "label": __("Contract Signed") },
				{ "value": "Finance Approved", "label": __("Finance Approved") },
				{ "value": "Client Won", "label": __("Client Won") },
				{ "value": "Client Lost", "label": __("Client Lost") },
				{ "value": "Client Disqualified", "label": __("Client Disqualified") }
			]
		}
	]
};
