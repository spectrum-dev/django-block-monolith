from django.http import JsonResponse

# Event Block (Signal Block with ID 1)
# ------------------------------------


def get_event_actions(request):
    """
    Retrieves a list of supported event actions
    """
    response = {"response": ["BUY", "SELL"]}

    return JsonResponse(response)


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
