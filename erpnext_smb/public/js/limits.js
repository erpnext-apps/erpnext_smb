frappe.provide('frappe.request');
frappe.provide('limits');


$(() => {
	frappe.request.on_error('PaywallReachedError', (r) => {

		let msg = JSON.parse(r._server_messages);
		limits.show_error_msg(JSON.parse(msg).message, 'Upgrade');
	});
})

limits.show_error_msg = function(message, label) {
	frappe.throw({
		message: message,
		primary_action: {
			label: __(label),
			action: () => {
				frappe.call({
					method: "erpnext_smb.limits.get_login_url",
					callback: function(url) {
						window.open(
							url.message,
							'_blank'
						);
					}
				})
			}
		}
	});
}