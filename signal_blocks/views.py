from django.shortcuts import render

from django.http import (
    JsonResponse
)

# Create your views here.

# Event Block (Signal Block with ID 1)
# ------------------------------------

def get_event_types(request):
    """
        Retrieves a list of supported event types
    """
    response = {
        "response": ["INTERSECT"]
    }
    
    JsonResponse(response)

def get_event_actions(request):
    """
        Retrieves a list of supported event actions
    """
    response = {
        "response": ["BUY"]
    }

    JsonResponse(response)

def post_run(request):
    pass