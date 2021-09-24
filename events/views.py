from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import requests


class RetrieveEvents(APIView):
    def get(self, request, format=None):
        url = "https://api.opensea.io/api/v1/events"
        querystring = {"only_opensea": "false", "offset": "0", "limit": "20"}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return Response(response.json(), status=status.HTTP_200_OK)
