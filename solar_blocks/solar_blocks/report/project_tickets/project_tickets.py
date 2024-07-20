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
		{"fieldname": "parent", "label": "Project", "fieldtype": "Data", "width": 150},
		{"fieldname": "project_name", "label": "Name of job", "fieldtype": "Data", "width": 150},
		{"fieldname": "assigned_to_team", "label": "Assigned Team", "fieldtype": "Data", "width": 200},
		{"fieldname": "assigned_to_individual", "label": "Assigned Individual", "fieldtype": "Data", "width": 200},
		{"fieldname": "task_status", "label": "Status", "fieldtype": "Data", "width": 200},
		{"fieldname": "timeline", "label": "Timeline", "fieldtype": "Data", "width": 200},
		{"fieldname": "priority", "label": "Priority", "fieldtype": "Data", "width": 100},
		{"fieldname": "started_on", "label": "Started On", "fieldtype": "Data", "width": 200},
		{"fieldname": "scheduled_close", "label": "Scheduled Close", "fieldtype": "Data", "width": 200},
		{"fieldname": "completion_date", "label": "Actual Close Date", "fieldtype": "Data", "width": 200},
		{"fieldname": "notes", "label": "Notes", "fieldtype": "Data", "width": 200},
		{"fieldname": "days_aging", "label": "Days Age", "fieldtype": "Data", "width": 100},
		{"fieldname": "aging_timeline", "label": "Aging Timeline", "fieldtype": "Data", "width": 100}
	]
	return columns

def get_data(filters):
	total_age = 0
	total_no_of_jobs = 0

	conditions = []
	values = []

	if filters.task_status and not filters.timeline:
		conditions.append("t.task_status = %s")
		values.append(filters.task_status)
	elif filters.timeline and not filters.task_status:
		conditions.append("t.timeline = %s")
		values.append(filters.timeline)
	elif filters.task_status and filters.timeline:
		conditions.append("t.task_status = %s")
		values.append(filters.task_status)
		conditions.append("t.timeline = %s")
		values.append(filters.timeline)

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	data = frappe.db.sql(f'''
		SELECT 
			p.project_name,
			t.*
		FROM 
			`tabProject` p
		JOIN 
			`tabTask Detail` t ON p.name = t.parent
		WHERE 
			{where_clause}
		ORDER BY
			t.modified Desc
	''', values, as_dict=True)
	for project in data:
		creation_date = project.get('modified')
		if creation_date:
			creation_date = get_datetime(creation_date)
			days_aging = (now_datetime() - creation_date).days
			project['days_aging'] = days_aging
			total_age += days_aging
			total_no_of_jobs += 1

			if days_aging > 3:
				project['aging_timeline'] = 'Late'
			elif days_aging < 3:
				project['aging_timeline'] = 'Before time'
			else:
				project['aging_timeline'] = 'On time'

		if project['started_on']:
			project['started_on'] = get_datetime(project['started_on']).strftime('%m-%d-%Y')
		if project['scheduled_close']:
			project['scheduled_close'] = get_datetime(project['scheduled_close']).strftime('%m-%d-%Y')
		if project['completion_date']:
			project['completion_date'] = get_datetime(project['completion_date']).strftime('%m-%d-%Y')

	if total_age > 0 and total_no_of_jobs > 0:
		average = round((total_age / total_no_of_jobs), 2)
		data.append({'task_status': total_no_of_jobs, 'assigned_to_individual': 'Total Tickets', 'notes': "Average Ageing", 'days_aging': average})

	return data
