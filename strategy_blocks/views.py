import json
from django.shortcuts import render

from django.http import (
    JsonResponse
)

from strategy_blocks.blocks.backtest.main import run

# Create your views here.

# Backtest (Strategy Block with ID 1)
# --------------------------------------------------

def post_run(request):
    request_body = json.loads(request.body)
    
    input = request_body["input"]
    output = request_body["output"]

    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "DATA_BLOCK":
            data_block = output[key]
            break
    
    signal_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "SIGNAL_BLOCK":
            data_block = output[key]
            break

    port_vals, trades = run(input, data_block, signal_block)

    response = {
        "response": {
            "portVals": port_vals,
            "trades": trades
        }
    }

    return JsonResponse(response)