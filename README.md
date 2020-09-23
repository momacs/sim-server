# PRAM SIMULATION SERVER
A simulation server for pram.
## Getting Started

Before you can start using the PRAM simulation server, you have to download docker. 
[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Once you have downloaded docker, you will need to clone the repository. 

    git clone https://github.com/momacs/sim-server

Next, you need to build the docker image, and create a docker container. 

    cd sim-server/docker
    docker build . -t pram
    docker create --name pram0 --network host  -t -i pram
    
You don't need to set the docker container's network to host, but it is strongly recommended that you do so. This will make it easier to access the simulation server from the public internet because you can open the port that the docker container is running the simulation server on. 


## Example Simulation

Running an example simulation using the docker container is very easy. However, the current version of the docker image still requires you to manually start the simulation server.

    docker start -a -i pram0
    cd && cd sim-server
    python3 server.py
    

You should now see the simulation server running at [http://127.0.0.1:8080/](http://127.0.0.1:8080/).


![](https://i.ibb.co/sRcmL3W/pram0.png)
Click the "Sample Simulation" button to run a simple simulation. The results should look like this. 
![](https://i.ibb.co/Mf3bMdZ/pram1.png)
You can find the source code for this simulation [here.](https://github.com/momacs/pram/blob/master/src/sim/01-simple/sim.py)

TODO
 - [ ] Implement support for streaming results
 - [ ] Finish adding support for configuring and running PRAM simulations
