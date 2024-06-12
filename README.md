# Customizable Load Balancer

## Prerequisites

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

# Load Balancer Performance Analysis

## A-1:

In this experiment, we launched 10,000 async requests on 3 server containers and measured the request count handled by each server instance. The results are shown in the bar chart below:

![pic1](https://github.com/ct-phil/DS_CustomLoadBalancer/assets/101468151/4d22d5e9-20b5-4b65-8d15-e4859e8335db)

The above image sugggests that load balancer distributes the requests fairly evenly among the 3 server containers, with each server handling around 33% of the total requests.

## A-2:

In this experiment, we incremented N from 2 to 6 and launched 10,000 requests on each increment. We measured the average load of the servers at each run and reported the results in a line chart below:

![pic2](https://github.com/ct-phil/DS_CustomLoadBalancer/assets/101468151/e7506701-be0b-47c0-95d4-030a5f1a7d73)

The average load per server decreases as N increases, indicating that the load balancer is able to distribute the load more evenly among the servers.

## A-3:

In this experiment, we tested all endpoints of the load balancer and simulated a server failure scenario. We observed that the load balancer quickly spawned a new instance to handle the load, ensuring minimal disruption to the system.

 Observations:
     The load balancer detected the server failure and spawned a new instance within a short period (less than 1 second).
     The new instance was able to handle the load seamlessly, ensuring that the system remained responsive

## A-4:

In this experiment, we modified the hash functions H(i) and Φ(i, j) and repeated experiments A-1 and A-2. The results are shown below:

### Experiment A-1 Modified Hash Functions Load Distribution Bar Chart:

![pic3](https://github.com/ct-phil/DS_CustomLoadBalancer/assets/101468151/2a4ade52-d298-4bac-9ca8-5a2070fcd38a)

### Experiment A-1 Modified Hash Functions Scalability Line Chart:

![pic4](https://github.com/ct-phil/DS_CustomLoadBalancer/assets/101468151/58cf73e4-6490-480b-8b9a-d63d53fd1606)

The modified hash functions result in a slightly different load distribution among the servers, but the overall performance and scalability of the load balancer remain unaffected.


# Group Details
95092 Omuga Derick Maxwel
145767 James Maikara Kaunda 
145623 Raynor Munene Mwenda 
140395 Shifwoko Phil Ogutu



