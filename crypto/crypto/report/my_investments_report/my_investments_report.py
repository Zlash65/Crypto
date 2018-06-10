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
	if filters:
		condition = "and child.parent like '%{0}%'".format(filters.coin)
	else:
		cond = []
		for d in get_my_coins():
			cond.append("(child.parent like '%{0}%')".format(d))
		condition = "and (" + " or ".join(cond) + ")" if cond else ""


	all_data = frappe.db.sql("""
		select parent.from_coin, parent.to_coin, child.market, child.current_ask_price,
		child.current_sell_price, child.volume, child.exchange_rate, child.last_trade_price,
		child.highest_buy_bid, child.lowest_sell_bid,
		(child.current_sell_price - child.current_ask_price - child.exchange_rate) as profit
		from `tabCoin Exchange` parent, `tabCoin Market Detail` child
		where child.parent=parent.name {0}
		order by parent.from_coin, profit desc""".format(condition), as_dict=True, debug=1)

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


@frappe.whitelist()
def get_my_coins(sold=False):
	condition = ""
	if sold:
		condition = " and sold=0"
	user = frappe.db.get_value("User Profile", {"email": frappe.session.user})
	my_coins = [d.coin for d in frappe.db.sql("""select distinct coin from `tabMy Investments` where user_profile='{0}' {1}""".format(user, condition), as_dict=True)]

	return my_coins