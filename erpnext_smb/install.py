import frappe
import json
import os
from frappe.utils import cstr

def after_install():
	create_module_profile()
	create_role_profile()
	update_existing_users()
	disable_workspaces()
	add_custom_workspaces()
	disable_onboarding()

def create_module_profile():
	module_profile = frappe.new_doc('Module Profile')
	module_profile.module_profile_name = 'SMB User'

	for app in ('frappe', 'erpnext'):
		for module in frappe.get_module_list(app):
			if module not in ["Accounts", "Buying", "Selling", "Stock"]:
				module_profile.append('block_modules', {
					'module': module
				})

	module_profile.insert()

def disable_onboarding():
	frappe.db.set_value('System Settings', 'System Settings', 'enable_onboarding', 0)

def create_role_profile():
	pass

def update_existing_users():
	for user in frappe.get_all('User', {'name': ('not in', ['Administrator', 'Guest'])}):
		user_doc = frappe.get_doc('User', user)
		user_doc.module_profile = 'SMB User'
		user_doc.save()


def update_module_profile(doc, method):
	doc.module_profile = 'SMB User'

def disable_workspaces():
	for workspace in frappe.get_all('Workspace', {'public': 1}, pluck='name'):
		try:
			workspace_doc = frappe.get_doc('Workspace', workspace)
			workspace_doc.flags.ignore_links = True
			workspace_doc.flags.ignore_validate = True
			workspace_doc.public = 0
			workspace_doc.save()
		except Exception as e:
			pass

def add_custom_workspaces():
	for workspace in ('accounts', 'inventory', 'sales_and_purchase', 'masters', 'setup'):
		add_workspace(workspace)

def add_workspace(file_name):
	workspace = read_json(file_name)
	workspace = json.loads(workspace)
	frappe.get_doc(workspace).insert()

def read_json(name):
	file_path = os.path.join(os.path.dirname(__file__), "{name}.json".format(name=name))
	with open(file_path, "r") as f:
		return cstr(f.read())