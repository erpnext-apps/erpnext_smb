from . import __version__ as app_version

app_name = "erpnext_smb"
app_title = "ERPNext"
app_publisher = "Frappe Technologies"
app_description = "ERPNext SMB Setup"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@frappe.io"
app_license = "MIT"

required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_smb/css/erpnext_smb.css"
app_include_js = "erpnext_smb.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_smb/css/erpnext_smb.css"
# web_include_js = "/assets/erpnext_smb/js/erpnext_smb.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext_smb/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "erpnext_smb.utils.jinja_methods",
# 	"filters": "erpnext_smb.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnext_smb.install.before_install"

# Uninstallation
# ------------

# before_uninstall = "erpnext_smb.uninstall.before_uninstall"
# after_uninstall = "erpnext_smb.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_smb.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"before_insert": "erpnext_smb.limits.validate_user_limit",
	},
	"Company": {
		"before_insert": "erpnext_smb.limits.validate_company",
	},
	"Custom Field": {
		"before_insert": "erpnext_smb.limits.validate_custom_fields",
	},
	"Client Script": {
		"before_insert": "erpnext_smb.limits.validate_client_scripts",
	},
	"Server Script": {
		"before_insert": "erpnext_smb.limits.validate_server_scripts",
	},
	"DocType": {
		"before_insert": "erpnext_smb.limits.validate_custom_doctypes",
	}
}

boot_session = "erpnext_smb.limits.add_plan_to_bootinfo"

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_smb.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_smb.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_smb.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_smb.tasks.weekly"
# 	],
# 	"monthly": [
# 		"erpnext_smb.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "erpnext_smb.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_smb.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_smb.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


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
# 	"erpnext_smb.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
