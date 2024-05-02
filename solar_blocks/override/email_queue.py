import frappe

def email_send(doc,method=None):
    if doc.status=="Not Sent":
        record = frappe.get_doc('Email Queue',doc.name)
        if record:
            record.check_permission()
            record.send()