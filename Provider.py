import json
import aiohttp
import asyncio
import ServiceFinder
import ArrowheadJson

class Provider:
    def __init__(self, name, definition, uri, port, address, interfaces, serviceregistryURL, metadata):
        self.name = name
        self.definition = definition
        self.uri = uri
        self.port = port
        self.interfaces = interfaces
        self.address = address
        self.metadata = metadata
        self.serviceregistryURL = "http://" + ServiceFinder.getInsecureServiceRegistry() + "/serviceregistry"
        self.orchestratorURL = ServiceFinder.getInsecureOrchestrator()
        self.authorizationURL = ServiceFinder.getInsecureAuthorization()
        self.data= self.createJSONdata()

    """Publishing the service to the ServiceRegister"""
    async def publish(self):
            async with aiohttp.ClientSession() as session:
                async with session.post(self.serviceregistryURL + '/register', json=self.data) as resp:
                    print(resp.status)
                    print (self.data)
                    if (resp.status == 201):
                        print("Service was registred to the service register")
                        print(await resp.json())
                    if (resp.status == 400):
                        print("Error: Service already exist")
                        print(await resp.json())
                    

    """Unpublishing the server from the serverRegister"""
    async def unpublish(self):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.serviceregistryURL + '/remove', json=self.data) as resp:
                if resp.status == 200:
                    print ("Service was unpublished from the register")
                else:
                    print ("Something went wrong. No message was received.")
                    return


    async def registerToOrchestrator(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):     
        async with aiohttp.ClientSession() as session:
            orchestrationData = ArrowheadJson.createOrchestratorData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, self.name, self.address, self.port, self.definition, self.interfaces, self.metadata)
            data = "["+json.dumps(orchestrationData) +"]" #Needs to be converted to a Java Array because thats what the arrowhead core wants... suck...
            jsonData = json.loads(data)
            print(jsonData)
            async with session.post("http://"+ self.orchestratorURL +"/orchestrator/mgmt/store", json=jsonData) as resp:
                print (resp.status)
                print (await resp.json())
                

    async def registerToAuthorization(self):
        async with aiohttp.ClientSession() as session:
            data = self.authorizationData()
            async with session.post("http://" + self.authorizationURL + "/authorization/mgmt/intracloud", json=data) as resp:
                print (resp.status)
                print (await resp.json())
                

    def authorizationData(self):
        with open('auth_entry.json') as file:
            data = json.load(file)
            consumer = data['consumer']

            consumer['systemName'] = "Test1"
            consumer['address'] = "localhost"
            consumer['port'] = 8083

            providerList = data['providerList'][0]

            providerList['systemName'] = "CurrenTimeSweden"
            providerList['address'] = "localhost"
            providerList['port'] = 8080


            serviceList = data['serviceList'][0]
            serviceList['serviceDefinition'] = "CurrentTime"

            data['serviceMetadata'] = ""
            
            print(data)
            return data
    
    def getData(self):
        with open('storeEntry.json') as file:
            data = json.load(file)
            print (data)
            service = data['service']
            service['serviceDefinition'] = self.definition
            service['interfaces'] = self.interfaces
            service['serviceMetadata'] = self.metadata

            consumer = data['consumer']
            consumer['systemName'] = "emilsnya"
            consumer['address'] = "localhost"
            consumer['port'] = 8082

            providerSystem = data['providerSystem']
            providerSystem['systemName'] = self.name
            providerSystem['address'] = self.address
            providerSystem['port'] = 8080

            
            print(data)
            return data
    
    """Converts the provider to JSON-format"""
    def createJSONdata(self):
        with open('ServiceRegistryEntry.json') as file:
            data = json.load(file)

            providedService = data['providedService']
            provider = data['provider']

            providedService['serviceDefinition'] = self.definition
            providedService['interfaces'] = self.interfaces
            provider['systemName'] = self.name
            provider['address'] = self.address
            provider['port'] = self.port

            metaData = providedService['serviceMetadata']
            for x,y in self.metadata.items():
                metaData[x] = y
            data['serviceURI'] = self.uri
            return data

    def start(self):
        loop.run_until_complete(self.publish())

    def stop(self):
        loop.run_until_complete(self.unpublish())

    def registerConsumer(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
        loop.run_until_complete(self.registerToOrchestrator(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))
        
        

loop = asyncio.get_event_loop()
