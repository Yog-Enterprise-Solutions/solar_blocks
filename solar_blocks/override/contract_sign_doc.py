import frappe

def set_value_in_contract(doc,method=None):
    cont=frappe.get_all("Contracts",filters={'name':doc.name},fields={'*'})
    if len(cont)>0:
        con_doc=frappe.get_doc("Contracts",cont[0]['name'])
        con_doc.signee_company=doc.customer_sign
        con_doc.customer2_signature=doc.primary_customer_sign
        con_doc.status="Signed"
        con_doc.save()

    email_id = doc.email
    url="https://solarblocks.onehash.is/api/method/frappe.utils.print_format.download_pdf?doctype=Contracts&name="+doc.name+"&format=Sample%20Solar%20Agreement&no_letterhead=0&letterhead=Solar%20Block&settings=%7B%7D&_lang=en"
    frappe.sendmail(
            recipients= email_id,
            subject="Signed Contract",
            message = f"Please see your Contract PDF {url} "
    )
