import frappe
from frappe import _

def validate_limits(doc, method):
	plan = frappe.conf.plan
	allowed_roles = frappe.get_hooks("allowed_roles")

	if frappe.session.user == "Administrator":
		return

	if plan == 'Professional':
		return
	elif plan in ('Basic', 'Essential'):
		if doc.name not in allowed_roles:
			frappe.throw(_("Error"))

def validate_role(doc, method):
	if frappe.session.user != "Administrator":
		frappe.throw(_("Error"))

