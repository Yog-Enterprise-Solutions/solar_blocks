# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import now_datetime, get_datetime


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)[0]
	summary_data=get_data(filters)[1]
	report_summary=get_report_summary(summary_data)
	chart=0
	# frappe.throw(f"{data}")
	# frappe.log_error('data',data)
	if not data:
		frappe.msgprint("No records found")
	return columns, data,None,chart,report_summary
	




def get_columns():
	columns = [
	
		{"fieldname": "custom_first_name", "label": ("Name of job"), "fieldtype": "Data", "width": 150},
		{"fieldname": "expected_closing_date", "label": ("Excepted Close Date"), "fieldtype": "Data", "width": 200},
		{"fieldname": "creation", "label": ("Date Created"), "fieldtype": "Data", "width": 200},
		{"fieldname": "aging", "label": ("Ageing"), "fieldtype": "Data", "width": 100},
		{"fieldname": "opportunity_status", "label": ("Opportunity Status"), "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": ("Timeline"), "fieldtype": "Data", "width": 100}
		
	]
	return columns





def get_data(filters):
	data = frappe.get_all(
    doctype="Opportunity",
    fields=["opportunity_status","custom_first_name", "custom_last_name", "expected_closing_date", "created_by", "creation", "opportunity_status"],
    filters=[{"opportunity_status": ["in", ['Client Won', 'Client Lost', 'Client Disqualified']]}]
)
	total_age=0
	total_no_of_jobs=0
	client_won=0
	client_lost=0
	client_disqualified=0
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
		if opportunity['opportunity_status']=='Client Won':
			client_won+=1
		if opportunity['opportunity_status']=='Client Lost':
			client_lost+=1
		if opportunity['opportunity_status']=='Client Disqualified':
			client_disqualified+=1
		expected_closing_date = opportunity.get('expected_closing_date')
		if expected_closing_date:
			opportunity['expected_closing_date']=expected_closing_date.strftime('%m-%d-%Y')
	if total_age>0 and total_no_of_jobs>0:
		average=round((total_age/total_no_of_jobs),2)
		data.append({'custom_first_name':None,'expected_closing_date': None, 'created_by': 'Average Ageing', 'creation':None, 'custom_customer_availability': None, 'aging': average, 'timeline':None})
	sum_data={'client_won':client_won,'client_lost':client_lost,'client_disqualified':client_disqualified}
	return data,sum_data



def get_report_summary(data):
	if not data:
		return None
	else:
		return[
			{
				'value':data.get('client_won'),
				'indicator':'Red',
				'label':"Client Won",
				'datatype':'Int'
			},
			{
				'value':data.get('client_lost'),
				'indicator':'Yellow',
				'label':"Client Lost",
				'datatype':'Int'
			},
			{
				'value':data.get('client_disqualified'),
				'indicator':'Green',
				'label':"Client Disqualified",
				'datatype':'Int'
			}
		]




