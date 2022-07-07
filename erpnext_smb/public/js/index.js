$(document).on('startup', () => {
	if (frappe.boot.trial_end_date && frappe.boot.setup_complete) {
		let diff_days = frappe.datetime.get_day_diff(cstr(frappe.boot.trial_end_date), frappe.datetime.get_today()) - 1;
		let subscription_string =  __("You have {0} days remaining in your trial.", [(cstr(diff_days)).bold()])
		
		let $bar = $(`<div class="shadow sm:rounded-lg py-2" style="position:fixed; left: 145px; bottom:20px; width:80%; margin: auto; border-radius: 10px; background-color: #F7FAFC; z-index: 1">
				<div style="display: inline-flex; align-items: center", class="text-muted">
				<p style="margin-left: 20px; margin-top:5px; font-size: 17px">${subscription_string}</p>
				<button type="button" class="button-renew px-4 py-2 border border-transparent text-white hover:bg-indigo-700 focus:outline-none focus:ring-offset-2 focus:ring-indigo-500" style="background-color: #007bff; border-radius: 5px; margin-left:650px; margin-right: 10px">Subscribe</button>
				<a type="button" class="dismiss-upgrade text-muted" data-dismiss="modal" aria-hidden="true" style="font-size:30px; margin-bottom: 5px; margin-right: 10px">×</a>
			</div>
		</div>`);

		$('footer').append($bar);
		
		$bar.find('.button-renew').on('click', () => {
			frappe.call({
				method: "erpnext_smb.limits.get_login_url",
				callback: function(url) {
					window.open(
						url.message,
						'_blank'
					);
				}
			})
		});

		$('.custom-actions').hide();

		$bar.find('.dismiss-upgrade').on('click', () => {
			$bar.remove();
		});
	}

	let help_menu = $('.dropdown-help #help-links');

	if (help_menu.length > 0) {
		frappe.call({
			method: "erpnext_smb.limits.get_login_url",
			callback: function(url) {
				$(`<a class="dropdown-item" \
				href="${url.message}">` + __('Manage Subscription') + '</a>\
				<div class="divider"></div>').insertBefore(help_menu);
				}
		})
	}
})