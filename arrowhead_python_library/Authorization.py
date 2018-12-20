import json
import aiohttp
import asyncio
import ArrowheadJson
import ServiceFinder
import Provider

authorizationURL = ServiceFinder.get_insecure_authorization()

async def _register_to_authorization(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):  
        async with aiohttp.ClientSession() as session:
            authorizationData = ArrowheadJson.createAuthorizationData(consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo, provider.name, provider.address, provider.port, provider.definition, provider.interfaces, provider.metadata)
            async with session.post("http://" + authorizationURL + "/authorization/mgmt/intracloud", json=authorizationData) as resp:
                print (resp.status)
                print (await resp.json())

async def _authorize(consumer, providerName, providerAddress, providerPort, servicedefinition):
        async with aiohttp.ClientSession() as session:
            authorizationData = ArrowheadJson.createIntraCloudAuthRequestData(consumer.systemName, consumer.address, consumer.port, providerName, providerAddress, providerPort, servicedefinition)
            async with session.put("http://" + authorizationURL + "/authorization/intracloud", json=authorizationData) as resp:
                print (resp.status)
                data = await resp.json()
                if resp.status == 404:
                        raise Exception("Consumer System is not in the authorization database.")
                else:
                        response = data['authorizationState'] #Detta response har en knepig key...
                        result = list(response.values())        #Because of the strange JSON key we get from the authorization we need to make a list to extract the value           
                        return result[0]
                
def register_to_authorization(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo):
        loop.run_until_complete(_register_to_authorization(provider, consumerSystemName, consumerAddress, consumerPort, consumerAuthenticationInfo))



def authorize(consumer, providerName, providerAddress, providerPort, servicedefinition):
        return loop.run_until_complete(_authorize(consumer, providerName, providerAddress, providerPort, servicedefinition))
        
        
loop = asyncio.get_event_loop()
