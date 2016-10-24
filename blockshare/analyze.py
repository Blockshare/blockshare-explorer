from django.shortcuts import HttpResponse, render

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
from blockshare.settings import GOOGLE_APPLICATION_CREDENTIALS

import json
import sys
import os

def analysis():

    #text = request.args.get('text')
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)

    service = discovery.build('language', 'v1beta1', http=http)

    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': 'Buy all the Bitcoin with Apple iPhones and such',
        }
    }

    response_one = service.documents().analyzeEntities(body=body).execute()
    response_two = service.documents().analyzeSentiment(body=body).execute()
    response = response_one, response_two
    return response


@api_view(['GET'])
@payment.required(10000)
def machine_learning(request):

    try:
        data = analysis()
        response = json.dumps(data, indent=2)
        return HttpResponse(response, status=200)
    except ValueError as e:
        return 'HTTP Status {}'.format(e.args[0]), 400

