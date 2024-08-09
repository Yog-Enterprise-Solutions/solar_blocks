import frappe
from datetime import datetime
import json

def create_link_for_folder(folder_name,lead):
    i_p=frappe.new_doc('image printer')
    i_p.title='For Email'
    i_p.flag='Flag'
    i_p.select='Medium'
    i_p.lead_ref=lead
    i_p.folder=folder_name
    i_p.insert()
    file_link=i_p.file_link
    return file_link
# send email on send email button that is in tasks
@frappe.whitelist()
def send_email_on_task(recipient_email,custom_customer_name,subject,custom_scheduled_on,project):
    emails=json.loads(recipient_email)
    recipient_email=[]
    for user in emails:
        recipient_email.append(user['user'])
    if subject=='Electrical Inspection':
        asbuilt_planset=''
        asbuilt_electrical_plan=''
        pro=frappe.db.get_value('Project',project,'custom_lead')
        if pro:
            lead=frappe.get_doc('Lead',pro)
            folder_name='Post Install Folder'
            file_link=create_link_for_folder(folder_name,lead)
            attachments=lead.custom_document_attachments
            for i in attachments:
                if i.name1=='Asbuilt Planset':
                    asbuilt_planset=i.attachment
                if i.name1=='Asbuilt Electrical Plan':
                    asbuilt_electrical_plan=i.attachment

        subject='Schedule an Electrical Inspection'
        message=f'''<p>Hello,</p>
                    <p>Greeting!</p>
                    <p>We have completed installation here, Can you please schedule an Electrical Inspection?</p>
                    <p>Do let us know whenever the inspection is scheduled.</p>
                    <p>Attached are the installed plans and Install pics for your reference.</p>
                    <ul>
                        <li><a href="{asbuilt_planset}">Asbuilt Planset</a></li>
                        <li><a href="{asbuilt_electrical_plan}">Asbuilt Electrical Plan</a></li>
                        <li><a href="{file_link}">Post Install Folder</a></li>
                    </ul>
                    <p>Thanks</p>
                    <p>Solarblocks</p>
                    '''
    if subject=='Electrical Permit':
        planset=''
        electrical_plan=''
        pro=frappe.db.get_value('Project',project,'custom_lead')
        project=frappe.get_doc('Project',project)
        address=project.custom_street + project.custom_city
        if pro:
            lead=frappe.get_doc('Lead',pro)
            folder_name='Pre Install Folder'
            file_link=create_link_for_folder(folder_name,lead)
            attachments=lead.custom_document_attachments
            for i in attachments:
                if i.name1=='Planset':
                    planset=i.attachment
                if i.name1=='Electrical Plans':
                    electrical_plan=i.attachment
        subject=f"{custom_customer_name} {address} , Electrical Permits"
        message=f'''<p>Hello,</p>
                    <p>Greetings!</p>
                    <p>Need to submit for Electrical permits for newly won project.</p>
                    <p>Please process the same</p>
                    <p>Documents Attached!</p>
                    <p>Thanks,</p>
                    <p>Solarblocks</p>
                     <ul>
                        <li><a href="{planset}">Planset</a></li>
                        <li><a href="{electrical_plan}">Electrical Plans</a></li>
                        <li><a href="{file_link}">Pre Install Folder</a></li>
                    </ul>
                    '''
    if subject=='Engineering':
        planset=''
        electrical_plan=''
        pro=frappe.db.get_value('Project',project,'custom_lead')
        if pro:
            lead=frappe.get_doc('Lead',pro)
            folder_name='Pre Install Folder'
            file_link=create_link_for_folder(folder_name,lead)
            attachments=lead.custom_document_attachments
            for i in attachments:
                if i.name1=='Planset':
                    planset=i.attachment
                if i.name1=='Electrical Plans':
                    electrical_plan=i.attachment
        subject='Planset Review'
        message=f'''<p>Hello,</p>
                    <p>Greetings!</p>
                    <p>Here is the newly won job,Please review the same</p>
                    <p>Kindly provide the PE letter with your observations for DOB permitting process.</p>
                    <p>Documents attached for your reference!</p>
                    <p>Thanks</p>
                    <ul>
                        <li><a href="{planset}">Planset</a></li>
                        <li><a href="{electrical_plan}">Electrical Plans</a></li>
                        <li><a href="{file_link}">Pre Install Folder</a></li>
                    </ul>
                    '''
    if subject=='Installation Work':
        dob_approved_plan=''
        dob_work_permit=''
        electrical_plans=''
        pro=frappe.db.get_value('Project',project,'custom_lead')
        if pro:
            lead=frappe.get_doc('Lead',pro)
            attachments=lead.custom_document_attachments
            for i in attachments:
                if i.name1=='DOB Approved Plans':
                    dob_approved_plan=i.attachment
                if i.name1=='DOB Work Permit':
                    dob_work_permit=i.attachment
                if i.name1=='Electrical Plans':
                    electrical_plans=i.attachment
        if custom_scheduled_on is not "":
            dt = datetime.strptime(str(custom_scheduled_on), "%Y-%m-%d %H:%M:%S")
            formatted_date=dt.strftime("%A %B %d %Y %I:%M %p")
        subject='Installation Work'
        message=f'''<p>Hi Team,</p>
                    <p>Installation is scheduled for this {formatted_date} .Attach approved plan and work permit.</p>
                    <p>Please let me know if you have any questions</p>
                    <p>Best Regards,</p>
                    <ul>
                        <li><a href="{dob_approved_plan}">DOB Approved Plans</a></li>
                        <li><a href="{dob_work_permit}">DOB Work Permit</a></li>
                        <li><a href="{electrical_plans}">Electrical Plans</a></li>
                    </ul>
                    '''
    frappe.sendmail(recipients=recipient_email,message=message,subject=subject)
    frappe.msgprint("Email send")
    return 1


