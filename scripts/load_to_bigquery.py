import sys
import os
from google.cloud import bigquery

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vars import PROJECT_ID, DATASET_ID

print(f"Project ID: {PROJECT_ID} | Dataset ID: {DATASET_ID}")

# Source CSV files and their corresponding BigQuery table names
CSV_FILES = {
    'data/raw/subscriptions.csv': 'raw_subscriptions',
    'data/raw/updated_subscriptions.csv': 'raw_updated_subscriptions',
}

def load_csv_to_bigquery(file_path, table_name, project_id, dataset_id):
    """Loads a CSV file into a BigQuery table using the Python client."""
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"
    print(f"Attempting to load {file_path} into BigQuery table: {full_table_id}")

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,   # Assumes CSVs have a header row
        autodetect=True        # Let BigQuery infer the schema
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
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue
        load_csv_to_bigquery(file_path, table_name, PROJECT_ID, DATASET_ID)

if __name__ == "__main__":
    main()
