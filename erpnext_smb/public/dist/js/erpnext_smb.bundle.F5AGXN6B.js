(() => {
  // ../erpnext_smb/erpnext_smb/public/js/list_sidebar.js
  $(document).on("list_sidebar_setup", function() {
    if (frappe.boot.trial_end_date) {
      let upgrade_list = $(`<ul class="list-unstyled sidebar-menu"></ul>`).appendTo(cur_list.page.sidebar);
      const content = {
        renew: {
          title: "Go Premium",
          body: `You don't have a subscription yet, upgrade to keep using ERPNext.`,
          button: "Subscribe"
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
        frappe.call({
          method: "erpnext_smb.limits.get_login_url",
          callback: function(url) {
            window.open(url.message, "_blank");
          }
        });
      });
      upgrade_box.find(".close").on("click", () => {
        upgrade_list.remove();
        frappe.flags.upgrade_dismissed = 1;
      });
    }
  });

  // ../erpnext_smb/erpnext_smb/public/js/index.js
  $(document).on("startup", () => {
    if (frappe.boot.trial_end_date && frappe.boot.setup_complete) {
      let diff_days = frappe.datetime.get_day_diff(cstr(frappe.boot.trial_end_date), frappe.datetime.get_today()) - 1;
      let subscription_string = __("You have {0} days remaining in your trial.", [cstr(diff_days).bold()]);
      let $bar = $(`<div class="shadow sm:rounded-lg py-2" style="position:fixed; left: 145px; bottom:20px; width:80%; margin: auto; border-radius: 10px; background-color: #F7FAFC; z-index: 1">
				<div style="display: inline-flex; align-items: center", class="text-muted">
				<p style="margin-left: 20px; margin-top:5px; font-size: 17px">${subscription_string}</p>
				<button type="button" class="button-renew px-4 py-2 border border-transparent text-white hover:bg-indigo-700 focus:outline-none focus:ring-offset-2 focus:ring-indigo-500" style="background-color: #007bff; border-radius: 5px; margin-left:650px; margin-right: 10px">Subscribe</button>
				<a type="button" class="dismiss-upgrade text-muted" data-dismiss="modal" aria-hidden="true" style="font-size:30px; margin-bottom: 5px; margin-right: 10px">\xD7</a>
			</div>
		</div>`);
      $("footer").append($bar);
      $bar.find(".button-renew").on("click", () => {
        frappe.call({
          method: "erpnext_smb.limits.get_login_url",
          callback: function(url) {
            window.open(url.message, "_blank");
          }
        });
      });
      $(".custom-actions").hide();
      $bar.find(".dismiss-upgrade").on("click", () => {
        $bar.remove();
      });
    }
    let help_menu = $(".dropdown-help #help-links");
    if (help_menu.length > 0) {
      frappe.call({
        method: "erpnext_smb.limits.get_login_url",
        callback: function(url) {
          $(`<a class="dropdown-item" 				href="${url.message}" target="_blank">` + __("Manage Subscription") + '</a>				<div class="divider"></div>').insertBefore(help_menu);
        }
      });
    }
  });

  // ../erpnext_smb/erpnext_smb/public/js/limits.js
  frappe.provide("frappe.request");
  frappe.provide("limits");
  $(() => {
    frappe.request.on_error("PaywallReachedError", (r) => {
      let msg = JSON.parse(r._server_messages);
      limits.show_error_msg(JSON.parse(msg).message, "Upgrade");
    });
  });
  limits.show_error_msg = function(message, label) {
    frappe.throw({
      message,
      primary_action: {
        label: __(label),
        action: () => {
          frappe.call({
            method: "erpnext_smb.limits.get_login_url",
            callback: function(url) {
              window.open(url.message, "_blank");
            }
          });
        }
      }
    });
  };
})();
//# sourceMappingURL=erpnext_smb.bundle.F5AGXN6B.js.map
