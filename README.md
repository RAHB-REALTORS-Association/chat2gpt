[![Python 3.11](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.11.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.11.yml)
[![GCP Deployment](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br/>
<p align="center">
<img src="https://raw.githubusercontent.com/RAHB-REALTORS-Association/chat2gpt/master/docs/chat2gpt.png" alt="Logo" width="300"/>
</p>
<hr/>

**Chat²GPT** is a [ChatGPT](https://openai.com/chatgpt) chat bot for Google Chat 🤖💬. It's designed to amplify the experience in your Google Chat rooms by offering personalized user sessions for coherent dialogues, a manual reset capability, the power to generate images via OpenAI's [DALL·E 2 API](https://openai.com/dall-e-2), and dynamic interactions through mentions or direct messaging. Moreover, with the integration of Eleven Labs TTS API, Chat²GPT now brings voice interactions, letting users convert textual prompts into audio. User input and text output is moderated with OpenAI's [Moderation API](https://platform.openai.com/docs/guides/moderation).

## 📖 Table of Contents
- [🛠️ Setup](#%EF%B8%8F-setup)
- [🧑‍💻 Usage](#-usage)
- [🛡️ Privacy](#%EF%B8%8F-privacy)
  - [Data Practices 📝](#data-practices-)
  - [OpenAI and User Awareness ℹ️](#openai-and-user-awareness-%E2%84%B9%EF%B8%8F)
- [🌐 Community](#-community)
  - [Contributing 👥🤝](#contributing-)
  - [Reporting Bugs 🐛📝](#reporting-bugs-)
- [📄 License](#-license)

## 🛠️ Setup
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/RAHB-REALTORS-Association/chat2gpt)

This bot is intended to be deployed on Google Cloud Functions and its continuous deployment pipeline is managed using GitHub Actions.

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
- Navigate to "IAM & Admin" > "Service Accounts".
- Click on "Create Service Account".
- Give your service account a name and description, then click "Create and Continue".
- Grant this service account the "Cloud Functions Developer" role (or any role that has the "cloudfunctions.functions.create" permission) to allow it to create and update Cloud 
Functions. If you plan to use other Google Cloud services, you might need to grant additional roles.
- Click "Continue" and then "Done".
- Click on the newly created service account from the list.
- Go to the "Keys" tab, click "Add Key" and select "Create new key".
- Choose "JSON" as the key type and click "Create". The JSON key file will be automatically downloaded to your local machine. This file contains the service account credentials that 
will be used by GitHub Actions for deploying your function. Be careful with this file as it provides admin access to your Google Cloud project.

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
  - `SYSTEM_PROMPT`: The system prompt to use for the OpenAI API.
  - `MAX_TURNS`: This sets the maximum number of exchanges the bot remembers in a user session before resetting. Default: 10 exchanges.
  - `TTL`: This sets the duration (in seconds) a user session stays active from the last received message before it resets. Default: 600 seconds (10 minutes).
  - `MAX_TOKENS_INPUT`: This sets the maximum number of tokens that can be sent. Default: 1000 tokens.
  - `MAX_TOKENS_OUTPUT`: This sets the maximum number of tokens that can be received. Default: 1000 tokens.
  - `TEMPERATURE`: This sets the temperature for the OpenAI API. Default: 0.8.
  - `IMAGE_SIZE`: This sets the image size for the DALL-E API. Default: "512x512".
  - `API_URL`: This sets the API endpoint for the chat completions API. Default: "https://api.openai.com/v1/chat/completions".
  - `ELEVENLABS_API_KEY`: Your Eleven Labs API key. Can be disabled by omitting this secret.
  - `ELEVENLABS_MODEL_NAME`: Eleven Labs model you're using. Default: "eleven_monolingual_v1".

**5. GitHub Actions 🚀**

The GitHub Actions workflow is configured to automatically deploy the bot to Google Cloud Functions whenever changes are pushed to the main branch of the repository.

**6. Configure Bot Access 🤝**

- Navigate to https://chat.google.com/u/0/botmanagement.
- Click on the bot you created.
- Under "Functionality", select "Bot works in...".
- Select "Spaces any user can create".
- Click "Save".

Now, your bot can be added to any room within your Google Workspace.

## 🧑‍💻 Usage

- **Dynamic Interactions:** Chat²GPT is attentive to its surroundings. You can invoke it in chat rooms by directly mentioning it using `@botname`. Alternatively, for more private interactions or queries, you can send a direct message to the bot.

- **Interactive Sessions:** This bot remembers multiple rounds of a conversation per user, creating an illusion of continuous dialogue. It can even reference past questions or answers, mimicking a natural conversation flow.

- **Session Management:** To maintain efficient performance, each conversation is limited by a configurable setting, recommended at 5-10 turns. Moreover, the bot keeps an eye on the time since the last message, auto-resetting the session if a set time limit is surpassed. And if needed, users can manually reset their own session anytime with the `/reset` command.

- **Image Generation:** Want to visualize an idea? Use the `/image <prompt>` command. Based on the given prompt, which can range from a word to a paragraph, the bot leverages OpenAI's DALL·E 2 API to generate a relevant image.

- **Text-to-Speech (TTS):** Utilize the power of Eleven Labs TTS API with the `/tts <voice> <prompt>` command. This command will return a voice response based on the given prompt in the specified voice. To see a list of available voices, use the `/voices` command.

- **Optimized Performance:** We prioritize a smooth experience. Before processing any message, the bot checks its size by counting its tokens. If found too lengthy, an error message suggests the user to condense their message. This ensures uninterrupted bot interactions without straining the system.

Remember, Chat²GPT is flexible, suitable for deployment on Google Cloud, FaaS (Function as a Service), or PaaS (Platform as a Service) environments, ensuring it's a perfect fit for all your Google Chat endeavors.

## 🛡️ Privacy

### Data Practices 📝

- **Ephemeral Conversations:** Chat²GPT doesn't store or retain conversation history. Every session is temporary, ending when a conversation concludes or times out.

- **Reactive Responses:** The bot only reacts to direct prompts, such as @mentions or direct messages, and doesn't "read the room".

- **Anonymous Sessions:** Users are tracked using anonymous ID numbers solely for session consistency. These IDs are cleared with each app redeployment.

### AI APIs and User Awareness ℹ️

- **OpenAI's Commitment:** We use OpenAI's APIs, which, as per OpenAI's policy, don't use user inputs for model training. More details are on [OpenAI's official site](https://openai.com/policies/api-data-usage-policies).

- **Eleven Labs' Commitment:** We use Eleven Labs' APIs, which, as per Eleven Labs' policy, don't use user inputs for model training. More details are on [Eleven Labs' official site](https://www.eleven-labs.com/en/legal/).

- **User Awareness:** Discussing sensitive topics? Exercise caution, especially in group settings. Chat²GPT doesn't log conversations, but your organization or platform might.

## 🌐 Community

### Contributing 👥🤝

Contributions of any kind are very welcome, and would be much appreciated. 🙏
For Code of Conduct, see [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

To get started, fork the repo, make your changes, add, commit and push the code, then come back here to open a pull request. If you're new to GitHub or open source, [this guide](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3#let-s-make-our-first-pull-request-) or the [git docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) may help you get started, but feel free to reach out if you need any support.

[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/compare)

### Reporting Bugs 🐛📝

If you've found something that doesn't work as it should, or would like to suggest a new feature, then go ahead and raise an issue on GitHub.
For bugs, please outline the steps needed to reproduce, and include relevant info like system info and resulting logs.

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/issues/new/choose)

## 📄 License
This project is open sourced under the MIT license. See the [LICENSE](LICENSE) file for more info.
