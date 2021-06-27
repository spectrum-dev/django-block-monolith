import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from data_blocks.blocks.equity_data.alpha_vantage import search_ticker
from data_blocks.blocks.equity_data.main import run as equity_run
from data_blocks.blocks.crypto_data.main import run as crpto_run

# Create your views here.

# Equity Data (Data Block with ID 1)
# -----------------------------------


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
            start_date = serializers.DateTimeField(required=True)
            end_date = serializers.DateTimeField(required=True)

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


def post_crypto_run(request):
    """
    Runs a data querying process against data source's API
    """
    request_body = json.loads(request.body)

    input = request_body["input"]

    #  TODO: Added this for testing - should be remomved when date ranges are fixed
    input["start_date"] = ""
    input["end_date"] = ""
    response = crpto_run(input)

    return JsonResponse(response)
