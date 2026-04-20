#!/bin/bash
docker rm -f plague_brewing
git pull origin main
docker build -t plague_brewing:latest .
docker run --name plague_brewing -p 127.0.0.1:63000:63421 -v $(pwd):/app plague_brewing:latest