"""
code to validate city and county for Romania
"""
import unicodedata
import requests


def has_diacritics(char):
    return any(unicodedata.combining(c) for c in char)


def remove_diacritics(input_string):
    normalized_string = unicodedata.normalize("NFD", input_string)
    return "".join(char for char in normalized_string if not has_diacritics(char))


def validate_city_str(city):

    loc = city.lower()
    city = remove_diacritics(loc)
    url = f"https://api.laurentiumarian.ro/orase/?search={city}"
    try:
        responce = requests.get(url=url, timeout=10).json()
        cities = responce.get("results")
        if cities:
            for location in cities:

                if city == "bucuresti":
                    return "Bucuresti"

                if city == "all":
                    return "all"

                if location.get("name").lower() == city:
                    return city

                if location.get("county").lower() == city:
                    return f"all {city}"
        else:
            return False

        print(f"{city.upper()}: is not a valid City in Romania")
        return False

    except requests.RequestException as e:
        # Handle exceptions (e.g., network errors, invalid responses)
        print(f"An error occurred: {e}")
        return False  # Ensure the function always returns a boolean value


def validate_city(cities):
    """code to check if cities is list or string then use apropriete
    call to validate list  of strings  or  just one string"""
    results = []
    if isinstance(cities, str):
        if " " in cities:
            city = cities.replace(" ", "-")
            return validate_city_str(city)
        return validate_city_str(cities)
    elif isinstance(cities, list):
        for city in cities:
            if " " in  city:
                city = city.replace(" ", "-")
            is_valid = validate_city_str(city)
            results.append(is_valid)
        return results


def get_county_json(loc):
    loc = loc.lower()
    city = remove_diacritics(loc)
    url = f"https://api.laurentiumarian.ro/orase/?search={city}"
    responce = requests.get(url=url, timeout=10).json()
    citis = responce.get("results")
    counties = []
    for location in citis:
        if location.get("name").lower() == city:
            counties.append(location.get("county"))
        elif location.get("county").lower() == city:
            counties.append(location.get("county"))
    return list(set(counties))


def update_location_if_is_county(counties, locations):
    if len(counties) >= 1:
        i = 0
        for location in locations:
            for county in counties:
                if county in remove_diacritics(location):
                    locations[i] = (f"all {county}")
            i += 1
        # return locations
    else:
        locations = "all"
    return locations


count = get_county_json("Prahova")
loca = ["Iasi", "Bucuresti", "cluj", 'targu mures']
lo = 'dej'
# print(count)
# print(update_location_if_is_county(count, loca))
# print(validate_city(loca))
