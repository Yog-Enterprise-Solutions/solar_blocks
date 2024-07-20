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
	
		{"fieldname": "parent", "label": ("Opportunity"), "fieldtype": "Data", "width": 150},
		{"fieldname": "title", "label": ("Name of job"), "fieldtype": "Data", "width": 150},
							#field from child table Task Detail
		{"fieldname": "assigned_to_team", "label": ("Assigned Team"), "fieldtype": "Data", "width": 200},
		{"fieldname": "assigned_to_individual", "label": ("Assigned Individual"), "fieldtype": "Data", "width": 200},
		{"fieldname": "task_status", "label": ("Status"), "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 200},
		{"fieldname": "priority", "label": ("Priority"), "fieldtype": "Data", "width": 100},
		{"fieldname": "started_on", "label": ("Started On"), "fieldtype": "Data", "width": 200},
		{"fieldname": "scheduled_close", "label": ("Scheduled Close"), "fieldtype": "Data", "width": 200},
		# {"fieldname": "completion_date", "label": ("Actual Close Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "notes", "label": ("Notes"), "fieldtype": "Data", "width": 200},
		{"fieldname": "days_aging", "label": ("DaysAge"), "fieldtype": "Data", "width":100},
		{"fieldname": "aging_timeline", "label": ("Aging Timeline"), "fieldtype": "Data", "width":100}
		
	]
	return columns





def get_data(filters):
	total_age=0
	total_no_of_jobs=0
	data = frappe.db.sql('''
	SELECT 
		o.party_name,
		o.title,
		t.*     
	FROM 
		`tabOpportunity` o
	JOIN 
		`tabTask Detail` t
	ON 
		o.name = t.parent
	WHERE 
		t.task_status = 'Pending';
''', as_dict=True)
	for opportunity in data:
		creation_date =opportunity.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			opportunity['days_aging'] =days_aging
			total_age+=days_aging
			total_no_of_jobs+=1
			after_three_day = frappe.utils.add_to_date(frappe.utils.getdate(creation_date), days=3)
			if days_aging>3:
				opportunity['aging_timeline']='Late'
			if days_aging<3:
				opportunity['aging_timeline']='Before time'
			if days_aging==3:
				opportunity['aging_timeline']='On time'
		if opportunity['started_on']:
			opportunity['started_on']=opportunity['started_on'].strftime('%m-%d-%Y')
		if opportunity['scheduled_close']:
			opportunity['scheduled_close']=opportunity['scheduled_close'].strftime('%m-%d-%Y')
	if total_age>0 and total_no_of_jobs>0:
		average=round((total_age/total_no_of_jobs),2)
		data.append({'task_status':total_no_of_jobs,'assigned_to_individual':'Total Tickets','notes':"Average Ageing",'days_aging':average})
	return data



