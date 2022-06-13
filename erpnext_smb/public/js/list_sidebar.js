$(document).on('list_sidebar_setup', function () {
	if (frappe.boot.plan == "Free") {
		let upgrade_list = $(`<ul class="list-unstyled sidebar-menu"></ul>`).appendTo(cur_list.page.sidebar);

		const content = {
			renew: {
				title: 'Go Premium',
				body: `Your don't have a subscription yet, upgrade to keep using ERPNext.`,
				button: 'Upgrade'
			}
		}

		let message = content.renew;
		let upgrade_box = $(`<div class="border" style="
					padding: 10px 10px;
					border-radius: 5px;
				">
				<a><i class="octicon octicon-x pull-right close" style="font-size: 15px"></i></a>
				<h5>${message.title}</h5>
				<p>${message.body}</p>
				<button class="btn btn-xs btn-default btn-upgrade" style="margin-bottom: 10px;">${message.button}</button>
				</div>`).appendTo(upgrade_list);

		upgrade_box.find('.btn-upgrade').on('click', () => {
			window.location.href = "https://frappecloud.com/dashboard/saas/login"
		});

		upgrade_box.find('.close').on('click', () => {
			upgrade_list.remove();
			frappe.flags.upgrade_dismissed = 1;
		});
	}
});