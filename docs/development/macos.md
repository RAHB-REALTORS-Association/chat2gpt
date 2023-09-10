---
layout: default
title: macOS 🍎
parent: 👷 Development
nav_order: 2
---

## macOS 🍎

To run Chat²GPT on macOS, you can use [Homebrew](https://brew.sh/) to manage your packages. Follow these steps:

1. **Install Homebrew**

   If you don't have Homebrew installed, open Terminal and run:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**

   Install Python using Homebrew:

   ```bash
   brew install python
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
