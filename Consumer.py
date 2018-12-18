import json
import aiohttp
import asyncio

#class Consumer:
 #   def __init__(self, )


async def consumeService(providerUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(providerUrl) as resp:
            data = (await resp.read())
            print (json.loads(data))
            
    #async def getOrchestratorUrl()

    #async def sendOrchestrationRequest()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(consumeService('http://localhost:8080'))
loop.close()
