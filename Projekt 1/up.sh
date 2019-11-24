#!/bin/bash
cd serwer 
sudo docker-compose -f docker-compose.yml up -d --build
cd ..
cd client
sudo docker-compose -f docker-compose.yml up -d --build
