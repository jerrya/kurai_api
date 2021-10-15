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
MAX_POINTS_TO_RENDER = 1000

class RetrieveEvents(APIView):
    def get(self, request, slug, format=None):
        if slug:
            # 1. fetch data from db, if it exists
            # 2a. Iterate through events api with offset, and save data to db.
            # 2b. 0.6 second delay.
            # logic to pull from db if such records already exist
            # ^ dependent on timestamp in database and use it as part of the occurred_before value
            data = []
            url = "https://api.opensea.io/api/v1/events"
            latest_time = None
            # fetch data from db, if it exists - https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist-in-django
            try:
                data_from_db = Event.objects.filter(collection_slug=slug).order_by('-timestamp')
            except:
                data_from_db = None
            print(data_from_db)
            if data_from_db is not None and len(data_from_db) > 0:
                data += data_from_db
                latest_time = data_from_db.first().timestamp  # ??? to feed into occurred_after?
            i = 0
            while True:
                querystring = {
                    "collection_slug": slug,
                    "event_type": "successful",
                    "only_opensea": "true",
                    "offset": str(i*API_PAGINATION_LIMIT),
                    "limit": str(API_PAGINATION_LIMIT),
                }
                if latest_time is not None:
                    querystring["occurred_after"] = latest_time
                headers = {"Accept": "application/json"}
                print(querystring)
                response = requests.request("GET", url, headers=headers, params=querystring)
                json = response.json()
                print(json)
                if response.status_code == status.HTTP_200_OK and len(json) > 0 and "asset_events" in json:
                    json = response.json()["asset_events"]
                    if not json:
                        break
                    print("Looping through offset {}".format(i*API_PAGINATION_LIMIT))
                    for trade in json:
                        print(trade)
                        if trade["transaction"]["timestamp"] is None:
                            continue
                        try:
                            e = Event.objects.create(
                                id=trade["transaction"]["transaction_hash"],
                                collection_slug=trade["asset"]["collection"]["slug"],
                                buyer_address=trade["winner_account"]["address"],
                                seller_address=trade["seller"]["address"],
                                contract_address=trade["asset"]["asset_contract"]["address"],
                                price=trade["total_price"],
                                timestamp=trade["transaction"]["timestamp"],
                                token_id=trade["asset"]["token_id"],
                                event_type=trade["event_type"]
                            )
                            data.append(e)
                        except:
                            print("One of the values was invalid!")
                else:
                    # we've exhausted the API history
                    break
                time.sleep(0.6)  # 2b. 0.6 second delay to prevent API throttling.
                i += 1
            print(len(data_from_db))
            print(len(data))
            compressed_data = []
            if len(data) <= 1000:
                compressed_data = data
            else:
                numerator_length = len(data)
                denominator_length = MAX_POINTS_TO_RENDER
                compressed_data = [data[i // denominator_length] for i in range(0, denominator_length*MAX_POINTS_TO_RENDER, numerator_length)]
            print("COMPRESSED")
            print(compressed_data[0:100])
            print("UN-COMPRESSED")
            print(data[0:100])
            serializer = EventSerializer(compressed_data, many=True)
            print(Response(serializer.data, status=status.HTTP_200_OK))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("An error occurred.", status=status.HTTP_404_NOT_FOUND)
