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
	
		{"fieldname": "custom_first_name", "label": ("Name of job"), "fieldtype": "Data", "width": 150},
		{"fieldname": "expected_closing_date", "label": ("Excepted Close Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Date Created"), "fieldtype": "Data", "width": 200},
		{"fieldname": "created_by", "label": ("Created By"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing"), "fieldtype": "Data", "width": 100},
		{"fieldname": "date_and_time_of_appointment", "label": ("Appt Date and Time Schedule"), "fieldtype": "Data", "width": 200},
		{"fieldname": "date_and_time", "label": ("Appt Reschedule Date and Time"), "fieldtype": "Data", "width": 200},
		{"fieldname": "notes_for_site_review", "label": ("Proposal Notes"), "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 100}
		
	]
	return columns





def get_data(filters):
	data=frappe.get_all(
		doctype="Opportunity",
		fields=["custom_first_name","custom_last_name","expected_closing_date","created_by","creation","date_and_time_of_appointment","date_and_time","notes_for_site_review"],
		filters=[{"opportunity_status":'Appointment Scheduled'}])
	
	total_age=0
	total_no_of_jobs=0
	for opportunity in data:
		if opportunity['custom_last_name'] is not None:
			custom_first_name=opportunity['custom_first_name']+" "+opportunity['custom_last_name']
		else:
			custom_first_name=opportunity['custom_first_name']
		opportunity['custom_first_name']=custom_first_name
		creation_date = opportunity.get('creation')
		if creation_date:
			days_aging = (datetime.now() - creation_date).days
			opportunity['aging'] =days_aging
			total_age+=days_aging
			total_no_of_jobs+=1
			opportunity['creation']=creation_date.strftime('%m-%d-%Y')
			after_three_day = frappe.utils.add_to_date(frappe.utils.getdate(creation_date), days=3)
			if days_aging>3:
				opportunity['timeline']='Late'
			if days_aging<3:
				opportunity['timeline']='Before time'
			if days_aging==3:
				opportunity['timeline']='On time'
		expected_closing_date = opportunity.get('expected_closing_date')
		if expected_closing_date:
			opportunity['expected_closing_date']=expected_closing_date.strftime('%m-%d-%Y')
		date_and_time_of_appointment_str = str(opportunity.get('date_and_time_of_appointment'))
		if date_and_time_of_appointment_str and date_and_time_of_appointment_str != 'None':
			current_datetime = datetime.strptime(date_and_time_of_appointment_str,'%Y-%m-%d %H:%M:%S')
			opportunity['date_and_time_of_appointment'] = current_datetime.strftime('%m-%d-%Y %H:%M:%S')
		date_and_time = str(opportunity.get('date_and_time'))
		if date_and_time and date_and_time != 'None':
			current_datetime = datetime.strptime(date_and_time,'%Y-%m-%d %H:%M:%S')
			opportunity['date_and_time'] = current_datetime.strftime('%m-%d-%Y %H:%M:%S')
	if total_age>0 and total_no_of_jobs>0:
		average=round((total_age/total_no_of_jobs),2)
		data.append({'custom_first_name':None,'expected_closing_date': None, 'created_by': 'Average Ageing', 'creation':None, 'custom_customer_availability': None, 'aging': average, 'timeline':None})
	return data



