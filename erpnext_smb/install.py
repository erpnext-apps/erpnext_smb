import frappe
import json
import os
from frappe.utils import cstr
from erpnext_smb.master_setup import setup_masters
from frappe.permissions import add_permission, update_permission_property

def after_install():
	create_module_profile()
	create_role_profile()
	update_existing_users()
	disable_workspaces()
	enable_workspace("Users")
	setup_roles()
	add_custom_workspaces()
	disable_onboarding()
	setup_masters()

def create_module_profile():
	module_profile = frappe.new_doc('Module Profile')
	module_profile.module_profile_name = 'SMB User'

	for app in ('frappe', 'erpnext'):
		for module in frappe.get_module_list(app):
			if module not in ["Accounts", "Buying", "Selling", "Stock", "Setup", "Core",
				"Desk", "Manufacturing"]:
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

def enable_workspace(workspace):
	workspace_doc = frappe.get_doc('Workspace', workspace)
	workspace_doc.flags.ignore_links = True
	workspace_doc.flags.ignore_validate = True
	workspace_doc.public = 1
	workspace_doc.save()

def add_custom_workspaces():
	for workspace in ('accounts', 'inventory', 'sales_and_purchase', 'masters', 'setup'):
		add_workspace(workspace)

def add_workspace(file_name):
	workspace = read_json(file_name)
	workspace = json.loads(workspace)
	frappe.get_doc(workspace).insert()

def setup_roles(plan="Basic"):
	allowed_roles = frappe.get_hooks("allowed_roles")

	if plan == 'Basic':
		roles_to_enable = allowed_roles.get(plan)
	elif plan == 'Essential':
		roles_to_enable = allowed_roles.get('Essential') + allowed_roles.get('Basic')
		enable_workspace("Manufacturing")
	elif plan == 'Professional':
		roles_to_enable = allowed_roles.get('Essential') + allowed_roles.get('Basic') + \
			allowed_roles.get('Professional')

	role = frappe.qb.DocType("Role")

	frappe.qb.update(role).set(
		role.disabled, 1
	).where(role.name.notin(roles_to_enable)).run()

	frappe.qb.update(role).set(
		role.disabled, 0
	).set(
		role.list_sidebar, 1
	).set(
		role.form_sidebar, 1
	).set(
		role.dashboard, 1
	).set(
		role.timeline, 1
	).set(
		role.bulk_actions, 1
	).set(
		role.view_switcher, 1
	).set(
		role.search_bar, 1
	).set(
		role.notifications, 1
	).where(role.name.isin(roles_to_enable)).run()

	for d in roles_to_enable:
		add_permission("User", d, 0)
		add_permission("User", d, 1)
		update_permission_property("User", d, 0, "write", 1)
		update_permission_property("User", d, 0, "create", 1)
		update_permission_property("User", d, 1, "write", 1)
		update_permission_property("User", d, 1, "create", 1)

def read_json(name):
	file_path = os.path.join(os.path.dirname(__file__), "{name}.json".format(name=name))
	with open(file_path, "r") as f:
		return cstr(f.read())