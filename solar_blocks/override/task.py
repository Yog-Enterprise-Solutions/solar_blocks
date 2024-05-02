import frappe

def require_a_call(doc,method=None):
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
                            A new project won and requires a welcome call. Here is the link to the project:<a href="https://myerp.solarblocks.us/app/project/{doc_name}">{doc_name}</a>'''
                frappe.sendmail(recipients=receiver,message=html_ccontent,subject="Requires a welcome call")
                # frappe.msgprint(f"Email sent for Welcome call")
                    
def task_before_save(doc,method=None):
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

    if doc.subject.lower() == "welcome call":
        # # if doc.get("__islocal"):
        # frappe.msgprint(f"{doc.project_status}")
        if doc.project_status=='Completed':
            doc.db_set("project_status", "Completed")
        # elif doc.project_status=='Not Started':
        #     doc.db_set("project_status", "Not Started")
        # elif doc.project_status=='On Hold':
        #     doc.db_set("project_status", "On Hold")
        # elif doc.project_status=='Cancelled':
        #     doc.db_set("project_status", "Cancelled")
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
            set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Site Visit'})
            for nm in ts:
                tsn=frappe.get_doc('Task',nm.name)
                tsn.started_on = doc.completed_on
                tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                tsn.custom_assigned_group="Project Managers"
                # assign_task(doc,"Project Managers")
                tsn.custom_assigned_group="Project Managers"
                tsn.project_status="In Progress"
                group="Project Managers"
                doc_name=nm.name
                assign(doc,group,doc_name)
                # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                tsn.save()
                break;        
    
    if doc.subject.lower() == "site visit":
        if doc.site_visit_scheduled and doc.site_visit_completed and doc.pre_install_review_completed:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
            
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Engineering'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Engineering'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 4)
                    tsn.custom_assigned_group="Design Team"
                    tsn.project_status="In Progress"
                    group="Design Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")

    if doc.subject.lower() == "engineering":
        if doc.complete_design_package and doc.pe_letter and doc.bom:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Interconnection'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Interconnection'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                    tsn.custom_assigned_group="Interconnection Team"
                    tsn.project_status="In Progress"
                    group="Interconnection Team"
                    doc_name=nm.name
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
                    tsn.project_status="In Progress"
                    group="Permitting Team"
                    doc_name=nm.name
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
                    tsn.project_status="In Progress"
                    group="Permitting Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.") 
    
    if doc.subject.lower() == "engineering":
        if doc.complete_design_package and doc.pe_letter and doc.bom:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Interconnection'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Interconnection'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                    tsn.custom_assigned_group="Interconnection Team"
                    tsn.project_status="In Progress"
                    group="Interconnection Team"
                    doc_name=nm.name
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
                    tsn.project_status="In Progress"
                    group="Permitting Team"
                    doc_name=nm.name
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
                    tsn.project_status="In Progress"
                    group="Permitting Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.") 
    
    if doc.subject.lower() == "structural permitting":
        if doc.submitted_for_permits and doc.permits_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
    
    if doc.subject.lower() == "electrical permit":
        if doc.submitted_for_permits and doc.permits_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
            
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Procurements'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Procurements'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 4)
                    tsn.custom_assigned_group="Procurement Team"
                    tsn.project_status="In Progress"
                    group="Procurement Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
    
    if doc.subject.lower() == "procurements":
        if doc.solar_material_ordered and doc.electrical_material_ordered_aggrey:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Pre Install Work'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Pre Install Work'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.custom_assigned_group="Project Managers"
                    tsn.project_status="In Progress"
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    group="Project Managers"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    tsn.save()
                    break;
                    
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Installation Work'},fields=['*'])
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.custom_assigned_group="Project Managers"
                    tsn.project_status="In Progress"
                    group="Project Managers"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
    
    if doc.subject.lower() == "pre install work":
        if doc.schedule_pre_install_works and doc.pre_install_work_completeds:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')

    if doc.subject.lower() == "installation work":
        if doc.installer_commissioning_performed and doc.schedule_installs and doc.solar_install_completed and doc.install_review_completed:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Commissioning'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'Commissioning'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.custom_assigned_group="Design Team"
                    tsn.project_status="In Progress"
                    group="Design Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
    
    if doc.subject.lower() == "commissioning":
        if doc.erray_layout_created_as_part_of_commissioning and doc.barcodes_scanned:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'ELECTRICAL INSPECTION'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'ELECTRICAL INSPECTION'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 14)
                    tsn.custom_assigned_group="Project Managers"
                    tsn.project_status="In Progress"
                    group="Project Managers"
                    doc_name=nm.name
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
                    tsn.project_status="In Progress"
                    group="Project Managers"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
        # else:
        #     frappe.throw("Please Complete Previous Tasks.")
    
    if doc.subject.lower() == "electrical inspection":
        if doc.electrical_inspection_scheduled and doc.electrical_inspection_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
    
    if doc.subject.lower() == "structural inspection":
        if doc.structural_inspection_scheduled and doc.structural_inspection_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
                
    # if doc.started_on and doc.expected_close_date:
        if doc.project_status=="Completed":
            if doc.completed_on:
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'PTO'},fields=['*'])
                set_custom_stage_in_project=frappe.db.set_value('Project',doc.project,{'custom_stage':'PTO'})
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                    tsn.custom_assigned_group="Interconnection Team"
                    tsn.project_status="In Progress"
                    group="Interconnection Team"
                    doc_name=nm.name
                    assign(doc,group,doc_name)
                    # tsn.scheduled_on = frappe.utils.add_days(tsn.started_on, 2)
                    tsn.save()
                    break;
                    
                ts=frappe.db.get_list('Task',filters={'project':doc.project,'subject':'Final submitted'},fields=['*'])
                for nm in ts:
                    tsn=frappe.get_doc('Task',nm.name)
                    tsn.started_on = doc.completed_on
                    tsn.expected_close_date = frappe.utils.add_days(tsn.started_on, 7)
                    tsn.custom_assigned_group="Permitting Team"
                    tsn.project_status="In Progress"
                    group="Permitting Team"
                    doc_name=nm.name
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
        if doc.pto_submitted and doc.pto_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
    
    if doc.subject.lower() == "interconnection":
        if doc.submitted_for_interconnection and doc.interconnection_received:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')

    if doc.subject.lower() == "installation work":
        if doc.installer_commissioning_performed and doc.schedule_installs and doc.solar_install_completed and doc.install_review_completed:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')

    if doc.subject.lower() == "structural inspection":
        if doc.structural_inspection_scheduled and doc.structural_inspection_approved:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
    
    if doc.subject.lower() == "final submitted":
        if doc.final_signed_off_submitted and doc.final_off_received:
            pass
        else:
            if doc.project_status=="Completed":
                frappe.throw('Task Status Should not be Completed !')
        if doc.project_status=="Completed":
            cur_date=frappe.utils.getdate()
            frappe.db.set_value('Project',doc.project,{'project_status':'Completed','custom_actual_close_date':cur_date})
    
    def get_project_stage(doc):
        res = frappe.db.sql("""SELECT subject from `tabTask` 
                    WHERE project = %(p_name)s and project_status = "In Progress" 
                    ORDER BY task_priority
                    LIMIT 1
                    """,({"p_name":doc.project}))[0][0]
        return res
    
    # if doc.project:
    #     if doc.project_status == "In Progress":
    #         stage = get_project_stage(doc)
    #         frappe.db.set_value("Project",doc.project,"custom_stage",stage) 
    #     if doc.project_status == "Completed":
    #         # status update,
    #         next_pr = doc.custom_task_priority + 1
    #         query = f""" SELECT name from `tabTask`  
    #                 WHERE project = '{doc.project}' and project_status = "Not Started" and custom_task_priority = {next_pr}
    #                 ORDER BY custom_task_priority;
    #             """
    #         names = frappe.db.sql(query)
    #         frappe.msgprint(f"{names}")
    #         for name in names:
    #             frappe.db.set_value("Task", name[0], "project_status", "In Progress")
    #         stage = get_project_stage(doc)
    #         frappe.db.set_value("Project",doc.project,"custom_stage",stage) 

    # custom_stage=frappe.db.get_value('Project',doc.project, 'custom_stage')
    # if custom_stage==doc.subject:
    #     doc.db_set("project_status","In Progress")

def assign_task(doc,method=None):
    if doc.project_status=='Completed':
        user_group=frappe.db.get_all("User Group Member",filters={'parent':doc.custom_assigned_group},fields={'*'})
        for i in user_group:
            todo = frappe.new_doc('ToDo')
            todo.allocated_to = i.user
            todo.reference_type = "Task"
            todo.reference_name = doc.name
            todo.description = "Assign"
            todo.insert(ignore_permissions=True)
            
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

def set_task_priority(doc,method=None):
    doc.db_set("custom_task_priority",doc.task_priority)

def task_dates_update(doc, method=None):
    if doc.subject.lower() == "welcome call":
        doc.started_on = frappe.utils.nowdate()
        doc.expected_close_date = frappe.utils.add_days(doc.started_on, 2)
        doc.scheduled_on = frappe.utils.add_days(doc.started_on, 2)