from django.shortcuts import HttpResponse, render

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import sys
import requests

def ethereum_market_price():
	""" 
	Scrape coinmarketcap website using Beautiful Soup and return data in json format. 
	Input: url = "https://coinmarketcap.com/currencies/<currency>/
	Ouput:
	{
		'name': 'currency name',
		'symbol': 'currency symbol',
		'price': 'currency price',
		'market_cap': 'market capitalization',
		'volume': 'volume',
		'supply': 'supply'
	}
	"""

	eth_url = "https://coinmarketcap.com/currencies/ethereum/"
	data = urlopen(eth_url)
	soup = BeautifulSoup(data, 'html.parser')

	symbol = soup.findAll(attrs={"class": "bold"})
	symbol = symbol[0].string

	ether = soup.findAll(attrs={"class": "text-large"})
	price = ether[1].string

	table = soup.find('table')
	cols = table.findAll('td')

	market_cap = cols[0].find('small').string
	volume = cols[1].find('small').string
	supply = cols[2].find('small').string

	data = {
		'name': 'ethereum',
		'symbol': symbol,
		'price': price,
		'market_cap': market_cap,
		'volume': volume,
		'supply': supply
	}

	return data

def bitcoin_market_price():
	""" 
	Scrape coinmarketcap website using Beautiful Soup and return data in json format. 
	Input: url = "https://coinmarketcap.com/currencies/<currency>/
	Ouput:
	{
		'name': 'currency name',
		'symbol': 'currency symbol',
		'price': 'currency price',
		'market_cap': 'market capitalization',
		'volume': 'volume',
		'supply': 'supply'
	}
	"""

	url = "https://coinmarketcap.com/currencies/bitcoin/"
	data = urlopen(url)
	soup = BeautifulSoup(data, 'html.parser')

	symbol = soup.findAll(attrs={"class": "bold"})
	symbol = symbol[0].string

	bitcoin = soup.findAll(attrs={"class": "text-large"})
	price = bitcoin[1].string

	table = soup.find('table')
	cols = table.findAll('td')

	market_cap = cols[0].find('small').string
	volume = cols[1].find('small').string
	supply = cols[2].find('small').string
	
	data = {
		'name': 'bitcoin',
		'symbol': symbol,
		'price': price,
		'market_cap': market_cap,
		'volume': volume,
		'supply': supply
	}

	return data



def index(request):
    parsed_data = []
    if request.method == 'POST':
        addr = request.POST.get('address')
        response = requests.get('https://api.blockcypher.com/v1/btc/main/addrs/' + addr)
        json_list = []
        json_list.append(response.json())
        parsed_data = []
        btc_data = {}
        for data in json_list:
            if data['final_n_tx'] != 0 or not data:
                btc_data['address'] = data['address']
                btc_data['final_balance'] = data['final_balance'] * 0.00000001
                btc_data['total_sent'] = data['total_sent'] * 0.00000001
                btc_data['total_received'] = data['total_received'] * 0.00000001
                btc_data['block_height'] = data['txrefs'][0]['block_height']
                btc_data['confirmations'] = data['txrefs'][0]['confirmations']
            else:
                btc_data['address'] = data['address']
                btc_data['final_balance'] = data['final_balance'] * 0.00000001
                btc_data['total_sent'] = data['total_sent'] * 0.00000001
                btc_data['total_received'] = data['total_received'] * 0.00000001
                btc_data['block_height'] = "Unavailable"
                btc_data['confirmations'] = "Unavailable"
        parsed_data.append(btc_data)
    return render(request, '../templates/profile.html', {'data': parsed_data})


@api_view(['GET']) 
@payment.required(5000)
def bitcoin(request):

    try:	
        data = bitcoin_market_price()
        response = json.dumps(data, indent=2)
        return HttpResponse(response, status=200)
    except ValueError as e:
        return 'HTTP Status 400 {}'.format(e.args[0]), 400
    

@api_view(['GET'])
@payment.required(5000)
def ether(request):

    try:
        data = ethereum_market_price()
        response = json.dumps(data, indent=2)
        return HttpResponse(response, status=200)
    except ValueError as e:
        return 'HTTP Status 400 {}'.format(e.args[0]), 400

