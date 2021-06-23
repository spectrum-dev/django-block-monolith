import json
import enum

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from signal_blocks.blocks.event_block.main import run

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
        
        if (len(request_body["output"].keys()) < 2):
            raise serializers.ValidationError("You must pass in at least two different streams of data")
        
        response = run(request_body["input"], request_body["output"])

        return JsonResponse({"response": response})