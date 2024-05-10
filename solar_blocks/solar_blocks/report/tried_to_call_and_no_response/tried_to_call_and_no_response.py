# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import now_datetime, get_datetime


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	# frappe.throw(f"{data}")
	# frappe.log_error('data',data)
	if not data:
		frappe.msgprint("No records found")
	return columns, data
	




def get_columns():
	columns = [
	
		{"fieldname": "first_name", "label": ("Name of job"), "fieldtype": "Data", "width": 150},
		{"fieldname": "source", "label": ("Source"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Date Created"), "fieldtype": "Data", "width": 200},
		{"fieldname": "lead_owner", "label": ("Created By"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing"), "fieldtype": "Data", "width": 100},
		{"fieldname": "custom_customer_availability", "label": ("Additional Notes"), "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 100}
		
	]
	return columns





def get_data(filters):
	data=frappe.get_all(
		doctype="Lead",
		fields=["first_name","last_name","lead_owner","creation","source","custom_customer_availability","lead_sub_status"],
		filters=[{"lead_sub_status":'Tried to Call & no response'}])
	
	total_age=0
	total_no_of_jobs=0
	for lead in data:
		if lead['last_name'] is not None:
			full_name=lead['first_name']+" "+lead['last_name']
		else:
			full_name=lead['first_name']
		lead['first_name']=full_name
		creation_date = lead.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			lead['aging'] =days_aging
			total_age+=days_aging
			total_no_of_jobs+=1
			# lead['creation']=frappe.utils.getdate(creation_date)
			lead['creation']=creation_date.strftime('%m-%d-%Y')
			after_three_day = frappe.utils.add_to_date(frappe.utils.getdate(creation_date), days=3)
			if days_aging>3:
				lead['timeline']='Late'
			if days_aging<3:
				lead['timeline']='Before time'
			if days_aging==3:
				lead['timeline']='On time'
	if total_age>0 and total_no_of_jobs>0:
		average=round((total_age/total_no_of_jobs),2)
		data.append({'first_name': '', 'lead_owner': 'Average Ageing', 'creation':'', 'source': '', 'custom_customer_availability':'', 'lead_sub_status': '', 'aging':average, 'timeline': ''})
	return data



