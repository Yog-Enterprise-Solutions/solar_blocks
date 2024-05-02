import frappe

@frappe.whitelist(allow_guest=True)
def assign_and_share_from_opportunity():
    request_data = frappe.form_dict
    assign_to_user_group = request_data.get('assign_to_user_group')
    name=  request_data.get('name')
    user_group=frappe.db.get_all("User Group Member",filters={'parent':assign_to_user_group},fields={'*'})

    for i in user_group:
        check_todo=frappe.db.get_all("ToDo",filters={'allocated_to':i.user,"reference_type":"Opportunity",'reference_name':name},fields={'*'})
        if len(check_todo)==0:
            todo = frappe.new_doc('ToDo')
            todo.allocated_to = i.user
            todo.reference_type = "Opportunity"
            todo.reference_name = name
            todo.description = "Assign"
            todo.insert(ignore_permissions=True)
    

        check_share=frappe.db.get_all("DocShare",filters={'user':i.user,"share_doctype":"Opportunity",'share_name':name},fields={'*'})
        if len(check_share)==0:
            share = frappe.new_doc('DocShare')
            share.user = i.user
            share.share_doctype = "Opportunity"
            share.share_name = name
            share.read = 1
            share.write=1
            share.notify_by_email=1
            share.insert(ignore_permissions=True)
        
        # else:
            # frappe.msgprint("Opportunity is Assigned to User")

# @frappe.whitelist(allow_guest=True)
# def api_webhook_call():
#     try:
#         raw_data = frappe.request.get_data()
#         if raw_data:
#             data = json.loads(raw_data.decode('utf-8'))
#             r_id = data["requests"]["request_id"]
#             access_token = data["requests"]["request_name"]
            
#             tmp=str(access_token)
#             access_token=(tmp.split('-'))[1]
#             r_name=(tmp.split('-'))[0]
            
#             cont = frappe.get_doc({
#             'doctype':'Contracts',
#             'add_url_attachment':str(r_id)+'    '+str(access_token)+'    '+str(r_name)
            
#             })
#             cont.insert(ignore_permissions = True)
#             url = "https://sign.zoho.in/api/v1/requests/"+str(r_id)+"/pdf"

#             payload = {}
#             headers = {
#             'Authorization': 'Zoho-oauthtoken '+str(access_token),
#             'Cookie': 'JSESSIONID=A221662ED0807CBBB998DDF83A0C55B7; _zcsr_tmp=b1ed60e9-39f1-4495-b069-8db74a9072d7; c61ac045a3=6b9cee97758e3400a29d7e000f9fb33f; zscsrfcookie=b1ed60e9-39f1-4495-b069-8db74a9072d7'
#             }

#             response = requests.request("GET", url, headers=headers, data=payload)
#             # contract=frappe.get_doc('Contracts',r_name)
#             # contract.add_url_attachment=str(response)
#             # contract.save()
#             # contract.add_attachment=response
#             # contract.save()

#     except Exception as e:
#         frappe.log_error(e,'e')

# @frappe.whitelist(allow_guest=True)
# def doc_submission_mail():
#     request_data = frappe.form_dict
#     email_id = request_data.get('email_id')
#     url = request_data.get('url')
#     frappe.sendmail(
#             recipients= email_id,
#             subject="Add Signature",
#             message = f"Please Sign the Contract {url} "
#     )

@frappe.whitelist(allow_guest=True)
def update_site_visit_status_on_opportunity():
    d=frappe.form_dict
    get_opp=frappe.db.get_all("Opportunity",filters={'name':d.opportunity},fields={'*'})
    for i in get_opp:
        get_doc_opp=frappe.get_doc("Opportunity",i.name)
        get_doc_opp.site_visit="Done"
        get_doc_opp.visit_date=d.visit_date
        get_doc_opp.visit_time=d.visit_time
        
        get_doc_opp.save()

@frappe.whitelist(allow_guest=True)
def update_contract_status_on_opportunity():
    d=frappe.form_dict
    get_opp=frappe.db.get_all("Opportunity",filters={'name':d.opportunity},fields={'*'})
    for i in get_opp:
        get_doc_opp=frappe.get_doc("Opportunity",i.name)
        get_doc_opp.opportunity_status="Contract Signed"
        get_doc_opp.save()    

@frappe.whitelist(allow_guest=True)
def get_data_from_user_group():
    d=frappe.form_dict
    user_group=frappe.db.get_all("User Group Member",filters={'parent':d.assign_to_user_group},fields={'*'})
    frappe.response['message']=user_group

@frappe.whitelist(allow_guest=True)
def check_task_priority():
    d=frappe.form_dict

    get_task_list=frappe.db.get_list("Task",filters={'project':d.project,'task_priority':d.prev_task})
    # if len(get_task_list)>0:
    get_task_doc=frappe.get_doc("Task",get_task_list[0]['name'])
    if get_task_doc.status == 'Completed':
        frappe.response['message']= 'Completed'
    else:
        frappe.response['message']='Not Completed'