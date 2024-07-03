import requests
import urllib

from collections.abc import Iterable
from typing import Union

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
            raise Exception("Missing API KEY")
        self._params["key"] = self._api_key

    def _validate_response(self, api: str, response: Response):
        if response.json()["status"] not in [
            self.RESPONSE_STATUS_OK,
            self.RESPONSE_ZERO_RESULTS,
        ]:
            raise Exception(
                "Request to %s failed with error %s", api, response.json()["status"]
            )

    def _fetch_results(self, api: str, params: dict) -> Union[str, Response]:
        encoded_data = {}
        for k, v in params.items():
            if isinstance(v, str):
                v = v.encode("utf-8")
            encoded_data[k] = v
        encoded_data = urllib.parse.urlencode(encoded_data)

        url = api + encoded_data
        response = requests.get(url)
        return url, response

    def _get_places_json(self, response: Response) -> dict:
        return [r for r in response.json()["candidates"]]

    def _get_place_details(self, response: Response) -> dict:
        return response.json()["result"]

    def find_place(self, query: str = None, inputtype: str = "textquery"):
        self._params = {"query": query}
        self._params["inputtype"] = inputtype
        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.FIND_PLACE_API, self._params
        )
        self._validate_response(api, response)
        return self._get_places_json(response)

    def place_details(self, place_id: str = None) -> dict:
        self._params = {"place_id": place_id}
        self._add_key_to_params()
        api, response = self._fetch_results(
            GooglePlacesAPI.PLACE_DETAIL_API, self._params
        )
        self._validate_response(api, response)
        return self._get_place_details(response)
