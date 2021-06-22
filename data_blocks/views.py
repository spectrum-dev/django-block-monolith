import json
from django.shortcuts import render

from django.http import JsonResponse

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


def post_equity_run(request):
    """
        Runs a data querying process against data source's API
    """
    request_body = json.loads(request.body)

    input = request_body["input"]

    #  TODO: Added this for testing - should be remomved when date ranges are fixed
    input["start_date"] = ""
    input["end_date"] = ""
    response = equity_run(input)

    return JsonResponse(response)


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
