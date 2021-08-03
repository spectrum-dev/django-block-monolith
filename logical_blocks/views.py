import json
import enum

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

from logical_blocks.blocks.and_block.main import main

# Create your views here.

class AndRunView(APIView):
    def post(self, request):
        request_body = json.loads(request.body)

        if len(request_body["output"].keys()) < 2:
            return JsonResponse(
                {"non_field_errors": ["You must pass in at least two streams of data"]},
                status=400,
            )

        response = main(request_body['output'])

        return JsonResponse({"response": response})
