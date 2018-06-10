# -*- coding: utf-8 -*-
# Copyright (c) 2018, Zlash65 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_years, get_timestamp, flt
from frappe.chat.doctype.chat_message.chat_message import send
from frappe.chat.doctype.chat_room.chat_room import create, is_direct, get_room
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
def get_dashboard_data(username):

	def get_market_price(market, temp):
		for i in temp:
			if market == i['market']:
				return i

	my_coins = frappe.db.get_all("My Investments", fields=['coin', 'market', 'buy_price'], filters={"user_profile": username})

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

@frappe.whitelist()
def send_notification_force():
	send_notification(True)

@frappe.whitelist()
def send_notification(ignore_condition=False):
	users = [d.name for d in frappe.db.get_all("User", filters={"name": ['not in', "Administrator, Guest"]})]
	for user in users:
		user_detail = frappe.db.get_all("User Profile", filters={"email": user}, fields=['username', 'notify_me', 'notify_threshold'])

		if not user_detail: continue
		else: user_detail = user_detail[0]

		if user_detail.notify_me:
			coin_detail = frappe.db.get_all('My Investments', filters={"user_profile": user_detail.username},
				fields=['coin', 'notify_me', 'notify_threshold', 'buy_price'])
		else:
			coin_detail = frappe.db.get_all("My Investments", filters={"user_profile": user_detail.username, 'notify_me': 1},
				fields=['coin', 'notify_me', 'notify_threshold', 'buy_price'])

		if not coin_detail:
			continue

		room = ""
		temp = frappe.session.user
		frappe.session.user = 'trading_bot@hackathon.com'
		if not is_direct('trading_bot@hackathon.com', user):
			room = create('Direct', 'trading_bot@hackathon.com', user)
		else:
			room = get_room('trading_bot@hackathon.com', user)

		for d in coin_detail:
			threshold = d.notify_threshold if d.notify_threshold!=0 else user_detail.notify_threshold

			hike_price = flt(d.buy_price + (d.buy_price * d.notify_threshold)/100, 3)

			data = frappe.db.sql("""
					select distinct cmd.market, cmd.current_sell_price
					from `tabCoin Market Detail` cmd, `tabCoin Exchange` ce
					where cmd.current_sell_price > 519699.0 and ce.from_coin='{0}'
					group by cmd.market order by cmd.current_sell_price desc
				""".format(d.coin), as_dict=True)

			message = []
			for i in data:
				message.append("{0} : {1}".format(i.market, i.current_sell_price))
			message = ' & '.join(message)

			# similar message shouldn't be sent again and again
			message_template = ("{0} price hiked by {1}% \t {2}").format(d.coin, d.notify_threshold, message)
			if not frappe.db.get_value('Chat Message', {'content': message_template}) or ignore_condition:
				frappe.sendmail(recipients=user,
					subject=_("{0} price hiked by {1}%").format(d.coin, threshold),
					message=_(message))
				room = room[0].name

				send('trading_bot@hackathon.com', room, threshold)
