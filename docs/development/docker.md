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
docker run -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
```

Here's a breakdown:

- `docker run`: This command creates and starts a container from a Docker image.
- `-p 5000:5000`: This maps port 5000 in the container to port 5000 on your host machine, allowing you to access the application.
  
### Additional Options:

1. **Detached Mode**: To run the container in the background, add the `-d` flag:

    ```bash
    docker run -d -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
    ```

2. **Environment Variables**: If you need to pass environment variables to your application:

    ```bash
    docker run -e VAR_NAME=value -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
    ```

3. **Name the Container**: To assign a name to your container for easy identification, use the `--name` flag:

    ```bash
    docker run --name chat2gpt-container -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
    ```

4. **Volume Mapping**: To persist data, use volume mapping:

    ```bash
    docker run -v /path/on/host:/path/in/container -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
    ```

You can combine these options as needed. For example:

```bash
docker run -d --name chat2gpt-container -e VAR_NAME=value -p 5000:5000 ghcr.io/rahb-realtors-assocaition/chat2gpt:latest
```

The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).
