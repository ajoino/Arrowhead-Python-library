import Provider
from datetime import datetime
import json
from aiohttp import web
import asyncio

provider = Provider.Provider("CurrentTimeSweden", "CurrentTime","/", 8080, "127.0.0.1", ["JSON"] ,"127.0.0.1:8442", {})
provider.start()

async def handle_request(request):
    try:          
        time = str(datetime.now())
        response = {'time':time}
        print (response)
        await provider.stop()
        return web.Response(text=json.dumps(response), status=200)
    except Exception as e:
        return web.Response(text=json.dumps({'message': 'Something went wrong'}), status=400)




app = web.Application()
app.router.add_get('/', handle_request)

web.run_app(app)




