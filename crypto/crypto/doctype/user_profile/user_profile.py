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

@frappe.whitelist()
def get_dashboard_data():

	def get_market_price(market, temp):
		for i in temp:
			if market == i['market']:
				return i

	my_coins = frappe.db.get_all("My Investments", fields=['coin', 'market', 'buy_price'])

	distinct_market = [d.name for d in frappe.db.get_all("Market")]
	columns = ["Coin", "Bought at"]
	columns.extend(distinct_market)

	data = []
	for coin in my_coins:
		coin_parent = "{0} - INR".format(coin.coin)
		temp = frappe.db.sql("""
			select distinct market, parent, current_sell_price
			from `tabCoin Market Detail`
			where market in ({0}) and parent='{1}'
			order by modified desc limit {2}
			""".format(', '.join(["'%s'" % d for d in distinct_market]), coin_parent, len(distinct_market)), as_dict=True)

		if not temp:
			continue

		out = []
		out.append(coin.coin)
		out.append("{0} ( {1} )".format(coin.buy_price, coin.market))
		for i in distinct_market:
			current = get_market_price(i, temp)
			out.append(current['current_sell_price'])
		data.append(out)

	out = {}
	out["columns"] = columns
	out["data"] = data
	return out
