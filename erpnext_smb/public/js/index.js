$(document).on('startup', () => {
	if (frappe.boot.plan == "Free" && frappe.boot.setup_complete) {
		let subscription_string = __("You have 14 days remaining in your trial.");
		
		console.log("startup");
		let $bar = $(`<div class="bg-white shadow sm:rounded-lg" style="position: sticky; bottom:0">
						<div class="px-7 py-2">
						<div style="text-align: center">
							<div style="display: inline-flex", class="text-muted">
							<p style="margin-top: 7px; margin-right: 10px">Your subscription is about to expire</p>
							<button type="button" class="px-2 py-1 border border-transparent text-white hover:bg-indigo-700 focus:outline-none focus:ring-offset-2 focus:ring-indigo-500" style="background-color: #007bff; border-radius: 5px">Renew</button>
							</div>
							<a type="button" class="dismiss-upgrade text-muted" data-dismiss="modal" aria-hidden="true" style="margin-top: 7px">×</a>
						</div>
						</div>
					</div>`);

		$('body').append($bar);

		$bar.find('.dismiss-upgrade').on('click', () => {
			$bar.remove();
		});
	}
})