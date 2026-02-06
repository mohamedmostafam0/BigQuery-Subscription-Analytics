import sys
import os
import argparse
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / '.env')

from vars import PROJECT_ID, DATASET_ID

TABLE_NAME = 'raw_subscriptions'

def run_bigquery_query(sql_content, project_id):
    """Executes a SQL query on BigQuery using the google-cloud-bigquery client library."""
    print(f"Executing query on project: {project_id}")

    try:
        client = bigquery.Client(project=project_id)
        query_job = client.query(sql_content)
        results = query_job.result()  # Waits for job to complete

        print("Query executed successfully!")
        for row in results:
            print(row)

    except Exception as e:
        print(f"Error executing BigQuery query: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Run a BigQuery SQL query.')
    parser.add_argument('--sql_file', required=True, help='The relative path to the SQL file to execute (e.g., analyses/acquired_users_feb_2025.sql).')
    args = parser.parse_args()

    if not PROJECT_ID or not DATASET_ID:
        print("Error: PROJECT_ID or DATASET_ID not set. Please check your .env file.")
        sys.exit(1)

    # Resolve SQL file path relative to project root
    sql_file_path = PROJECT_ROOT / args.sql_file

    try:
        with open(sql_file_path, 'r') as f:
            sql_template = f.read()
    except FileNotFoundError:
        print(f"Error: SQL file not found at {sql_file_path}")
        sys.exit(1)

    print(f"\n--- Running query for table: {TABLE_NAME} ---")
    # Replace placeholders with actual values
    final_sql = sql_template.replace('{{ dataset_name }}', DATASET_ID)
    final_sql = final_sql.replace('{{ table_name }}', TABLE_NAME)

    run_bigquery_query(final_sql, PROJECT_ID)

if __name__ == "__main__":
    main()
