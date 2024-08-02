import frappe
from solar_blocks.override.lead import assign_permissions


def safe_float_conversion(value):
    try:
        return float(value.replace(',', ''))
    except (ValueError, AttributeError):
        return 0.0  # or any default value you prefer


# ------------------set user permissin after save on assign team field
def after_save(doc,method=None):
    #set user permission for assign team
    if doc.has_value_changed("custom_assign_team"):
        assign_permissions(doc,'Project')





def before_save(doc,method=None):
    # ----------------------insert or append selling amount child table in profitability section----------
    doc.custom_selling_amount = []
    finance = {'Cash Amount': 0, 'Financing Amount': 0, 'Lease Amount': 0}

    if doc.cash_amount:
        finance['Cash Amount'] = safe_float_conversion(doc.cash_amount)
    if doc.financing_amount:
        finance['Financing Amount'] = safe_float_conversion(doc.financing_amount)
    if doc.lease_amount:
        finance['Lease Amount'] = safe_float_conversion(doc.lease_amount)

    for key, value in finance.items():
        doc.append('custom_selling_amount', {
            'service_name': key,
            'total': value
        })
#-----------------set timeline in ticket
    if doc.get("task_details"):
        for oc in doc.get("task_details"):
            oc.scheduled_close=frappe.utils.add_days(oc.started_on, 2)
            if oc.completion_date:
                if oc.completion_date==oc.scheduled_close:
                    oc.timeline='On-Time'
                else:
                    if oc.completion_date>oc.scheduled_close:
                        oc.timeline='Delayed'
                    else:
                        oc.timeline='Before Time'
            if oc.assigned_to_team:
            
                user_group=frappe.db.get_all("User Group Member",filters={'parent':oc.assigned_to_team},fields={'*'})
            
                users = [entry['user'] for entry in user_group]
                
                for u in users:
                    child_row = doc.append("notify_users", {})
                    child_row.notifyto = str(u)
                
                
            if oc.assigned_to_individual:
                child_row = doc.append("notify_users", {})
                child_row.notifyto = str(oc.assigned_to_individual)
#---------------------send mails on ticket
        doc_name=doc.name
        receiver=[]
        for i in doc.task_details:
            cur_date=frappe.utils.getdate()
            if i.task_status=='Completed':
                if i.is_completed==0:
                
                    actual=frappe.utils.getdate(i.completion_date)
                    if actual==cur_date:
                    
                        notes=i.notes
                        created_by=i.created_by
                        html_ccontent=f'''Hi, <br>
                                    Your Ticket has been worked upon and Completed:<br>
                                    Link: <a href="https://erp.solarblocks.us/app/project/{doc_name}">{doc_name}</a> <br>
                                    Notes: {notes}'''
                        # receiver.append(frappe.db.get_value('User',{'first_name':created_by},'email'))
                        receiver.append(created_by)
                        if receiver:
                            frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Ticket Completed")
                            frappe.msgprint(f"Email sent for ticket completed")
                            i.is_completed=1
                            receiver=[]
            elif i.task_status=='Open':
                if i.is_notified==0:
                    started_on=frappe.utils.getdate(i.started_on)
                    notes=i.notes
                    html_ccontent=f'''Hi, <br>
                                    You have been assigned the following ticket:<br>
                                    Link: <a href="https://erp.solarblocks.us/app/project/{doc_name}">{doc_name}</a> <br>
                                    Notes: {notes}'''
                    if cur_date==started_on:
                        i.is_notified=1
                        
                        if i.assigned_to_individual:
                            individual=i.assigned_to_individual
                            receiver.append(individual)
                        elif i.assigned_to_team:
                            # frappe.throw(f"oem")
                            team=i.assigned_to_team
                            user_group=frappe.db.get_all("User Group Member",filters={'parent':team},fields={'*'})
                            for i in user_group:
                                receiver.append(i.user)
                    if receiver:
                        frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Ticket Created")
                        frappe.msgprint(f"Email sent for assigned ticket")
                        receiver=[]



def after_insert(doc,method=None):
    if str(doc.expected_start_date)=="None":
        doc.expected_start_date=frappe.utils.nowdate()
        doc.expected_end_date=frappe.utils.add_months(doc.expected_start_date, 2)
    

    proj_template=frappe.db.get_all("Project Template Task",filters={'parent':doc.project_template},fields={'*'})
    for i in proj_template:
        task=frappe.db.get_all("Task",filters={'project':doc.name,'subject':i.subject},fields={'*'})
        if len(task)>0: 
            get_task_doc=frappe.get_doc("Task",task[0]['name'])
            get_task_doc.task_priority=i.idx
            get_task_doc.custom_customer_name=doc.project_name
            get_task_doc.save()
    # -------------------create bom after project insert---------------------
    # # Initialize totals for each group
    totals = {
        'SOLAR ITEMS': 0,
        'ELECTRICAL': 0,
        'IRONRIDGE SKIRTS': 0,
        'ROOF TECH PITCHED ROOF ATTACHMENTS': 0,
        'UNIRAC FLAT ROOF': 0,
        'IRONRIDGE PITCHED ROOF': 0,
        'IRONRIDGE FLAT ROOF': 0,
        'CONDUITS AND ACCESORIES (METTALIC)': 0,
        'WIRES/CABLES': 0,
        'APPROVALS/FEES': 0,
        'MANPOWER': 0
    }
    list_opp = frappe.db.get_list('Item')
    bos = frappe.new_doc('BOS')
    bos.project_name=doc.project_name
    bos.project=doc.name
    for key,value in totals.items():
        bos.append('totals_of__services',{'service_name':key,'total':value})


    group_to_field_map = {
        'SOLAR ITEMS': 'solar_items',
        'ELECTRICAL': 'electrical',
        'IRONRIDGE SKIRTS': 'ironridge_skirts',
        'ROOF TECH PITCHED ROOF ATTACHMENTS': 'roof_tech_pitched_roof_attachments',
        'UNIRAC FLAT ROOF': 'unirac_flat_roof',
        'IRONRIDGE PITCHED ROOF': 'ironridge_pitched_roof',
        'IRONRIDGE FLAT ROOF': 'ironridge_flat_roof',
        'CONDUITS AND ACCESORIES (METTALIC)': 'conduits_and_accesories_mettalic',
        'WIRES/CABLES': 'wires_cables',
        'APPROVALS/FEES': 'approvals_fees',
        'MANPOWER': 'manpower'
    }

    for i in list_opp:
        item = frappe.get_doc('Item', i['name'])
        field_name = group_to_field_map.get(item.custom_bos_item_group)
        if field_name:
            # amount = item.custom_test * item.valuation_rate
            bos.append(field_name, {
                'item_code': item.name,
                'uom': item.stock_uom,
                'rate': item.valuation_rate
                # 'amount': amount
            })
        

    bos.insert()


    # -------------------------send mail on project create------------------------
    teams = frappe.get_all('Team')
    receipients = set()
    parent_user=frappe.session.user
    # Iterate through each team
    for team in teams:
        team_doc = frappe.get_doc('Team', team.name)
        # Check the child table for the specified user and 'Sales Closure' role
        if any(member.user == parent_user for member in team_doc.get('user_and_role')):
            for member in team_doc.get('user_and_role'):
                if member.role ==doc.assign_to_user_group:
                    receipients.add(member.user)
    # Send email if recipients are found
    if receipients:
        subject = 'Project Assign'
        message = f'''
        <p>New Project Assigned</p>
        '''
        frappe.sendmail(recipients=list(receipients), message=message, subject=subject)


                        
                    
                    



