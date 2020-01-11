#!/bin/bash
docker build -t rpi_server .
docker run -d -p 5000:5000 --name=rpi_server -it rpi_server
