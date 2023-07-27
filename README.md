# Chat²GPT
Chat²GPT is a ChatGPT chat bot for Google Chat.

## Instructions

**1. Install Google Cloud SDK**

If you haven't already done so, install the Google Cloud SDK on your local machine. The SDK includes the `gcloud` command-line tool, which you'll use to deploy your function.

You can download it [here](https://cloud.google.com/sdk/docs/install) and follow the instructions for your specific operating system.

**2. Set Up Your Project**

In the Google Cloud Console, create a new project or select an existing one.

**3. Authenticate Your SDK**

To authenticate your SDK and set your project, run the following command in your terminal:

```bash
gcloud auth login
gcloud config set project PROJECT_ID
```

Replace `PROJECT_ID` with the ID of your Google Cloud project.

**4. Write Your Function**

Copy the project files to the function directory. The directory structure should look like this:

```
/myfunction
    main.py
    requirements.txt
```

**5. Create a Service Account and JSON Key**

In the Google Cloud Console:

- Navigate to "IAM & Admin" > "Service Accounts".
- Click on "Create Service Account".
- Give your service account a name and description, then click "Create and Continue".
- Grant this service account the "Cloud Functions Developer" role (or any role that has the "cloudfunctions.functions.create" permission) to allow it to create and update - - Cloud Functions. If you plan to use other Google Cloud services, you might need to grant additional roles.
- Click "Continue" and then "Done".
- Click on the newly created service account from the list.
- Go to the "Keys" tab, click "Add Key" and select "Create new key".
- Choose "JSON" as the key type and click "Create". The JSON key file will be automatically downloaded to your local machine. This file contains the service account credentials that will be used by GitHub Actions for deploying your function. Be careful with this file as it provides admin access to your Google Cloud project.

**6. Deploy Your Function**

Deploy your function to Google Cloud Functions using the `gcloud` command-line tool:

```bash
cd /path/to/your/function/directory
gcloud functions deploy your-function-name --runtime python39 --trigger-http --allow-unauthenticated --entry-point process_event
```

Replace `/path/to/your/function/directory` with the path to the directory containing your `main.py` and `requirements.txt` files, and replace `your-function-name` with the name you want for your function.

The `--runtime python39` flag specifies that your function should be run with Python 3.9, the `--trigger-http` flag indicates that your function is triggered by HTTP requests, and the `--entry-point process_event` specifies that the `process_event` function in your `main.py` file should be executed when your function is triggered.

**7. Set Environment Variables**

In the Google Cloud Console, navigate to your deployed function and set the `OPENAI_API_KEY`, `MODEL_NAME`, and `SYSTEM_PROMPT` environment variables to their appropriate values.

And that's it! Your function is now deployed and ready to be used. Remember to check the logs in Google Cloud Console for any issues that may arise when your function is invoked.

**8. Configure Bot Access**

- Navigate to https://chat.google.com/u/0/botmanagement.
- Click on the bot you created.
- Under "Functionality", select "Bot works in...".
- Select "Spaces any user can create".
- Click "Save".

Now, your bot can be added to any room within your Google Workspace.

Remember, the bot will be able to interact only when it's explicitly mentioned (@botname) or directly messaged, depending on the functionality you've programmed it with.
