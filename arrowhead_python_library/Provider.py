import json
import aiohttp
import asyncio
import ServiceFinder
import ArrowheadJson

"""An Arrowhead provider that can publish and unpublish itself from the service registry."""
class Provider:
    def __init__(self, name, definition, uri, port, address, interfaces, serviceregistryURL, metadata):
        self.name = name
        self.definition = definition
        self.uri = uri
        self.port = port
        self.interfaces = interfaces
        self.address = address
        self.metadata = metadata
        self.serviceregistryURL = "http://" + ServiceFinder.get_insecure_service_registry() + "/serviceregistry"
        self.orchestratorURL = ServiceFinder.get_insecure_orchestrator()
        self.authorizationURL = ServiceFinder.get_insecure_authorization()
        self.data= self._create_json_data()

    """Publishing the service provider to the ServiceRegister"""
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
                    

    """Unpublishing the service provider from the service register"""
    async def unpublish(self):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.serviceregistryURL + '/remove', json=self.data) as resp:
                if resp.status == 200:
                    print ("Service was unpublished from the register")
                else:
                    print ("Something went wrong. No message was received.")
                    return

    """A consumer can be registred to the orchestrator for allowing the consumer to find the service provider """
    async def _register_to_orchestrator(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):     
        async with aiohttp.ClientSession() as session:
            orchestrationData = ArrowheadJson.createOrchestratorData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, self.name, self.address, self.port, self.definition, self.interfaces, self.metadata)
            data = "["+json.dumps(orchestrationData) +"]" #Needs to be converted to a Java Array because thats what the arrowhead core wants... suck...
            jsonData = json.loads(data)
            print(jsonData)
            async with session.post("http://"+ self.orchestratorURL +"/orchestrator/mgmt/store", json=jsonData) as resp:
                print (resp.status)
                print (await resp.json())
                
                
    async def _register_to_authorization(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):  
        async with aiohttp.ClientSession() as session:
            authorizationData = ArrowheadJson.createAuthorizationData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, self.name, self.address, self.port, self.definition, self.interfaces, self.metadata)
            async with session.post("http://" + self.authorizationURL + "/authorization/mgmt/intracloud", json=authorizationData) as resp:
                print (resp.status)
                print (await resp.json())
                
    
    """ Converts the provider to JSON-format  """
    def _create_json_data(self):
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
            for _x,_y in self.metadata.items():
                metaData[_x] = _y
            data['serviceURI'] = self.uri
            return data

    """ Publishes the service to the service register.  """
    def start(self):
        loop.run_until_complete(self.publish())

    """ Unpublishes the service from the service register.  """
    def stop(self):
        loop.run_until_complete(self.unpublish())

    """ A consumer can be registred to the orchestrator for allowing the consumer to find the service provider  """
    def register_consumer(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
        loop.run_until_complete(self._register_to_orchestrator(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))
        
    def register_to_authorization(self, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
        loop.run_until_complete(self._register_to_authorization(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))

loop = asyncio.get_event_loop()