# -------------------------------------------------HELPER fUNCTIONS---------------------------------
def assign(doc,group,doc_name):
    user_group=frappe.db.get_all("User Group Member",filters={'parent':group},fields={'*'})
    for i in user_group:
        todo = frappe.new_doc('ToDo')
        todo.allocated_to = i.user
        todo.reference_type = "Task"
        todo.reference_name = doc_name
        todo.description = "Assign"
        todo.insert(ignore_permissions=True)
        
        share = frappe.new_doc('DocShare')
        share.user = i.user
        share.share_doctype = "Task"
        share.share_name = doc_name
        share.read = 1
        share.write=1
        share.notify_by_email=1
        share.insert(ignore_permissions=True)

def set_customer(doc):
    customer_name=frappe.db.get_value('Project',doc.project,'project_name')
    doc.db_set('custom_customer_name',customer_name)


def update_multiple_custom_stage(project_name, remove_value):
    current_stage = frappe.db.get_value('Project', project_name, 'custom_stage')
    if current_stage:
        stage_list = current_stage.split(",")
        if remove_value in stage_list:
            stage_list.remove(remove_value)
        final_stage = ','.join(stage_list)
        if len(stage_list)>0:
            frappe.db.set_value('Project', project_name, {'custom_stage':final_stage,'custom_project_stage':stage_list[0]})


def create_event_with_participants(doc,date,formatted_date,schedule_task):
        project=frappe.db.get_value('Project',doc.project,['opportunity','custom_first_name','custom_last_name','custom_street'],as_dict=1)
        lead_name=frappe.db.get_value('Opportunity',project['opportunity'],'party_name')
        subject=f"{schedule_task} is scheduled at {formatted_date} for {project['custom_first_name']} {project['custom_last_name']} at {project['custom_street']}"
        event = frappe.new_doc("Event")
        event.subject = subject  
        event.starts_on = date
        event.sync_with_google_calendar = 1
        event.google_calendar = "erp calendar"
        # participants = [{"reference_doctype": "Task", "reference_docname": doc.name, "email": doc.email}]
        participants = []
        user_group_members = frappe.db.get_all("User Group Member", filters={'parent': doc.custom_assigned_group}, fields={'user'})
        for user_group_member in user_group_members:
            email = user_group_member.user
            participants.append({"reference_doctype": "Lead", "reference_docname":lead_name, "email":email})
        for participant_data in participants:
            event_participant = event.append('event_participants', participant_data)
        event.save()

