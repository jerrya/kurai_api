from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from events.models import Event
from events.serializers import EventSerializer
import time

WEI = 10 ** 18
API_PAGINATION_LIMIT = 300

class RetrieveEvents(APIView):
    def get(self, request, slug, format=None):
        if slug:
            # save data to db
            # Iterate through events api with offset
            # 0.6 second delay
            # logic to pull from db if such records already exist
            # ^ dependent on timestamp in database and use it as part of the occurred_before value
            data = []
            url = "https://api.opensea.io/api/v1/events"
            i = 0
            while True:
                querystring = {
                    "collection_slug": slug,
                    "event_type": "successful",
                    "only_opensea": "true",
                    "offset": str(i*API_PAGINATION_LIMIT),
                    "limit": str(API_PAGINATION_LIMIT),
                    # "occurred_after": "" # TODO
                }
                headers = {"Accept": "application/json"}

                response = requests.request("GET", url, headers=headers, params=querystring)
                json = response.json()["asset_events"]
                if response.status_code == status.HTTP_200_OK and len(json) > 0:
                    print("Looping through offset {}".format(i*API_PAGINATION_LIMIT))
                    for trade in json:
                        if trade["transaction"]["timestamp"] is None:
                            continue
                        try:
                            e = Event.objects.create(
                                collection_slug=trade["asset"]["collection"]["slug"],
                                buyer_address=trade["winner_account"]["address"],
                                seller_address=trade["seller"]["address"],
                                contract_address=trade["asset"]["asset_contract"]["address"],
                                price=trade["total_price"],
                                timestamp=trade["transaction"]["timestamp"],
                                token_id=trade["asset"]["token_id"],
                                transaction_hash=trade["transaction"]["transaction_hash"],
                                event_type=trade["event_type"]
                            )
                            data.append(e)
                        except:
                            print("One of the values was invalid!")
                else:
                    # we've exhausted the API history
                    break
                time.sleep(0.6)  # sleep to prevent throttling.
                i += 1
            serializer = EventSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("An error occurred.", status=status.HTTP_404_NOT_FOUND)
