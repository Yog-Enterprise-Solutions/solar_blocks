app_name = "solar_blocks"
app_title = "Solar Blocks"
app_publisher = "yes@tranqwality.com"
app_description = "Createing Dashboards"
app_email = "yes@tranqwality.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/solar_blocks/css/solar_blocks.css"
# app_include_js = "/assets/solar_blocks/js/solar_blocks.js"

# include js, css files in header of web template
# web_include_css = "/assets/solar_blocks/css/solar_blocks.css"
# web_include_js = "/assets/solar_blocks/js/solar_blocks.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "solar_blocks/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Lead" : "public/js/lead.js",
#     "Project": "public/js/project.js",
    "Opportunity": "public/js/opportunity.js"
#     "Branch": "public/js/branch.js",
    # "Task": "public/js/Task.js"
#     "Proposal": "public/js/proposal.js",
#     "Site Visit": "public/js/site_visit.js",
#     "Quotation": "public/js/quotation.js",
#     # "Contract Sign Doc": "public/js/contract_sign_doc.js",
#     # "Contracts" ; "public/js/contracts.js"

    }
# doctype_list_js = {"Lead" : "public/js/lead_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "solar_blocks/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "solar_blocks.utils.jinja_methods",
# 	"filters": "solar_blocks.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "solar_blocks.install.before_install"
# after_install = "solar_blocks.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "solar_blocks.uninstall.before_uninstall"
# after_uninstall = "solar_blocks.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "solar_blocks.utils.before_app_install"
# after_app_install = "solar_blocks.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "solar_blocks.utils.before_app_uninstall"
# after_app_uninstall = "solar_blocks.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "solar_blocks.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Opportunity": "solar_blocks.override.opportunity.CustomOpportunity"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Lead": {
        "on_update" : "solar_blocks.override.lead.after_save",
        "before_insert" : "solar_blocks.override.lead.enqueue_create_document_template"
    },
    "Opportunity":{
        "on_update": "solar_blocks.override.opportunity.enqueue_todo_and_share_on_maxfit_completed",
        "after_insert": "solar_blocks.override.opportunity.enqueue_todo_and_share",
        "before_insert": "solar_blocks.override.opportunity.set_user_group_and_document_status_template_before_insert"
        # "validate": "solar_blocks.override.opportunity.assign_users_and_send_mails"
    },
	"Task": {
        "after_insert": "solar_blocks.override.task.after_insert",
        "on_update": "solar_blocks.override.task.after_save",
        "validate": "solar_blocks.override.task.before_save",
        "before_insert": "solar_blocks.override.task.before_insert",
        "before_validate": "solar_blocks.override.task.before_validate"
    },
    "Project":{
        "on_update": "solar_blocks.override.project.after_save",
        "validate": "solar_blocks.override.project.before_save",
        "after_insert": "solar_blocks.override.project.after_insert"
    },
    "User": {
        "before_insert": "solar_blocks.override.user.assign_raven_user_role_remove_modules"
    },
    "Error Log": {
        "before_insert": "solar_blocks.override.error_log.error_log_fix"
    },
    "Email Queue":{
        "after_insert": "solar_blocks.override.email_queue.email_send"
    },
    "BOS":{
        "validate": "solar_blocks.override.bos.calculate_totals_and_subtotal",
        "on_submit": "solar_blocks.override.bos.calculate_totals_and_subtotal"
    },
    "Quotation": {
        "after_insert": "solar_blocks.override.quotation.update_quotation_created_status_in_opportunity",
        "after_submit": "solar_blocks.override.quotation.update_quotation_status_in_opportunity",
    }
#     "Proposal":{
#         "before_save": "solar_blocks.override.proposal.api_call"
#     },
#     # "Contract Sign Doc":{
#     #     "before_save": "solar_blocks.solar_blocks.override.contract_sign_doc.set_value_in_contract"
#     # }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"solar_blocks.solar_blocks.override.schedulers.opp_auto_disqualified_in_case_of_meeting_and_appointment",
#         "solar_blocks.solar_blocks.override.schedulers.auto_disqualified_lead_in_4_weeks"
# 	],
# 	# "daily": [
# 	# 	"solar_blocks.tasks.daily"
# 	# ],
# 	# "hourly": [
# 	# 	"solar_blocks.tasks.hourly"
# 	# ],
# 	# "weekly": [
# 	# 	"solar_blocks.tasks.weekly"
# 	# ],
# 	# "monthly": [
# 	# 	"solar_blocks.tasks.monthly"
# 	# ],
# }

# Testing
# -------

# before_tests = "solar_blocks.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "solar_blocks.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "solar_blocks.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["solar_blocks.utils.before_request"]
# after_request = ["solar_blocks.utils.after_request"]

# Job Events
# ----------
# before_job = ["solar_blocks.utils.before_job"]
# after_job = ["solar_blocks.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"solar_blocks.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt" : "Custom Field", "filters" : [
       [ "dt" , "in", [
            "Lead","Project","Opportunity","Task"
        ]
       ]
    ]}
]