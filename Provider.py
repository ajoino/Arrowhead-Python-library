import json
import aiohttp
import asyncio

class Provider:
    def __init__(self, name, definition, uri, port, address, interfaces, serviceregistryURL, metadata):
        self.name = name
        self.definition = definition
        self.uri = uri
        self.port = port
        self.interfaces = interfaces
        self.address = address
        self.metadata = metadata
        self.serviceregistryURL = "http://" + serviceregistryURL + "/serviceregistry"
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
                        await self.registerToStore()
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


    async def registerToStore(self):
        async with aiohttp.ClientSession() as session:
            
            data = "["+json.dumps(self.getData()) +"]" #Needs to be converted to a Java Array
            jsonData = json.loads(data)
            print(jsonData)
            async with session.post("http://localhost:8440/orchestrator/mgmt/store", json=jsonData) as resp:
                print (resp.status)
                print (await resp.json())
                
    
    def getData(self):
        with open('storeEntry.json') as file:
            data = json.load(file)
            print (data)
            service = data['service']
            service['serviceDefinition'] = self.definition
            service['interfaces'] = self.interfaces
            service['serviceMetadata'] = self.metadata

            consumer = data['consumer']
            consumer['systemName'] = "EmilTest"
            consumer['address'] = "localhost"
            consumer['port'] = 8080

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

    async def stop(self):
        await self.unpublish()

        
        

loop = asyncio.get_event_loop()
#loop = asyncio.get_event_loop()
#print(json.loads('{"gg" : "cool"}'))
#test = Provider("Test", "gg","123", 8040, "127.0.0.1", ["KUL", "KILLE"] ,"127.0.0.1:8442", {"apa": "djur", "bil": "Ford"})
#print (test.serviceregistryURL)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(test.publish())
#loop.close()
