import requests
import json
from datetime import datetime

def saving_contact(properties):

    """
    Saves a contact by sending the properties to the HubSpot CRM API.

    Args:
        properties (dict): Contact properties to be saved.

    Returns:
        None
    """
    
    access_token='Bearer pat-na1-b9e940d3-ab11-4995-8f6b-68f172a6d739'

    headers={
        'Authorization':access_token,
        'Content-Type': 'application/json'
    }

    data={
        "properties": properties
    }


    url='https://api.hubapi.com/crm/v3/objects/contacts'

    response=requests.post(url,headers=headers,data=json.dumps(data))

    if response.status_code!=201:
        print('An error ocurred ', response.text)



def load_record_management(record):

    """
    Manages the loading of a record by updating keys and date format.

    Args:
        record (dict): Input record as a dictionary.

    Returns:
        updated_record (dict): Updated record with modified keys and date format.
    """

    key_changes = {'hs_object_id': 'temporary_id', 'lastmodifieddate': 'original_create_date', 'industry': 'original_industry'}
    updated_record = {key_changes.get(k, k): v for k, v in record.items()}
    date_object = datetime.strptime(updated_record['original_create_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    updated_record['original_create_date'] = date_object.strftime("%Y-%m-%d")

    return updated_record


