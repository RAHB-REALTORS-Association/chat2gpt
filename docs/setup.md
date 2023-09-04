---
title: "🛠️ Setup"
layout: page
nav_order: 1
---

# 🛠️ Setup
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
  - `SYSTEM_PROMPT`: The system prompt to use for the OpenAI API.
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
