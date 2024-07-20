import frappe
from datetime import datetime


def get_data(filter,report_name):
    total_age = 0
    total_no_of_jobs = 0
    late = 0
    before_time = 0
    on_time = 0
    dashboard='Project Dashboard'
    if filter=='Interconnection' or filter=='Structural Permitting' or filter=='Electrical Permit' or filter=='Installation Work' or filter=='Pre Install Work' or filter=="Structural Inspection" or filter=='Electrical Inspection' or filter=="PTO":
        data = frappe.get_all(
        doctype="Project",
        fields=["creation", "custom_project_stage"],
        filters={"custom_stage": ["like", f"%{filter}%"],"project_status": ("!=", "Cancelled")}
    )
    else:
        data = frappe.get_all(
            doctype="Project",
            fields=["creation", "custom_project_stage"],
            filters={"custom_project_stage":filter,"project_status": ("!=","Cancelled")}
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
    #Welcome Call 
    data.append(get_data('Welcome Call','Welcome Call'))
    #Site Visit
    data.append(get_data('Site Visit','Site Visit'))
    #Engineering
    data.append(get_data('Engineering','Engineering'))
    #Interconnection
    data.append(get_data('Interconnection','Interconnection'))
    #Structural Permitting
    data.append(get_data('Structural Permitting','Structural Permitting'))
    #Electrical Permit
    data.append(get_data('Electrical Permit','Electrical Permit'))
    #Procurements
    data.append(get_data('Procurements','Procurement'))
    #Pre Install Work
    data.append(get_data('Pre Install Work','Pre Install Date'))
    #Installation Work
    data.append(get_data('Installation Work','Install Work'))
    #Commissioning
    data.append(get_data('Commissioning','Commissioning'))
    #Electrical Inspection
    data.append(get_data('Electrical Inspection','Electrical Inspection'))
    #Structural Inspection
    data.append(get_data('Structural Inspection','Structural Inspection'))
    #PTO
    data.append(get_data('PTO','PTO'))
    #Final Submitted
    data.append(get_data('Final Submitted','Final Submitted'))
    return data
    #hello committ the new 

