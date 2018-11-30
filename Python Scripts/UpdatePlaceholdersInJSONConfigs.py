#Update placeholders in config JSON files
#Uses Artifactory Pro REST API
#Can be run manually or as part of Jenkins pipeline

import os
import json
import requests

#enter credentials
username = "admin" #auth not required for this api
password = "admin"
artifactory = "http://127.0.0.1:8081/artifactory/" #artifactory URL
#set json path
path_to_json = 'C:\\Configs\\'

def replace_placeholders_in_json_files( json_files ):
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js), 'r') as json_file:
            json_data = json.load(json_file)
            updated = False
            for item in json_data['services']:
                if '{{{' in item['item']:
                    item_value = item['item']
                    #get latest version from artifactory
                    package = item_value.lstrip('{{{').rstrip('}}}')
                    api = "api/search/latestVersion?g=" + package
                    url = artifactory + api
                    r = requests.get(url, auth = (username, password))
                    if r.status_code == 200:
                        print(r.content)
                        version = r.content
                        #update item
                        item['item'] = package + '.' + version
                        updated = True
                    else:
                        print("Fail")
                        response = json.loads(r.content)
                        print(response["errors"])
                        print("x-request-id : " + r.headers['x-artifactory-id'])
                        print("Status Code : " + str(r.status_code))
        if updated == True:
            with open(os.path.join(path_to_json, js), 'w') as file:
                json.dump(json_data, file, indent=4)

#set json path
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
replace_placeholders_in_json_files(json_files)
