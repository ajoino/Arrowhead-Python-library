import sys, os

home_dir = os.environ['HOME']
source_dir = home_dir + '/Arrowhead-Python-library/source/'
sys.path.append(home_dir + '/Arrowhead-Python-library/source/')

import json

def get_insecure_service_registry():
    with open(source_dir + 'ServiceLocations.json') as file:
        data = json.load(file)
        serviceRegistry = data['service_registry']
        url = serviceRegistry['url']
        port = serviceRegistry['insecure_port']
        fullUrl = url + ":" + str(port)
        return fullUrl

def get_insecure_orchestrator():
    with open(source_dir + 'ServiceLocations.json') as file:
        data = json.load(file)
        orchestrator = data['orchestrator']
        url = orchestrator['url']
        port = orchestrator['insecure_port']
        fullUrl = url + ":" + str(port)
        return fullUrl

def get_insecure_authorization():
    with open(source_dir + 'ServiceLocations.json') as file:
        data = json.load(file)
        auth = data['authorization']
        url = auth['url']
        port = auth['insecure_port']
        fullUrl = url + ":" + str(port)
        return fullUrl
