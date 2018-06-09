import frappe
import requests

def get_data(doc):
	''' request data from api link and normalize it for consistency '''
	response = requests.get(doc.api_link)
	value = response.json()

	out = []

	for d in value:

		from_currency, to_curreny = value[d]['name'].split('/')
		temp = {
			'market': doc.market,
			'from_coin': from_currency,
			'to_coin': 'INR',
			'current_ask_price': value[d]['buy'],
			'last_trade_price': value[d]['last'],
			'current_sell_price': value[d]['sell'],
			'volume': value[d]['volume'],
			'highest_buy_bid': value[d]['high'],
			'lowest_sell_bid': value[d]['low']
		}

		out.append(temp)
	
	return out