import frappe
from frappe import _
import requests

class PaywallReachedError(frappe.ValidationError): pass

def validate_custom_fields(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("Custom Field", {"owner": ("!=", "Administrator")})

	if plan == "Basic" and count >= 100:
		frappe.throw(_("Only 100 custom fields are allowed as per your plan"), exc=PaywallReachedError)

def validate_user_limit(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("User", {"name": ("not in", ["Guest", "Administrator"])})

	if plan == "Basic" and count >= 5:
		frappe.throw(_("Only 10 users are allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Essential" and count > 25:
		frappe.throw(_("Only 25 users are allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Professional" and count > 50:
		frappe.throw(_("Only 50 users are allowed as per your plan"), exc=PaywallReachedError)

def validate_company(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("Company")

	if plan == "Basic" and count >= 1:
		frappe.throw(_("Only one company allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Essential" and count >= 2:
		frappe.throw(_("Only 2 companies are allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Professional" and count >= 5:
		frappe.throw(_("Only 5 companie,s are allowed as per your plan"), exc=PaywallReachedError)

def validate_custom_doctypes(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("DocType", {"custom": 1})

	if plan == "Basic" and count > 0:
		frappe.throw(_("No custom forms allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Essential" and count >= 5:
		frappe.throw(_("Only 5 custom forms are allowed as per your plan"), exc=PaywallReachedError)

def validate_client_scripts(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("Client Script", {"disabled": 0})

	if plan == "Basic" and count > 0:
		frappe.throw(_("No client scripts allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Essential" and count >= 10:
		frappe.throw(_("Only 10 client scripts are allowed as per your plan"), exc=PaywallReachedError)

def validate_server_scripts(doc, method):
	plan = frappe.conf.plan
	count = frappe.db.count("Server Script", {"disabled": 0})

	if plan == "Basic" and count > 0:
		frappe.throw(_("No server scripts allowed as per your plan"), exc=PaywallReachedError)
	elif plan == "Essential" and count >= 10:
		frappe.throw(_("Only 10 server scripts are allowed as per your plan"), exc=PaywallReachedError)

def add_plan_to_bootinfo(bootinfo):
	bootinfo.plan = frappe.conf.plan

	secret_key = frappe.conf.sk_erpnext_smb
	url = "https://frappecloud.com/api/method/press.api.developer.saas.get_trial_expiry?secret_key={key}".format(key=secret_key)
	response = requests.request(
		method="POST",
		url=url,
		timeout=5
	)

	bootinfo.trial_end_date = response.json().get('message')

@frappe.whitelist()
def get_login_url():
	secret_key = frappe.conf.sk_erpnext_smb
	url = "https://frappecloud.com/api/method/press.api.developer.saas.get_login_url?secret_key={key}".format(key=secret_key)
	response = requests.request(
		method="POST",
		url=url,
		timeout=5
	)

	return response.json().get('message')