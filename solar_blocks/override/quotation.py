import frappe

def update_quotation_created_status_in_opportunity(doc, method=None):
    get_opp=frappe.db.get_all("Opportunity",filters={'name':doc.opportunity},fields={'*'})
    for i in get_opp:
        get_doc_opp=frappe.get_doc("Opportunity",i.name)
        get_doc_opp.proposal_sub_status="Quotation Sent"
        get_doc_opp.save()

def update_quotation_status_in_opportunity(doc, method=None):
    get_opp=frappe.db.get_all("Opportunity",filters={'party_name':doc.party_name},fields={'*'})
    for i in get_opp:
        get_doc_opp=frappe.get_doc("Opportunity",i.name)
        get_doc_opp.proposal_sub_status="Quotation Approved"
        get_doc_opp.save()