(() => {
  // ../erpnext_smb/erpnext_smb/public/js/list_sidebar.js
  $(document).on("list_sidebar_setup", function() {
    if (frappe.boot.plan == "Free") {
      let upgrade_list = $(`<ul class="list-unstyled sidebar-menu"></ul>`).appendTo(cur_list.page.sidebar);
      const content = {
        renew: {
          title: "Go Premium",
          body: `Your don't have a subscription yet, upgrade to keep using ERPNext.`,
          button: "Upgrade"
        }
      };
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
      upgrade_box.find(".btn-upgrade").on("click", () => {
        window.location.href = "https://frappecloud.com/dashboard/saas/login";
      });
      upgrade_box.find(".close").on("click", () => {
        upgrade_list.remove();
        frappe.flags.upgrade_dismissed = 1;
      });
    }
  });

  // ../erpnext_smb/erpnext_smb/public/js/index.js
  $(document).on("startup", () => {
    if (frappe.boot.plan == "Free" && frappe.boot.setup_complete) {
      let subscription_string = __("You have 14 days remaining in your trial.");
      console.log("startup");
      let $bar = $(`<div class="bg-white shadow sm:rounded-lg" style="position: stick; top:0">
						<div class="px-7 py-2">
						<div style="text-align: center">
							<div style="display: inline-flex", class="text-muted">
							<p style="margin-top: 7px; margin-right: 10px">Your subscription is about to expire</p>
							<button type="button" class="px-2 py-1 border border-transparent text-white hover:bg-indigo-700 focus:outline-none focus:ring-offset-2 focus:ring-indigo-500" style="background-color: #007bff; border-radius: 5px">Renew</button>
							</div>
							<a type="button" class="dismiss-upgrade text-muted" data-dismiss="modal" aria-hidden="true" style="margin-top: 7px">\xD7</a>
						</div>
						</div>
					</div>`);
      $("body").append($bar);
      $bar.find(".dismiss-upgrade").on("click", () => {
        $bar.remove();
      });
    }
  });
})();
//# sourceMappingURL=erpnext_smb.bundle.VHOGLSGZ.js.map
