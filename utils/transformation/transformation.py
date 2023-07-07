import re
import json
import requests


def country_recognition(name):
    """
    Performs country recognition based on a given name using OpenStreetMap Nominatim API.

    Args:
        name (str): Name or address for which country recognition is to be performed.

    Returns:
        out (tuple): A tuple containing the recognized country and the input name.
                    If country is not found, the country value is None.
    """

    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': name, 'format': 'json', 'addressdetails': 1}
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.ok and data:
        city_filter=list(filter(lambda x:'city' in x['address'],data))
        if city_filter:
            first_result=city_filter[0]
            country_found = first_result['address'].get('country')
            if country_found == 'United Kingdom':
                country_found = first_result['address'].get('state')
            else:
                country_found = re.sub(r"\s+", "", country_found).split('/')[-1]
            out=(country_found,name)
        else:
            out=(name,None)
        return out
    else:
        return (None,None)



def found_emails(raw_email):
    """
    Extracts the email address from a raw email string.

    Args:
        raw_email (str): Raw email string containing the email address.

    Returns:
        fixed_email (str or None): Extracted email address. Returns None if no email address is found.
    """
    if raw_email:
        pattern = re.escape("<") + "(.*?)" + re.escape(">")
        match = re.search(pattern, raw_email)
        if match:
            fixed_email=match.group(1)
            return fixed_email
        else:
            return None
    else:
        return None


def fix_phone_numbers(raw_phone,country):
    """
    Formats the phone number by adding the country code and applying a standard format.

    Args:
        raw_phone (str): Raw phone number string.
        country (str): Country name or code to determine the country code.

    Returns:
        out_phone (str): Formatted phone number. Returns the input as-is if it is empty.
    """
    if raw_phone:
        digits = re.sub(r'\D', '', raw_phone).lstrip('0')
        country_code=country_phone_code(country)
        out_phone = f"({country_code}) {digits[0:4]} {digits[4:]}"
    else:
        out_phone=raw_phone

    return out_phone


def country_phone_code(country):
    """
    Retrieves the phone code for a given country.

    Args:
        country (str): Country name.

    Returns:
        country_code (str): Phone code for the country. Returns an empty string if the country code is not found.
    """
    
    with open('utils/transformation/files/phone_codes.json') as file:
        countries_data = json.load(file)
        country_data=list(filter(lambda x:(x['name']==country),countries_data['countries']))[0]
        if country_data:
            country_code=country_data['code']
        else:
            country_code=""

    return country_code


