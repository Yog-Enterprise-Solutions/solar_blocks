import frappe

def assign_after_save_for_maxfit_complete(doc,method=None):
    if doc.opportunity_status=='Maxfit Completed':
        user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    # frappe.msgprint(f"{user_group}")
    for i in user_group:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = i.user
        todo.reference_type = "Opportunity"
        todo.reference_name = doc.name
        todo.description = "Assign"
        todo.insert(ignore_permissions=True)
        
        share = frappe.new_doc('DocShare')
        share.user = i.user
        share.share_doctype = "Opportunity"
        share.share_name = doc.name
        share.read = 1
        share.write=1
        share.notify_by_email=1
        share.insert(ignore_permissions=True)
        
    

def assign_and_share_opportunity_initially_from_user_group(doc,method=None):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    for i in user_group:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = i.user
        todo.reference_type = "Opportunity"
        todo.reference_name = doc.name
        todo.description = "Assign"
        todo.insert(ignore_permissions=True)
        
        share = frappe.new_doc('DocShare')
        share.user = i.user
        share.share_doctype = "Opportunity"
        share.share_name = doc.name
        share.read = 1
        share.write=1
        share.notify_by_email=1
        share.insert(ignore_permissions=True)
        
        
    #     for i in user_group:
    #         row = doc.append("task_user", {
    #     	"user":i.user,
    #     	"email":i.user
    #     })
    # doc.save()
    
def set_user_group_before_insert(doc,method=None):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    for i in user_group:
        doc.append('users', {
            'user':i.user
        })
    
def add_task_users_in_opportunity(doc,method=None):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    for i in user_group:
        row = doc.append("task_user", {
        "user":i.user,
        "email":i.user
    })

    # ------------------------------------------------------send email on ticket----------------------
    
    if doc.task_details:
        doc_name=doc.name
        receiver=[]
        for i in doc.task_details:
            cur_date=frappe.utils.getdate()
            if i.task_status=='Completed':
                if i.is_completed==0:
                    actual=frappe.utils.getdate(i.completion_date)
                    if actual==cur_date:
                        i.is_completed=1
                        notes=i.notes
                        created_by=i.created_by
                        html_ccontent=f'''Hi, <br>
                                    Your Ticket has been worked upon and Completed:<br>
                                    Link: <a href="https://myerp.solarblocks.us/app/opportunity/{doc_name}">{doc_name}</a> <br>
                                    Notes: {notes}'''
                        receiver.append(frappe.db.get_value('User',{'first_name':created_by},'email'))
                        # frappe.throw(f"{receiver}")
                        if receiver:
                            frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Ticket Completed")
                            frappe.msgprint(f"Email sent for ticket completed")
                            
                            receiver=[]
            elif i.task_status=='Open':
                if i.is_notified==0:
                    started_on=frappe.utils.getdate(i.started_on)
                    notes=i.notes
                    html_ccontent=f'''Hi, <br>
                                    You have been assigned the following ticket:<br>
                                    Link: <a href="https://myerp.solarblocks.us/app/opportunity/{doc_name}">{doc_name}</a> <br>
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
                    
                    
# -------------------------------------------------email on proposal----------------------------------------
def create_event_with_participants(doc,subject,date):
    exist_event = frappe.db.exists("Event",{'subject':subject}, {"name": ("in", frappe.get_all("Event Participants", filters={"email":doc.email}, pluck="parent"))})
    if not exist_event:
        event = frappe.new_doc("Event")
        event.subject = subject  
        event.starts_on = date
        event.sync_with_google_calendar = 1
        event.google_calendar = "erp calendar"
        unique_emails =set()
        unique_participants = []
        participants = [{"reference_doctype": "Opportunity", "reference_docname": doc.name, "email":'info@solarblocks.us'}]
        user_group_members = frappe.db.get_all("User Group Member", filters={'parent': 'Sales closure'}, fields={'user'})
        for user_group_member in user_group_members:
            email = user_group_member.user
            participants.append({"reference_doctype": "Opportunity", "reference_docname": doc.name, "email": email})
        for participant in participants:
            email = participant["email"]
            if email not in unique_emails:
                unique_emails.add(email)
                unique_participants.append(participant)
        for participant_data in unique_participants:
            event_participant = event.append('event_participants', participant_data)
        event.save()
    

    if doc.opportunity_status=='Proposal' and doc.custom_is_proposed==0 and doc.date_and_time_of_appointment:
        cur_date=doc.date_and_time_of_appointment
        formatted_date=frappe.utils.format_datetime(cur_date, "dd MMMM yyyy")
        subject=f"Congratulations!!! {doc.custom_first_name} {doc.custom_last_name} at {doc.custom_street} - Your Appointment is scheduled at {formatted_date}"
        create_event_with_participants(doc,subject,cur_date)
        doc.custom_is_proposed=1
        
    elif doc.opportunity_status=='Proposal' and doc.custom_is_later==0 and doc.date_and_time:
        cur_date=doc.date_and_time
        formatted_date=frappe.utils.format_datetime(cur_date, "dd MMMM yyyy")
        subject=f"Congratulations!!! {doc.custom_first_name} {doc.custom_last_name} at {doc.custom_street} - Your Appointment is scheduled at {formatted_date}"
        create_event_with_participants(doc,subject,cur_date)
        doc.custom_is_later=1
        
     

def notify_opportunity(doc,method=None):
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
                
    # ts=frappe.db.get_list('Task',filters={'project':doc.name},fields=['*'])
    # for t in ts:
    # 	child_row = doc.append("taskss", {})
    # 	child_row.subject = t.subject
    # 	child_row.task_status = t.task_status