// Copyright (c) 2016, Zlash65 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["My Investments Report"] = {
	"filters": [
		{
			"fieldname":"coin",
			"label": __("Coin"),
			"fieldtype": "Link",
			"options": "Coin",
			get_query: function() {
				let my_coins = [];
				frappe.call({
					method: "crypto.crypto.report.my_investments_report.my_investments_report.get_my_coins",
					async: false
				}).then(r => {
					my_coins = r.message;
				});

				return {
					"filters": [
						['Coin', 'name', 'in', my_coins]
					]
				};


			}
		},
	]
}
