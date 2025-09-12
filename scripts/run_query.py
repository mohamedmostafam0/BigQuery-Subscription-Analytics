import sys
import os
import argparse
from google.cloud import bigquery

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    parser.add_argument('--sql_file', required=True, help='The path to the SQL file to execute (e.g., analyses/acquired_users_feb_2025.sql).')
    args = parser.parse_args()

    if not PROJECT_ID or not DATASET_ID:
        print("Error: PROJECT_ID or DATASET_ID not set. Please check your .env file.")
        sys.exit(1)

    try:
        with open(args.sql_file, 'r') as f:
            sql_template = f.read()
    except FileNotFoundError:
        print(f"Error: SQL file not found at {args.sql_file}")
        sys.exit(1)

    print(f"\n--- Running query for table: {TABLE_NAME} ---")
    # Replace placeholders with actual values
    final_sql = sql_template.replace('{{ dataset_name }}', DATASET_ID)
    final_sql = final_sql.replace('{{ table_name }}', TABLE_NAME)

    run_bigquery_query(final_sql, PROJECT_ID)

if __name__ == "__main__":
    main()
