import sys, os

home_dir = os.environ['HOME']
source_dir = home_dir + '/Arrowhead-Python-library/source/'
sys.path.append(home_dir + '/Arrowhead-Python-library/source/')

#Regular imports
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

    def __enter__(self):
        self.start()

    async def __exit__(self, exc_type, exc_val, traceback):
        await self.stop()

    """Publishing the service provider to the ServiceRegister"""
    async def publish(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.serviceregistryURL + '/register', json=self.data) as resp:
                if (resp.status == 201):
                    print("Service was registred to the service register")
                    return True
                    if (resp.status == 400):
                        print("Error: Service already exist")
                        return False


    """Unpublishing the service provider from the service register"""
    async def unpublish(self):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.serviceregistryURL + '/remove', json=self.data) as resp:
                if resp.status == 200:
                    print ("Service was unpublished from the register")
                    return True
                else:
                    print ("This service is not in the registry")
                    return False


    """ Converts the provider to JSON-format  """
    def _create_json_data(self):
        with open(source_dir + 'ServiceRegistryEntry.json') as file:
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
    async def stop(self):
        await(self.unpublish())


loop = asyncio.get_event_loop()
