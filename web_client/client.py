import asyncio

import logging

import aiohttp
from aiohttp import ClientSession
from aiohttp import web

from flask import *
import csv
import docker
import os
import socket
#Maintainer:Derick Omuga 
def get_replica(service_name):
    try:
        # Resolve the DNS entry for the service name
        ips = socket.gethostbyname_ex(service_name)[2]
        return ips
    except socket.gaierror as e:
        print(f"Error resolving service '{service_name}': {e}")
        return []

async def make_request(session, url):
    async with session.get(url) as response:
        return await response.text()

async def experiment_a1():
    #url = 'http://localhost:5000/home'
    docker_service_name = "load_balancer"
    replica_ips = get_replica(docker_service_name)
    server =replica_ips[0]
    url=f"http://{server}:5000/home"
    tasks = []
  
  # Register your catcher as an aiohttp middleware:
    try:
        async with ClientSession() as session:
            for _ in range(10000):
                tasks.append(make_request(session, url))
            responses = await asyncio.gather(*tasks)
    except Exception as e:
            return None
    # Process responses to count requests handled by each server instance
    count = {}
    count2=0
    result=[]
    result3=[]
    data3=[]
    for response in responses:
      count2=count2+1
      #print(response)
      data = json.loads(response)
   #   print(data["message"])
      #pattern = r'(?<="web_server-\d+")\w+'
      result=data["message"].split(":")
   
      #print(result[1])
      #result = re.match(pattern,data["message"])
      #print(result)
      #try:
       #result  = re.match(pattern response).group()
      #except AttributeError:
       #   result  = re.match(pattern, response)
   #Maintainer:Derick Omuga         
      
      server=result[1]
      data3.append(str(server)+","+str(count2))
      
      #count2.append(count)
      result3.append(result[1])
      with open('experiment_a1_results.csv', 'w',encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        for line in data3:
             writer.writerow(line.strip().split(','))
      
        
        
      
        #file.write(str(server)+","+str(count2)+"\n")
        #print(response)
        #server_instance = response  # Assuming server instance is in the response
        #count[server_instance] = count.get(server_instance, 0) + 1
    # Save results to a file
  #Maintainer:Derick Omuga 
    #with open('experiment_a1_results.txt', 'w') as file:
        #for server, request_count in count.items():
           
    # Visualize results as a bar chart
    # Visualization code...
    #plt.bar(result[1] ,[item2 for item in count2])
    #plt.xlabel('Server Instance')
    #plt.ylabel('Request Count')
    #plt.title('Requests Handled by Each Server Instance (Experiment A-1)')
    #plt.show()

async def main():
    # Experiment A-1
    await experiment_a1()



asyncio.run(main())
