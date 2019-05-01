# Order generator

## The program that generates the change history of orders

Order generator is a program that generates input data for some financial process. Features include:

* Generate order change history.
* Publish order history to RabbitMQ.
* Order history consuming from RabbitMQ queues.
* Insert order history into database.

### Order structure

| Attribute         | Description                                           |
| --------------    | ----------------------------------------------------- |
| Identifier        | Unique order identifier                               |
| Currency pair     | The pair that interests the trader                    |
| Direction         | Selected operation. Can be **buy** or **sell**        |
| Status            | The status of the order at the specified time         |
| Date              | Date in which the order was in a certain status       |
| Initial price     | Starting price of a currency pair                     |
| Filled price      | Price of the currency pair at the end of the order.   |
|                   | May differ from the initial price by +/- 5%           |
| Initial volume    | Amount of currency that interests the trader          |
| Filled volume     | Amount of currency that the trader                    |
|                   | has received at the end of the order.                 |
| Description       | A note left by the trader when creating an order      |
| Tags              | A few single words regarding the order                |

Each order can fall into one of three zones:

* Red: Order started in previous periods of trading and finish in current period.
* Green: Order start and finish in same period.
* Blue: Order start in current period and finish in next periods.

### Getting started

First of all, DON’T PANIC. 
It will take 5 minutes to get the gist of what Order generator is all about.

#### Requirements

##### Python

You need to have a recent version of Python installed. 
See the [Python](python.org) page for actual information.

To work with RabbitMQ and MySQL, you must also install additional Python modules using the command: 

```bash
python3 -m pip install -r requirements.txt
```

##### RabbitMQ

Understandably, to work with it, we need the message broker itself. 
To avoid problems with the program, please install [RabbitMQ](rabbitmq.com) from its page.

##### MySQL

In conclusion, we need the MySQL for the full operation of the application.
It will be enough to install only the MySQL Server. 
On the page [MySQL](mysql.com) you can find a free community version of the server, or purchase it.

#### Running

To run the application in normal mode, use the command:

```bash
python3 program.py
```

For specific settings for connecting to services, use the config file. 
Also in this file you can change the generation volume and the percentage of zones.

To quickly set some parameters, use the arguments before running the program. 
More detailed information:

```bash
python3 program.py -H 
```

After starting the application will create a database and tables in it. 
As well as the exchange point and queue in the message broker. 
As soon as preparation is completed, the generator will automatically perform the necessary actions.

### Alternative start

This method uses a docker to run an application in a container.

If you want to try this method you need to install the docker 
according to the instructions from the official [Docker](docker.com) site for your system.

You will also need docker-compose if you do not know how to manually start containers with the necessary services.

Use the following commands to run an application in a container:

```bash
docker-compose up
docker build -t generator .
docker run -i --network generator_default --name=generator generator
```

These commands are already described in the script `docker.sh`. 
Instead of the commands above, just enter:

```bash
./docker.sh
```

After these actions, the application will start in the container. 
In case of failure, please check the settings file, after re-build the application:

```bash
docker-compose down
docker rm generator
docker rmi generator
```

