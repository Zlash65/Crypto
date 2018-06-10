from __future__ import unicode_literals
import frappe
import imp
from frappe import _
from frappe.model.document import Document

class MarketAPI(Document):
	def autoname(self):
		self.name = "{0} - api".format(frappe.db.escape(self.market))

@frappe.whitelist()
def fetch_from_api():
	'''
		query all markets api added and commonify their data

		Add the api file for a new market in the apis folder and map the data to the existing schema
	'''
	markets = frappe.db.get_all("Market API", fields=['*'])

	data = []
	for d in markets:
		try:
			exec "from crypto.crypto.doctype.market_api.apis.%s import get_data" % frappe.scrub(d.name.replace(" ", ""))
			data.extend(get_data(d))
		except ImportError:
			frappe.msgprint(_('Create a connector file for {0} api inside apis folder.'.format(d.market)))

	withdrawal_fees = frappe.db.get_all("Withdrawal Fees", fields=['parent', 'coin', 'rate'])
	wfees = {}
	for d in withdrawal_fees:
		temp = {}
		temp[d.coin] = d.rate
		if d.parent not in wfees:
			wfees[d.parent] = temp
		else:
			wfees[d.parent][d.coin] = d.rate

	all_exchange = [d.name for d in frappe.db.get_all('Coin Exchange') if d]
	for d in data:
		name = "{0} - {1}".format(frappe.db.escape(d['from_coin']), frappe.db.escape(d['to_coin']))
		from_coin = d['from_coin']
		to_coin = d['to_coin']
		del d['from_coin']
		del d['to_coin']
		d.update({"doctype": "Coin Market Detail"})
		if from_coin in wfees[d['market']]:
			d.update({"exchange_rate": wfees[d['market']][from_coin]})

		if name in all_exchange:
			doc = frappe.get_doc('Coin Exchange', name)
			doc.append("markets", d)
			doc.save()
		else:
			doc = frappe.new_doc("Coin Exchange")
			doc.from_coin = from_coin
			doc.to_coin = to_coin

			doc.append("markets", d)
			doc.insert()
			all_exchange.append(doc.name)
