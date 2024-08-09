import frappe


def create_event_with_participants(doc,subject,date):
    exist_event = frappe.db.exists("Event",{'subject':subject}, {"name": ("in", frappe.get_all("Event Participants", filters={"email":doc.email}, pluck="parent"))})
    # if exist_event:
    #     frappe.msgprint(f"existl")
    if not exist_event:
        event = frappe.new_doc("Event")
        event.subject = subject  
        event.starts_on = date
        event.sync_with_google_calendar = 1
        # event.ends_on=frappe.utils.get_datetime('05-15-2024 03:00:21')
        event.google_calendar = "erp calendar"
        participants = [{"reference_doctype": "Lead", "reference_docname": doc.name, "email": doc.email}]
        
        parent_user=frappe.session.user
        receipients = set()
        team_doc = frappe.get_doc('Team',doc.custom_assign_team)
        # Check the child table for the specified user and 'Sales Closure' role
        if any(member.user ==parent_user for member in team_doc.get('user_and_role')):
            for member in team_doc.get('user_and_role'):
                if member.role=='Sales Closure':
                    receipients.add(member.user)
        for email in list(receipients):
            participants.append({"reference_doctype": "Lead", "reference_docname": doc.name, "email": email})
        for participant_data in participants:
            event_participant = event.append('event_participants', participant_data)
        event.save()


def assign_permissions(doc,doctype_name):
    if not doc.custom_assign_team:
        return

    team_doc = frappe.get_doc("Team",doc.custom_assign_team)

    if not team_doc:
        frappe.throw(f"Team {team} not found")

     # Get all share records for the document
    shares = frappe.get_all('DocShare', filters={
        'share_doctype': doctype_name,
        'share_name': doc.name
    }, fields=['name'])

    # Loop through each share and delete it
    for share in shares:
        frappe.delete_doc('DocShare', share['name'])

    #share documnet with user
    for user_role in team_doc.user_and_role:
        user = user_role.user
        if not user:
            continue

        # Check if the permission already exists
        # if not frappe.db.exists("User Permission", {"user": user, "allow": doctype_name, "for_value": doc.name}):
        #     # Create user permission for this user
        #     user_permission = frappe.new_doc("User Permission")
        #     user_permission.user = user
        #     user_permission.allow = doctype_name
        #     user_permission.for_value = doc.name
        #     user_permission.insert(ignore_permissions=True)
        #     frappe.msgprint(f"User Permission created for user {user} on {doctype_name} {doc.name}")
        if not frappe.db.exists('DocShare',{'user':user,'share_name':doc.name}):
            share = frappe.new_doc('DocShare')
            share.user =user
            share.share_doctype =doctype_name
            share.share_name =doc.name
            share.read = 1
            share.write = 1
            share.notify_by_email = 1
            share.insert(ignore_permissions=True)
        


    


def after_save(doc,method=None):
    if doc.lead_sub_status=='Appointment Setup' and not doc.custom_appointment_status:
        # frappe.msgprint(f"nahi")
        cur_date=doc.custom_call_date_and_time
        formatted_date=frappe.utils.format_datetime(cur_date, "MMMM dd yyyy")
        subject=f"Congratulations!!! {doc.first_name} {doc.last_name} at {doc.street} - Your Appointment is set for {formatted_date}"
        create_event_with_participants(doc,subject,cur_date)
        
    if doc.custom_appointment_status=='Rescheduled':
        date=doc.custom_call_date_and_time
        formatted_date=frappe.utils.format_datetime(date, "MMMM dd yyyy")
        subject=f"Congratulations!!! {doc.first_name} {doc.last_name} at {doc.street} - appointment is rescheduled for {formatted_date}"
        create_event_with_participants(doc,subject,date)
    if doc.lead_sub_status=='Call at later Date':
        cur_date=doc.reminder_date1
        subject=f"Reminder to call {doc.first_name} {doc.last_name} at {doc.street}."
        create_event_with_participants(doc,subject,cur_date)

    #set user permissin for team
    if doc.has_value_changed("custom_assign_team"):
        assign_permissions(doc,'Lead')

    # Image uploader email
    if doc.has_value_changed("custom_pre_install_status"):
        if doc.custom_pre_install_status=='Assessment completed - Site Assessor':
            message=f'''<p>Hey team,</p>
                        <p>Site Assessment has been completed.<p>
                        <p>Please review all the pictures and let me know if anything is missing.<p>
                        <p>Thanks<p>'''
            parent_user = frappe.session.user
            recipients = set()

            team_doc = frappe.get_doc('Team',doc.custom_assign_team)
            parent_user_in_team = False
            for member in team_doc.get('user_and_role'):
                if member.user == parent_user:
                    parent_user_in_team = True
                    break

            if parent_user_in_team:
                for member in team_doc.get('user_and_role'):
                    if member.role =='Design Team':
                        recipients.add(member.user)
            if receipients:
                frappe.sendmail(recipients=list(recipients),message=message,subject="Site Assessment has been completed.")

    if doc.has_value_changed("custom_post_install_status"):
        if doc.custom_post_install_status=='Assessment completed - Site Assessor':
            message=f'''<p>Hey team,</p>
                        <p>Installtion has been completed.<p>
                        <p>Please review all the pictures and let me know if anything is missing.<p>
                        <p>Thanks<p>'''
            parent_user = frappe.session.user
            recipients = set()

            team_doc = frappe.get_doc('Team',doc.custom_assign_team)
            parent_user_in_team = False
            for member in team_doc.get('user_and_role'):
                if member.user == parent_user:
                    parent_user_in_team = True
                    break

            if parent_user_in_team:
                for member in team_doc.get('user_and_role'):
                    if member.role =='Design Team':
                        recipients.add(member.user)
            if receipients:
                frappe.sendmail(recipients=list(recipients),message=message,subject="Installation has been completed.")


def enqueue_create_document_template(doc, method):
    full_name=frappe.db.get_value('User',frappe.session.user,'full_name')
    doc.db_set('custom_leads_owner',full_name)
    #create document template
    list_of_documents = [

        "IC Letter",
        "PTO Letter",
        "DOB Approved Plans",
        "Structural Pass Certificate",
        "DOB Work Permit",
        "Electrical Pass Certificate",
        "Electrical Work Permit",
        "Signed Contract",
        "ACP5",
        "Property Survey",
        "Property Deed / Property Tax",
        "Utility Bill",
        "Planset",
        "Electrical Plans",
        "PE Letter",
        "PIL Letter",
        "Shade Report",
        "Asbuilt Planset",
        "Asbuilt Electrical Plan"
    ]
    for i in list_of_documents:
        doc.append("custom_document_attachments", 
        {'name1':i})
    for j in ["Proposal 1","Proposal 2","Proposal 3"]:
        doc.append("custom_proposals", 
        {'name1':j})
    # frappe.enqueue(create_document_template,queue="long", doc=doc)














  
    






    

    
    
    
    
    

    
    
    
   





