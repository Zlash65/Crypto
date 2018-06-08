# -*- coding: utf-8 -*-
# Copyright (c) 2018, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CoinExchange(Document):
	def autoname(self):
		self.name = "{0} - {1}".format(frappe.db.escape(self.to_coin), frappe.db.escape(self.from_coin))
