import json
import aiohttp
import asyncio
import ArrowheadJson
import ServiceFinder
import Provider

orchestratorURL = ServiceFinder.get_insecure_orchestrator() #The location of the orchestrator

"""A consumer can be registred to the orchestrator for allowing the consumer to find the service provider """
async def _register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
    async with aiohttp.ClientSession() as session:
        orchestrationData = ArrowheadJson.createOrchestratorData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, provider.name, provider.address, provider.port, provider.definition, provider.interfaces, provider.metadata)
        data = "["+json.dumps(orchestrationData) +"]" #Needs to be converted to a Java Array because thats what the arrowhead core wants... suck...
        jsonData = json.loads(data)
        print(jsonData)
        async with session.post("http://"+ orchestratorURL +"/orchestrator/mgmt/store", json=jsonData) as resp:
            print (resp.status)
            print (await resp.json())

async def _orchestration_request(consumer, serviceDefinition):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://" + orchestratorURL + "/orchestrator/store/consumername/" + consumer.name + "/servicedef/" + serviceDefinition) as resp:
            data = json.loads(await resp.read())        
            responseJson = (data[0])
            providerSystem = responseJson['providerSystem']
            address = providerSystem['address']
            port = providerSystem['port']
            fullAddress = "http://" + address + ":" + str(port)
            print(fullAddress)
            return fullAddress

""" A consumer can be registred to the orchestrator for allowing the consumer to find the service provider  """
def register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
    loop.run_until_complete(_register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))

loop = asyncio.get_event_loop()
