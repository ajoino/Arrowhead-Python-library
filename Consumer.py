import json
import aiohttp
import asyncio

class Consumer:
    def __init__(self, name):
        self.name = name
        self.orchestrator = "http://127.0.0.1:8440/"
        


    async def consumeService(self, providerUrl):
        async with aiohttp.ClientSession() as session:
            async with session.get(providerUrl) as resp:
                data = (await resp.read())
                jsonData = json.loads(data)
                print(jsonData)
                return jsonData

    async def orchestrationRequest(self, serviceDefinition):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.orchestrator + "orchestrator/store/consumername/" + self.name + "/servicedef/" + serviceDefinition) as resp:
                data = json.loads(await resp.read())        
                responseJson = (data[0])
                providerSystem = responseJson['providerSystem']
                address = providerSystem['address']
                port = providerSystem['port']
                fullAddress = "http://" + address + ":" + str(port)
                print(fullAddress)
                return fullAddress

                
consumer = Consumer("emilsnya")
loop = asyncio.get_event_loop()
g = loop.run_until_complete(consumer.orchestrationRequest("CurrentTime"))
loop.run_until_complete(consumer.consumeService(g))
loop.close()
