import frappe

def error_log_fix(doc, method=None):
    if doc.seen==0 or doc.status=="Not Seen":
        record = frappe.get_doc('Error Log',doc.name)
        if record:
            doc_status=0
            doc.seen=1