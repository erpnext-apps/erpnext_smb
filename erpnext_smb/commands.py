import click
import frappe
from frappe.commands import get_site, pass_context
from erpnext_smb.install import setup_roles


@click.command("update-site-plan")
@click.option("--site", help="site name")
@click.argument("plan", type=click.Choice(["Free", "Basic", "Essential", "Professional"]))
@pass_context
def update_site_plan(context, plan, site=None):
	print("Updating plan...")
	from frappe.installer import update_site_config

	if not site:
		site = get_site(context)

	frappe.init(site=site)

	try:
		update_site_config("plan", plan)
		setup_roles(plan=plan)
		frappe.db.commit()
	except Exception as e:
		raise e

commands = [update_site_plan]