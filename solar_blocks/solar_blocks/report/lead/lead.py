# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import now_datetime, get_datetime


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	if not data:
		frappe.msgprint("No records found")
	return columns, data
	




def get_columns():
	columns = [
	
		{"fieldname": "first_name", "label": ("Job Name"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Created ON"), "fieldtype": "Data", "width": 200},
		{"fieldname": "lead_owner", "label": ("Created BY"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing of the Job"), "fieldtype": "Data", "width": 100},
		
	]
	return columns





def get_data(filters):
	conditions=get_conditions(filters)
	data=frappe.get_all(
		doctype="Lead",
		fields=["first_name","lead_owner","creation"],
		filters=conditions,

	)
	# frappe.throw(f"{filters}")

	for lead in data:
		creation_date = lead.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			lead['aging'] =days_aging
	# frappe.throw(f"{conditions}")
	return data


def get_conditions(filters):
	conditions={}
	for key,value in filters.items():
		if filters.get(key):
			conditions[key]=value
	# frappe.throw(f"{conditions}")
	
	return conditions


