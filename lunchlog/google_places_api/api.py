import requests
import urllib

from collections.abc import Iterable
from typing import Union

from google_places_api.exceptions import GooglePlacesException

type Response[S] = Iterable[S] | int


class GooglePlacesAPI(object):
    """Google Places API interface"""

    BASE_API = "https://maps.googleapis.com/maps/api"
    BASE_PLACE_API = f"{BASE_API}/place"
    FIND_PLACE_API = f"{BASE_PLACE_API}/findplacefromtext/json?"
    PLACE_DETAIL_API = f"{BASE_PLACE_API}/details/json?"

    RESPONSE_STATUS_OK = "OK"
    RESPONSE_ZERO_RESULTS = "ZERO_RESULTS"
    RESPONSE_INVALID_REQUEST = "INVALID_REQUEST"
    RESPONSE_NOT_FOUND = "NOT_FOUND"
    RESPONSE_REQUEST_DENIED = "REQUEST_DENIED"

    def __init__(self, api_key: str = None):
        self._api_key = api_key
        self._params = {}

    def _add_key_to_params(self):
        if self._api_key is None:
            raise GooglePlacesException("Missing API KEY")
        self._params["key"] = self._api_key

    def _validate_response(self, api: str, response: Response):
        if response.json()["status"] not in [
            self.RESPONSE_STATUS_OK,
            self.RESPONSE_ZERO_RESULTS,
        ]:
            msg = "Request to %s failed with error %s"
            err = ""
            raise GooglePlacesException(msg, err)

    def _encode_data(self, params: dict) -> str:
        encoded_data = {}
        for k, v in params.items():
            if isinstance(v, str):
                v = v.encode("utf-8")
            elif isinstance(v, list):
                new_value = ",".join([item for item in v])
                v = new_value.replace(" ", "").encode("utf-8")
            encoded_data[k] = v
        return urllib.parse.urlencode(encoded_data)

    def _fetch_results(self, api: str, params: dict) -> Union[str, Response]:
        encoded_data = self._encode_data(params)
        url = api + encoded_data
        response = requests.get(url)
        return url, response

    def _get_place_id(self, response: Response) -> dict:
        if "candidates" not in response.json():
            return []

        if len(response.json()["candidates"]) < 1:
            return []

        return [
            r["place_id"] for r in response.json()["candidates"] if "place_id" in r
        ][0]

    def _get_place_details(self, response: Response) -> dict:
        return GooglePlaceDetail(response.json()["result"])

    def find_place_id(self, input: str = None, inputtype: str = "textquery"):
        # if no fields is provided the api will return the place_id only
        self._params = {"input": input}
        self._params["inputtype"] = inputtype

        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.FIND_PLACE_API, self._params
        )
        self._validate_response(api, response)
        return self._get_place_id(response)

    def place_details(self, place_id: str = None) -> dict:
        self._params = {"place_id": place_id}
        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.PLACE_DETAIL_API, self._params
        )
        self._validate_response(api, response)
        return self._get_place_details(response)


class GooglePlaceDetail(object):
    def __init__(self, place_data):
        self.name = place_data.get("name")
        self.address = place_data.get("formatted_address")
        self.serves_beer = place_data.get("serves_beer")
        self.serves_breakfast = place_data.get("serves_breakfast")
        self.serves_brunch = place_data.get("serves_brunch")
        self.serves_dinner = place_data.get("serves_dinner")
        self.serves_lunch = place_data.get("serves_lunch")
        self.serves_vegetarian_food = place_data.get("serves_vegetarian_food")
        self.serves_wine = place_data.get("serves_wine")
        self.takeout = place_data.get("takeout")
        self.delivery = place_data.get("delivery")
        self.opening_hours = place_data.get("opening_hours")
        self.place_id = place_data.get("place_id")

    def to_dict(self):
        return {
            "place_id": self.place_id,
            "name": self.name,
            "address": self.address,
            "serves_beer": self.serves_beer,
            "serves_breakfast": self.serves_breakfast,
            "serves_brunch": self.serves_brunch,
            "serves_dinner": self.serves_dinner,
            "serves_lunch": self.serves_lunch,
            "serves_vegetarian_food": self.serves_vegetarian_food,
            "serves_wine": self.serves_wine,
            "takeout": self.takeout,
            "delivery": self.delivery,
            "opening_hours": self.opening_hours,
        }
