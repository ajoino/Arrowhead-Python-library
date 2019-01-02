import json
import aiohttp
import asyncio
import ServiceFinder


class Consumer:
    def __init__(self, name, address, port):
        self.systemName = name
        self.address = address
        self.port = port
        


    async def consume_service(self, providerUrl):
        async with aiohttp.ClientSession() as session:
            async with session.get(providerUrl) as resp:
                data = (await resp.read())
                jsonData = json.loads(data)
                print(jsonData)
                return jsonData

    async def orchestration_request(self, serviceDefinition):
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

                
#consumer = Consumer("emilsnya", "127.0.0.1", 8082)
#loop = asyncio.get_event_loop()
#g = loop.run_until_complete(consumer.orchestration_request("CurrentTime"))
#loop.run_until_complete(consumer.consume_service(g))
#loop.close()
