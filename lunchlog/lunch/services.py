from typing import TYPE_CHECKING
from django.conf import settings
from django.db import transaction

from google_places_api.api import GooglePlacesAPI

if TYPE_CHECKING:
    from lunch.models import Receipt


def populate_restaurant(receipt: "Receipt") -> None:
    """
    Makes a call to Google Places API and store information about the
    searched place into the Restaurant model.
    """
    from lunch.models import Restaurant

    api = GooglePlacesAPI(settings.GOOGLE_PLACES_API_KEY)
    query = f"{receipt.restaurant_name} {receipt.restaurant_address}"

    with transaction.atomic():
        place_id = api.find_place_id(query)
        place = api.place_details(place_id)
        Restaurant.objects.create(**place.to_dict(), receipt=receipt, user=receipt.user)
