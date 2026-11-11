"""Procedural filtering and aggregation of the supplied city dataset."""
import csv
from pathlib import Path


def load_cities(filename):
    """Read CSV rows and convert numeric columns to floats."""
    with open(filename, newline="", encoding="utf-8-sig") as file:
        cities = list(csv.DictReader(file))
    for city in cities:
        for key in ("latitude", "longitude", "temperature"):
            city[key] = float(city[key])
    return cities


def filter_items(condition, dict_list):
    """Return a new list of dictionaries that satisfy condition(item)."""
    return [item for item in dict_list if condition(item)]


def aggregate(aggregation_key, aggregation_function, dict_list):
    """Collect values for the key and pass them to the aggregation function."""
    values = [item[aggregation_key] for item in dict_list]
    return aggregation_function(values)


def main():
    cities = load_cities(Path(__file__).with_name("Cities.csv"))
    average = lambda values: sum(values) / len(values)

    print("The average temperature of all the cities:")
    print(aggregate("temperature", average, cities))

    germany = filter_items(lambda city: city["country"] == "Germany", cities)
    print("\nAll cities in Germany:")
    for city in germany:
        print(city["city"])

    spain = filter_items(
        lambda city: city["country"] == "Spain" and city["temperature"] > 12,
        cities,
    )
    print("\nCities in Spain with a temperature above 12°C:")
    for city in spain:
        print(city["city"])

    print("\nNumber of unique countries:")
    print(aggregate("country", lambda values: len(set(values)), cities))

    print("\nThe average temperature of all the cities in Germany:")
    print(aggregate("temperature", average, germany))

    italy = filter_items(lambda city: city["country"] == "Italy", cities)
    print("\nThe maximum temperature of all the cities in Italy:")
    print(aggregate("temperature", max, italy))


if __name__ == "__main__":
    main()
