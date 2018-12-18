import json
import aiohttp
import asyncio

class Client:
    def __init__(self, name, definition, uri, port, address, serviceregistryURL):
        self.name = name
        self.definition = definition
        self.uri = uri
        self.port = port
        self.address = address
        self.serviceregistryURL = "http://" + serviceregistryURL + "/serviceregistry"
        self.data= self.createJSONdata()

    """Publishing the service to the ServiceRegister"""
    async def publish(self):
            async with aiohttp.ClientSession() as session:
                async with session.post(self.serviceregistryURL + '/register', json=self.data) as resp:
                    if (resp.status == 201):
                        print("Service was registred to the service register")

                    if (resp.status == 400):
                        print("Error: Service already exist")
                        print(await resp.json())

    """Unpublishing the server from the serverRegister"""
    async def unpublish(self):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.serviceregistryURL + '/remove', json=self.data) as resp:
                if resp.status == 200:
                    print("Service is unpublished from the register")
                else:
                    print ("Something went wrong. No message was received.")



    """Converts the provider to JSON-format"""
    def createJSONdata(self):
        with open('ServiceRegistryEntry.json') as file:
            data = json.load(file)

            providedService = data['providedService']
            provider = data['provider']

            providedService['serviceDefinition'] = self.definition
            provider['systemName'] = self.name
            provider['address'] = self.address
            provider['port'] = self.port
            
            data['serviceURI'] = self.uri
            return data


#loop = asyncio.get_event_loop()
#test = Client("Test", "gg","123", 8040, "127.0.0.1", "127.0.0.1:8442")
#loop = asyncio.get_event_loop()
#loop.run_until_complete(test.publish())
#loop.close()
