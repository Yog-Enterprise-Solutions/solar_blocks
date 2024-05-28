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
	
		{"fieldname": "project_name", "label": ("Name of job"), "fieldtype": "Data", "width": 150},
		{"fieldname": "expected_close_date", "label": ("Excepted Close Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Date Created"), "fieldtype": "Data", "width": 200},
		{"fieldname": "date_ordered", "label": ("Order Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "delivery_date", "label": ("Delivery Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing"), "fieldtype": "Data", "width": 100},
		{"fieldname": "description", "label": ("Notes"), "fieldtype": "Data", "width": 200},
		{"fieldname": "custom_completed_by", "label": ("Completed By"), "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 100}
		
	]
	return columns





def get_data(filters):
	data = frappe.get_all(
    doctype="Project",
    fields=["name","project_name", "creation"],
    filters={"custom_project_stage": "Procurements", "project_status": ("!=", "Cancelled")}
)

	
	total_age=0
	total_no_of_jobs=0
	for project in data:
		task=frappe.db.get_all("Task",filters={'project':project.name,'subject':'Procurements'},fields={'custom_name_completed_by','expected_close_date','description','delivery_date','date_ordered'})
		# frappe.throw(f"{task}")
		for task in task:
			project['custom_completed_by'] = task['custom_name_completed_by']
			project['description'] = task['description']
			expected_close_date=task['expected_close_date']
			if expected_close_date:
				project['expected_close_date']=expected_close_date.strftime('%m-%d-%Y')
			delivery_date=task['delivery_date']
			if delivery_date:
				project['delivery_date']=delivery_date.strftime('%m-%d-%Y')
			date_ordered=task['date_ordered']
			if date_ordered:
				project['date_ordered']=date_ordered.strftime('%m-%d-%Y')
		creation_date = project.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			project['aging'] =days_aging
			total_age+=days_aging
			total_no_of_jobs+=1
			project['creation']=creation_date.strftime('%m-%d-%Y')
			after_three_day = frappe.utils.add_to_date(frappe.utils.getdate(creation_date), days=3)
			if days_aging>3:
				project['timeline']='Late'
			if days_aging<3:
				project['timeline']='Before time'
			if days_aging==3:
				project['timeline']='On time'
	if total_age>0 and total_no_of_jobs>0:
		average=round((total_age/total_no_of_jobs),2)
		data.append({'project_name': None, 'expected_end_date': None, 'creation': 'Average ageing', 'custom_completed_by': None, 'aging':average, 'timeline': None})
	return data



