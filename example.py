import pandas as pd
from petfinder_api import SearchFilters, pet_search

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def main():
    filters = SearchFilters(country="US", state="CA", zip_code="94020", pet_type="cats")
    filters.sort = "recently_added"
    df = pd.DataFrame(pet_search(filters, max_pages=5))
    # sort by date_added
    df["date_added"] = pd.to_datetime(df["date_added"])
    df = df.sort_values("date_added", ascending=False).reset_index(drop=True)
    print(df)


if __name__ == "__main__":
    main()
