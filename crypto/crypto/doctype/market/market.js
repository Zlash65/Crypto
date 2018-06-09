// Copyright (c) 2018, Zlash65 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Market', {
	onload_post_render: function(frm) {
		if(!frm.doc.__islocal) {
			frappe.model.with_doc("Market API", (frm.doc.market_name + " - api"), function(r) {
				let market_api = frappe.model.get_doc("Market API", (frm.doc.market_name + " - api"));
				if(!market_api) {
					frappe.show_alert(__("Please fill the api details for this Market."));
					frm.add_custom_button(__('Api Setup'), function() {
						frappe.model.with_doctype('Market API', function() {
							var doc = frappe.model.get_new_doc('Market API');
							doc.market = frm.doc.market_name;
							frappe.set_route('Form', doc.doctype, doc.name);
						})
					});
				} else {
					frm.add_custom_button(__('View Api'), function() {
						frappe.set_route("Form", "Market API", market_api.name);
					});
					return;
				}
			});
		}
	}
});
