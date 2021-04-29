import json
from django.shortcuts import render

from django.http import (
    JsonResponse
)

from data_blocks.blocks.equity_data_block.main import run

# Create your views here.

# Equity Data (Data Block with ID 1)
# -----------------------------------


# Dropdowns
def get_equity_name(request):
    """
        Gets a list of supported equity names (search)
    """
    response_payload = ["AAPL"]
    return JsonResponse({"response": response_payload})


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
    response_payload = ["full"]
    return JsonResponse({"response": response_payload})

def post_run(request):
    """
        Runs a data querying process against data source's API
    """
    request_body = json.loads(request.body)

    input = request_body["input"]

    #  TODO: Added this for testing - should be remomved when date ranges are fixed
    input["start_date"] = ""
    input["end_date"] = ""

    response = run(input)

    return JsonResponse(response)
