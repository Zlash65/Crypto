import frappe
import requests

def get_data(doc):
	''' request data from api link and normalize it for consistency '''
	response = requests.get(doc.api_link)
	value = response.json()

	out = []
	current_prices = value['prices']['inr']
	stats = value['stats']['inr']

	for d in stats:
		temp = {
			'market': doc.market,
			'from_coin': d,
			'to_coin': 'INR',
			'current_ask_price': current_prices[d],
			'last_trade_price': stats[d]['last_traded_price'],
			'current_sell_price': stats[d]['last_traded_price'],
			'volume': stats[d]['trade_volume'],
			'highest_buy_bid': stats[d]['highest_bid'],
			'lowest_sell_bid': stats[d]['lowest_ask']
		}

		out.append(temp)
	
	return out