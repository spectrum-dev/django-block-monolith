from django.http import JsonResponse

from computational_blocks.one.mappings import INDICATORS


# Technical Analysis (Computational Block with ID 1)
# --------------------------------------------------

# Dropdowns
def get_indicators(request):
    response = {"response": list(INDICATORS.keys())}

    return JsonResponse(response)


def get_indiciator_fields(request):
    indicator_name = request.GET.get("indicatorName", None)

    indicator_information = INDICATORS.get(indicator_name)

    if not indicator_information:
        return JsonResponse({"error": f"The indicator {indicator_name} was not found"})

    return JsonResponse({"response": indicator_information["params"]})


# Operation Block (Computational Block with ID 2)
# --------------------------------------------------

# Dropdowns
def get_operation_types(request):
    response = {
        "response": [
            "+",
            "-",
            "*",
            "/",
            "^",
        ]
    }
    return JsonResponse(response)
