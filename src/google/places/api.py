from src.api import Api
from typing import Any, Dict, List, Optional

from .config import PLACES_DETAIL_URL, PLACES_NEARBY_URL, PLACES_KEY
from .models import PlaceRequest, GoogleException


def fetch_detail(place_id: str, fields: Optional[List[str]]) -> Dict[str, Any]:
    place_id_param = f"place_id={place_id}"
    params = (
        place_id_param
        if not fields
        else f"fields={','.join(fields)}&{place_id_param}"
    )
    return _validate_google_response(
        Api(fallback="/google/places/detail")
        .get(PLACES_DETAIL_URL, params=_add_key(params))
        .json()
    ).get("result", {})


def search_nearby(place: PlaceRequest) -> List[Dict[str, Any]]:
    params = place.to_query()
    return _validate_google_response(
        Api().get(PLACES_NEARBY_URL, params=_add_key(params)).json()
    ).get("results", [])


def _add_key(params: str) -> str:
    return f"language=en&key={PLACES_KEY}&{params}"


def _validate_google_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if (status := response.get("status", "OK")) != "OK":
        raise GoogleException(
            status, response.get("error_message", "¯\\_(ツ)_/¯")
        )
    else:
        return response
