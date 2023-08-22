import os
import json
import base64
from google.cloud import storage
from google.oauth2.service_account import Credentials

def initialize_gcs_client(bucket_name):
    # Decode the base64 service account JSON
    decoded_service_account_info = base64.b64decode(os.getenv('GCP_SA_KEY')).decode('utf-8')
    service_account_info = json.loads(decoded_service_account_info)

    # Create credentials from the decoded service account JSON
    credentials = Credentials.from_service_account_info(service_account_info)

    # Create a GCS client with the credentials
    storage_client = storage.Client(credentials=credentials)

    return storage_client
