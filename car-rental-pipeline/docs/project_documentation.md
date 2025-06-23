# 🚗 Car Rental Data Processing Pipeline - Project Documentation

## 📌 Project Overview

This project implements a scalable and automated **Big Data Processing Pipeline** for a **Car Rental Marketplace** using AWS services. It leverages **Apache Spark on EMR** to process raw CSV data, **AWS Glue** for cataloging, **Amazon Athena** for querying, and **Step Functions** for orchestration.

---

## 🧱 Architecture

### ✅ AWS Services Used

* **Amazon S3**: Raw and processed data storage
* **Amazon EMR**: Spark cluster for transformation jobs
* **AWS Glue**: Crawlers to catalog Parquet outputs
* **Amazon Athena**: SQL querying engine
* **AWS Step Functions**: Workflow orchestration

---

## 📁 Project Structure

```
car-rental-pipeline/
├── scripts/
│   ├── job1_location_metrics.py
│   ├── job2_user_metrics.py
│   └── __init__.py
│
├── data/
│   ├── raw/
│   │   ├── rental_transactions.csv
│   │   ├── users.csv
│   │   ├── vehicles.csv
│   │   └── locations.csv
│   └── processed/
│
├── stepfunctions/
│   ├── emr_workflow_with_athena.json
│   ├── emr_workflow_basic.json
│   └── README.md
│
├── glue_crawlers/
│   ├── crawler_definitions.md
│   └── glue_catalog_structure.md
│
├── athena_queries/
│   ├── top_users_by_spend.sql
│   ├── daily_revenue_trend.sql
│   ├── top_locations_by_revenue.sql
│   └── README.md
│
├── docs/
│   ├── architecture_diagram.drawio
│   ├── architecture_diagram.png
│   ├── project_documentation.md
│   └── IAM_permissions.md
│
├── cloudformation/
│   ├── emr_cluster.yaml
│   ├── glue_crawlers.yaml
│   └── step_functions.yaml
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔥 PySpark Jobs

### 1️⃣ job1\_location\_metrics.py

* Computes location-based and vehicle-based KPIs
* Output: `processed/location_metrics/`, `processed/vehicle_metrics/`

### 2️⃣ job2\_user\_metrics.py

* Computes user KPIs and daily trends
* Output: `processed/user_transaction_metrics/user_metrics/`, `processed/user_transaction_metrics/daily_metrics/`

---

## 🧠 Glue Crawlers

### Database: `car_rental_db`

| Crawler Name               | S3 Target Path                                      | Table Name         |
| -------------------------- | --------------------------------------------------- | ------------------ |
| `crawler_location_metrics` | `processed/location_metrics/`                       | `location_metrics` |
| `crawler_vehicle_metrics`  | `processed/vehicle_metrics/`                        | `vehicle_metrics`  |
| `crawler_user_metrics`     | `processed/user_transaction_metrics/user_metrics/`  | `user_metrics`     |
| `crawler_daily_metrics`    | `processed/user_transaction_metrics/daily_metrics/` | `daily_metrics`    |

---

## 🔍 Athena Setup

1. Set Query Result Location: `s3://car-rental-data-project/athena-results/`
2. Database: `car_rental_db`
3. Sample Queries:

```sql
SELECT user_id, total_spent FROM user_metrics ORDER BY total_spent DESC LIMIT 5;
SELECT rental_date, daily_revenue FROM daily_metrics ORDER BY rental_date;
SELECT pickup_location, total_revenue FROM location_metrics ORDER BY total_revenue DESC LIMIT 5;
```

---

## 🔄 Step Functions Automation

### Workflow:

1. Run EMR Spark jobs
2. Trigger Glue crawlers
3. Run Athena queries in parallel

### IAM Requirements:

* `elasticmapreduce:AddStep`
* `glue:StartCrawler`
* `athena:StartQueryExecution`, `athena:GetQueryExecution`, `athena:GetQueryResults`
* `s3:PutObject` and `s3:GetObject` to `athena-results/`

---

## 🧾 requirements.txt

```txt
pyspark==3.3.0
boto3
```

---

## 📘 README.md

```markdown
# 🚗 Car Rental Analytics Pipeline

A fully automated big data pipeline built with PySpark on EMR, Glue, Athena, and Step Functions.

## 📊 Features
- Process raw rental data in S3 using Spark
- Store KPIs as Parquet in `processed/`
- Catalog datasets using AWS Glue Crawlers
- Query KPIs using Amazon Athena
- Orchestrated via AWS Step Functions

## 🗂 Project Structure
Refer to `docs/project_documentation.md` or see this summary:
- `scripts/`: PySpark jobs
- `data/raw/`: Raw CSV input
- `athena_queries/`: SQL analytics
- `stepfunctions/`: Automation definitions

## 🚀 Getting Started
1. Upload raw data to `s3://car-rental-data-project/raw/`
2. Upload PySpark scripts to `s3://car-rental-data-project/scripts/`
3. Run Step Function (`emr_workflow_with_athena.json`)
4. Check Athena `car_rental_db` for output

## 📈 Example Queries
- Top 5 Users by Spend
- Daily Revenue Trend
- Top Locations by Revenue

## 🛡 IAM Policy Requirements
See `docs/IAM_permissions.md`

## 📌 Notes
- EMR cluster must be configured with Spark
- Glue Crawlers must be run after Spark jobs complete
```

---

Let me know if you'd like me to generate this as downloadable files, ZIP package, or GitHub-ready folder. ✅
