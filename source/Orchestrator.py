import json
import aiohttp
import asyncio
import ArrowheadJson
import ServiceFinder
import Provider
import Authorization

orchestratorURL = ServiceFinder.get_insecure_orchestrator() #The location of the orchestrator

"""A consumer can be registred to the orchestrator for allowing the consumer to find the service provider """
async def _register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
    async with aiohttp.ClientSession() as session:
        orchestrationData = ArrowheadJson.createOrchestratorData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, provider.name, provider.address, provider.port, provider.definition, provider.interfaces, provider.metadata)
        data = "["+json.dumps(orchestrationData) +"]" #Needs to be converted to a Java Array because thats what the arrowhead core wants... suck...
        jsonData = json.loads(data)
        async with session.post("http://"+ orchestratorURL +"/orchestrator/mgmt/store", json=jsonData) as resp:
            print("Service was added to orchestrator with consumer: " + consumerSystemName)

async def _orchestration_request(consumer, serviceDefinition):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://" + orchestratorURL + "/orchestrator/store/consumername/" + consumer.systemName + "/servicedef/" + serviceDefinition) as resp:
            if resp.status == 404:
                return False
            data = json.loads(await resp.read())
            responseJson = (data[0])
            
            providerSystem = responseJson['providerSystem']

            systemName = providerSystem['systemName']
            address = providerSystem['address']
            port = providerSystem['port']
            
            authorized = Authorization.authorize(consumer, systemName, address, port, serviceDefinition) #Authorization conrol

            if authorized:
                fullAddress = "http://" + address + ":" + str(port)
                print(fullAddress)
                return fullAddress

            else:
                raise Exception("System is not authrized")
            
            

""" A consumer can be registred to the orchestrator for allowing the consumer to find the service provider  """
def register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
    loop.run_until_complete(_register_to_orchestrator(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))

def orchestration_request(consumer, serviceDefinition):
    return loop.run_until_complete(_orchestration_request(consumer, serviceDefinition))

loop = asyncio.get_event_loop()
