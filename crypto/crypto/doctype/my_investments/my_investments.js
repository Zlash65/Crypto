// Copyright (c) 2018, Zlash65 and contributors
// For license information, please see license.txt

frappe.ui.form.on('My Investments', {
	refresh: function(frm) {
		// if an investment is bought as well as sold make everything non editable
		if(frm.doc.sold && !frm.doc.__islocal) {
			let fields = ["quantity", "buy_price", "sell_price", 'sold', 'sell_enabled'];
			fields.forEach(d => {
				frm.set_df_property(d, 'read_only', 1);
			})
		}
	},
	onload_post_render: function(frm) {
		frm.add_custom_button(__('View calendar'), function() {
			frappe.set_route('List', 'Event', 'Calendar')
		});
	},
	sold: function(frm){
		frm.trigger("refresh");
	},
	validate: function(frm) {
		// add event data to view calendar as to when its bought and sold
		if(frm.doc.buy_date) {
			frappe.call({
				"method": "crypto.crypto.doctype.my_investments.my_investments.add_event",
				args: {
					"doc": frm.doc,
					"bot_sold": "buy_date"
				}
			})
		}
		if(frm.doc.sell_date) {
			frappe.call({
				"method": "crypto.crypto.doctype.my_investments.my_investments.add_event",
				args: {
					"doc": frm.doc,
					"bot_sold": "sell_date"
				}
			})
		}
	}
});
