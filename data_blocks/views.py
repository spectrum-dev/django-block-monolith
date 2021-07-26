import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField


# Create your views here.

# Equity Data (Data Block with ID 1)
# -----------------------------------
from data_blocks.blocks.equity_data.alpha_vantage import search_ticker
from data_blocks.blocks.equity_data.main import run as equity_run

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


def get_data_type(request):
    """
    Gets list of data typed
    """
    response_payload = ["intraday", "daily_adjusted"]
    return JsonResponse({"response": response_payload})


def get_interval(request):
    """
    Gets supported intervals
    """
    response_payload = ["1min"]
    return JsonResponse({"response": response_payload})


def get_output_size(request):
    """
    Gets supported output size
    """
    response_payload = ["compact", "full"]
    return JsonResponse({"response": response_payload})


class EquityRunView(APIView):
    def post(self, request):
        """
        Runs a data querying process against data source's API
        """

        class DataType(enum.Enum):
            INTRADAY = "intraday"
            DAILY_ADJUSTED = "daily_adjusted"

        class Interval(enum.Enum):
            ONE_MINUTE = "1min"
            FIVE_MINUTES = "5min"

        class OutputSize(enum.Enum):
            COMPACT = "compact"
            FULL = "full"

        class InputSerializer(serializers.Serializer):
            equity_name = serializers.CharField(max_length=10, required=True)
            data_type = EnumField(choices=DataType)
            interval = EnumField(choices=Interval)
            outputsize = EnumField(choices=OutputSize)
            start_date = serializers.CharField(max_length=20)
            end_date = serializers.CharField(max_length=20)

            def validate(self, data):
                if data["start_date"] > data["end_date"]:
                    raise serializers.ValidationError("finish must occur after start")
                return data

        request_body = json.loads(request.body)
        input = request_body["input"]

        response = {"response": []}
        if InputSerializer(data=input).is_valid(raise_exception=True):
            response = equity_run(input)

        return JsonResponse(response)


# Crypto Data (Data Block with ID 2)
# -----------------------------------
from data_blocks.blocks.crypto_data.supported_crypto import SUPPORTED_CRYPTO
from data_blocks.blocks.crypto_data.main import run as crpto_run


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
                {"value": value["currency_code"], "label": value["currency_name"]}
            )

    return JsonResponse({"response": response})


def get_candlesticks(request):
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
            response = crpto_run(input)

        return JsonResponse(response)
