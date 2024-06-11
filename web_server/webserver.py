from flask import Flask, jsonify
import os
import docker
app = Flask(__name__)
client = docker.from_env()
container_id = os.getenv("HOSTNAME")
container = client.containers.get(container_id)
#Maintainer:Derick Omuga 

server_id = container.name
# Define /home endpoint
@app.route('/home', methods=['GET'])
def home():
    return jsonify({
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    })

# Define /heartbeat endpoint
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8000")

