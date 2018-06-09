import frappe
import requests

def get_data(doc):
	''' request data from api link and normalize it for consistency '''
	response = requests.get(doc.api_link)
	value = response.json()

	out = []

	for d in value:
		try:
			temp = {
				'market': doc.market,
				'from_coin': d,
				'to_coin': 'INR',
				'current_ask_price': value[d]['yes_price'],
				'last_trade_price': value[d]['last_traded_price'],
				'current_sell_price': value[d]['lowest_sell_bid'],
				'volume': value[d]['volume']['volume'],
				'highest_buy_bid': value[d]['volume']['max'],
				'lowest_sell_bid': value[d]['volume']['min']
			}

			out.append(temp)
		except:
			pass
	
	return out