import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField


# US Stock Data (Data Block with ID 1)
# -----------------------------------
from data_blocks.one.alpha_vantage import search_ticker
from data_blocks.one.main import run as us_stock_data_run

# Dropdowns
def get_equity_name(request):
    """
    Gets a list of supported equity names (search)
    """
    ticker_fuzzy_name = request.GET.get("name")
    if ticker_fuzzy_name:
        response = search_ticker(ticker_fuzzy_name)
    else:
        response = {"response": []}

    return JsonResponse(response)


def get_crypto_candlesticks(request):
    response_payload = [
        "1min",
        "5min",
        "15min",
        "30min",
        "60min",
        "1day",
        "1week",
        "1month",
    ]
    return JsonResponse({"response": response_payload})


# Crypto Data (Data Block with ID 2)
# -----------------------------------
from data_blocks.two.supported_crypto import SUPPORTED_CRYPTO
from data_blocks.two.main import run as crypto_run


def get_symbol(request):
    crypto_fuzzy_name = str(request.GET.get("name")).lower()

    response = []
    for value in SUPPORTED_CRYPTO:
        currency_code = value["currency_code"].lower()
        currency_name = value["currency_name"].lower()
        if (
            currency_code.find(crypto_fuzzy_name) != -1
            or currency_name.find(crypto_fuzzy_name) != -1
        ):
            response.append(
                {
                    "value": value["currency_code"],
                    "label": f'{value["currency_name"]} ({value["currency_code"]})',
                }
            )

    return JsonResponse({"response": response})


def get_us_stock_data_candlesticks(request):
    response_payload = [
        "1min",
        "5min",
        "15min",
        "30min",
        "60min",
        "1day",
        "1week",
        "1month",
    ]
    return JsonResponse({"response": response_payload})
