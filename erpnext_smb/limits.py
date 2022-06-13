import frappe
from frappe import _
from frappe.utils import getdate

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

def validate_custom_fields(doc, method):
	plan = frappe.conf.plan

	if plan != "Professional" and doc.owner != "Administrator":
		frappe.throw(_("Customizations are not allowed in your current plan"))

def validate_property_setter(doc, method):
	plan = frappe.conf.plan
	
	if plan != "Professional" and doc.owner != "Administrator":
		frappe.throw(_("Customizations are not allowed in your current plan"))

def add_plan_to_bootinfo(bootinfo):
	bootinfo.plan = frappe.conf.plan
	bootinfo.trial_end_date = getdate(frappe.conf.trial_end_date)