def list_of_rece_for_tasks_emails(subject,message,role):
    parent_user=frappe.session.user
    receipients = set()
    teams = frappe.get_all('Team')
    for team in teams:
        team_doc = frappe.get_doc('Team', team.name)
        # Check the child table for the specified user and 'Sales Closure' role
        if any(member.user ==parent_user for member in team_doc.get('user_and_role')):
            for member in team_doc.get('user_and_role'):
                if member.role==role:
                    receipients.add(member.user)
    if receipients:
        frappe.sendmail(recipients=list(receipients),message=message,subject=subject)


# -----------------------------------------------doc events--------------------------------------------------------------

def after_save(doc,Method=None):
    if doc.subject.lower() == "welcome call":
        set_customer(doc)
        if doc.project_status=='Completed':
            doc.db_set("project_status", "Completed")
        else:
            doc.db_set("project_status", "In Progress")
            # doc.db_set("custom_assigned_group","Customer Success")
            # group="Customer Success"
            # doc_name=doc.name
            # assign(doc,group,doc_name)
            # Check if the document is being saved for the first time
            # frappe.msgprint("Document is not new.")
            # # Document is not new, so we can change the project status if needed
            # if doc.project_status != 'Completed' and doc.project_status != 'Cancelled' \
            #         and doc.project_status != 'Not Started' and doc.project_status != 'On Hold':
            #     doc.db_set("project_status", "In Progress")
            #     frappe.msgprint("Project status updated to 'In Progress'.")
            # else:
            #     frappe.msgprint("Project status remains unchanged.")
        # else:
        #     frappe.msgprint("Document is new.")
        #     # Document is new, so set the project status to "In Progress"
        #     doc.db_set("project_status", "In Progress")
        #     frappe.msgprint("Project status set to 'In Progress'.")


        if doc.briefed_about_contract_add_ons_ and doc.discuss_any_adds_on and doc.all_documents_collected_:
                pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                    
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Site Visit'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Site Visit','custom_project_stage':'Site Visit'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.custom_assigned_group="Project Managers"
                    # assign_task(doc,"Project Managers")
                    tsn.custom_assigned_group="Project Managers"
                    group="Project Managers"
                    doc_name=nm.name
                    status_changed = doc.has_value_changed("project_status")
                    if status_changed:
                        tsn.project_status="In Progress"
                        assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;

    if doc.subject.lower() == "site visit":
            set_customer(doc)
            if doc.site_visit_scheduled and doc.site_visit_completed and doc.pre_install_review_completed:
                    pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Engineering'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Engineering','custom_project_stage':'Engineering'})
                
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 4)
                        tsn.custom_assigned_group="Design Team"
                        status_changed = doc.has_value_changed("project_status")
                        doc_name=nm.name
                        group="Design Team"
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
                    
    if doc.subject.lower() == "engineering":
            set_customer(doc)
            if doc.complete_design_package and doc.pe_letter and doc.bom and doc.custom_enphase_account_setup:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Interconnection'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Interconnection,Structural Permitting,Electrical Permit','custom_project_stage':'Interconnection'})
                
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                        tsn.custom_assigned_group="Interconnection Team"
                        status_changed = doc.has_value_changed("project_status")
                        group="Interconnection Team"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
                        
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'STRUCTURAL PERMITTING'},fields=['*'])
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
                        tsn.custom_assigned_group="Permitting Team"
                        group="Permitting Team"
                        doc_name=nm.name
                        status_changed = doc.has_value_changed("project_status")
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
                    #section modify electrical permit   
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Electrical Permit'},fields=['*'])
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
                        tsn.custom_assigned_group="Permitting Team"
                        status_changed = doc.has_value_changed("project_status")
                        group="Permitting Team"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.") 
    if doc.subject.lower() == "structural permitting":
            set_customer(doc)
            if doc.submitted_for_permits and doc.permits_approved and doc.custom_work_permit_received:
                if doc.project_status=="Completed":
                    update_multiple_custom_stage(doc.project,'Structural Permitting')
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
    
    #modify thisline from strutural permitting to electrical permit
    if doc.subject.lower() == "electrical permit":
            set_customer(doc)
            if doc.submitted_for_permits and doc.permits_approved:
                if doc.project_status=="Completed":
                    pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
                
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                update_multiple_custom_stage(doc.project, 'Electrical Permit')
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Procurements'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Procurements','custom_project_stage':'Procurements'})
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 4)
                        tsn.custom_assigned_group="Procurement Team"
                        status_changed = doc.has_value_changed("project_status")
                        group="Procurement Team"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
                    
    if doc.subject.lower() == "procurements":
            set_customer(doc)
            if doc.solar_material_ordered and doc.electrical_material_ordered_aggrey:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Pre Install Work'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Pre Install Work,Installation Work','custom_project_stage':'Pre Install Work'})
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.custom_assigned_group="Project Managers"
                        status_changed = doc.has_value_changed("project_status")
                        group="Project Managers"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                            assign(doc,group,doc_name)
                        tsn.save()
                        break;
                        
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Installation Work'},fields=['*'])
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.custom_assigned_group="Project Managers"
                        status_changed = doc.has_value_changed("project_status")
                        group="Project Managers"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
        
        

    if doc.subject.lower() == "pre install work":
        set_customer(doc)
        # if (doc.schedule_pre_install_works and doc.pre_install_work_completeds) or doc.custom_pre_installed_not_required:
        #     if doc.schedule_pre_install_works or doc.pre_install_work_completeds and doc.custom_pre_installed_not_required:
        #         doc.db_set('project_status', 'In Progress')
        #         frappe.throw("Either you should complete sub task or not required pre install.")



        # ----comment
        # if doc.schedule_pre_install_works and doc.pre_install_work_completeds and not doc.custom_pre_installed_not_required:
        #     doc.db_set('project_status', 'Completed')
        #     update_multiple_custom_stage(doc.project,'Pre Install Work')
        # elif doc.custom_pre_installed_not_required and not doc.schedule_pre_install_works and not doc.pre_install_work_completeds:
        #     doc.db_set('project_status', 'Completed')
        #     update_multiple_custom_stage(doc.project,'Pre Install Work')
        # else:
        #     if doc.project_status=='Completed':
        #         frappe.throw('Task Status Should not be Completed !')
        # -----comment
                
            # if doc.schedule_pre_install_works and doc.pre_install_work_completeds:
            #     pass
            
            # else:
            #     if doc.project_status=="Completed":
            #         frappe.throw('Task Status Should not be Completed !')
                    
            
    if doc.subject.lower() == "installation work":
            set_customer(doc)
            if doc.installer_commissioning_performed and doc.schedule_installs and doc.solar_install_completed and doc.install_review_completed:
                update_multiple_custom_stage(doc.project,'Installation Work')
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Commissioning'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Commissioning','custom_project_stage':'Commissioning'})
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.custom_assigned_group="Design Team"
                        status_changed = doc.has_value_changed("project_status")
                        group="Design Team"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
            
    if doc.subject.lower() == "commissioning":
            set_customer(doc)
            if doc.erray_layout_created_as_part_of_commissioning and doc.barcodes_scanned:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'ELECTRICAL INSPECTION'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Electrical Inspection,Structural Inspection','custom_project_stage':'Electrical Inspection'})
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
                        tsn.custom_assigned_group="Project Managers"
                        status_changed = doc.has_value_changed("project_status")
                        group="Project Managers"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
                        
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Structural Inspection'},fields=['*'])
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
                        tsn.custom_assigned_group="Project Managers"
                        group="Project Managers"
                        doc_name=nm.name
                        status_changed = doc.has_value_changed("project_status")
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
        
    if doc.subject.lower() == "structural inspection":
            set_customer(doc)
            # -----comment----
            if doc.structural_inspection_scheduled and doc.structural_inspection_approved and not doc.custom_not_required:
                doc.db_set('project_status', 'Completed')
                update_multiple_custom_stage(doc.project,'Structural Inspection')
            elif doc.custom_not_required:
                if not doc.structural_inspection_scheduled and not doc.structural_inspection_approved:
                    doc.db_set('project_status', 'Completed')
                    update_multiple_custom_stage(doc.project,'Structural Inspection')
            else:
                if doc.project_status=='Completed':
                    frappe.throw('Task Status Should not be Completed !')


            # -------comment------
            # if doc.structural_inspection_scheduled and doc.structural_inspection_approved:
            #     pass
            # else:
            #     if doc.project_status=="Completed":
            #         frappe.throw('Task Status Should not be Completed !')
            if doc.project_status=="Completed":
                electrical_inspection=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Electrical Inspection'},fields=['*'])
                for si in electrical_inspection:
                    if si.project_status=='Completed':
                        ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Final submitted'},fields=['*'])
                        for nm in ts:
                            tsn=frappe.get_doc('Task',nm.name)
                            tsn.started_on = doc.completed_on
                            tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                            tsn.custom_assigned_group="Permitting Team"
                            group="Permitting Team"
                            doc_name=nm.name
                            status_changed = doc.has_value_changed("project_status")
                            if status_changed:
                                tsn.project_status="In Progress"
                                assign(doc,group,doc_name)
                            # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                            tsn.save()
                            break;
                    
                    
    if doc.subject.lower() == "electrical inspection":
            set_customer(doc)
            if doc.electrical_inspection_scheduled and doc.electrical_inspection_approved:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
                    
        # if doc.started_on and doc.expected_close_date:
            if doc.project_status=="Completed":
                update_multiple_custom_stage(doc.project,'Electrical Inspection')
                if doc.completed_on:
                    ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'PTO'},fields=['*'])
                    set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Structural Inspection,PTO','custom_project_stage':'PTO'})
                    for nm in ts:
                        tsn=frappe.get_doc('Task',nm.name)
                        tsn.started_on = doc.completed_on
                        tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                        tsn.custom_assigned_group="Interconnection Team"
                        status_changed = doc.has_value_changed("project_status")
                        group="Interconnection Team"
                        doc_name=nm.name
                        if status_changed:
                            tsn.project_status="In Progress"
                            assign(doc,group,doc_name)
                        # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                        tsn.save()
                        break;
                structural_inspection=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Structural Inspection'},fields=['*'])
                for si in structural_inspection:
                    if si.project_status=='Completed':
                        ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Final submitted'},fields=['*'])
                        for nm in ts:
                            tsn=frappe.get_doc('Task',nm.name)
                            tsn.started_on = doc.completed_on
                            tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                            tsn.custom_assigned_group="Permitting Team"
                            group="Permitting Team"
                            doc_name=nm.name
                            status_changed = doc.has_value_changed("project_status")
                            if status_changed:
                                tsn.project_status="In Progress"
                                assign(doc,group,doc_name)
                            # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                            tsn.save()
                            break;
                        
    # if doc.subject.lower() == "pto":
    #     # if doc.started_on and doc.expected_close_date:
    #         if doc.project_status=="Completed":
    #             if doc.completed_on:
    #                 ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'ELECTRICAL PERMIT'},fields=['*'])
    #                 for nm in ts:
    #                     tsn=frappe.get_doc('Task',nm.name)
    #                     tsn.started_on = doc.completed_on
    #                     tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
    #                     # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
    #                     tsn.save()
    #                     break;
                        
                        
                        
                        
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
            
    if doc.subject.lower() == "pto":
            set_customer(doc)
            if doc.pto_submitted and doc.pto_approved:
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Final Submitted','custom_project_stage':'Final Submitted'})
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
    
    if doc.subject.lower() == "interconnection":
            set_customer(doc)
            if doc.submitted_for_interconnection and doc.interconnection_received:
                if doc.project_status=="Completed":
                    update_multiple_custom_stage(doc.project,'Interconnection')
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')

    if doc.subject.lower() == "installation work":
            set_customer(doc)
            if doc.installer_commissioning_performed and doc.schedule_installs and doc.solar_install_completed and doc.install_review_completed:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
                    
    # if doc.subject.lower() == "structural inspection":
    #         set_customer(doc)
    #         if doc.structural_inspection_scheduled and doc.structural_inspection_approved:
    #             update_multiple_custom_stage(doc.project,'Structural Inspection')
    #         else:
    #             if doc.project_status=="Completed":
    #                 frappe.throw('Task Status Should not be Completed !')

    if doc.subject.lower() == "final submitted":
            set_customer(doc)
            if doc.final_signed_off_submitted and doc.final_off_received:
                pass
            else:
                if doc.project_status=="Completed":
                    frappe.throw('Task Status Should not be Completed !')
            if doc.project_status=="Completed":
                cur_date=frappe.utils.getdate()
                completed_by=frappe.db.get_value('User',frappe.session.user,'full_name')
                frappe.db.set_value('Project',doc.project,{'project_status':'Completed','custom_actual_close_date':cur_date})
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Final Submitted','custom_project_stage':'Final Submitted'})
                    
    # ------------------------------create events for task on schedule on -------------------------------------

    subjects_to_check = [
        'Site Visit',
        'procurements',
        'Pre Install Work',
        'Installation Work',
        'Electrical Inspection',
        'Structural Inspection'
    ]

    if doc.custom_scheduled_on:
        for subject in subjects_to_check:
            if doc.subject == subject:
                schedule_task=subject
                date_changed = doc.has_value_changed("custom_scheduled_on")
                if date_changed:
                    cur_date = doc.custom_scheduled_on
                    formatted_date = frappe.utils.format_datetime(cur_date, "MMMM dd yyyy")
                    create_event_with_participants(doc, cur_date, formatted_date,schedule_task)
                    break  # If you only want to process the first matching condition

    

    

