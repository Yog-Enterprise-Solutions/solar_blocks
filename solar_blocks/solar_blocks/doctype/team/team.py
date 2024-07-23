# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Team(Document):
	pass

# Server script for assigning roles to users based on entries in the child table

def assign_roles_to_users(doc, method):
	for user_role in doc.user_and_role:
		user = user_role.user
		role = user_role.role
		
		# Check if the user exists
		if not frappe.db.exists("User", user):
			frappe.throw(f"User {user} does not exist.")
		
		# Check if the role exists
		if not frappe.db.exists("Role", role):
			frappe.throw(f"Role {role} does not exist.")
		
		# Assign the role to the user
		user_doc = frappe.get_doc("User", user)
		if role not in [r.role for r in user_doc.roles]:
			user_doc.append("roles", {"role": role})
			user_doc.save()
			frappe.msgprint(f"Assigned role {role} to user {user}")


