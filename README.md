# 💬 Chat²GPT 🤖

[![Python 3.9](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.9.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/python-3.9.yml)
[![GCP Deployment](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/chat2gpt/actions/workflows/gcp-deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Chat²GPT is a ChatGPT chat bot for Google Chat. 💬🤖 It enhances communication and productivity in Google Chat rooms, providing an intelligent and responsive virtual assistant. Designed to run on Google Cloud or your preferred FaaS (Function as a Service) or PaaS (Platform as a Service) environment.

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
  - `MODEL_NAME`: The name of the OpenAI model you're using. For this project, we recommend "gpt-3.5-turbo".
  - `SYSTEM_PROMPT`: The system prompt to use for the OpenAI API.

**5. GitHub Actions 🚀**

The GitHub Actions workflow is configured to automatically deploy the bot to Google Cloud Functions whenever changes are pushed to the main branch of the repository.

**6. Configure Bot Access 🤝**

- Navigate to https://chat.google.com/u/0/botmanagement.
- Click on the bot you created.
- Under "Functionality", select "Bot works in...".
- Select "Spaces any user can create".
- Click "Save".

Now, your bot can be added to any room within your Google Workspace.

Your bot is now ready! It can interact in any chat room when it's explicitly mentioned (@botname) or directly messaged, depending on the functionality you've programmed it with.

## 🌐 Community

### Contributing 👥🤝

Contributions of any kind are very welcome, and would be much appreciated. 🙏
For Code of Conduct, see [Contributor Convent](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

To get started, fork the repo, make your changes, add, commit and push the code, then come back here to open a pull request. If you're new to GitHub or open source, [this guide](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3#let-s-make-our-first-pull-request-) or the [git docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) may help you get started, but feel free to reach out if you need any support.

[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/compare)

### Reporting Bugs 🐛📝

If you've found something that doesn't work as it should, or would like to suggest a new feature, then go ahead and raise an issue on GitHub.
For bugs, please outline the steps needed to reproduce, and include relevant info like system info and resulting logs.

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/chat2gpt/issues/new/choose)

## 📄 License
This project is open sourced under the MIT license. See the [LICENSE](LICENSE) file for more info. 📜
