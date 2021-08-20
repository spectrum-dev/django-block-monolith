import json
import enum

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from strategy_blocks.blocks.simple_backtest.main import run


# Create your views here.

# Backtest (Strategy Block with ID 1)
# ------------------------------------

class PostRun(APIView):
    def post(self, request):
        class TradeAmountUnit(enum.Enum):
            PERCENTAGE = "PERCENTAGE"

        class InputSerializer(serializers.Serializer):
            start_value = serializers.FloatField()
            commission = serializers.FloatField()
            trade_amount_value = serializers.FloatField()
            # TODO: Comment this in if decide to maintain this field
            # trade_amount_unit = EnumField(choices=TradeAmountUnit)

            def validate(self, data):
                if data["start_value"] <= 0.00:
                    raise serializers.ValidationError(
                        "Start value must be greater than 0"
                    )
                return data

        def validate_output(output):
            keys = output.keys()
            if len(output.keys()) < 2:
                raise serializers.ValidationError(
                    {"outputs_error": "You must have at least two output keys"}
                )

            block_types = []
            for key in keys:
                block_types.append(key.split("-")[0])

            if "DATA_BLOCK" not in block_types:
                raise serializers.ValidationError(
                    {
                        "outputs_error": "You must have a DATA_BLOCK in the outputs payload"
                    }
                )

            if "SIGNAL_BLOCK" not in block_types:
                raise serializers.ValidationError(
                    {
                        "outputs_error": "You must have a SIGNAL_BLOCK in the outputs payload"
                    }
                )

            is_valid = True
            for key in keys:
                is_valid = is_valid and len(output[key]) > 0

            if not is_valid:
                raise serializers.ValidationError(
                    {"outputs_error": "Data for outputs must have more than one entry"}
                )

        request_body = json.loads(request.body)

        input = request_body["input"]
        output = request_body["output"]

        InputSerializer(data=input).is_valid(raise_exception=True)
        validate_output(output)

        response = run(input, output)

        return JsonResponse(response)
