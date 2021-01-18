import requests
from datetime import datetime, timezone, timedelta
import time

#dt = datetime.utcnow()
current_time = datetime.now(timezone.utc)
current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print (f'starting time now is = {current_time_str}')

# Subtract 4wks (672hrs)
current_sub = current_time - timedelta(weeks=4)
current_time_loop = current_sub.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

url = "https://platform-dev06.dragos.services/assets/api/v4/associateAddresses"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46RHJAZ29zU3lzdDNt'
}

for i in range(10000):
    print(f'current_time_loop = {current_time_loop}')
    payload="{\n    \"lookups\": {\n        \"mac\": {\n            \"type\": \"coordinates\",\n            \"coordinates\": {\n                \"type\": \"MAC\",\n                \"networkId\": \"test_network1\",\n                \"value\": \"DE:AD:BE:EF:BE:BE\"\n            },\n            \"createIfMissing\": true\n        },\n        \"ip\": {\n            \"type\": \"coordinates\",\n            \"coordinates\": {\n                \"type\": \"IP\",\n                \"value\": \"1.2.3.4\",\n                \"networkId\": \"test_network1\"\n            },\n            \"createIfMissing\": true\n        }\n    },\n    \"associateLookups\": {\n        \"mac\": [\"ip\"]\n    },\n    \"at\":" + "\"" + current_time_loop + "\"" + "\n}"
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f'==> status code = {response.status_code}')
    print(response.text)

    add_2m = current_sub + timedelta(minutes=2)
    current_time_loop = add_2m.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    current_sub = add_2m
    print(f'current_time_loop = {current_time_loop}')
    payload="{\n    \"lookups\": {\n        \"mac\": {\n            \"type\": \"coordinates\",\n            \"coordinates\": {\n                \"type\": \"MAC\",\n                \"networkId\": \"test_network1\",\n                \"value\": \"DE:AD:BE:EF:DE:AD\"\n            },\n            \"createIfMissing\": true\n        },\n        \"ip\": {\n            \"type\": \"coordinates\",\n            \"coordinates\": {\n                \"type\": \"IP\",\n                \"value\": \"1.2.3.4\",\n                \"networkId\": \"test_network1\"\n            },\n            \"createIfMissing\": true\n        }\n    },\n    \"associateLookups\": {\n        \"mac\": [\"ip\"]\n    },\n    \"at\":" + "\"" + current_time_loop + "\"" + "\n}"
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f'==> status code = {response.status_code}')
    print(response.text)

    add_2m = current_sub + timedelta(minutes=2)
    current_time_loop = add_2m.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    current_sub = add_2m
    print(f'====> loop({i})')

