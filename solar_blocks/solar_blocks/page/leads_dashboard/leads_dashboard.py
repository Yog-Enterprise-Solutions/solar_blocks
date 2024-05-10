import frappe
from datetime import datetime


def get_data(filter,report_name):
    total_age = 0
    total_no_of_jobs = 0
    late = 0
    before_time = 0
    on_time = 0
    
    data = frappe.get_all(
        doctype="Lead",
        fields=["creation", "lead_sub_status"],
        filters=[{"lead_sub_status":filter}]
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
        'total_no_of_jobs': total_no_of_jobs,
        "on_time": on_time,
        "before_time": before_time,
        "late": late,
        "average":average
    }
    
    
    return final_data

@frappe.whitelist()
def get_leads():
    data=[]
    #lead 
    data.append(get_data('Lead','Lead'))
    #pending additional information
    data.append(get_data('Pending additional information','Pending Additional Information'))
    #Tried to Call & no response
    data.append(get_data('Tried to Call & no response','Tried to call and no response'))
    #Call at later Date
    data.append(get_data('Call at later Date','Call at later date'))
    #Not Interested
    data.append(get_data('Not Interested','Not Interested'))
    #Lead Disqualified
    data.append(get_data('Lead Disqualified','Lead Disqualified'))
    #Convert to Opportunity
    data.append(get_data('Convert to Opportunity','Convert to Opportunity'))
    # frappe.throw(f"{data}")
    return data

