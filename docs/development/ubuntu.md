---
layout: default
title: Ubuntu 🤓
parent: 👷 Development
nav_order: 1
---

## Ubuntu 🤓

To run Chat²GPT on Ubuntu, follow these steps:

1. **Update Packages**

   Open Terminal and update your package list:

   ```bash
   sudo apt update
   ```

2. **Install Required Dependencies**

   Install Python and other necessary packages:

   ```bash
   sudo apt install python3 python3-pip git
   ```

3. **Clone the Repository**

   Clone the Chat²GPT repository:

   ```bash
   git clone https://github.com/RAHB-REALTORS-Association/chat2gpt.git
   ```

   Navigate to the cloned directory:

   ```bash
   cd chat2gpt
   ```

4. **Install Python Packages**

   Install the required Python packages:

   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the Server**

   Start the Chat²GPT server:

   ```bash
   python3 server.py
   ```

The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).
