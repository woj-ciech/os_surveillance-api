import requests
import json
import time

BASE_URL = "https://osint.os-surveillance.io/api"

workspace_id = ""
item_type = "snapchat"
item_id = ""
modules_to_run = ['snapchat', 'vkontakte']

headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

def get_items(workspace_id, item_type):
    r = requests.get(f"{BASE_URL}/getCoordinatesItems/{workspace_id}/{item_type}?page=1&limit=40", headers=headers)

    return json.loads(r.text)

def get_item(workspace_id, item_type, item_id):
    r = requests.get(f"{BASE_URL}/getCoordinatesItem/{workspace_id}/{item_type}/{item_id}", headers=headers)

    return json.loads(r.text)


def get_workspace_info(workspace_id):
    r = requests.get(f"{BASE_URL}/getCoordinates/{workspace_id}", headers=headers)

    return json.loads(r.text)

def get_workspaces():
    r = requests.get(f"{BASE_URL}/getCoordinates", headers=headers)

    return json.loads(r.text)

def get_user_info():
    r = requests.get(f"{BASE_URL}/getUserInfo", headers=headers)

    return json.loads(r.text)

# Check progress of the search request
def get_progress(search_pk):
    url = BASE_URL + f"/getProgress/{search_pk}/"

    response = requests.request("GET", url, headers=headers)

    return response.json()

def search(workspace_id):
    url = BASE_URL + f"/search/"
    payload = {
        "options":
            modules_to_run,
        "keywords": None,
        "date_from": None,
        "date_to": None,
        "coordinates_id": workspace_id,
        "lat": 40.71846412371451,  # center latitude (Coordinates inside the workspace - example New York Manhattan)
        "lng": -73.99740740984262,  # center longitude
        "ne_lat": 40.74334880686837,  # north east latitude
        "ne_lng": -73.81237074710944,  # north east longitude
        "sw_lat": 40.67945984569057,  # south west latitude
        "sw_lng": -74.16341826297858  # south west longitude
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    search_pk = response.json()['search_pk']

    while True:
        progress = get_progress(search_pk)
        print(f"Progress {progress['progress']} %")
        if progress['progress'] == 100.0:
            url = BASE_URL + f"/getSearchResults/{search_pk}/"
            response = requests.request("GET", url, headers=headers)

            return response.json()
        else:
            time.sleep(1)

    return response.json()