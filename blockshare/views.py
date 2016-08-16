from django.shortcuts import HttpResponse, render

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

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


from blockshare.scrape import bitcoin_market_price, ethereum_market_price

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
