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
def get_equity_types(request):
    """
        Gets a list of supported equity types
    """
    response_payload = [ "STOCKS" ]
    return JsonResponse({"response": response_payload})

def get_equity_regions(request):
    """
        Get list of supported equity regions
    """
    response_payload = [ "US" ]
    return JsonResponse({"response": response_payload})

def post_run(request):
    """
        Runs a data querying process against data source's API
    """
    request_body = json.loads(request.body)
    input = request_body["input"]
    
    response = run(input)

    return JsonResponse(response)