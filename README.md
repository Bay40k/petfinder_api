# Petfinder API

The `petfinder_api` package allows you to interact with the Petfinder website to search for adoptable pets. The package provides a convenient way to filter and retrieve pet data using Python.

## Requirements

- Python >= 3.10
- `requests` library

## Installation

First, install the required `requests` package:

```bash
pip install requests
```

## Cloning the Repository

To get started, clone the repository:

```bash
git clone https://github.com/Bay40k/petfinder_api.git
```

**Important:** Do not change directories into the `petfinder_api` folder. The file where you are using the package should be outside the `petfinder_api` directory.

## Usage

Here's a basic example of how to use the package:

```python
from petfinder_api import pet_search, SearchFilters

# Define your search filters
filters = SearchFilters(
    country="US",
    state="CA",
    zip_code="90210",
    pet_type="dogs",
    distance=50,
    include_transportable=True,
    sort="nearest"
)

# Perform the search
for pet in pet_search(filters, max_results=20):
    print(pet.name, pet.breed, pet.location)
```

This script will search for dogs within 50 miles of the 90210 ZIP code in California and print out their names, breeds, and locations.

## PetResult Class

The `pet_search` function returns an iterable of `PetResult` objects. The class is defined as follows:

```python
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
```
