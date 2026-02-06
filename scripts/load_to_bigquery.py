import sys
import os
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

# Get the project root directory (two levels up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env file in project root
load_dotenv(PROJECT_ROOT / '.env')

from vars import PROJECT_ID, DATASET_ID

print(f"Project ID: {PROJECT_ID} | Dataset ID: {DATASET_ID}")

# Define paths relative to project root
CSV_FILES = {
    PROJECT_ROOT / 'data/raw/subscriptions.csv': 'raw_subscriptions',
    PROJECT_ROOT / 'data/raw/updated_subscriptions.csv': 'raw_updated_subscriptions',
}

# Define the schema explicitly to ensure data integrity
# This replaces autodetect=True which can be unreliable
SUBSCRIPTION_SCHEMA = [
    bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("user_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("start_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("expiry_date", "DATE", mode="NULLABLE"),
    bigquery.SchemaField("type_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
]

def load_csv_to_bigquery(file_path, table_name, project_id, dataset_id):
    """Loads a CSV file into a BigQuery table using the Python client with explicit schema."""
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"
    print(f"Attempting to load {file_path} into BigQuery table: {full_table_id}")

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,   # Assumes CSVs have a header row
        schema=SUBSCRIPTION_SCHEMA, # Use explicit schema
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE # Overwrite existing table
    )

    try:
        with open(file_path, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file,
                full_table_id,
                job_config=job_config
            )

        load_job.result()  # Waits for job to complete
        table = client.get_table(full_table_id)
        print(f"✅ Successfully loaded {table.num_rows} rows into {full_table_id}")

    except Exception as e:
        print(f"❌ Error loading {file_path} to {full_table_id}: {e}")
        sys.exit(1)

def main():
    for file_path, table_name in CSV_FILES.items():
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}")
            continue
        load_csv_to_bigquery(file_path, table_name, PROJECT_ID, DATASET_ID)

if __name__ == "__main__":
    main()
