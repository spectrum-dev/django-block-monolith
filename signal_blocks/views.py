import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from signal_blocks.blocks.event_block.main import run as signal_block_run
from signal_blocks.blocks.saddle_block.main import run as saddle_block_run
from signal_blocks.blocks.and_block.main import run as and_run
from signal_blocks.blocks.or_block.main import run as or_run


# Create your views here.

# Event Block (Signal Block with ID 1)
# ------------------------------------


def get_event_types(request):
    """
    Retrieves a list of supported event types
    """
    response = {"response": ["INTERSECT"]}

    return JsonResponse(response)


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

        class EventType(enum.Enum):
            INTERSECT = "INTERSECT"

        class EventAction(enum.Enum):
            BUY = "BUY"
            SELL = "SELL"

        class InputSerializer(serializers.Serializer):
            event_type = EnumField(choices=EventType)
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
    print("Getting Saddle Type")
    response = {"response": ["DOWNWARD", "UPWARD"]}
    print("Response: ", response)

    return JsonResponse(response)


class PostSaddleRun(APIView):
    def post(self, request):
        """
        Runs the event block
        """

        class EventType(enum.Enum):
            UPWARD = "UPWARD"
            DOWNWARD = "DOWNWARD"

        class EventAction(enum.Enum):
            BUY = "BUY"
            SELL = "SELL"

        class InputSerializer(serializers.Serializer):
            saddle_type = EnumField(choices=EventType)
            event_action = EnumField(choices=EventAction)
            consecutive_up = serializers.CharField()
            consecutive_down = serializers.CharField()

        request_body = json.loads(request.body)

        response = []
        InputSerializer(data=request_body["input"]).is_valid(raise_exception=True)

        if len(request_body["output"].keys()) > 1:
            return JsonResponse(
                {"non_field_errors": ["You must pass in at most one stream of data"]},
                status=400,
            )

        response = saddle_block_run(request_body["input"], request_body["output"])

        return JsonResponse({"response": response})


class PostAndRunView(APIView):
    def post(self, request):
        request_body = json.loads(request.body)

        if len(request_body["output"].keys()) < 2:
            return JsonResponse(
                {"non_field_errors": ["You must pass in at least two streams of data"]},
                status=400,
            )

        response = and_run(request_body["output"])

        return JsonResponse({"response": response})


class PostOrRunView(APIView):
    """
    Runs an OR logic on output of 2 or more Signal Blocks
    """

    def post(self, request):

        request_body = json.loads(request.body)

        if len(request_body["output"].keys()) < 2:
            return JsonResponse(
                {"non_field_errors": ["You must pass in at least two streams of data"]},
                status=400,
            )

        response = or_run(request_body["output"])

        return JsonResponse({"response": response})
