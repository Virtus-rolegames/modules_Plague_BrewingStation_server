#!/bin/bash
docker rm -f plague_brewing
git pull origin main
docker build -t plague_brewing:latest .
docker run --name plague_brewing -p 63421:63421 -v $(pwd):/app plague_brewing:latest