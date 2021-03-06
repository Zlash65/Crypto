# Copyright (c) 2013, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns = get_columns()

	data = get_data(columns, filters)

	return columns, data

def get_columns():
	return ['Coin', 'Market', 'Profit', 'Current Ask Price', 'Current Sell Price', 'Volume',
		'Exchange Rate', 'Last Trade Price', 'Highest Buy Bid', 'Lowest Sell Bid']

def get_data(columns, filters=None):
	frappe.errprint(filters.coin)
	condition = "and child.parent like '%{0}%'".format(filters.coin) if filters else ""

	all_data = frappe.db.sql("""
		select parent.from_coin, parent.to_coin, child.market, child.current_ask_price,
		child.current_sell_price, child.volume, child.exchange_rate, child.last_trade_price,
		child.highest_buy_bid, child.lowest_sell_bid,
		(child.current_sell_price - child.current_ask_price - child.exchange_rate) as profit
		from `tabCoin Exchange` parent, `tabCoin Market Detail` child
		where child.parent=parent.name {0}
		order by parent.from_coin, profit desc""".format(condition), as_dict=True)

	data = {}
	for d in all_data:
		data.setdefault(d.from_coin, []).append(d)

	out = []
	for d in data:
		added = []
		for k in data[d]:
			temp = []
			if not k.market in added:
				added.append(k.market)
				temp.append(d)
				temp.append(k['market'])
				for j in columns[2:]:
					temp.append(flt(k[frappe.scrub(j)], 4))
				out.append(temp)
		out.append([''] * len(columns))

	return out
