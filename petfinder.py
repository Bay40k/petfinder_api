from dataclasses import dataclass
from typing import Literal, get_type_hints, get_origin, get_args, Union, Iterable
from urllib.parse import urljoin

import requests


class APIHandler:
    def __init__(self):
        self.url = "https://www.petfinder.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
        }

    def get(self, endpoint: str, params: dict = None) -> dict:
        self.url = urljoin(self.url, endpoint)
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.json()


@dataclass
class PetResult:
    distance: int
    id: int
    type: str
    species: str
    breed: str
    is_mixed_breed: bool
    primary_color: str
    secondary_color: str
    tertiary_color: str
    age: str
    sex: str
    size: str
    coat_length: str
    name: str
    description: str
    photo_url: str
    attributes: dict[str]
    home_environment_attributes: dict[str, bool]
    tags: list[str]
    contact: dict[str, str]
    location: dict[str, str] | str
    url: str
    date_added: str

    def __init__(self, pet: dict):
        self.distance = pet.get("distance")

        self.contact = pet.get("contact")
        organization = pet.get("organization", {}).get("name")
        self.contact["organization"] = organization

        self.location = pet.get("location", {}).get("address", "Not listed")

        animal = pet.get("animal", {})
        self.id = animal.get("id")
        self.type = animal.get("type", {}).get("name")
        self.species = animal.get("species", {}).get("name")
        self.breed = animal.get("breeds_label")
        self.is_mixed_breed = animal.get("is_mixed_breed")
        self.primary_color = animal.get("primary_color")
        self.secondary_color = animal.get("secondary_color")
        self.tertiary_color = animal.get("tertiary_color")
        self.age = animal.get("age")
        self.sex = animal.get("sex")
        self.size = animal.get("size")
        self.coat_length = animal.get("coat_length")
        self.name = animal.get("name")
        self.description = animal.get("description")
        self.photo_url = animal.get("primary_photo_url")
        self.attributes = animal.get("attributes")
        self.home_environment_attributes = animal.get("home_environment_attributes")
        self.tags = animal.get("tags")
        self.url = animal.get("social_sharing", {}).get("email_url")
        self.date_added = animal.get("published_at")


@dataclass
class SearchFilters:
    country: str  # 2-letter country code
    state: str  # 2-letter state code
    zip_code: str  # 5-digit zip code
    pet_type: Literal[
        "cats",
        "dogs",
        "small-furry",
        "birds",
        "scales-fins-other",
        "rabbits",
        "horses",
        "barnyard",
    ]
    distance: int = 30  # miles
    include_transportable: bool = True
    sort: Literal[
        "nearest", "furthest", "recently_added", "available_longest", "random"
    ] = "nearest"

    def __init__(self, country, state, zip_code, pet_type, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.country = country.lower()
        self.state = state.lower()
        self.zip_code = zip_code
        self.pet_type = pet_type

        if len(self.zip_code) != 5:
            raise ValueError("Zip code must be 5 digits.")
        if len(self.state) != 2:
            raise ValueError("State code must be 2 letters.")
        if len(self.country) != 2:
            raise ValueError("Country code must be 2 letters.")

        self.location_slug = f"{self.country}/{self.state}/{self.zip_code}"
        self.params = {
            "distance[]": self.distance,
            "type[]": self.pet_type,
            "sort[]": self.sort,
            "location_slug[]": self.location_slug,
            "include_transportable": self.include_transportable,
        }

    def __post_init__(self):
        self._validate_attributes()

    def _validate_attributes(self):
        type_hints = get_type_hints(self)
        for attr, attr_type in type_hints.items():
            value = getattr(self, attr)
            if value is not None and not self._is_valid_type(value, attr_type):
                raise TypeError(
                    f"Invalid type for {attr}: Expected {attr_type}, got {type(value)}"
                )

    def _is_valid_type(self, value, expected_type):
        origin = get_origin(expected_type)
        args = get_args(expected_type)

        if origin is Union:
            return any(self._is_valid_type(value, arg) for arg in args)

        if origin is list:
            if not isinstance(value, list):
                return False
            return all(self._is_valid_type(item, args[0]) for item in value)

        if origin is Literal:
            return value in args

        if isinstance(expected_type, type):
            return isinstance(value, expected_type)

        return False

    def __setattr__(self, key, value):
        type_hints = get_type_hints(self)
        if key in type_hints:
            expected_type = type_hints[key]
            if value is not None and not self._is_valid_type(value, expected_type):
                raise TypeError(
                    f"Invalid type for {key}: Expected {expected_type}, got {type(value)}"
                )
        super().__setattr__(key, value)


def pet_search(
    filters: SearchFilters,
    max_results: int = 40,
    page: int = 1,
    max_pages: int = 1,
) -> Iterable[PetResult]:

    params = {
        "page": page,
        "limit[]": max_results,
        "status": "adoptable",
        **filters.params,
    }

    api = APIHandler()
    while page <= max_pages:
        print(f"Fetching page {page} with filters: {filters.__dict__}")
        pets = api.get("/search/", params=params)["result"]["animals"]
        for pet in pets:
            yield PetResult(pet)

        page += 1
        params["page"] = page
