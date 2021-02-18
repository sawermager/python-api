import requests
from datetime import datetime, timezone, timedelta
import json
import socket
import random
import struct
import time

"""
SBACK-875: Associate a HOSTNAME to two different assets
at the same (or close) time and verify associating the
second doesn’t bounce the association from the first one
but both exist in parallel

Expected results should show overlapping time ranges for associations:
asset1  t1 <--h----------------------------><some time>
asset2             t2 <--h----------><somme time>
i.e when the hostname is seen with another asset it just starts
another association without ending the original. The address can
be associated to multiple assets at the same time.

Manually inspect assets "hostname" timeRanges. They should overlap.
POST https://platform-dev06.dragos.services/assets/api/v4/getAssets
payload:
{
    "selector": {
        "idOrOldIdIn": [
            68832,
            68833
        ]
    }
}
"""

# utcnow() has funky issues (bug?) with using timedelta() to add/subtract
# timestamps. So, ditched it for now(timezone.utc).
# Sidenote, utcnow() also isn't timezone aware.
current_time = datetime.now(timezone.utc)
current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print (f'starting time is = {current_time_str}')

#url = "https://sitestore-test-reg4.hq.dragos.services/assets/api/v4/associateAddresses"
url = "https://platform-dev06.dragos.services/assets/api/v4/associateAddresses"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46RHJAZ29zU3lzdDNt'
}

# json grabbed from POSTMAN. Could have just used python code generated by POSTMAN
# but variable substitution into a python dict (produced by json.loads()) is easier/cleaner
# than doing it a python string.
# Using 'r' for 'raw' data to keep python from complaining about json value,'true',
# not being defined.
payload_json_1 = r'''{
    "lookups": {
        "hostname": {
            "type": "coordinates",
            "coordinates": {
                "type": "HOSTNAME",
                "networkId": "test_network1",
                "value": "hostname_test_2"
            },
            "createIfMissing": true
        },
        "ip": {
            "type": "coordinates",
            "coordinates": {
                "type": "IP",
                "value": "1.2.3.4",
                "networkId": "test_network2"
            },
            "createIfMissing": true
        }
    },
    "associateLookups": {
        "ip": ["hostname"]
    },
    "at": "time_stub"
    }'''

payload_json_2 = r'''{
    "lookups": {
        "hostname": {
            "type": "coordinates",
            "coordinates": {
                "type": "HOSTNAME",
                "networkId": "test_network1",
                "value": "hostname_test_2"
            },
            "createIfMissing": true
        },
        "ip": {
            "type": "coordinates",
            "coordinates": {
                "type": "IP",
                "value": "4.3.2.1",
                "networkId": "test_network3"
            },
            "createIfMissing": true
        }
    },
    "associateLookups": {
        "ip": ["hostname"]
    },
    "at": "time_stub"
    }'''

for i in range(1):

    print(f'====> loop({i})')

    # utcnow() has funky issues (bug?) with using timedelta() to add/subtract
    # timestamps. So, ditched it for now(timezone.utc).
    # Sidenote, utcnow() also isn't timezone aware.
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print (f't1 = {current_time_str}')

    # Create "random" and hopefully unique IP_1 and IP_2
    IP_1 = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    IP_2 = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    # Convert json into python object (dict) for easier variable substitution of incrementing
    # timestamp and IP[1|2]
    payload_1 = json.loads(payload_json_1)
    payload_1['lookups']['ip']['coordinates']['value'] = IP_1
    payload_1['at'] = current_time_str

    # Make 1st request and output the status code and response
    response_1 = requests.request("POST", url, headers=headers, json=payload_1, verify=False)
    print(f'==> status code request_1 = {response_1.status_code}')
    print(response_1.text)

    # Sleep for 1min (less code than adjusting utc time
    # but of course doesn't look as cool)
    time.sleep(60)
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print (f't2 = {current_time_str}')

    payload_2 = json.loads(payload_json_2)
    payload_2['lookups']['ip']['coordinates']['value'] = IP_2
    payload_2['at'] = current_time_str

    # Make 2st request and output the status code and response
    response_2 = requests.request("POST", url, headers=headers, json=payload_2, verify=False)
    print(f'==> status code request_2 = {response_2.status_code}')
    print(response_2.text)