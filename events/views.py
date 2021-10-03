from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import requests


WEI = 10 ** 18


class RetrieveEvents(APIView):
    def get(self, request, slug, format=None):
        if slug:
            # Iterate through events api with offset
            # 0.6 second delay
            # logic to pull from db if such records already exist
            # ^ dependent on timestamp in database and use it as part of the occured_before value
            url = "https://api.opensea.io/api/v1/events"
            querystring = {
                "collection_slug": slug,
                "event_type": "successful",
                "only_opensea": "true",
                "offset": "0",
                "limit": "300",
                "occurred_after": ""
            }
            headers = {
                "Accept": "application/json"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            json = response.json()["asset_events"]
            if response.status_code == status.HTTP_200_OK and len(json) > 0:
                return Response(response.json(), status=status.HTTP_200_OK)
        return Response("An error occurred.", status=status.HTTP_404_NOT_FOUND)
