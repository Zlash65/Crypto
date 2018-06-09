# -*- coding: utf-8 -*-
# Copyright (c) 2018, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_years, get_timestamp
from six import iteritems

class UserProfile(Document):
	def get_feed(self):
		return self.name

	def autoname(self):
		self.name = self.username or self.email

@frappe.whitelist()
def get_timeline_data(doctype, name):
	'''returns timeline data for the past one year'''
	from frappe.desk.form.load import get_communication_data
	print(doctype, name, "here")
	out = {}
	fields = 'date(creation), count(name)'
	after = add_years(None, -1).strftime('%Y-%m-%d')
	group_by='group by date(creation)'

	data = get_communication_data(doctype, name,
		fields=fields, after=after, group_by=group_by, as_dict=False)

	# fetch and append data from Activity Log
	data += frappe.db.sql("""select {fields}
		from `tabActivity Log`
		where reference_doctype='{doctype}' and reference_name='{name}'
		and status!='Success' and creation > {after}
		{group_by} order by creation desc
		""".format(doctype=doctype, name=name, fields=fields,
			group_by=group_by, after=after), as_dict=False)

	timeline_items = dict(data)

	for date, count in iteritems(timeline_items):
		timestamp = get_timestamp(date)
		out.update({ timestamp: count })

	return out
