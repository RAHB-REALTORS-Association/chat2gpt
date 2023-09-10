---
title: "👷 Development"
layout: page
nav_order: 2
has_children: true
---

# 👷 Development

The `server.py` script included in this repository serves as a lightweight, local development server for Chat²GPT. This enables you to test new features, debug issues, or get a firsthand experience of the chatbot's capabilities without deploying it to a production environment. Running the server starts a web service that you can access at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Setup
The following are only applicable if using the `server.py` script or Docker:
- Additional environment variables:
  - `LOG_FILE`: Path to save server log file to. Default: None (disabled)
  - `DEBUG`: [True/False] Enable Flask server debugging. Default: False
  - `HOST`: Interfaces to bind server to. Default: 127.0.0.1
  - `PORT`: Port to bind server to. Default 5000
