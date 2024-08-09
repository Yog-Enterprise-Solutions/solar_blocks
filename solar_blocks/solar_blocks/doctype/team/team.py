# Copyright (c) 2024, yes@tranqwality.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Team(Document):

# Server script for assigning roles to users based on entries in the child table

	def validate(doc,method=None):
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


	def on_update(doc, method=None):
		lead_list = frappe.db.get_list('Lead', filters={'custom_assign_team': doc.name}, fields=['name'])
		opp_list = frappe.db.get_list('Opportunity', filters={'custom_assign_team': doc.name}, fields=['name'])
		pro_list = frappe.db.get_list('Project', filters={'custom_assign_team': doc.name}, fields=['name'])

		share_doc_with_users(doc, 'Lead', lead_list)
		share_doc_with_users(doc, 'Opportunity', opp_list)
		share_doc_with_users(doc, 'Project', pro_list)


# --------------remove share permission of document if user remove from team--------------------
		old_doc = doc.get_doc_before_save()
		old_child_tab=old_doc.user_and_role
		new_child_tab=doc.user_and_role
		# Extract user lists from both child tables
		old_users = {d.user for d in old_child_tab}
		new_users = {d.user for d in new_child_tab}

		# Find users who are in the old list but not in the new list
		removed_users = old_users - new_users

		# Convert the set back to a list if needed
		removed_users_list = list(removed_users)
		lead_list = frappe.db.get_list('Lead', filters={'custom_assign_team': doc.name}, fields=['name'])
		opp_list = frappe.db.get_list('Opportunity', filters={'custom_assign_team': doc.name}, fields=['name'])
		pro_list = frappe.db.get_list('Project', filters={'custom_assign_team': doc.name}, fields=['name'])

		# Remove shares for leads
		for lead in lead_list:
			lead_name = lead['name']
			for user in removed_users_list:
				frappe.db.delete('DocShare', filters={'user': user, 'share_doctype': 'Lead', 'share_name': lead_name})

		# Remove shares for opportunities
		for opp in opp_list:
			opp_name = opp['name']
			for user in removed_users_list:
				frappe.db.delete('DocShare', filters={'user': user, 'share_doctype': 'Opportunity', 'share_name': opp_name})

		# Remove shares for projects
		for pro in pro_list:
			pro_name = pro['name']
			for user in removed_users_list:
				frappe.db.delete('DocShare', filters={'user': user, 'share_doctype': 'Project', 'share_name': pro_name})
				task_list = frappe.db.get_list('Task', filters={'project': pro_name}, fields=['name'])
				for task in task_list:
					task_name = task['name']
					frappe.db.delete('DocShare', filters={'user': user, 'share_doctype': 'Task', 'share_name': task_name})




# -----------helper function-------------------

def share_doc_with_users(doc, doctype, items):
    for item in items:
        item_name = item['name']
        share_item_with_users(doc, doctype, item_name)

        # If the item is a Project, share related tasks as well
        if doctype == 'Project':
            task_list = frappe.db.get_list('Task', filters={'project': item_name}, fields=['name'])
            for task in task_list:
                task_name = task['name']
                share_item_with_users(doc, 'Task', task_name)


def share_item_with_users(doc, doctype, item_name):
    for user_role in doc.user_and_role:
        user = user_role.user
        if not frappe.db.exists('DocShare', {'user': user, 'share_name': item_name}):
            share = frappe.new_doc('DocShare')
            share.user = user
            share.share_doctype = doctype
            share.share_name = item_name
            share.read = 1
            share.write = 1
            share.notify_by_email = 1
            share.insert(ignore_permissions=True)

