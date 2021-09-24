from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests


class RetrieveOrder(APIView):
    def get(self, request, slug, format=None):
        # 0x06012c8cf97bead5deae237070f9587f8e7a266d
        if slug:
            url = "https://api.opensea.io/wyvern/v1/orders"
            querystring = {
                "bundled": "false",
                "include_bundled": "false",
                "include_invalid": "false",
                "limit": "20",
                "offset": "0",
                "order_by": "created_date",
                "order_direction": "desc"
            }
            headers = {"Accept": "application/json"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == status.HTTP_200_OK:
                return Response(response.json(), status=status.HTTP_200_OK)
        else:
            raise Http404
        return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
