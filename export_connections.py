import requests
import json
import urllib
from pprint import pprint
import urllib3
import csv

urllib3.disable_warnings()

netbox_api_key = 'XYZ'
server_name = 'SERVER_NAME'
tenant_name = 'TENANT_NAME'

headers = {
    'Authorization': 'Token ' + netbox_api_key
}

def response_to_json(response):
    json_data = json.loads(response.text)
    return json_data


def get_tenant_id(headers):
    response = requests.get('https://' + server_name + '/api/tenancy/tenants/?name=' + tenant_name, headers=headers, verify=False)
    return response


def get_devices(headers, tenant_id_number):
    response = requests.get('https://' + server_name + '/api/dcim/devices/?tenant_id=' + str(tenant_id_number), headers=headers, verify=False)
    return response


def get_interface_connections(headers, device_id):
    response = requests.get('https://' + server_name + '/api/dcim/interface-connections/?device_id=' + str(device_id), headers=headers, verify=False)
    return response


def get_device_info(headers, device_id):
    response = requests.get('https://' + server_name + '/api/dcim/devices/' + str(device_id), headers=headers, verify=False)
    return response


# Get tenant ID number
tenant_id = response_to_json(get_tenant_id(headers))
tenant_id_number = tenant_id['results'][0]['id']

# Get devices assigned to that tenant
devices = response_to_json(get_devices(headers, tenant_id_number))


device_id_list = []
for device in devices['results']:
	device_id_list.append(device['id'])



csv_list = []
for device in device_id_list:
    #hostname of device
    #hostname = response_to_json(get_device_info(headers, device))['name']
    connections = response_to_json(get_interface_connections(headers, device))
    #pprint(connections)
    #local device name
    #pprint(connections['results'][0]['interface_b']['device']['name'])
    #local interface name
    #pprint(connections['results'][0]['interface_b']['name'])
    #remote device name
    #pprint(connections['results'][0]['interface_a']['device']['name'])
    #local interface name
    #pprint(connections['results'][0]['interface_a']['name'])
    
    if connections['count'] == 0:
        pass
    else:
        for result in connections['results']:
        	another_list = [result['interface_a']['device']['display_name'], 
        	                result['interface_a']['name'],
        	                result['interface_b']['device']['display_name'],
        	                result['interface_b']['name']]
        	#print(another_list)
        	csv_list.append(another_list) 
            #print(str(result['interface_a']['device']['display_name']) + " - " + str(result['interface_a']['name'])  + " - " + str(result['interface_b']['device']['display_name']) + " - " + str(result['interface_b']['name']))

print(csv_list)

with open('connections.csv', 'w') as f:
    for connection in csv_list:
        for item in connection:
            f.write(item + ',')
        f.write('\n')
