(()=>{$(document).on("list_sidebar_setup",function(){if(frappe.boot.plan=="Free"){let t=$('<ul class="list-unstyled sidebar-menu"></ul>').appendTo(cur_list.page.sidebar),e={renew:{title:"Go Premium",body:"Your don't have a subscription yet, upgrade to keep using ERPNext.",button:"Upgrade"}}.renew,o=$(`<div class="border" style="
					padding: 10px 10px;
					border-radius: 5px;
				">
				<a><i class="octicon octicon-x pull-right close" style="font-size: 15px"></i></a>
				<h5>${e.title}</h5>
				<p>${e.body}</p>
				<button class="btn btn-xs btn-default btn-upgrade" style="margin-bottom: 10px;">${e.button}</button>
				</div>`).appendTo(t);o.find(".btn-upgrade").on("click",()=>{frappe.set_route("usage-info")}),o.find(".close").on("click",()=>{t.remove(),frappe.flags.upgrade_dismissed=1})}});})();
//# sourceMappingURL=erpnext_smb.bundle.W5AN6S77.js.map
