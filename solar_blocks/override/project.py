import frappe

def project_as(doc,method=None):
    # frappe.throw(f"validate")
    # frappe.throw(f"validate")
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




    if doc.task_details:
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
                                    Link: <a href="https://myerp.solarblocks.us/app/project/{doc_name}">{doc_name}</a> <br>
                                    Notes: {notes}'''
                        receiver.append(frappe.db.get_value('User',{'first_name':created_by},'email'))
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
                                    Link: <a href="https://myerp.solarblocks.us/app/project/{doc_name}">{doc_name}</a> <br>
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
                            

def update_auto_number_in_task_for_priority(doc, method=None):    
    proj_template=frappe.db.get_all("Project Template Task",filters={'parent':doc.project_template},fields={'*'})
    for i in proj_template:
        task=frappe.db.get_all("Task",filters={'project':doc.name,'subject':i.subject},fields={'*'})
        # frappe.msgprint("jjjj")
        if len(task)>0: 
            get_task_doc=frappe.get_doc("Task",task[0]['name'])
            get_task_doc.task_priority=i.idx
            get_task_doc.save()

def project_bs(doc, method=None):

    if str(doc.expected_start_date)=="None":
        doc.expected_start_date=frappe.utils.nowdate()
        doc.expected_end_date=frappe.utils.add_months(doc.expected_start_date, 2)
        
        
        

        
    # if not doc.get("task_details"):
    #     opportunity = frappe.get_doc('Opportunity', doc.opportunity)

    #     for oc in opportunity.get("task_details"):	
    #     	child_row = doc.append("task_details", {})
    #     	child_row.assigned_to_team = oc.assigned_to_team
    #     	child_row.task_status = oc.task_status
    #     	child_row.assign_date = oc.assign_date
    #     	child_row.completion_date = oc.completion_date
    #     	child_row.notes=oc.notes
    #     	child_row.attachment=oc.attachment


    # if task_details_opportunity:
    #     if not doc.get('task_details'):
    #         doc.set('task_details', [])

    #     for task_detail in task_details_opportunity:
        
    #         doc.append('task_details', task_detail)

def assign_project_for_require_welcome_call(doc,method=None):
    frappe.throw(f"yesss")
    user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.assign_to_user_group},fields={'*'})

    for i in user_group:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = i.user
        todo.reference_type = "Task"
        todo.reference_name = doc.name
        todo.description = "Assign"
        frappe.throw("yha")
        todo.insert(ignore_permissions=True)
        frappe.throw("bha")
        
        share = frappe.new_doc('DocShare')
        share.user = i.user
        share.share_doctype = "Task"
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
        
                