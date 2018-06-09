from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("User"),
			"items": [
				{
					"type": "doctype",
					"name": "User Profile",
					"description": _("User data.")
				},
				{
					"type": "doctype",
					"name": "My Investments",
					"description": _("Keep track of invested coins.")
				},
				{
					"type": "report",
					"name": "My Investments Report",
					"doctype": "My Investments",
					"description": _("Arbitrage coin data pertaining to User's investments"),
					"is_query_report": True
				}
			]
		},
		{
			"label": _("Exchange"),
			"items": [
				{
					"type": "doctype",
					"name": "Coin Exchange",
					"description": _("Data fetched from each market.")
				},
				{
					"type": "report",
					"name": "Arbitrage Report",
					"doctype": "Coin Exchange",
					"description": _("Overall Arbitrage data"),
					"is_query_report": True
				}
			]
		},
		{
			"label": _("Master Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Coin",
					"description": _("Coin Symbol and its full name.")
				},
				{
					"type": "doctype",
					"name": "Market",
					"description": _("Market detail and fees for each coin.")
				},
				{
					"type": "doctype",
					"name": "Market API",
					"description": _("Setup API's for market added.")
				}
			]
		}
	]
