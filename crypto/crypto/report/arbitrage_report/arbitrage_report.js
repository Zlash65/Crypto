// Copyright (c) 2016, Zlash65 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Arbitrage Report"] = {
	"filters": [
		{
			"fieldname":"coin",
			"label": __("Coin"),
			"fieldtype": "Link",
			"options": "Coin",
		},
	]
}
