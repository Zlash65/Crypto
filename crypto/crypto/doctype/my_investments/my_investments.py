# -*- coding: utf-8 -*-
# Copyright (c) 2018, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
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
