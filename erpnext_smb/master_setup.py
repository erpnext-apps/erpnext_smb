import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def setup_masters():
	for master in ["Customer", "Supplier", "Customer Group", "Supplier Group", "Item Group", "Quotation"]:
		hide_fields(master)
		update_settings()

	delete_stock_entry_types()


def hide_fields(master):
	fields = get_fields(master)

	for fieldname in fields:
		make_property_setter(master, fieldname, "hidden", 1, "Check", validate_fields_for_doctype=False)

def delete_stock_entry_types():
	allowed_types = ["Repack", "Material Transfer", "Material Receipt", "Material Issue"]
	for d in frappe.db.get_all("Stock Entry Type"):
		if d.name not in allowed_types:
			frappe.delete_doc_if_exists("Stock Entry Type", d.name)

def update_settings():
	frappe.db.set_single_value('Selling Settings', {
		"customer_group": "All Customer Groups",
		"territory": "All Territories"
	})

	frappe.db.set_single_value('Buying Settings', {
		"supplier_group": "All Supplier Groups"
	})

def get_fields(master):
	field_map = {
		'Customer': ['default_bank_account', 'lead_name', 'opportunity_name', 'tax_id', 'tax_category',
				'account_manager','so_required', 'dn_required', 'is_internal_customer', 'column_break_38',
				'sales_team_section_break', 'sales_team_section'],
		'Supplier': ['default_bank_account', 'country', 'tax_id', 'tax_category', 'is_internal_supplier',
				'allow_purchase_invoice_creation_without_purchase_order', 'allow_purchase_invoice_creation_without_purchase_receipt',
				'warn_rfqs', 'warn_pos', 'prevent_rfqs', 'prevent_pos'],
		"Customer Group": ["credit_limit_section"],
		"Supplier Group": ["section_credit_limit"],
		"Item Group": ["sb9"],
		"Quotation": ["taxes_section", "more_info", "scan_barcode"],
		"Sales Invoice": ["is_pos", "project", "time_sheet_list", "loyalty_points_redemption", "sales_team_section_break", "subscription_section"],
		"Sales Invoice Item": ["deferred_revenue", "project"],
		"User": ["sb_allow_modules"],
		"Item": ["is_fixed_asset"]
	}

	return field_map.get(master)