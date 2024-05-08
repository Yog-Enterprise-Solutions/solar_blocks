# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import now_datetime, get_datetime


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	frappe.throw(f"{data}")
	if not data:
		frappe.msgprint("No records found")
	return columns, data
	




def get_columns():
	columns = [
	
		{"fieldname": "first_name", "label": ("Name of job"), "fieldtype": "Data", "width": 200},
		{"fieldname": "source", "label": ("Source"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Date Created"), "fieldtype": "Data", "width": 200},
		{"fieldname": "lead_owner", "label": ("Created By"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing"), "fieldtype": "Data", "width": 100},
		{"fieldname": "custom_customer_availability", "label": ("Additional Notes"), "fieldtype": "Data", "width": 100}
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 100}
		
	]
	return columns





def get_data(filters):
	data=frappe.get_all(
		doctype="Lead",
		fields=["first_name","lead_owner","creation","source","custom_customer_availability","lead_sub_status"])
	

	for lead in data:
		creation_date = lead.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			lead['aging'] =days_aging
			after_three_day = frappe.utils.add_to_date(frappe.utils.getdate(creation_date), days=3)
			# if lead.get('lead_sub_status')=='Lead':
			# 	if frappe.utils.getdate()>after_three_day:
			# 		lead['timeline']=Late
			# elif lead.get('lead_sub_status')!='Lead':
			# 	if after_three_day==frappe.utils.getdate():
			# 		lead['timeline']=On timeline
			# 	elif frappe.utils.getdate()<after_three_day:
			# 		lead['timeline']=Before time


		
	return data



