import sys
import os
import glob
from pathlib import Path
from google.cloud import bigquery
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama
init()

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / '.env')

from vars import PROJECT_ID, DATASET_ID

def run_test(client, sql_file):
    """
    Executes a SQL test file.
    Returns True if the test passed (0 rows returned), False otherwise.
    """
    with open(sql_file, 'r') as f:
        sql_template = f.read()

    # Inject variables
    sql = sql_template.replace('{{ dataset_name }}', DATASET_ID)
    
    try:
        query_job = client.query(sql)
        results = list(query_job.result())
        
        if len(results) == 0:
            return True, None
        else:
            return False, results
    except Exception as e:
        return False, f"Execution Error: {str(e)}"

def main():
    print(f"{Style.BRIGHT}🚀 Starting Data Quality Tests...{Style.RESET_ALL}\n")
    
    if not PROJECT_ID or not DATASET_ID:
        print(f"{Fore.RED}❌ Error: PROJECT_ID or DATASET_ID not set.{Style.RESET_ALL}")
        sys.exit(1)

    client = bigquery.Client(project=PROJECT_ID)
    
    # Find all SQL files in tests/ directory using pathlib
    tests_dir = PROJECT_ROOT / 'tests'
    test_files = list(tests_dir.glob('*.sql'))
    
    if not test_files:
        print(f"{Fore.YELLOW}⚠️ No tests found in tests/ directory.{Style.RESET_ALL}")
        return

    passed_count = 0
    failed_count = 0
    failures = []

    for sql_file in test_files:
        test_name = sql_file.name
        print(f"Running {test_name}...", end=' ', flush=True)
        
        passed, error_or_rows = run_test(client, sql_file)
        
        if passed:
            print(f"{Fore.GREEN}PASS{Style.RESET_ALL}")
            passed_count += 1
        else:
            print(f"{Fore.RED}FAIL{Style.RESET_ALL}")
            failed_count += 1
            failures.append((test_name, error_or_rows))

    print(f"\n{Style.BRIGHT}--- Test Summary ---{Style.RESET_ALL}")
    print(f"Total Tests: {len(test_files)}")
    print(f"Passed: {Fore.GREEN}{passed_count}{Style.RESET_ALL}")
    print(f"Failed: {Fore.RED}{failed_count}{Style.RESET_ALL}")

    if failures:
        print(f"\n{Fore.RED}🔍 Failure Details:{Style.RESET_ALL}")
        for name, details in failures:
            print(f"\n{Style.BRIGHT}Test: {name}{Style.RESET_ALL}")
            if isinstance(details, str):
                print(f"  Error: {details}")
            else:
                print(f"  Failed Rows ({len(details)}):")
                for row in details[:5]:  # Show first 5 failing rows
                    print(f"    {dict(row)}")
                if len(details) > 5:
                    print(f"    ... and {len(details) - 5} more.")
        sys.exit(1)
    else:
        print(f"\n{Fore.GREEN}✅ All data quality tests passed!{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main()
