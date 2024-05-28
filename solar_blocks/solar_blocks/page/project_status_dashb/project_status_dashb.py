import frappe
from datetime import datetime


def get_data(filter,report_name):
    total_age = 0
    total_no_of_jobs = 0
    late = 0
    before_time = 0
    on_time = 0
    dashboard='Project Dashboard'
    
    data = frappe.get_all(
        doctype="Project",
        fields=["creation", "project_status"],
        filters=[{"project_status":filter}]
    )
    
    for project in data:
        creation_date = project.get('creation')
        if creation_date:
            days_aging = (datetime.now() - creation_date).days
            total_age += days_aging
            total_no_of_jobs += 1
            if days_aging > 3:
                late += 1
            if days_aging < 3:
                before_time += 1
            if days_aging == 3:
                on_time += 1
    
    if total_age > 0 and total_no_of_jobs > 0:
        average = round((total_age / total_no_of_jobs), 2)
    else:
        average = total_age
        
    final_data = {
        'project_name':filter,
        'report_name':frappe.utils.get_url(f'app/query-report/{report_name}'),
        # 'dashboard_name':frappe.utils.get_url(f'app/dashboard-view/{dashboard}'),
        'total_no_of_jobs': total_no_of_jobs,
        "on_time": on_time,
        "before_time": before_time,
        "late": late,
        "average":average
    }
    
    
    return final_data

@frappe.whitelist()
def get_project():
    data=[]
    #Not Started
    data.append(get_data('Not Started','Not Started'))
    #In Progress
    data.append(get_data('In Progress','In Progress'))
    #On Hold
    data.append(get_data('On Hold','On Hold'))
    #Completed
    data.append(get_data('Completed','Completed'))
    return data
    #hello committ the new 

