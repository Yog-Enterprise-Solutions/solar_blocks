import frappe
from datetime import datetime


def get_data(filter,report_name):
    total_age = 0
    total_no_of_jobs = 0
    late = 0
    before_time = 0
    on_time = 0
    dashboard='Opportunity Dashboard'
    
    data = frappe.get_all(
        doctype="Opportunity",
        fields=["creation", "opportunity_status"],
        filters=[{"opportunity_status":filter}]
    )
    
    for lead in data:
        creation_date = lead.get('creation')
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
        'lead_name':filter,
        'report_name':frappe.utils.get_url(f'app/query-report/{report_name}'),
        'dashboard_name':frappe.utils.get_url(f'app/dashboard-view/{dashboard}'),
        'total_no_of_jobs': total_no_of_jobs,
        "on_time": on_time,
        "before_time": before_time,
        "late": late,
        "average":average
    }
    
    
    return final_data

@frappe.whitelist()
def get_opportunity():
    data=[]
    #Opportunity 
    data.append(get_data('Opportunity','Opportunity'))
    #Appointment Scheduled
    data.append(get_data('Appointment Scheduled','Appointment Scheduled'))
    #Maxfit Completed
    data.append(get_data('Maxfit Completed','Maxfit Completed'))
    #Proposal
    data.append(get_data('Proposal','Proposal'))
    #Contract Sent
    data.append(get_data('Contract Sent','Contract Sent'))
    #Client Won
    data.append(get_data('Client Won','Opportunity Status'))
    #Client Lost
    data.append(get_data('Client Lost','Opportunity Status'))
    #Client Disqualified
    data.append(get_data('Client Disqualified','Opportunity Status'))
    return data
    #hello committ the new 

