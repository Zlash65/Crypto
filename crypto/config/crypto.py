from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Exchange"),
			"items": [
				{
					"type": "doctype",
					"name": "Coin Exchange",
					"description": _("Data fetched from each market.")
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
				}
			]
		}
	]
