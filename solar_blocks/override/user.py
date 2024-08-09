import frappe

def assign_raven_user_role_remove_modules(doc,Method=None):
    doc.append("roles", {"role": 'Raven User'})
    doc.module_profile='No Module'