from django.http import JsonResponse

# Screener Data (Data Block with ID 3)
# -----------------------------------


def get_screener_exchanges(request):
    response_payload = [
        "US",
        "KLSE",
    ]
    return JsonResponse({"response": response_payload})


def get_screener_candlesticks(request):
    response_payload = [
        "1day",
    ]
    return JsonResponse({"response": response_payload})
