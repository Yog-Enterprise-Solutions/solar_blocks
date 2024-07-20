def create_event_with_participants(doc,subject,date):
    # if doc.lead_sub_status!='Convert to Opportunity':
    # frappe.msgprint(f"yessss")
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
        user_group_members = frappe.db.get_all("User Group Member", filters={'parent': doc.assign_user_groups}, fields={'user'})
        for user_group_member in user_group_members:
            email = user_group_member.user
            participants.append({"reference_doctype": "Lead", "reference_docname": doc.name, "email": email})
        for participant_data in participants:
            event_participant = event.append('event_participants', participant_data)
        event.save()



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
    
    
    

    
    
    
    
    

    
    
    
   





