# 📊 Subscription Analytics with BigQuery

A robust Analytics Engineering project designed to ingest, transform, and analyze subscription data using **Google BigQuery** and **Python**. This project demonstrates a production-grade ELT (Extract, Load, Transform) pipeline, handling Type 2 Slowly Changing Dimensions (SCD) and complex user lifecycle metrics.

---

## 🚀 Key Features

*   **ELT Pipeline**: Automated ingestion of raw CSV data into BigQuery.
*   **Data Transformation**: SQL-based merging logic to handle updates and maintain data integrity (Upserts).
*   **Lifecycle Analysis**: Pre-built queries for acquiring, churning, converting, and retaining users.
*   **Infrastructure as Code**: Python scripts for orchestration and environment management.

---

## 📂 Project Structure

```bash
.
├── analyses/               # 📈 SQL scripts for business intelligence queries
│   ├── acquired_users_*.sql
│   ├── churned_users_*.sql
│   └── ...
├── data/raw/              # 💾 Raw data source (CSV)
│   ├── subscriptions.csv
│   └── updated_subscriptions.csv
├── models/                # 🛠️ Data transformation models (DML)
│   └── merge_subscriptions.sql
├── scripts/               # 🐍 Python automation scripts
│   ├── load_to_bigquery.py
│   └── run_query.py
├── .env.example           # 🔒 Environment configuration template
├── requirements.txt       # 📦 Python dependencies
├── vars.py                # ⚙️ Configuration management
└── README.md              # 📖 Project documentation
```

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.8+** installed.
2.  **Google Cloud Platform (GCP)** account with:
    *   A generic Project created.
    *   **BigQuery API** enabled.
    *   A **Service Account** with `BigQuery Admin` or `BigQuery Data Editor` and `BigQuery Job User` roles.
    *   A JSON key file for the service account.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd BigQuery-Subscription-Analytics
```

### 2. Install Dependencies
It's recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory (copy from `.env.example` if available) and populate it with your GCP credentials.

```ini
# .env
PROJECT_ID=your-gcp-project-id
DATASET_ID=your_bigquery_dataset_id
GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

> **Note**: Ensure your `DATASET_ID` exists in BigQuery or the scripts have permission to create it (current scripts assume existence).

---

## 🏃 Usage Guide

### Step 1: Ingest Data (Extract & Load)
Load the raw CSV files (`subscriptions.csv`, `updated_subscriptions.csv`) into BigQuery. This script autodetects schemas and handles loading.

```bash
python scripts/load_to_bigquery.py
```
*   **Output**: Creates/Overwrites `raw_subscriptions` and `raw_updated_subscriptions` tables in your specified dataset.

### Step 2: Transform Data (Merge/Upsert)
Apply updates from `raw_updated_subscriptions` to the main `raw_subscriptions` table using the MERGE model. This handles new records and updates existing ones.

```bash
python scripts/run_query.py --sql_file models/merge_subscriptions.sql
```

### Step 3: Run Analysis
Execute analytical queries to derive insights. The `run_query.py` script dynamically injects your dataset ID into the SQL templates.

**Example: Analyze Churned Users in August 2025**
```bash
python scripts/run_query.py --sql_file analyses/churned_users_aug_2025.sql
```

**Example: Analyze Acquired Users**
```bash
python scripts/run_query.py --sql_file analyses/acquired_users_apr_2025.sql
```

---

## 🧠 Architecture & Logic

### Data Flow
1.  **Raw Layer**: Data lands in CSV format in `data/raw`.
2.  **Staging Layer**: `load_to_bigquery.py` loads these directly to BigQuery tables (`raw_...`).
3.  **Transformation Layer**: `merge_subscriptions.sql` performs a `MERGE` operation:
    *   **MATCH**: Updates attributes (Start Date, Expiry, Type, Amount) for existing users.
    *   **NOT MATCH**: Inserts new user records.
4.  **Analysis Layer**: SQL queries in `analyses/` read from the consolidated `raw_subscriptions` table to calculate metrics.

### Key Metrics
*   **Acquisition**: New users starting subscriptions in a given month.
*   **Churn**: Users active in the previous month but not the current month.
*   **Upgrades/Downgrades**: Changes in subscription tiers (TBD in analysis SQLs).

---

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

## 🐳 Running with Docker

To run the project in a containerized environment (recommended):

1.  **Build the Image**:
    ```bash
    docker build -t bq-analytics .
    ```

2.  **Run Data Load**:
    ```bash
    docker run --env-file .env -v $(pwd)/data:/app/data bq-analytics python -m scripts.load_to_bigquery
    ```
    *(Note: Ensure your Service Account key path in `.env` is accessible to the container, or mount it separately)*

3.  **Run Tests**:
    ```bash
    docker run --env-file .env bq-analytics python -m scripts.run_tests
    ```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
