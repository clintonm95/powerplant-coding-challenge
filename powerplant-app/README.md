# Power Plant Optimization App

## Overview

This FastAPI application calculates the optimal production plan for power plants based on the load and fuel prices. The app runs in a Docker container, providing an easy and lightweight environment for deployment and testing.

## Prerequisites

Before running the application, ensure the following are installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)

## Getting Started

### 1. Clone the Repository

Clone the `test` branch from the repository:

```bash
git clone --branch test https://github.com/clintonm95/powerplant-coding-challenge.git
cd powerplant-coding-challenge/powerplant-app
```

### 2. Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -f config/Dockerfile -t powerplant-app .
```

### 3. Run the Application

Run the FastAPI app in a container:

```bash
docker run -d --name powerplant-app -p 8888:8888 powerplant-app
```

The app will now be running at `http://0.0.0.0:8888/`. You can access the Swagger documentation at `http://0.0.0.0:8888/docs`.

### 4. Stopping the Application

To stop and remove the running container, use the following commands:

```bash
docker stop powerplant-app
docker rm powerplant-app
```

## Running Tests

### 1. Build the Image (if not done already)

If you haven't built the Docker image yet, run:

```bash
docker build -t powerplant-app .
```

### 2. Run Tests in the Running Container

If the app is already running, you can run the tests in the existing container using:

```bash
docker exec -it powerplant-app pytest
```

## Example Requests

After starting the app, you can test it by sending a `POST` request to `/productionplan` with one of the available payload contained in the example_payloads folder as json.
