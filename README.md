# Chat²GPT
Chat²GPT is a Google Chat bot powered by OpenAI's GPT model.

## Setup
This bot is intended to be deployed on Google Cloud Functions and its continuous deployment pipeline is managed using GitHub Actions.

Follow these steps to setup your Chat²GPT bot:

**1. Clone the Repository**

Clone this repository to your local machine using the command:

```bash
git clone https://github.com/RAHB-REALTORS-Association/chat2gpt.git
```

**2. Create Google Cloud Project**

Create a new project in your Google Cloud Console or select an existing one.

**3. Create a Service Account and JSON Key**

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

**4. Set GitHub Secrets**

In your GitHub repository:
- Navigate to "Settings" > "Secrets" > "New repository secret".
- Add the following secrets:
  - `GCP_PROJECT`: Your Google Cloud project ID.
  - `GCP_SA_KEY`: The entire JSON key file content that was downloaded in the previous step, encoded as base64.
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `MODEL_NAME`: The name of the OpenAI model you're using. For this project, we recommend "gpt-3.5-turbo".
  - `SYSTEM_PROMPT`: The system prompt to use for the OpenAI API.

**5. GitHub Actions**

The GitHub Actions workflow is configured to automatically deploy the bot to Google Cloud Functions whenever changes are pushed to the main branch of the repository.

**6. Configure Bot Access**

- Navigate to https://chat.google.com/u/0/botmanagement.
- Click on the bot you created.
- Under "Functionality", select "Bot works in...".
- Select "Spaces any user can create".
- Click "Save".

Now, your bot can be added to any room within your Google Workspace.

Your bot is now ready! It can interact in any chat room when it's explicitly mentioned (@botname) or directly messaged, depending on the functionality you've programmed it with.
