import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Explicitly specify the path to the .env file, assuming it's in the same directory as vars.py
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Configuration Variables ---
PROJECT_ID = os.getenv('PROJECT_ID') # Corrected variable name
DATASET_ID = os.getenv('DATASET_ID') # Corrected variable name

# GOOGLE_APPLICATION_CREDENTIALS should be set to the path of your service account key file
# This variable is automatically picked up by Google Cloud client libraries and the `bq` tool
# when set in the environment.
# We'll just check if it's set for informational purposes.
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# --- Validation (Optional but Recommended) ---
if not PROJECT_ID:
    print("Warning: PROJECT_ID environment variable not set.")
if not DATASET_ID:
    print("Warning: DATASET_ID environment variable not set.")
if not GOOGLE_APPLICATION_CREDENTIALS:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. BigQuery authentication might fail.")