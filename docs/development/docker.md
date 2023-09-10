---
layout: default
title: Docker 🐳
parent: 👷 Development
nav_order: 0
---

## Docker 🐳

To quickly set up and run the Chat²GPT application, you can use the pre-built Docker image available at `ghcr.io/rahb-realtors-assocaition/chat2gpt:latest`. Below are the steps and options for running the Docker container.

### Basic Usage:

Run the following command to pull the image and start a container:

```bash
docker run -d -e OPENAI_API_KEY=sk-myopenaisecretapikey -p 5000:5000 --name chat2gpt ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
```
  
### Additional Options:

**Volume Mapping**: To load from .env file or persist logs, use volume mapping:

```bash
docker run -d -v ./.env:/app/.env -v ./server-log.txt:/app/server-log.txt -e LOG_FILE=server-log.txt -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
```

**Host Networking**: To access an API_URL running on the Docker host:

```bash
docker run -d -e API_URL=http://127.0.0.1:1234/v1/chat/completions --network host --name chat2gpt ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
```

The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).
