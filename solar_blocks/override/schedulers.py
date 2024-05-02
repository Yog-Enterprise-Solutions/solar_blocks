import frappe

def opp_auto_disqualified_in_case_of_meeting_and_appointment():
    d=frappe.form_dict
    current_date = frappe.utils.nowdate()
    current_dates=frappe.utils.getdate(current_date)

    # Auto disqualify lead in 4 weeks
    opp_data = frappe.get_all('Opportunity', fields=['*'])
    for i in opp_data:
        doc=frappe.get_doc("Opportunity",i.name)
        meeting_date=i.meeting_date
        date_and_time_of_appoinment=i.date_and_time_of_appoinment
        slice_date1=0
        slice_date2=0
        if(meeting_date):
            only_date1=frappe.utils.getdate(meeting_date)
            date_diff1=current_dates-only_date1
            slice_date1=str(date_diff1)[:1]
        if(date_and_time_of_appoinment):
            only_date2=frappe.utils.getdate(date_and_time_of_appoinment)
            date_diff2=current_dates-only_date2
            slice_date2=str(date_diff2)[:1]
        
        if((slice_date1=="28" and (i.meeting_done=="No" or i.meeting_done=="") and i.action_performed=="Meeting and Negotiation" and i.opportunity_status=="Maxfit Completed") or (i.opportunity_status=="Maxfit Completed" and i.action_performed=="Schedule Appointment" and slice_date2=="28")):
            doc.opportunity_status="Client Disqualified"
            doc.save()
            
            
def auto_disqualified_lead_in_4_weeks():
    d=frappe.form_dict
    current_date = frappe.utils.nowdate()
    current_dates=frappe.utils.getdate(current_date)

    # Auto disqualify lead in 4 weeks
    lead_data = frappe.get_all('Lead', fields=['*'])
    for i in lead_data:
        doc=frappe.get_doc("Lead",i.name)
        pending_info_date=i.pending_info_date
        tried_to_call=i.tried_to_call
        slice_date1=0
        slice_date2=0
        if(pending_info_date):
            date_diff1=current_dates-pending_info_date
            slice_date1=str(date_diff1)[:1]
        if(tried_to_call):
            date_diff2=current_dates-tried_to_call
            slice_date2=str(date_diff2)[:1]
        
        if((slice_date1=="0" and doc.lead_sub_status=="Pending additional information" and doc.lead_status=="Lead" ) or (slice_date1=="28" and doc.lead_sub_status=="Tried to Call & no response") and doc.lead_status=="Lead"):
            doc.lead_status="Client Disqualified"
            doc.save()
            
