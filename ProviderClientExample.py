import Provider
from datetime import datetime
import json
from aiohttp import web
import asyncio
import Orchestrator
import Authorization
import Consumer


consumer = Consumer.Consumer("emilsnya", "127.0.0.1", 8082)
provider = Provider.Provider("CurrentTimeSweden", "CurrentTime","/", 8080, "127.0.0.1", ["JSON"] ,"127.0.0.1:8442", {})
Authorization.authorize(consumer, provider.name, provider.address, provider.port, provider.definition, provider.interfaces, provider.metadata)
#provider.start()
#provider.registerToOrch()
#Orchestrator.register_to_orchestrator(provider, "emilsnya", "127.0.0.1", 8082, "null")
#Authorization.register_to_authorization(provider,"emilsnya", "127.0.0.1", 8082, "null")

async def handle_request(request):
    try:          
        time = str(datetime.now())
        response = {'time':time}
        print (response)
        provider.stop()
        return web.Response(text=json.dumps(response), status=200)
    except Exception as e:
        return web.Response(text=json.dumps({'message': 'Something went wrong'}), status=400)




app = web.Application()
app.router.add_get('/', handle_request)

web.run_app(app)




