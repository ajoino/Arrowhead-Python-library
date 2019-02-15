import sys, os

home_dir = os.environ['HOME']
source_dir = home_dir + '/Arrowhead-Python-library/source/'
sys.path.append(home_dir + '/Arrowhead-Python-library/source/')


import json
def createAuthorizationData(consumerSystemName,
                                consumerAddress,
                                consumerPort,
                                consumerAuthenticationInfo,
                                providerSystemName,
                                providerAddress,
                                providerPort,
                                serviceDefinition,
                                interfaces,
                                metadata):
    
    with open(source_dir + 'auth_entry.json') as file:
            data = json.load(file)
            consumer = data['consumer']

            consumer['systemName'] = consumerSystemName
            consumer['address'] = consumerAddress
            consumer['port'] = consumerPort
            consumer['authenticationInfo'] = consumerAuthenticationInfo

            providerList = data['providerList'][0]

            providerList['systemName'] = providerSystemName
            providerList['address'] = providerAddress
            providerList['port'] = providerPort


            serviceList = data['serviceList'][0]
            serviceList['serviceDefinition'] = serviceDefinition
            serviceList['interfaces'] = interfaces

            data['serviceMetadata'] = ""
            
            return data


def createOrchestratorData(consumerSystemName,
                                consumerAddress,
                                consumerPort,
                                consumerAuthenticationInfo,
                                providerSystemName,
                                providerAddress,
                                providerPort,
                                serviceDefinition,
                                interfaces,
                                metadata):
    
    with open(source_dir + 'storeEntry.json') as file:
            data = json.load(file)
            service = data['service']
            service['serviceDefinition'] = serviceDefinition
            service['interfaces'] = interfaces
            service['serviceMetadata'] = metadata

            consumer = data['consumer']
            consumer['systemName'] = consumerSystemName
            consumer['address'] = consumerAddress
            consumer['port'] = consumerPort

            providerSystem = data['providerSystem']
            providerSystem['systemName'] = providerSystemName
            providerSystem['address'] = providerAddress
            providerSystem['port'] = providerPort
            return data

def createIntraCloudAuthRequestData(consumerSystemName,
                                consumerAddress,
                                consumerPort,
                                providerSystemName,
                                providerAddress,
                                providerPort,
                                serviceDefinition):
    
    with open(source_dir + 'IntraCloudAuthRequest.json') as file:
            data = json.load(file)
            print (data)
            service = data['service']
            service['serviceDefinition'] = serviceDefinition

            consumer = data['consumer']
            consumer['systemName'] = consumerSystemName
            consumer['address'] = consumerAddress
            consumer['port'] = consumerPort

            providerSystem = data['providers'][0]
            providerSystem['systemName'] = providerSystemName
            providerSystem['address'] = providerAddress
            providerSystem['port'] = providerPort
            return data



    