# ------------before save event------------
def before_save(doc,Method=None):
    if doc.custom_customer_name:
        doc.custom_task_title = doc.subject + "\n" + doc.custom_customer_name

# ------------------before validate event-----------
def before_validate(doc,method=None):
    doc.db_set("custom_task_priority",doc.task_priority)
    if doc.project_status=='Completed':
        name=frappe.db.get_value('User',frappe.session.user,'full_name')
        doc.db_set('completed_by',frappe.session.user)
        doc.db_set('custom_name_completed_by',name)
        # frappe.throw(f"{frappe.utils.getdate()}")
        doc.db_set('completed_on',frappe.utils.getdate())

    if doc.has_value_changed('project_status'):
    # if "s"=="p":
        # frappe.throw("ppp")
        if doc.project_status=="In Progress" and doc.subject=="Site Visit":
            subject='Requires a Site Visit'
            message=f'''<p>Hello,</p>
            <h3>Project Managers,</h3>
            A new project won and requires a Site Visit. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Project Managers')

        if doc.project_status=="In Progress" and doc.subject=="Engineering":
            subject='Requires an Engineering Design'
            message=f'''<p>Hello,</p>
                        <h3>Design Team,</h3>
                        A new project won and requires an Engineering Design. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Design Team')

        if doc.project_status=="In Progress" and doc.subject=="Interconnection":
            subject='Requires an Interconnection'
            message=f'''<p>Hello,</p>
                        <h3>Interconnection Team,</h3>
                        A new project won and requires an Interconnection. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Interconnection Team')

        if doc.project_status=="In Progress" and doc.subject=="Structural Permitting":
            subject='Requires Permitting'
            message=f'''<p>Hello,</p>
                        <h3>Permitting Team,</h3>
                        A new project won and requires Permitting. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.project}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Permitting Team')

        if doc.project_status=="In Progress" and doc.subject=="Electrical Permit":
            subject='Requires Electrical Permit'
            message=f'''<p>Hello,</p>
                        <h3>Permitting Team,</h3>
                        A new project won and requires an Electrical Permit. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Permitting Team')

        if doc.project_status=="In Progress" and doc.subject=="Procurements":
            subject='Requires a Procurement'
            message=f'''<p>Hello,</p>
                        <h3>Procurement Team,</h3>
                        A new project won and requires a Procurement. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Procurement Team')

        if doc.project_status=="In Progress" and doc.subject=="Pre Install Work":
            subject='Requires Pre Install Works'
            message=f'''<p>Hello,</p>
                        <h3>Project Managers,</h3>
                        A new project won and requires Pre Install Works. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Project Managers')

        if doc.project_status=="In Progress" and doc.subject=="Installation Work":
            subject='Requires an Installation'
            message=f'''<p>Hello,</p>
                        <h3>Project Managers,</h3>
                        A new project won and requires an Installation. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Project Managers')

        if doc.project_status=="In Progress" and doc.subject=="Commissioning":
            subject='Requires Commissioning'
            message=f'''<p>Hello,</p>
                        <h3>Design Team,</h3>
                        A new project won and requires commissioning. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Design Team')

        if doc.project_status=="In Progress" and doc.subject=="Electrical Inspection":
            subject='Requires an Electrical Inspection'
            message=f'''<p>Hello,</p>
                    <h3>Project Managers,</h3>
                    A new project won and requires an Electrical Inspection. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Project Managers')

        if doc.project_status=="In Progress" and doc.subject=="Structural Inspection":
            subject='Requires a Structural Inspection'
            message=f'''<p>Hello,</p>
                        <h3>Project Managers,</h3>
                        A new project won and requires a Structural Inspection. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Project Managers')

        if doc.project_status=="In Progress" and doc.subject=="PTO":
            subject='Requires an PTO'
            message=f'''<p>Hello,</p>
                        <h3>Interconnection team,</h3>
                        A new project won and requires an PTO. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Interconnection Team')

        if doc.project_status=="In Progress" and doc.subject=="PTO":
            subject='Requires an PTO'
            message=f'''<p>Hello,</p>
                        <h3>Interconnection team,</h3>
                        A new project won and requires an PTO. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc.project}">{doc.custom_customer_name}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Interconnection Team')

        if doc.project_status=="In Progress" and doc.subject=="Final submitted":
            subject='Requires a final submission'
            message=f'''<p>Hello,</p>
                        <h3>Permitting team,</h3>
                        A new project won and requires a final submission. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{{ doc.project }}">{{ doc.custom_customer_name }}</a>'''
            list_of_rece_for_tasks_emails(subject,message,'Permitting Team')
    
    
    



    
# ----------------after_insert event-------------\
def after_insert(doc,Method=None):
    if doc.subject.lower() == "welcome call":
        doc.db_set("custom_assigned_group","Customer Success")
        group="Customer Success"
        doc_name=doc.name
        assign(doc,group,doc_name)
        
        user_group=frappe.db.get_all("User Group Member",filters={'parent':group},fields={'*'})
        if user_group:
            receiver=[]
            for i in user_group:
                receiver.append(i.user)
                html_ccontent=f'''<p>Hello,</p>
                            <h3>Customer Success Team,</h3>
                            A new project won and requires a welcome call. Here is the link to the project:<a href="https://erp.solarblocks.us/app/project/{doc_name}">{doc.custom_customer_name}</a>'''
                frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Requires a welcome call")
                # frappe.msgprint(f"Email sent for Welcome call")
                    
# ---------------before insert event---------------
def before_insert(doc,method=None):
    if doc.subject.lower() == "welcome call":
        doc.started_on = frappe.utils.nowdate()
        doc.expected_close_date = frappe.utils.add_days(doc.started_on, 2)
        doc.scheduled_on = frappe.utils.add_days(doc.started_on, 2)
    
    
	
    