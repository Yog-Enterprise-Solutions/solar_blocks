import frappe
from datetime import datetime, timedelta
from frappe.utils import now_datetime, get_datetime, add_days

def execute(filters=None):
	columns, data = get_columns(), get_data()[0]
	# summary_data=get_data()[1]
	# frappe.throw(f"{data}")
	chart=get_chart_data(data)
	# report_summary=get_report_summary(summary_data)
	if not data:
		frappe.msgprint("No records found")
	return columns, data,None,chart

def get_columns():
	columns = [
		{"fieldname": "week", "label": ("Week"), "fieldtype": "Data", "width": 150},
		{"fieldname": "weekdate", "label": ("date"), "fieldtype": "Data", "width": 250},
		{"fieldname": "number_of_jobs", "label": ("Number of Jobs"), "fieldtype": "Int", "width": 200},
		{"fieldname": "average_aging", "label": ("Average Aging"), "fieldtype": "Float", "width": 200},
	]
	return columns

def get_data():
	six_weeks_ago = frappe.utils.add_to_date(frappe.utils.getdate(), days=-42)
	todays_date = frappe.utils.getdate()
	date_after_todays_date = frappe.utils.add_to_date(todays_date, days=-6)
	current_date = todays_date
	f_data = []
	late=0
	before_time=0
	on_time=0
	for i in range(6):
		total_age = 0
		total_no_of_jobs = 0
		data = frappe.get_all(
			doctype="Opportunity",
			fields=["creation"],
			filters=[
				{"opportunity_status": "Appointment Scheduled"},
				{"creation": ["between", [date_after_todays_date, current_date]]}
			]
		)
		# if i==1:
		# 	frappe.throw(f"{len(data)}")
		if not data:
			f_data.append({'week': f"week {i+1}", "weekdate": f"{date_after_todays_date.strftime('%m/%d/%Y')} - {current_date.strftime('%m/%d/%Y')}", "no_of_jobs": 0, "average_ageing": 0})
		else:
			# frappe.throw(f"{i}")
			for opportunity in data:
				total_no_of_jobs += 1
				creation_date = opportunity.get('creation')
				# frappe.throw(f"{creation_date}")
				if creation_date:
					days_aging = (datetime.now() - creation_date).days
					total_age += days_aging
					if days_aging>3:
						late+=1
					if days_aging<3:
						before_time+=1
					if days_aging==3:
						on_time+=1
			average = round((total_age / total_no_of_jobs), 2) if total_no_of_jobs > 0 else 0
			# frappe.throw(f"{average}")
			f_data.append({'week': f"week {i+1}", "weekdate": f"{date_after_todays_date.strftime('%m/%d/%Y')} - {current_date.strftime('%m/%d/%Y')}", "number_of_jobs": total_no_of_jobs, "average_aging": average})
			# if i==1:
				# frappe.throw(f"{f_data}")
		current_date = frappe.utils.add_to_date(date_after_todays_date, days=-1)
		# frappe.throw(f"{current_date}")  2024-05-09
		date_after_todays_date = frappe.utils.add_to_date(date_after_todays_date, days=-7)
		k={'late':late,"before_time":before_time,"on_time":on_time}
		# frappe.throw(f"{date_after_todays_date}")  2024-05-03
	return f_data,k


def get_chart_data(data):
    if not data:
        return None
    
    labels = []
    job_counts = []
    age_averages = []
    
    for i in data:
        labels.append(i.get('weekdate'))
        job_counts.append(i.get('number_of_jobs'))
        age_averages.append(i.get('average_aging'))
    
    datasets = [
        {
            'name': 'Number of Jobs',
            'type': 'bar',
            'values': job_counts,
            'bar_percentage': 0.6,  # Adjust as needed
            'yaxis': 'y'
        },
        {
            'name': 'Average Aging',
            'type': 'bar',
            'values': age_averages,
            'bar_percentage': 0.6,  # Adjust as needed
            'yaxis': 'y2'
        }
    ]
    
    chart = {
        'data': {
            'labels': labels,
            'datasets': datasets
        },
        'type': 'bar',
        'height': 300
    }
    
    return chart
