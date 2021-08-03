import enum

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_enumfield import EnumField

# Create your views here.

class AndRunView(APIView):
    def post(self, request):
        pass