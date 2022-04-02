from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_smb/__init__.py
from erpnext_smb import __version__ as version

setup(
	name="erpnext_smb",
	version=version,
	description="ERPNext SMB Setup",
	author="Frappe Technologies",
	author_email="hello@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
