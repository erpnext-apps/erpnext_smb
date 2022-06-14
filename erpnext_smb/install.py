import frappe
import json
import os
from frappe.utils import cstr
from erpnext_smb.master_setup import setup_masters
from frappe.permissions import add_permission, update_permission_property
from frappe.utils import cint
from frappe import _

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
	for workspace in ('accounts', 'inventory', 'sales', 'purchase', 
		'masters', 'setup', 'manufacturing_smb'):
		add_workspace(workspace)
	
	frappe.get_doc({
		"doctype": "Translation",
		"language": "en",
		"source_text": "Manufacturing SMB",
		"translated_text": "Manufacturing"
	}).insert()

def add_workspace(file_name):
	workspace = read_json(file_name)
	workspace = json.loads(workspace)
	frappe.get_doc(workspace).insert()

def setup_roles(plan="Basic"):
	allowed_roles = frappe.get_hooks("allowed_roles")

	if plan in ('Basic', 'Free'):
		roles_to_enable = allowed_roles.get('Basic')
	elif plan == 'Essential':
		roles_to_enable = allowed_roles.get('Essential') + allowed_roles.get('Basic')
	elif plan == 'Professional':
		roles_to_enable = allowed_roles.get('Essential') + allowed_roles.get('Basic')

	disable_roles(roles_to_enable)
	enable_roles(roles_to_enable)
	if not frappe.db.exists("Role", "Site Admin"):
		add_site_admin_role()

	update_permission_for_settings("System Settings")
	update_permission_for_settings("Print Settings")

	if plan == "Professional":
		add_perm_for_customization()

def disable_roles(roles_to_enable):
	role = frappe.qb.DocType("Role")
	frappe.qb.update(role).set(
		role.disabled, 1
	).where(role.name.notin(roles_to_enable)).run()

def enable_roles(roles_to_enable):
	role = frappe.qb.DocType("Role")
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


def update_permission_for_settings(doctype):
	for d in ["Accounts Manager", "Purchase Manager","Sales Manager", "Stock Manager", "Item Manager"]:
		add_permission(doctype, d, 0)
		update_permission_property(doctype, d, 0, "write", 1)
		update_permission_property(doctype, d, 0, "create", 1)

def add_perm_for_customization():
	frappe.get_doc({
		"doctype": "Role",
		"role_name": "Document Editor",
		"desk_access": 1,
		"is_custom": 1
	}).insert()

	_add_permission("Custom Field", "Document Editor")
	_add_permission("DocType", "Document Editor")
	_add_permission("Property Setter", "Document Editor")

def add_site_admin_role():
	frappe.get_doc({
		"doctype": "Role",
		"role_name": "Site Admin",
		"desk_access": 1,
		"is_custom": 1
	}).insert()

	add_permission("User", "Site Admin", 0)
	add_permission("User", "Site Admin", 1)
	update_permission_property("User", "Site Admin", 0, "write", 1)
	update_permission_property("User", "Site Admin", 0, "create", 1)
	update_permission_property("Role Profile", "Site Admin", 0, "write", 1)
	update_permission_property("Role Profile", "Site Admin", 0, "create", 1)
	update_permission_property("User", "Site Admin", 1, "write", 1)
	update_permission_property("User", "Site Admin", 1, "create", 1)

def _add_permission(doctype, role):
	add_permission(doctype, role, 0)
	update_permission_property(doctype, role, 0, "write", 1)
	update_permission_property(doctype, role, 0, "create", 1)

def read_json(name):
	file_path = os.path.join(os.path.dirname(__file__), "{name}.json".format(name=name))
	with open(file_path, "r") as f:
		return cstr(f.read())

def update_site_admin_role(doc, method):
	if not frappe.db.exists("Role", "Site Admin"):
		add_site_admin_role()

	add_site_admin_role_to_user(doc)

def add_site_admin_role_to_user(doc):
	# if adding system manager, do nothing
	if not cint(doc.enabled) or (
		"Site Admin" in [user_role.role for user_role in doc.get("roles")]
	):
		return

	if (
		doc.name not in frappe.STANDARD_USERS
		and doc.user_type == "System User"
		and not get_other_site_admins(doc.name)
		and cint(frappe.db.get_single_value("System Settings", "setup_complete"))
	):
		frappe.msgprint(_("Adding Site Admin to this User as there must be atleast one Site Admin"))
		doc.append("roles", {"doctype": "Has Role", "role": "Site Admin"})

def get_other_site_admins(name):
	user_doctype = frappe.qb.DocType("User").as_("user")
	user_role_doctype = frappe.qb.DocType("Has Role").as_("user_role")

	return (
		frappe.qb.from_(user_doctype)
		.from_(user_role_doctype)
		.select(user_doctype.name)
		.where(user_role_doctype.role == "Site Admin")
		.where(user_doctype.docstatus < 2)
		.where(user_doctype.enabled == 1)
		.where(user_role_doctype.parent == user_doctype.name)
		.where(user_role_doctype.parent.notin(["Administrator", name]))
		.limit(1)
		.distinct()
	).run()