# Real-time-Predictive-maintenance-system


## Table of Contents

- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Prerequisites](#prerequisites)
- [Setup and Running Instructions](#setup-and-running-instructions)
- [How to launch kibana dashboard](#how-to-launch-kibana-dashboard)
- [Final result](#final-result)

## Project Overview
The aim of the project is to design a dashboard for real time monitoring of air ventilation systems in industrial sites as well as predict a potention engine failure. 
The present code and project provides an simulation of the process with the help of a Kaggle dataset as a real time producer and another one for the model training.
This proof of concept features a real time data producer with kafka, a consumer apache spark and data integration and visualization through elasticseach and kibana.

## Project Architecture
Practically, data will be collected through sensors and sent to kafka topic with the help of MQTT Protocol.
along with the processing with spark, the failure production column will be added to the index to be then visualised in Kibana along with other relevant data. 
Below is the illustrated architecture

![Architecture](/images/architecture.png)

## Prerequisites

* Kafka: any version with the scala 2.12 version
* Spark: version 3.4.2 >> [Download link (linux version)](https://archive.apache.org/dist/spark/spark-3.2.4/spark-3.2.4-bin-hadoop3.2.tgz) 
* Elasticsearch and kibana: version 8.8.2 >> [Download link for elasticsearch](https://www.elastic.co/downloads/past-releases/elasticsearch-8-8-2)
[Download link for kibana](https://www.elastic.co/downloads/past-releases/kibana-8-8-2)

## Setup and Running Instructions
- Install the above preresuisites and name the installation folders respectively kafka, elasticsearch and kibana
- Open all servers in terminal
    - Open kafka server with running these commands in order and in different shells:
    ```
    ~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties
    ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties

    ```
    
    - Open the elasticsearch and kibana servers by running the
      

    ```
    bin/elasticsearch
    ```
    
    - and 

    ``̀

    bin/kibana
    
    ```
    commands in order and respectively in the elasticsearch and kibana folders. 
- Open the localhost on port 5601 and go to the following path: http://localhost:5601/app/management/kibana/objects
- Import the export.ndjson file to kibana and open the dashboard named "system de maintenance industriel"
