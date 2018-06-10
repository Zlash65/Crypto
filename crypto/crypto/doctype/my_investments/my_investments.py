# -*- coding: utf-8 -*-
# Copyright (c) 2018, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class MyInvestments(Document):
	def autoname(self):
		name = "{0} - {1} / ".format(self.coin, self.market)
		self.name = make_autoname(name)

	def validate(self):
		self.set_missing_values()

	def set_missing_values(self):
		self.total_investment = self.quantity * self.buy_price
		if self.sold:
			self.total_sold_amount = self.quantity * self.sell_price

@frappe.whitelist()
def add_event(doc, bot_sold):
	doc = json.loads(doc)
	b_or_s = "Bought" if bot_sold=='buy_date' else "Sold"
	user = frappe.db.get_value('User Profile', {"email": frappe.session.user})
	subject = "{0} {1} {2} - {3}".format(b_or_s, doc['quantity'], doc['coin'], doc['market'])
	if not frappe.db.exists('Event', {'subject': subject, 'starts_on': doc[bot_sold], 'description': doc['name']}):
		frappe.get_doc({
			'doctype': 'Event',
			'subject': "{0} {1} {2} - {3}".format(b_or_s, doc['quantity'], doc['coin'], doc['market']),
			'starts_on': doc[bot_sold],
			'send_reminder': 0,
			'description': doc['name'],
			'ref_type': 'User Profile',
			'ref_name': user,
			'my_investments': doc['name']
		}).insert(ignore_permissions=True)
