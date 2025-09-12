# Analytics Engineering BigQuery Assessment

This project contains a series of SQL queries and scripts to analyze subscription data in Google BigQuery. The SQL queries cover various analyses, including customer acquisition, churn, upgrades, and downgrades.

## Project Structure

```
.
├── analyses/
│   ├── acquired_users_apr_2025.sql
│   ├── acquired_users_feb_2025.sql
│   ├── acquired_users_mar_2025.sql
│   ├── churned_users_aug_2025.sql
│   ├── churned_users_oct_2025.sql
│   ├── churned_users_sep_2025.sql
│   ├── converted_users_apr_2025.sql
│   ├── converted_users_jun_2025.sql
│   ├── converted_users_may_2025.sql
│   ├── downgraded_users_apr_2025.sql
│   ├── downgraded_users_jun_2025.sql
│   ├── downgraded_users_may_2025.sql
│   ├── upgraded_users_apr_2025.sql
│   ├── upgraded_users_jun_2025.sql
│   └── upgraded_users_may_2025.sql
├── data/
│   └── raw/
│       ├── subscriptions.csv
│       └── updated_subscriptions.csv
├── models/
│   └── merge_subscriptions.sql
├── scripts/
│   ├── load_to_bigquery.py
│   └── run_query.py
├── .gitignore
├── README.md
└── vars.py
```

-   **analyses/**: Contains SQL scripts for various analytical queries.
-   **data/raw/**: Contains the raw subscription data in CSV format.
-   **models/**: Contains SQL models for data transformation.
-   **scripts/**: Contains Python scripts to interact with BigQuery.
-   **vars.py**: Manages configuration variables for the project.

## Setup

1.  **Prerequisites**:
    *   Python 3.x
    *   Google Cloud SDK installed and authenticated.
    *   A Google Cloud project with BigQuery enabled.

2.  **Configuration**:
    *   Create a `.env` file in the root of the project.
    *   Add the following environment variables to the `.env` file:
        ```
        PROJECT_ID=<your-gcp-project-id>
        DATASET_ID=<your-bigquery-dataset-id>
        GOOGLE_APPLICATION_CREDENTIALS=<path-to-your-service-account-key.json>
        ```

## How to Run a SQL Query

To run a SQL query from the `analyses` directory, use the `run_query.py` script.

**Example:**

```bash
python scripts/run_query.py --sql_file analyses/acquired_users_apr_2025.sql
```

This command will execute the specified SQL file against the `raw_subscriptions` table in your BigQuery dataset.