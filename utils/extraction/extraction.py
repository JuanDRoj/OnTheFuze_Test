import requests
import json


def contact_collector():

    """
    Collects contact records from HubSpot CRM.

    Returns:
    record_properties (list): List of dictionaries representing contact properties.
    """

    data_limit=100
    all_records=[]
    paging_count=0

    access_token='Bearer pat-na1-3c7b0af9-bb66-40e7-a256-ce4c5eb27e81'

    headers={
        'Authorization':access_token,
        'Content-Type': 'application/json'
    }

    data={
        "limit":data_limit,
        "filterGroups":[
        {
            "filters":[
            {
                "propertyName": "allowed_to_collect",
                "operator": "EQ",
                "value": True
            }
            ]
        }
        ],
        "properties": [ "raw_email", "country", "phone", "technical_test__create_date","industry","address","hs_object_id"]
    }

    url='https://api.hubapi.com/crm/v3/objects/contacts/search'

    while True:
        response=requests.post(url,headers=headers,data=json.dumps(data))
        if response.status_code==200:
            r=response.json()
            all_records+=r['results']
            if not 'paging' in r:
                break
            else:
                paging_count+=data_limit
                data['after'] = paging_count
        else:
            break
    
    record_properties=[record['properties'] for record in all_records]


    return record_properties
