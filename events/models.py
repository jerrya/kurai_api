from django.db import models


class Event(models.Model):
    buyer_address = models.CharField(max_length=100)  # [asset_events][i][winner_account][address]
    seller_address = models.CharField(max_length=100)  # [asset_events][i]["seller"]["address"]
    contract_address = models.CharField(max_length=100)  # [asset_events][i][asset][asset_contract][address]
    price = models.BigIntegerField()  # [asset_events][i][total_price]
    timestamp = models.DateTimeField()  # [asset_events][i][timestamp]
    token_id = models.CharField(max_length=256)  # [asset_events][i][asset][token_id]
    transaction_hash = models.CharField(max_length=100)  # [asset_events][i][transaction][transaction_hash]
    event_type = models.CharField(max_length=20)  # successful, withdrawn, etc.... [asset_events][i][event_type]
