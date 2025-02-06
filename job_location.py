"""
code to validate city and county for Romania
"""
import unicodedata
import requests


def has_diacritics(char):
    """replace char in string with unicode"""
    return any(unicodedata.combining(c) for c in char)


def remove_diacritics(input_string):
    """check if string has diacritics 
    if True then call has_diacritics(char) to replase it"""
    normalized_string = unicodedata.normalize("NFD", input_string)
    return "".join(char for char in normalized_string if not has_diacritics(char))


def validate_city_str(city):
    """Check  if city  is a valid city in Romania

    Args:
        city (str): name of the city 

    Returns:
        False or city: return false or city string for further data validation
    """
    # Remove diacritics and Convert to lowercase for comparison
    city = remove_diacritics(city.lower())

    try:
        if city == "bucuresti":
            return "Bucuresti"

        if city == "all":
            return "all"

        url = f"https://api.laurentiumarian.ro/orase/?search={city}"
        responce = requests.get(url=url, timeout=10).json()
        cities = responce.get("results")

        if not cities:
            # Try replacing spaces with dashes and check again
            if  " " in city:
                city = city.replace(" ", "-")
                url = f"https://api.laurentiumarian.ro/orase/?search={city}"
                responce = requests.get(url=url, timeout=10).json()
                cities = responce.get("results")

            # Try replacing dashes with spaces and check again
            elif  "-" in city:
                city = city.replace("-"," ")
                url = f"https://api.laurentiumarian.ro/orase/?search={city}"
                responce = requests.get(url=url, timeout=10).json()
                cities = responce.get("results")
                
        #if cities not empty iterate and validatte if city exist in the data
            for location in cities:

                if location.get("name").lower() == city:
                    return city

                elif location.get("county").lower() == city:
                    return f"all {city}"

        else:
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
        return validate_city_str(cities)
    elif isinstance(cities, list):
        for city in cities:
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
