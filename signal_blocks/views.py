import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from signal_blocks.intersect_block.main import run as signal_block_run
from signal_blocks.saddle_block.main import run as saddle_block_run
from signal_blocks.and_block.main import run as and_run
from signal_blocks.or_block.main import run as or_run
from signal_blocks.crossover_block.main import run as crossover_block_run
from signal_blocks.candle_close_block.main import run as candle_close_run


# Event Block (Signal Block with ID 1)
# ------------------------------------

def get_event_actions(request):
    """
    Retrieves a list of supported event actions
    """
    response = {"response": ["BUY", "SELL"]}

    return JsonResponse(response)


class PostRun(APIView):
    def post(self, request):
        """
        Runs the event block
        """

        class EventAction(enum.Enum):
            BUY = "BUY"
            SELL = "SELL"

        class InputSerializer(serializers.Serializer):
            event_action = EnumField(choices=EventAction)

        request_body = json.loads(request.body)

        response = []
        InputSerializer(data=request_body["input"]).is_valid(raise_exception=True)

        if len(request_body["output"].keys()) < 2:
            return JsonResponse(
                {
                    "non_field_errors": [
                        "You must pass in at least two different streams of data"
                    ]
                },
                status=400,
            )

        response = signal_block_run(request_body["input"], request_body["output"])

        return JsonResponse({"response": response})


# Saddle Block (Signal Block with ID 2)
# ------------------------------------


def get_saddle_types(request):
    """
    Retrieves a list of supported event types
    """
    response = {"response": ["DOWNWARD", "UPWARD"]}

    return JsonResponse(response)



# Cross-Over Block (Signal Block with ID 4)
# ------------------------------------


def get_crossover_types(request):
    """
    Retrieves a list of supported crossover types
    """
    response = {"response": ["ABOVE", "BELOW"]}

    return JsonResponse(response)

# Candle Close Green Block (Signal Block with ID 6)
# ------------------------------------


def get_candle_close_types(request):
    """
    Retrieves a list of supported candle close condition types
    """
    response = {
        "response": [
            "CLOSE_ABOVE_OPEN",
            "CLOSE_BELOW_OPEN",
            "CLOSE_EQ_HIGH",
            "CLOSE_BELOW_HIGH",
            "CLOSE_ABOVE_LOW",
            "CLOSE_EQ_LOW",
        ]
    }

    return JsonResponse(response)

# Comparison Block (Signal Block with ID 7)
# ------------------------------------


def get_comparison_types(request):
    """
    Retrieves a list of supported logical comparison types
    """
    response = {
        "response": [
            "<",
            "<=",
            ">",
            ">=",
        ]
    }

    return JsonResponse(response)
