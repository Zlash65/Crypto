// Copyright (c) 2018, Zlash65 and contributors
// For license information, please see license.txt

frappe.ui.form.on('My Investments', {
	refresh: function(frm) {
		if(frm.doc.sold && !frm.doc.__islocal) {
			let fields = ["quantity", "buy_price", "sell_price"];
			fields.forEach(d => {
				frm.set_df_property(d, 'read_only', 1);
			})
		}
	},
	sold: function(frm){
		frm.trigger("refresh");
	},
	validate: function(frm) {
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
