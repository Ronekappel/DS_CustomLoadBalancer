# Customizable Load Balancer

# Prerequisites

## 1. Docker: latest

    sudo apt-get update

    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io

## 2. Docker-compose standalone 
    sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    
    sudo chmod +x /usr/local/bin/docker-compose
    
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


# Getting Started


## Building Docker Images
To create the necessary Docker images for the load balancer and servers, execute the following command:

```bash
make install
```

## Running Docker Containers
To initiate the deployment of load balancer containers, execute the following command:

```bash
make deploy
```
This command will launch the load balancer container, which, in turn, will spawn the initial N server Docker containers along with their heartbeat probing threads. Ensure that the necessary configurations are in place for a seamless deployment. The command also clears any existing containers using server or load balancer image (i.e. execute make clean).

<span style="color:red">**Note:** The deployment command launches Docker in the background mode. Therefore, users are advised to check the docker-compose logs to view load-balancer logs.</span>

## Interact with System
To interact with the load balancer and send GET/POST requests, launch the interactive terminal using the following command:

```bash
bash client.sh
```
## Remove Existing Container
To stop and remove all containers using the server image and load balancer, run the following command:

```bash
make clean
```

Executing this command is recommended before running the main code to ensure there are no conflicting container instances already running. This helps prevent potential errors and ensures a clean environment for the code execution.

## Clear Existing Images
To remove previously created server and load balancer images, execute the following command:

```bash
make deepclean
```

