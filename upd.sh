#!/bin/bash
docker rm -f plague_brewing
git pull origin main
docker build -t plague_brewing:latest .
docker run --name plague_brewing -v $(pwd):/app plague_brewing:latest