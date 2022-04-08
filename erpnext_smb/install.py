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
	add_accounting_workspace()
	add_buying_workspace()
	add_selling_workspace()
	add_inventory_workspace()

def add_accounting_workspace():
	accounting_workspace = read_json('accounting')
	accounting_workspace = json.loads(accounting_workspace)
	frappe.get_doc(accounting_workspace).insert()

def add_buying_workspace():
	buying_workspace = read_json('buying')
	buying_workspace = json.loads(buying_workspace)
	frappe.get_doc(buying_workspace).insert()

def add_selling_workspace():
	selling_workspace = read_json('selling')
	selling_workspace = json.loads(selling_workspace)
	frappe.get_doc(selling_workspace).insert()

def add_inventory_workspace():
	stock_workspace = read_json('inventory')
	stock_workspace = json.loads(stock_workspace)
	frappe.get_doc(stock_workspace).insert()


def read_json(name):
	file_path = os.path.join(os.path.dirname(__file__), "{name}.json".format(name=name))
	with open(file_path, "r") as f:
		return cstr(f.read())