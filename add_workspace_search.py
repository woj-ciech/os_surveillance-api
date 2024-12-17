import requests
import time

headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json"
}
BASE_URL = "https://osint.os-surveillance.io/api"

modules_to_run = ["flickr"] # list of modules to run

# Add new workspace to the database
def add_workspace():
    url = BASE_URL + "/addCoordinates/"
    payload = {
        "title": "New York",
        "position": {
            "lat": 40.72020796700515, # example New York coordinates
            "lng": -74.0401684945897
        },
        "radius": 30000
    }

    response = requests.post(url, headers=headers, json=payload)

    workspace_id = response.json()['workspace_id']

    return workspace_id


# Search for data in the workspace
# pass workspace_id from add_workspace()
# include latitude, longitude and bounding box of the area
def search(wokspace_id):
    url = BASE_URL + f"/search/"
    payload = {
        "options":
            modules_to_run,
        "keywords": None,
        "date_from": None,
        "date_to": None,
        "only_new": False,
        "coordinates_id": wokspace_id,
        "lat": 40.71846412371451,  # center latitude (Coordinates inside the workspace - example New York Manhattan)
        "lng": -73.99740740984262,  # center longitude
        "ne_lat": 40.74334880686837,  # north east latitude
        "ne_lng": -73.81237074710944,  # north east longitude
        "sw_lat": 40.67945984569057,  # south west latitude
        "sw_lng": -74.16341826297858  # south west longitude
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    search_pk = response.json()['search_pk']

    return search_pk

    
# Check progress of the search request
def get_progress(search_pk):
    url = BASE_URL + f"/getProgress/{search_pk}/"

    response = requests.request("GET", url, headers=headers)

    return response.json()


# Get results of the search request
def get_results(search_pk):
    url = BASE_URL + f"/getSearchResults/{search_pk}/"
    response = requests.request("GET", url, headers=headers)

    r_json = response.json()

    return response.json()

# check whether some module failed
def check_errors():
    url = BASE_URL + "/checkErrors/"
    response = requests.request("GET", url, headers=headers)

    return response.json()['errors']


workspace_id = add_workspace()
print(f"Workspace has been created: {workspace_id}")
search_pk = search(workspace_id)  # next time when searching in this area, use same workspace_id
while True:
    progress = get_progress(search_pk)
    print(f"Progress {progress['progress']} %")
    if progress['progress'] == 100.0:
        results = get_results(search_pk)
        break
    else:
        time.sleep(1)

print("Results")
for result in results:
    print(result.get("type"), None)
    for item in result['objects']:
        print(json.dumps(item, indent=4))
        # print(item['title'])
        # print(item['timestamp'])
        # print(item['photo_url'])
        # print(item['location'])
