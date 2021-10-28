import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField


# US Stock Data (Data Block with ID 1)
# -----------------------------------
from data_blocks.us_stock_data.alpha_vantage import search_ticker
from data_blocks.us_stock_data.main import run as us_stock_data_run

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
from data_blocks.crypto_data.supported_crypto import SUPPORTED_CRYPTO
from data_blocks.crypto_data.main import run as crypto_run


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


class CryptoRunView(APIView):
    def post(self, request):
        class Candlestick(enum.Enum):
            ONE_MINUTE = "1min"
            FIVE_MINUTE = "5min"
            FIFTEEN_MINUTE = "15min"
            THIRTY_MINUTE = "30min"
            SIXTY_MINUTE = "60min"
            ONE_DAY = "1day"
            ONE_WEEK = "1week"
            ONE_MONTH = "1month"

        class InputSerializer(serializers.Serializer):
            crypto_name = serializers.CharField(max_length=10, required=True)
            candlestick = EnumField(choices=Candlestick)
            start_date = serializers.CharField(max_length=20)
            end_date = serializers.CharField(max_length=20)

            def validate(self, data):
                if data["start_date"] > data["end_date"]:
                    raise serializers.ValidationError("finish must occur after start")
                return data

        request_body = json.loads(request.body)
        input = request_body["input"]
        if InputSerializer(data=input).is_valid(raise_exception=True):
            response = crypto_run(input)

        return JsonResponse(response)


# Screener Data (Data Block with ID 3)
# -----------------------------------


def get_screener_exchanges(request):
    response_payload = [
        "US",
        "KLSE",
    ]
    return JsonResponse({"response": response_payload})


def get_screener_candlesticks(request):
    response_payload = [
        "1day",
    ]
    return JsonResponse({"response": response_payload})
