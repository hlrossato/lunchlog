import pytest
from unittest import mock
from google_places_api.api import GooglePlacesAPI


API_KEY = "test"


def test_google_places_api__missing_api_key():
    with pytest.raises(Exception):
        gpapi = GooglePlacesAPI()
        gpapi._add_key_to_params()


def test_google_places_api__api_key_added_to_params():
    gpapi = GooglePlacesAPI(API_KEY)
    gpapi._add_key_to_params()
    assert "key" in gpapi._params


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
def test_find_places__successful(mocked_request_get):
    response_json = {
        "candidates": [
            {
                "formatted_address": "Hunsrückenstraße 15, 40213 Düsseldorf, Deutschland",
                "name": "Casita Mexicana Altstadt",
                "opening_hours": {"open_now": False},
                "rating": 4.4,
                "place_id": "test",
            }
        ],
        "status": GooglePlacesAPI.RESPONSE_STATUS_OK,
    }

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    result = gpapi.find_place("Casita Mexicana Dusseldorf")

    assert (
        result[0]["formatted_address"]
        == response_json["candidates"][0]["formatted_address"]
    )
    assert result[0]["name"] == response_json["candidates"][0]["name"]
    assert result[0]["opening_hours"] == response_json["candidates"][0]["opening_hours"]
    assert result[0]["rating"] == response_json["candidates"][0]["rating"]
    assert result[0]["place_id"] == response_json["candidates"][0]["place_id"]


@mock.patch("google_places_api.api.requests.get")
def test_find_places__passing_specific_fields(mocked_request_get):
    response_json = {
        "candidates": [
            {
                "formatted_address": "Hunsrückenstraße 15, 40213 Düsseldorf, Deutschland",
                "name": "Casita Mexicana Altstadt",
                "place_id": "test",
            }
        ],
        "status": GooglePlacesAPI.RESPONSE_STATUS_OK,
    }

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    result = gpapi.find_place(
        "Casita Mexicana Dusseldorf", fields=["formatted_address", "name"]
    )

    assert (
        result[0]["formatted_address"]
        == response_json["candidates"][0]["formatted_address"]
    )
    assert result[0]["name"] == response_json["candidates"][0]["name"]
    assert result[0]["place_id"] == response_json["candidates"][0]["place_id"]


@mock.patch("google_places_api.api.requests.get")
def test_find_places__empty_results(mocked_request_get):
    response_json = {
        "candidates": [],
        "status": GooglePlacesAPI.RESPONSE_ZERO_RESULTS,
    }

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    result = gpapi.find_place("Bla Bla Bla")
    assert result == []


@mock.patch("google_places_api.api.requests.get")
def test_find_places__invalid_request(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_INVALID_REQUEST}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json
    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(Exception):
        gpapi.find_place()


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__successful(mocked_request_get, google_place_detail):
    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = google_place_detail

    gpapi = GooglePlacesAPI(API_KEY)

    place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"
    result = gpapi.place_details(place_id)

    assert result["place_id"] == place_id


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__not_found(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_NOT_FOUND}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json

    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(Exception):
        gpapi.place_details("test")


@mock.patch("google_places_api.api.requests.get")
def test_get_place_details__invalid_request(mocked_request_get):
    response_json = {"status": GooglePlacesAPI.RESPONSE_INVALID_REQUEST}

    mocked_request_get.return_value = mock.Mock(ok=True)
    mocked_request_get.return_value.json.return_value = response_json

    gpapi = GooglePlacesAPI(API_KEY)

    with pytest.raises(Exception):
        gpapi.place_details()
