import json

from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.views import APIView

from computational_blocks.blocks.technical_analysis.mappings import INDICATORS
from computational_blocks.blocks.technical_analysis.main import run


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

    response = []
    for indicator in indicator_information["params"]:
        response.append(
            {
                "fieldName": indicator["name"],
                "fieldType": "input",
                "fieldVariableName": indicator["internalName"],
            }
        )

    return JsonResponse({"response": response})


def process_technical_analysis_run(input, output):
    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "DATA_BLOCK":
            data_block = output[key]
            break

    return run(input, data_block)

class TechnicalAnalysisRunView(APIView):
    def post(self, request):
        request_body = json.loads(request.body)

        input = request_body["input"]
        output = request_body["output"]

        response = process_technical_analysis_run(input, output)

        return JsonResponse({"response": response})
