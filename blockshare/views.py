from django.shortcuts import HttpResponse, render

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from urllib.request import urlopen
import json
import sys
import requests

# Function that outputs Bitcoin wallet information.
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

def prices():

    btc_data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin")
    eth_data = requests.get("https://api.coinmarketcap.com/v1/ticker/ethereum")
    ltc_data = requests.get("https://api.coinmarketcap.com/v1/ticker/litecoin")

    bitcoin = btc_data.json()
    ethereum = eth_data.json()
    litecoin = ltc_data.json()

    btc_params = {
        'price': bitcoin[0]['price_usd'],
        'symbol': bitcoin[0]['symbol'],
        'market_cap': bitcoin[0]['market_cap_usd'],
        '24h_%_change': bitcoin[0]['percent_change_24h'],
        'volume': bitcoin[0]['24h_volume_usd']
    }

    eth_params = {
        'price': ethereum[0]['price_usd'],
        'symbol': ethereum[0]['symbol'],
        'market_cap': ethereum[0]['market_cap_usd'],
        '24h_%_change': ethereum[0]['percent_change_24h'],
        'volume': ethereum[0]['24h_volume_usd']
    }

    ltc_params = {
        'price': litecoin[0]['price_usd'],
        'symbol': litecoin[0]['symbol'],
        'market_cap': litecoin[0]['market_cap_usd'],
        '24h_%_change': litecoin[0]['percent_change_24h'],
        'volume': litecoin[0]['24h_volume_usd']
    }

    params = {
        'market_prices': {
            'bitcoin': btc_params,
            'ethereum': eth_params,
            'litecoin': ltc_params
        }
    }

    return params
    print(params)

@api_view(['GET']) 
@payment.required(2500)
def market(request):

    try:
        data = prices()
        response = json.dumps(data, indent=2)
        return HttpResponse(response, status=200)
    except ValueError as e:
        return 'HTTP Status 400 {}'.format(e.args[0]), 400
