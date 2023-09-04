---
layout: default
title: Android
parent: 👷 Development
nav_order: 3
---

## Android 🤖

To run Chat²GPT on an Android device using Termux, follow these steps:

1. **Update and Upgrade Termux Packages**

   Open Termux and run the following command to update and upgrade existing packages:

   ```bash
   pkg upgrade
   ```

2. **Install Required Dependencies**

   Install the necessary packages like OpenSSL, Python, pip, Git, Rust, and Binutils by executing:

   ```bash
   pkg install openssl python python-pip git rust binutils
   ```

3. **Clone the Repository**

   Use the `git` command to clone the Chat²GPT repository to your device:

   ```bash
   git clone https://github.com/RAHB-REALTORS-Association/chat2gpt.git
   ```

   Navigate to the cloned directory:

   ```bash
   cd chat2gpt
   ```

4. **Install Python Packages**

   Run the following command to install the Python packages required for Chat²GPT:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Test Server**

   Finally, start the Chat²GPT server using the `python` command:

   ```bash
   python test_server.py
   ```

   The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).
