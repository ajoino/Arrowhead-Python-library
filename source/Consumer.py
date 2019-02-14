import json
import aiohttp
import asyncio
#import ServiceFinder
import os


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


