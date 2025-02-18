# os_surveillance-api

[API documentation for Open Source Surveillance ](https://app.theneo.io/offensive-osint/oss/open-source-surveillance-api)


## Main endpoints

This endpoints will make your geo search possible.

Attached script creates a new workspace, searches for Flickr in specific coordinates, in the added workspace, then checkes for progress of the search and gets results at the end.

Attached script (add_workspace_search.py) does it automatically.

Example output
```
Workspace has been created: 13603
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 0.0 %
Progress 100.0 %
Errors:  []
Results
{
    "id": 145920,
    "location": {
        "lat": 40.7122,
        "lng": -73.995613
    },
    "person": [],
    "date_created": "2024-12-17T16:21:36.694019Z",
    "notes": "",
    "url": "https://flickr.com/photos/81601686@N00/15851616658/",
    "is_favorite": false,
    "title": "Spencer Tunick in Chinatown",
    "photo_id": "15851616658",
    "user_id": "81601686@N00",
    "photo_url": "https://live.staticflickr.com/7579/15851616658_74cd2a0fc3_n.jpg",
    "timestamp": "2014-12-10T13:17:08Z",
    "coordinates": 13603,
    "search_request": 10660,
    "type": "flickr"
}
{
    "id": 145921,
    "location": {
        "lat": 40.724953,
        "lng": -74.002724
    },
    "person": [],
    "date_created": "2024-12-17T16:21:36.694102Z",
    "notes": "",
    "url": "https://flickr.com/photos/48889052497@N01/10996166044/",
    "is_favorite": false,
    "title": "O",
    "photo_id": "10996166044",
    "user_id": "48889052497@N01",
    "photo_url": "https://live.staticflickr.com/5529/10996166044_e657e98a27_n.jpg",
    "timestamp": "2013-11-22T11:37:28Z",
    "coordinates": 13603,
    "search_request": 10660,
    "type": "flickr"
}
```

### Add Workspace

This is initial endpoint which creates a new workspace based on latitude, longitude and radius. Title is also mandatory.

Maximum radius is 3000000m.

```python
import requests
import json

url = "https://osint.os-surveillance.io/api/addCoordinates"

payload = json.dumps({
  "title": "New York",
  "position": {
    "lat": 40.72020796700515,
    "lng": -74.0401684945897
  },
  "radius": 30000
})
headers = {
  'Authorization': 'Bearer',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

### Search

Run modules for given workspace and coordinates.
You must provide centre of your search and bounding box.
Bounding box must be inside of the bounding box as defined in Workspace.
Options parameter contains list of modules to run.

    flickr
    vkontakte

All modules are described in section Modules

Possible error messages:

    Please active your account.
    Coordinates are not in the bounding box
    Bounding box is not inside the workspace bounding box
    Bounding box area exceeds the limit of 1500 km²
    Too many modules chosen


```python
import requests
import json

url = "https://osint.os-surveillance.io/api/search"

payload = json.dumps({
  "options": [
    "flickr",
    "vkontakte"
  ],
  "keywords": None,
  "date_from": None,
  "date_to": None,
  "only_new": False,
  "coordinates_id": 2,
  "lat": 40.72695348506061,
  "lng": -73.99575186426779,
  "ne_lat": 40.81369273143631,
  "ne_lng": -73.15672826021006,
  "sw_lat": 40.605495194313995,
  "sw_lng": -74.56091832368662
})
headers = {
  'Authorization': 'Bearer',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

### Get progress

Get progress of the running modules.

```python
import requests
import json

url = "https://osint.os-surveillance.io/api/getProgress/{task_id}/"

payload = {}
headers = {
  'Authorization': 'Bearer',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

### Get search results

Get search results after all or some modules finished

```python
import requests
import json

url = "https://osint.os-surveillance.io/api/getSearchResults/{task_id}/"

payload = {}
headers = {
  'Authorization': 'Bearer',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
