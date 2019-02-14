"Change path to find the libraries"
import sys
sys.path.append('..')

"Normal imports"
from ..source.Consumer import Consumer
from datetime import datetime
import json
from aiohttp import web
import aiohttp
import asyncio
#from .source.Orchestrator import Orchestrator
#import Authorization

""" Creating a new consumer.  """
consumer = Consumer.Consumer("test_consumer", "127.0.0.1", 8081)

serviceProviderUrl = Orchestrator.orchestration_request(consumer, "CurrentTimeSweden")

async def send_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(resp.text())



loop = asyncio.get_event_loop()
g = loop.run_until_complete(Orchestrator.orchestration_request(consumer, "CurrentTime"))
loop.run_until_complete(consumer.consume_service(g))
loop.close()
