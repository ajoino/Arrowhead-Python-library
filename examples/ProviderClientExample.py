import Provider
from datetime import datetime
import json
from aiohttp import web
import asyncio
import Orchestrator
import Authorization

""" Creating a new service provider object.  """
provider = Provider.Provider("CurrentTimeSweden", "CurrentTime","/", 8080, "127.0.0.1", ["JSON"] ,"127.0.0.1:8442", {})

""" Publishing the service to the service registry.  """
provider.start()

""" Adding the provider to the orchestrator with a specific consumer.  """
Orchestrator.register_to_orchestrator(provider, "test_consumer1", "127.0.0.1", 8081, "null")

Authorization.register_to_authorization(provider, "test_consumer1", "127.0.0.1", 8081, "null")


#consumer = Consumer.Consumer("test_consumer", "127.0.0.1", 8081)

#Authorization.authorize(consumer, "CurrentTimeSweden", "127.0.0.1", 8080, "CurrentTime")


##with Provider.Provider("CurrentTimeSweden", "CurrentTime","/", 8080, "127.0.0.1", ["JSON"] ,"127.0.0.1:8442", {}) as provider:
##    while True:
##        i = 1
        
    
""" The application to be runned. This is a basic web application that returns the current time in JSON format.  """
async def handle_request(request):
    try:          
        time = str(datetime.now())
        response = {'time':time}
        await(provider.stop())
        return web.Response(text=json.dumps(response), status=200)
    except Exception as e:
        print(e)
        return web.Response(text=json.dumps({'message': 'Something went wrong'}), status=400)




app = web.Application()
app.router.add_get('/', handle_request)
web.run_app(app)
