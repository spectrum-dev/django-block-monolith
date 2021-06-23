import json
import enum

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from strategy_blocks.blocks.backtest.main import run


# Create your views here.

# Backtest (Strategy Block with ID 1)
# ------------------------------------

class PostRun(APIView):
    def post(self, request):
        class TradeAmountUnit(enum.Enum):
            PERCENTAGE = "PERCENTAGE"
        class InputSerializer(serializers.Serializer):
            start_value = serializers.DecimalField(decimal_places=2)
            commission = serializers.DecimalField(decimal_places=2)
            impact = serializers.DecimalField()
            stop_loss = serializers.DecimalField()
            take_profit = serializers.DecimalField()
            trade_amount_value = serializers.DecimalField()
            trade_amount_unit = EnumField(choices=TradeAmountUnit)

        request_body = json.loads(request.body)

        input = request_body["input"]
        output = request_body["output"]

        InputSerializer(data=input).is_valid(raise_exception=True)

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
                signal_block = output[key]
                break

        port_vals, trades = run(input, data_block, signal_block)

        response = {"response": {"portVals": port_vals, "trades": trades}}

        return JsonResponse(response)