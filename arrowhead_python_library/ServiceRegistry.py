import json
import aiohttp
import asyncio
import ServiceFinder
import ArrowheadJson

"""Publishing the service provider to the ServiceRegister"""
async def publish(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.serviceregistryURL + '/register', json=self.data) as resp:
                print(resp.status)
                print (self.data)
                if (resp.status == 201):
                    print("Service was registred to the service register")
                    print(await resp.json())
                    return True
                if (resp.status == 400):
                    print("Error: Service already exist")
                    print(await resp.json())
                    return False
                

"""Unpublishing the service provider from the service register"""
async def unpublish(self):
    async with aiohttp.ClientSession() as session:
        async with session.put(self.serviceregistryURL + '/remove', json=self.data) as resp:
            if resp.status == 200:
                print ("Service was unpublished from the register")
                return True
            else:
                print ("Something went wrong. No message was received.")
                return False
