import json

from django.shortcuts import render

from django.http import JsonResponse

from computational_blocks.blocks.technical_analysis.mappings import INDICATORS
from computational_blocks.blocks.technical_analysis.main import run

# Create your views here.

# Technical Analysis (Computational Block with ID 1)
# --------------------------------------------------

# Dropdowns
def get_indicators(request):
    response = {"response": list(INDICATORS.keys())}

    return JsonResponse(response)


def get_indiciator_fields(request):
    indicator_name = request.GET.get("indicatorName", None)

    indicator_information = INDICATORS.get(indicator_name)

    response = []
    for indicator in indicator_information["params"]:
        if "values" in indicator:
            response.append(
                {
                    "fieldName": indicator["name"],
                    "fieldType": "dropdown",
                    "fieldVariableName": indicator["internalName"],
                    "fieldData": {"options": indicator["values"]},
                }
            )
        else:
            response.append(
                {
                    "fieldName": indicator["name"],
                    "fieldType": "input",
                    "fieldVariableName": indicator["internalName"],
                }
            )

    if indicator_information:
        response = {"response": response}
    else:
        response = {"error": f"The indicator {indicator_name} was not found"}

    return JsonResponse(response)


# Runner
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

    response = run(input, data_block)

    return JsonResponse({"response": response})
