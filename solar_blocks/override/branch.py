import frappe

def test(doc,method=None):
      #send mail on create opp
    created_by=doc.opportunity_owner
    teams = frappe.get_all('Team')
    matching_teams = []

    # Iterate through each team
    for team in teams:
        team_doc = frappe.get_doc('Team', team.name)
        # Check the child table for the specified user with the 'Sales Closure' role
        for member in team_doc.get('user_and_role'):
            if member.user == frappe.session.user:
                matching_teams.append(team.name)
    frappe.throw(f"{matching_teams}")

