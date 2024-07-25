import frappe

from erpnext.crm.doctype.opportunity.opportunity  import Opportunity
from solar_blocks.override.lead import assign_permissions


# ---------------------------------------------------------
#assign opportunity on after save on maxfit completed -----------------

def assign_and_share_opportunity_on_maxfit_completed(user_group, name):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':user_group},fields={'*'})
    # frappe.msgprint(f"{user_group}")
    for i in user_group:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = i.user
        todo.reference_type = "Opportunity"
        todo.reference_name =name
        todo.description = "Assign"
        todo.insert(ignore_permissions=True)
        if not frappe.db.exists('DocShare',{'user':i.user,'share_name':name}):
            share = frappe.new_doc('DocShare')
            share.user = i.user
            share.share_doctype = "Opportunity"
            share.share_name =name
            share.read = 1
            share.write=1
            share.notify_by_email=1
            share.insert(ignore_permissions=True)
        

        

def enqueue_todo_and_share_on_maxfit_completed(doc, method=None):
    #set user permissin for team
    if doc.has_value_changed("custom_assign_team"):
        assign_permissions(doc,'Opportunity')
    if doc.opportunity_status=='Maxfit Completed':
        user_group_members = frappe.db.get_all("User Group Member", filters={'parent': doc.custom_assign_user_group}, fields={'*'})
        for member in user_group_members:
            if not frappe.db.exists('ToDo',{'reference_name':doc.name,'allocated_to':member.user,'status':'Open'}):
                frappe.enqueue(
                assign_and_share_opportunity_on_maxfit_completed,
                now=True,
                # queue='long',
                job_name='Assign Todo On Maxfit Completed',
                user_group=doc.custom_assign_user_group,
                name=doc.name
            )


#assign opportunity on insert -----------------

def assign_and_share(user_group, name):
    user_group_members = frappe.db.get_all("User Group Member", filters={'parent': user_group}, fields={'*'})
    for member in user_group_members:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = member.user
        todo.reference_type = "Opportunity"
        todo.reference_name = name
        todo.description = "Assign"
        todo.insert(ignore_permissions=True)
        if not frappe.db.exists('DocShare',{'user':member.user,'share_name':name}):
            share = frappe.new_doc('DocShare')
            share.user = member.user
            share.share_doctype = "Opportunity"
            share.share_name = name
            share.read = 1
            share.write = 1
            share.notify_by_email = 1
            share.insert(ignore_permissions=True)
        

def enqueue_todo_and_share(doc, method=None):
    user_group_members = frappe.db.get_all("User Group Member", filters={'parent': doc.custom_assign_user_group}, fields={'*'})
    for member in user_group_members:
        if not frappe.db.exists('ToDo',{'reference_name':doc.name,'allocated_to':member.user,'status':'Open'}):
            frappe.enqueue(
            assign_and_share,
            now=True,
            # queue='long',
            job_name='Assign Todo On Opportunity Insert',
            user_group=doc.custom_assign_user_group,
            name=doc.name
        )




#before insert set document status template and user
def set_user_group_and_document_status_template_before_insert(doc,method=None):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    for i in user_group:
        doc.append('users', {
            'user':i.user
        })
    # ---------create document template in document status child table--------------
    #create document template
    list_of_documents = [
        "ACP5 Report",
        "Property Survey",
        "FZ Survey",
        "Lift Required",
        "Historical Building",
        "Stop Work Order",
        "Utility Bills",
        "Property Tax",
        "Property Deed"
    ]
    for i in list_of_documents:
        doc.append("custom_document_status", 
        {'document':i})


# ---------assign user and send email on multiple condition on validate
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
def assign_users_and_send_mails(doc,Method=None):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
    for i in user_group:
        row = doc.append("task_user", {
        "user":i.user,
        "email":i.user
    })

    # ------------------------------------------------------send email on ticket----------------------
    
    if doc.task_details:
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
                                    Link: <a href="https://erp.solarblocks.us/app/opportunity/{doc_name}">{doc_name}</a> <br>
                                    Notes: {notes}'''
                        # receiver.append(frappe.db.get_value('User',{'first_name':created_by},'email'))
                        receiver.append(created_by)
                        # frappe.throw(f"{receiver}")
                        if receiver:
                            frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Ticket Completed")
                            frappe.msgprint(f"Email sent for ticket completed")
                            receiver=[]
            elif i.task_status=='Open':
                cur_date=frappe.utils.getdate()
                if i.is_notified==0:
                    started_on=frappe.utils.getdate(i.started_on)
                    notes=i.notes
                    html_ccontent=f'''Hi, <br>
                                    You have been assigned the following ticket:<br>
                                    Link: <a href="https://erp.solarblocks.us/app/opportunity/{doc_name}">{doc_name}</a> <br>
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
    #on scheduled appointment
    if doc.opportunity_status=='Proposal' or doc.opportunity_status=='Opportunity' or doc.opportunity_status=='Appointment Scheduled':
        if doc.custom_is_proposed==0 and doc.date_and_time_of_appointment!=None:
            frappe.throw(f"{doc.email}")
            # frappe.throw(f"{doc.date_and_time_of_appointment}")
            cur_date=doc.date_and_time_of_appointment
            formatted_date=frappe.utils.format_datetime(cur_date, "MMMM dd yyyy")
            subject=f"Congratulations!!! {doc.custom_first_name} {doc.custom_last_name} at {doc.custom_street} - Your Appointment is scheduled on {formatted_date}"
            create_event_with_participants(doc,subject,cur_date)
            doc.custom_is_proposed=1
    
    #on scheduled at later date   
    if doc.opportunity_status=='Proposal' or doc.opportunity_status=='Opportunity' or doc.opportunity_status=='Appointment Scheduled':
        if doc.custom_is_later==0 and doc.date_and_time!=None:
            cur_date=doc.date_and_time
            formatted_date=frappe.utils.format_datetime(cur_date, "MMMM dd yyyy")
            subject=f"Congratulations!!! {doc.custom_first_name} {doc.custom_last_name} at {doc.custom_street} - Your Appointment is scheduled on {formatted_date}"
            create_event_with_participants(doc,subject,cur_date)
            doc.custom_is_later=1
        
        
        
        
    # ----------------------------------email on appointment schedule to design team------------------------------
    status_changed = doc.has_value_changed("opportunity_status")
    if status_changed:
        if doc.opportunity_status=='Appointment Scheduled':
            user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assign_user_group},fields={'*'})
            subject='Opportunity is Created and Assigned'
            message=f'''Hello, <br>
                        <p><strong>Design Team,</strong><br></p>
                        <p>A new opportunity is generated and requires Maxfit. Here is the link to the opportunity: <a href="https://erp.solarblocks.us/app/opportunity/{doc.name}">{doc.custom_first_name} {doc.custom_last_name}</a></p>
                        '''
            for i in user_group:
                frappe.sendmail(recipients=i.user,message=message,subject=subject)
                        
# ------------------------------------

# ------------------------------------


        
     

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




class CustomOpportunity(Opportunity):
    def after_insert(self):
        if self.opportunity_from == "Lead":
            frappe.get_doc("Lead", self.party_name).db_set('status','Open')

            # link_open_tasks(self.opportunity_from, self.party_name, self)
            # link_open_events(self.opportunity_from, self.party_name, self)
            # if frappe.db.get_single_value("CRM Settings", "carry_forward_communication_and_comments"):
            #     copy_comments(self.opportunity_from, self.party_name, self)
            #     link_communications(self.opportunity_from, self.party_name, self)



