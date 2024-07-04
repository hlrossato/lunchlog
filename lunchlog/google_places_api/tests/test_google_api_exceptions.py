from google_places_api.exceptions import GooglePlacesException
from google_places_api.api import GooglePlacesAPI


def test_google_place_exception():
    test_api = "https://test_api.com"
    exc = GooglePlacesException(GooglePlacesAPI.RESPONSE_INVALID_REQUEST, test_api)

    assert GooglePlacesAPI.RESPONSE_INVALID_REQUEST in exc.args
    assert test_api in exc.args
