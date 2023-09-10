<br/>
<p align="center">
<img src="https://raw.githubusercontent.com/RAHB-REALTORS-Association/chat2gpt/master/docs/chat2gpt.png" alt="Logo" width="300"/>
</p>
<hr/>

[![Python 3.11](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.11.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.11.yml)
[![GCP Deployment](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml)
[![Docker Image](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/docker-image.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/docker-image.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Chat²GPT** is a [ChatGPT](https://openai.com/chatgpt) chat bot for Google Chat 🤖💬. It's designed to amplify the experience in your Google Chat rooms by offering personalized user sessions for coherent dialogues, a manual reset capability, the power to generate images via OpenAI's [DALL·E 2 API](https://openai.com/dall-e-2), and dynamic interactions through mentions or direct messaging. Moreover, with the integration of ElevenLabs' [Text-to-Speech API](https://docs.elevenlabs.io/api-reference/text-to-speech), Chat²GPT now brings voice interactions, letting users convert textual prompts into audio. User input and text output is moderated with OpenAI's [Moderation API](https://platform.openai.com/docs/guides/moderation).

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [🛠️ Setup](#️-setup)
- [👷 Development](#-development)
  - [Docker 🐳](#docker-)
    - [Basic Usage:](#basic-usage)
    - [Additional Options:](#additional-options)
  - [Ubuntu 🤓](#ubuntu-)
  - [macOS 🍎](#macos-)
  - [Android 🤖](#android-)
- [🧑‍💻 Usage](#-usage)
  - [Commands ⌨️](#commands-️)
- [🛡️ Privacy](#️-privacy)
  - [Data Practices 📝](#data-practices-)
- [AI APIs and User Awareness ℹ️](#ai-apis-and-user-awareness-ℹ️)
- [🌐 Community](#-community)
  - [Contributing 👥](#contributing-)
  - [Reporting Bugs 🐛](#reporting-bugs-)
- [📄 License](#-license)

## 🛠️ Setup
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/RAHB-REALTORS-Association/chat2gpt)

This bot is intended to be deployed on Google Cloud Functions, with audio data temporarily stored in Google Cloud Storage. Its continuous deployment pipeline is managed using GitHub Actions.

Follow these steps to setup your Chat²GPT bot:

**1. Clone the Repository 📁**

Clone this repository to your local machine using the command:

```bash
git clone https://github.com/RAHB-REALTORS-Association/chat2gpt.git
```

**2. Create Google Cloud Project ☁️**

Create a new project in your Google Cloud Console or select an existing one.

**3. Create a Service Account and JSON Key 📑**

In the Google Cloud Console:
- Head to "IAM & Admin" > "Service Accounts".
- Click "Create Service Account".
- Assign a name and description, then hit "Create and Continue".
- Grant this account the "Cloud Functions Developer" role for Cloud Functions creation and updating. If leveraging other Google Cloud services, additional roles may be required.
- Click "Continue" and then "Done".
- From the list, select the new service account.
- Under the "Keys" tab, choose "Add Key" > "Create new key".
- Opt for "JSON" as the key type and hit "Create". This auto-downloads the JSON key file to your device. This file, containing the service account credentials, facilitates GitHub Actions in deploying your function. Handle with caution.

When assigning roles to your service account:
- For the bot to read/write objects and metadata in the Cloud Storage bucket, grant the "Storage Object Admin" `(roles/storage.objectAdmin)` role.
- For the GitHub action to create and delete the bucket, grant the "Storage Admin" `(roles/storage.admin)` role.

**4. Set GitHub Secrets 🔒**

In your GitHub repository:
- Navigate to "Settings" > "Secrets" > "New repository secret".
- Add the following secrets:
  - `GCP_PROJECT_ID`: Your Google Cloud Project identifier.
  - `GCP_FUNCTION`: Your desired Google Cloud Function name.
  - `GCP_REGION`: Your chosen Google Cloud region.
  - `GCP_SA_KEY`: The entire JSON key file content that was downloaded in the previous step, encoded as base64.
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `MODEL_NAME`: The name of the OpenAI model you're using. Default: "gpt-3.5-turbo".
  - `SYSTEM_PROMPT`: The system prompt to use for the text-generation API.
  - `PROMPT_PREFIX`: Prefix added to beginning of user prompt for local model API. Default: LLaMa2 style.
  - `PROMPT_SUFFIX`: Suffix added to ending of user prompt for local model API. Default: LLaMa2 style.
  - `MAX_TURNS`: This sets the maximum number of exchanges the bot remembers in a user session before resetting. Default: 10 exchanges.
  - `TTL`: This sets the duration (in seconds) a user session stays active from the last received message before it resets. Default: 600 seconds (10 minutes).
  - `MAX_TOKENS_INPUT`: This sets the maximum number of tokens that can be sent. Default: 1000 tokens.
  - `MAX_TOKENS_OUTPUT`: This sets the maximum number of tokens that can be received. Default: 1000 tokens.
  - `TEMPERATURE`: This sets the temperature for the OpenAI API. Default: 0.8.
  - `IMAGE_SIZE`: This sets the image size for the DALL-E API. Default: "512x512".
  - `API_URL`: This sets the API endpoint for the chat completions API. Default: "https://api.openai.com/v1/chat/completions".
  - `ELEVENLABS_API_KEY`: Your ElevenLabs API key. Can be disabled by omitting this secret.
  - `ELEVENLABS_MODEL_NAME`: ElevenLabs model you're using. Default: "eleven_multilingual_v2".
  - `GCS_BUCKET_NAME`: Your chosen name for the GCS bucket meant for TTS audio file storage.

**5. GitHub Actions 🚀**

The bot's deployment to Google Cloud Functions and Storage gets automatically handled by the GitHub Actions workflow upon pushing changes to the main branch.

**6. Configure Bot Access 🤝**

- Navigate to [https://chat.google.com/u/0/botmanagement](https://chat.google.com/u/0/botmanagement).
- Click on the bot you created.
- Under "Functionality", select "Bot works in...".
- Select "Spaces any user can create".
- Click "Save".

Now, your bot can be added to any room within your Google Workspace.

## 👷 Development

The `server.py` script included in this repository serves as a lightweight, local development server for Chat²GPT. This enables you to test new features, debug issues, or get a firsthand experience of the chatbot's capabilities without deploying it to a production environment. Running the server starts a web service that you can access at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Setup
The following are only applicable if using the `server.py` script or Docker:
- Additional environment variables:
  - `LOG_FILE`: Path to save server log file to. Default: None (disabled)
  - `DEBUG`: [True/False] Enable Flask server debugging. Default: False
  - `HOST`: Interfaces to bind server to. Default: "0.0.0.0"
  - `PORT`: Port to bind server to. Default 5000

### Docker 🐳

To quickly set up and run the Chat²GPT application, you can use the pre-built Docker image available at `ghcr.io/rahb-realtors-association/chat2gpt:latest`. Below are the steps and options for running the Docker container.

#### Basic Usage:

Run the following command to pull the image and start a container:

```bash
docker run -d -e OPENAI_API_KEY=sk-myopenaisecretapikey -p 5000:5000 --name chat2gpt ghcr.io/rahb-realtors-association/chat2gpt:latest
```
  
#### Additional Options:

**Volume Mapping**: To load from .env file or persist logs, use volume mapping:

```bash
docker run -d -v ./.env:/app/.env -v ./chat2gpt-server-log.txt:/app/chat2gpt-server-log.txt -e LOG_FILE=chat2gpt-server-log.txt -p 5000:5000 ghcr.io/rahb-realtors-association/chat2gpt:latest
```

**Host Networking**: To access an API_URL running on the Docker host:

```bash
docker run -d -e API_URL=http://127.0.0.1:1234/v1/chat/completions --network host --name chat2gpt ghcr.io/rahb-realtors-association/chat2gpt:latest
```

The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Ubuntu 🤓

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

### macOS 🍎

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

### Android 🤖

To run Chat²GPT on an Android device using [Termux](https://termux.dev/en/), follow these steps:

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

5. **Run the Server**

   Finally, start the Chat²GPT server using the `python` command:

   ```bash
   python server.py
   ```

The server should start successfully and can be accessed at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 🧑‍💻 Usage

- **Dynamic Interactions:** Chat²GPT is attentive to its surroundings. You can invoke it in chat rooms by directly mentioning it using `@botname`. Alternatively, for more private interactions or queries, you can send a direct message to the bot.

- **Interactive Sessions:** This bot remembers multiple rounds of a conversation per user, creating an illusion of continuous dialogue. It can even reference past questions or answers, mimicking a natural conversation flow.

- **Session Management:** To maintain efficient performance, each conversation is limited by a configurable setting, recommended at 5-10 turns. Moreover, the bot keeps an eye on the time since the last message, auto-resetting the session if a set time limit is surpassed. And if needed, users can manually reset their own session anytime with the `/reset` command.

- **Image Generation:** Want to visualize an idea? Use the `/image <prompt>` command. Based on the given prompt, which can range from a word to a paragraph, the bot leverages OpenAI's DALL·E 2 API to generate a relevant image.

- **Text-to-Speech (TTS):** Utilize the power of Eleven Labs TTS API with the `/tts <voice> <prompt>` command. This command will return a voice response based on the given prompt in the specified voice. To see a list of available voices, use the `/voices` command.

- **Optimized Performance:** We prioritize a smooth experience. Before processing any message, the bot checks its size by counting its tokens. If found too lengthy, an error message suggests the user to condense their message. This ensures uninterrupted bot interactions without straining the system.

- **Help On-Demand:** Have questions on how to use Chat²GPT? Just type in the `/help` command. The bot fetches content directly from the `docs/usage.md` file, ensuring users get accurate, up-to-date information.

Remember, Chat²GPT is flexible, suitable for deployment on Google Cloud, FaaS (Function as a Service), or PaaS (Platform as a Service) environments, ensuring it's a perfect fit for all your Google Chat endeavors.

### Commands ⌨️

Use the following commands for Chat²GPT:

- `/reset`: Reinitialize your session.
- `/image <prompt>`: Generate an image using OpenAI's DALL·E 2 API.
- `/tts <voice> <prompt>`: Get a voice response with ElevenLabs' TTS API.
- `/voices`: View available voices for TTS.
- `/help`: Access accurate, up-to-date information from the docs.

## 🛡️ Privacy

### Data Practices 📝

- **Ephemeral Conversations:** Chat²GPT doesn't store or retain conversation history. Every session is temporary, ending when a conversation concludes or times out.

- **Temporary Audio Storage:** Audio files are stored temporarily in Google Cloud Storage to allow users enough time for downloading. To ensure data privacy and efficient storage utilization, these files are deleted with each app redeployment.

- **Reactive Responses:** The bot only reacts to direct prompts, such as @mentions or direct messages, and doesn't "read the room".

- **Anonymous Sessions:** Users are tracked using anonymous ID numbers solely for session consistency. These IDs are cleared with each app redeployment.

## AI APIs and User Awareness ℹ️

- **OpenAI's Commitment:** We use OpenAI's APIs, which, as per OpenAI's policy, don't use user inputs for model training. More details are on [OpenAI's official site](https://openai.com/policies/api-data-usage-policies).

- **ElevenLabs' Commitment:** We use ElevenLabs' APIs, which, as per ElevenLabs' policy, don't use user inputs for model training. More details are on [ElevenLabs' official site](https://elevenlabs.io/terms)).

- **User Awareness:** Discussing sensitive topics? Exercise caution, especially in group settings. Chat²GPT doesn't log conversations, but your organization or platform might.

## 🌐 Community

### Contributing 👥

Contributions of any kind are very welcome, and would be much appreciated. 🙏
For Code of Conduct, see [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

To get started, fork the repo, make your changes, add, commit and push the code, then come back here to open a pull request. If you're new to GitHub or open source, [this guide](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3#let-s-make-our-first-pull-request-) or the [git docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) may help you get started, but feel free to reach out if you need any support.

[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/compare)

### Reporting Bugs 🐛

If you've found something that doesn't work as it should, or would like to suggest a new feature, then go ahead and raise an issue on GitHub.
For bugs, please outline the steps needed to reproduce, and include relevant info like system info and resulting logs.

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/issues/new/choose)

## 📄 License
This project is open sourced under the MIT license. See the [LICENSE](LICENSE) file for more info.
