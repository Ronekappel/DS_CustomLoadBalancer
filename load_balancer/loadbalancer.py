import requests
import threading
import time
import random
import string
import zlib
import os
import docker
import socket
from flask import Flask, request, jsonify
from requests.exceptions import RequestException
import math
import hashlib
import bisect
import random
import re
#Maintainer:Derick Omuga 

app = Flask(__name__)
def scale_service(service_name, replica_count):
    try:
        service = docker_client.services.get(service_name)
        service.update(replicas=replica_count)
    except docker.errors.APIError as e:
        print(f"Error scaling service '{service_name}': {e}")

def get_replica(service_name):
    try:
        # Resolve the DNS entry for the service name
        ips = socket.gethostbyname_ex(service_name)[2]
        return ips
    except socket.gaierror as e:
        print(f"Error resolving service '{service_name}': {e}")
        return []
        
def is_ipv4_address(string):
    ipv4_pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ipv4_pattern, string) is not None



class ConsistentHashing:
    def __init__(self,num_servers, num_slots, num_virtual_nodes, replication_factor):
        self.num_slots = num_slots
        self.num_servers = num_servers
        self.num_virtual_nodes = num_virtual_nodes
        self.replication_factor = replication_factor
        self.hash_ring = {}
        self.sorted_hashes = []
        self._initialize_hash_ring()


    def _hash_function(self, key):
        return (hash(key) + 2 * hash(key) + 17) % self.num_slots

    def _virtual_server_hash_function(self, server_id, virtual_node_id):
        return (hash(server_id) + hash(virtual_node_id) + 2 * hash(virtual_node_id) + 25) % self.num_slots

    def _add_virtual_node(self, server_id, virtual_node_id):
        hash_value = self._virtual_server_hash_function(server_id, virtual_node_id)
        if hash_value not in self.hash_ring:
            self.hash_ring[hash_value] = server_id
            bisect.insort(self.sorted_hashes, hash_value)
    
    def _initialize_hash_ring(self):
        for server_id in range(self.num_servers):
            for virtual_node_id in range(self.num_virtual_nodes):
                hash_value = self._virtual_server_hash_function(server_id, virtual_node_id)
                self.hash_ring[hash_value] = (server_id, virtual_node_id)
                bisect.insort(self.sorted_hashes, hash_value)


    def add_server(self, server_id):
        for virtual_node_id in range(self.num_virtual_nodes):
            self._add_virtual_node(server_id, virtual_node_id)

    def _remove_virtual_node(self, server_id, virtual_node_id):
        hash_value = self._virtual_server_hash_function(server_id, virtual_node_id)
        if hash_value in self.hash_ring:
            self.hash_ring.pop(hash_value)
            self.sorted_hashes.remove(hash_value)

    def remove_server(self, server_id):
        for virtual_node_id in range(self.num_virtual_nodes):
            self._remove_virtual_node(server_id, virtual_node_id)

    def _get_server(self, request_key):
     if not self.sorted_hashes:
       print(f"None")  # Or handle this case appropriately
     hash_value = self._hash_function(request_key)
     idx = bisect.bisect_right(self.sorted_hashes, hash_value)
     if idx == len(self.sorted_hashes):
        idx = 0
     return self.sorted_hashes[idx]
     
    def get_assigned_server(self, request_key):
      primary_hash = self._get_server(request_key)
      primary_idx = self.sorted_hashes.index(primary_hash)
      servers = []
      for i in range(self.replication_factor):
         server_idx = (primary_idx + i) % len(self.sorted_hashes)
         server_hash = self.sorted_hashes[server_idx]
         servers.append(self.hash_ring[server_hash])
      return random.choice(servers)
     
    def get_servers_for_request(self, request_key):
      primary_hash = self._get_server(request_key)
      primary_idx = self.sorted_hashes.index(primary_hash)
      servers = []
      for i in range(self.replication_factor):
        server_idx = (primary_idx + i) % len(self.sorted_hashes)
        server_hash = self.sorted_hashes[server_idx]
        servers.append(self.hash_ring[server_hash])
      return servers


    
# Parameters
num_slots = 512  # Total number of slots in the consistent hash map
K = 9  # Number of virtual servers for each server container
replication_factor = 3  # Number of replicas for redundancy
N=3
# Create Consistent Hashing instance
consistent_hashing = ConsistentHashing(N,num_slots=num_slots, num_virtual_nodes=K, replication_factor=replication_factor)

# Add servers



# Example usage: Map request keys to servers

# Parameters
#Maintainer:Derick Omuga 

# Initialize consistent hash ring

hash_ring = consistent_hashing


# Placeholder for managed replicas
replicas = []

# Health check interval in seconds
health_check_interval = 10

# Docker service name
docker_service_name = "web_server"  # Adjust with your Docker service name
#Maintainer:Derick Omuga 
# Docker client
docker_client = docker.from_env()

def health_check():
    global replicas
    global hash_map
    global docker_client
    while True:
        try:
            # Get current replica IPs
            replica_ips = get_replica(docker_service_name)
            if replica_ips:
                # Add new servers to hash map
                for server in replica_ips:
                    if server not in replicas:
                        hash_ring.add_server(server)
                replicas = replica_ips
                # Perform health checks and remove unhealthy servers
                for server in replicas:
                    try:
                        response = requests.get(f"http://{server}:8000/heartbeat", timeout=5)
                        response.raise_for_status()
                        # Server is healthy, do nothing
                    except RequestException as e:
                        print(f"Error checking server {server}: {e}")
                        replicas.remove(server)
                        hash_ring.remove_server(server)
                # Spawn new web server instance if necessary
                if len(replicas) < N and  len(replicas) != N:
                    new_replica_count = N
                    scale_service(docker_service_name, new_replica_count)
        except Exception as e:
            print(f"Error in health check: {e}")
        # Sleep for health check interval
        time.sleep(health_check_interval)

# Start health check thread
health_check_thread = threading.Thread(target=health_check)
health_check_thread.daemon = True
health_check_thread.start()



@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    if len(hostnames) != n:
        return jsonify({"error": "Number of hostnames does not match the number of instances to add"}), 400

    # Add servers to consistent hash map
    for hostname in hostnames:
        hash_ring.add_server(hostname)

    replicas.extend(hostnames)
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    hostnames = data.get('hostnames', [])
    for hostname in hostnames:
        if hostname in replicas:
            replicas.remove(hostname)
            hash_ring.remove_server(hostname)
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/<path>', methods=['GET'])
def route_request(path):
    # Route request using consistent hash map
    assigned_server = hash_ring.get_assigned_server(path)
    try:
        if is_ipv4_address(f"{assigned_server}")==True:
            response = requests.get(f"http://{assigned_server}:8000/{path}")
            return response.content, response.status_code
    except RequestException as e:
                        print(f"Error requesting server {assigned_server}: {e}")
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

