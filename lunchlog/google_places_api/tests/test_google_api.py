import pytest
from unittest import mock
from google_places_api.api import GooglePlacesAPI, GooglePlaceDetail
from google_places_api.exceptions import GooglePlacesException


API_KEY = "test"


def test_google_places_api__missing_api_key():
    with pytest.raises(GooglePlacesException):
        gpapi = GooglePlacesAPI(None)
        gpapi._add_key_to_params()


def test_google_places_api__api_key_added_to_params():
    gpapi = GooglePlacesAPI(API_KEY)
    gpapi._add_key_to_params()
    assert "key" in gpapi._params


@mock.patch("google_places_api.api.requests.get")
def test_google_places_api__get_place_id__empty_list(mocked_request_get):
    gpapi = GooglePlacesAPI(API_KEY)
    response_json = {}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json

    place_id = gpapi._get_place_id(mocked_request_get.return_value)
    assert place_id == ""


def test_google_places_api__encode_data():
    params = {
        "input": "test",
        "inputtype": "textquery",
        "fields": ["test", "hello", "world"],
    }
    gpapi = GooglePlacesAPI(API_KEY)
    encoded = gpapi._encode_data(params)
    assert encoded == "input=test&inputtype=textquery&fields=test%2Chello%2Cworld"


@mock.patch("google_places_api.api.requests.get")
def test_find_place_id__successful(mocked_request_get):
    response_json = {
        "candidates": [
            {
                "place_id": "test",
            }
        ],
        "status": GooglePlacesAPI.RESPONSE_STATUS_OK,
    }

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    result = gpapi.find_place_id("Casita Mexicana Dusseldorf")

    assert result == response_json["candidates"][0]["place_id"]


@mock.patch("google_places_api.api.requests.get")
def test_find_places__empty_results(mocked_request_get):
    response_json = {
        "candidates": [],
        "status": GooglePlacesAPI.RESPONSE_ZERO_RESULTS,
    }

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    result = gpapi.find_place_id("Bla Bla Bla")
    assert result == []


@mock.patch("google_places_api.api.requests.get")
def test_find_places__invalid_request(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_INVALID_REQUEST}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(GooglePlacesException):
        gpapi.find_place_id()


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__successful(mocked_request_get, google_place_detail):
    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = google_place_detail

    gpapi = GooglePlacesAPI(API_KEY)

    place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"
    result = gpapi.place_details(place_id)

    assert result.place_id == place_id


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__not_found(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_NOT_FOUND}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json

    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(GooglePlacesException):
        gpapi.place_details("test")


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__invalid_request(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_INVALID_REQUEST}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json

    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(GooglePlacesException):
        gpapi.place_details()


def test_google_places_detail__extract_address(google_place_detail):
    detail = GooglePlaceDetail(google_place_detail["result"])
    address = detail._extract_address()

    expected_address = {
        "street_number": "48",
        "route": "Pirrama Road",
        "administrative_area_level_2": "Sydney",
        "administrative_area_level_1": "New South Wales",
        "country": "Australia",
        "postal_code": "2009",
    }

    assert address == expected_address
