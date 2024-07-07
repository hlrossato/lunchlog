import requests
from urllib.parse import urlencode

from typing import Self, Type, Tuple

from google_places_api.exceptions import GooglePlacesException

Response = Type[requests.models.Response]


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

    def __init__(self: Self, api_key: str) -> None:
        self._api_key = api_key
        self._params: dict = {}

    def _add_key_to_params(self: Self) -> None:
        if self._api_key is None:
            raise GooglePlacesException("Missing API KEY")
        self._params["key"] = self._api_key

    def _validate_response(self: Self, api: str, response: Response) -> None:
        if response.json()["status"] not in [
            self.RESPONSE_STATUS_OK,
            self.RESPONSE_ZERO_RESULTS,
        ]:
            msg = "Request to %s failed with error %s"
            err = ""
            raise GooglePlacesException(msg, err)

    def _encode_data(self: Self, params: dict) -> str:
        encoded_data = {}
        for k, v in params.items():
            if isinstance(v, str):
                v = v.encode("utf-8")
            elif isinstance(v, list):
                new_value = ",".join([item for item in v])
                v = new_value.replace(" ", "").encode("utf-8")
            encoded_data[k] = v
        return urlencode(encoded_data)

    def _fetch_results(self: Self, api: str, params: dict) -> Tuple[str, Response]:
        encoded_data = self._encode_data(params)
        url = api + encoded_data
        response = requests.get(url)
        return url, response

    def _get_place_id(self: Self, response: Response) -> str:
        if "candidates" not in response.json():
            return ""

        if len(response.json()["candidates"]) < 1:
            return ""

        return [
            r["place_id"] for r in response.json()["candidates"] if "place_id" in r
        ][0]

    def _get_place_details(self: Self, response: Response) -> "GooglePlaceDetail":
        return GooglePlaceDetail(response.json()["result"])

    def find_place_id(self: Self, input: str, inputtype: str = "textquery") -> str:
        # if no fields is provided the api will return the place_id only
        self._params = {"input": input}
        self._params["inputtype"] = inputtype

        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.FIND_PLACE_API, self._params
        )
        self._validate_response(api, response)
        return self._get_place_id(response)

    def place_details(self: Self, place_id: str) -> "GooglePlaceDetail":
        self._params = {"place_id": place_id}
        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.PLACE_DETAIL_API, self._params
        )
        self._validate_response(api, response)
        return self._get_place_details(response)


class GooglePlaceDetail(object):
    """Wrapper class to seriaze"""

    def __init__(self: Self, place_data: dict) -> None:
        self._data = place_data
        self.name = place_data.get("name")
        self.formatted_address = place_data.get("formatted_address")
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

        address = self._extract_address()
        self.street_name = address.get("route")
        self.street_number = address.get("street_number")
        self.city = address.get("administrative_area_level_2")
        self.state = address.get("administrative_area_level_1")
        self.country = address.get("country")
        self.postal_code = address.get("postal_code")

    def _extract_address(self: Self) -> dict:
        types = [
            "street_number",
            "route",
            "administrative_area_level_1",
            "administrative_area_level_2",
            "country",
            "postal_code",
        ]
        address = {}

        for item in self._data["address_components"]:
            long_name = item["long_name"]

            if "types" in item.keys():
                if len(item["types"]) == 1:
                    address[item["types"][0]] = long_name
                else:
                    for t in item["types"]:
                        if t in types:
                            address[t] = long_name
        return address

    def to_dict(self: Self) -> dict:
        return {
            "place_id": self.place_id,
            "name": self.name,
            "formatted_address": self.formatted_address,
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
            "street_name": self.street_name,
            "street_number": self.street_number,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
        }
