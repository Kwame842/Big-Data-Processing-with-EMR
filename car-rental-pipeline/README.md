# Car Rental Data Processing Pipeline - Project Documentation

## Project Overview

This project implements a scalable and automated **Big Data Processing Pipeline** for a **Car Rental Marketplace** using AWS services. It leverages **Apache Spark on EMR** to process raw CSV data, **AWS Glue** for cataloging, **Amazon Athena** for querying, and **Step Functions** for orchestration.

---

## Architecture
![Architecture Diagram](car-rental-pipeline/diagram/lab4-architecture.png)

### AWS Services Used

* **Amazon S3**: Raw and processed data storage
* **Amazon EMR**: Spark cluster for transformation jobs
* **AWS Glue**: Crawlers to catalog Parquet outputs
* **Amazon Athena**: SQL querying engine
* **AWS Step Functions**: Workflow orchestration

---

## Data Sources

Located in: `s3://car-rental-data-project/raw/`

### Files:

* `rental_transactions.csv`
* `users.csv`
* `vehicles.csv`
* `locations.csv`

---

## S3 Bucket Structure

```
s3://car-rental-data-project/
├── raw/
│   ├── rental_transactions.csv
│   ├── users.csv
│   ├── vehicles.csv
│   └── locations.csv
├── processed/
│   ├── location_metrics/
│   ├── vehicle_metrics/
│   ├── user_transaction_metrics/
│   │   ├── daily_metrics/
│   │   └── user_metrics/
├── scripts/
│   ├── job1_location_metrics.py
│   └── job2_user_metrics.py
├── logs/
└── athena-results/
```

---

## PySpark Jobs

### 1️⃣ job1\_location\_metrics.py

**Purpose**: Computes metrics by location and vehicle type

**Outputs**:

* Total revenue per location
* Total transactions per location
* Min/Max/Average transaction values
* Unique vehicles used
* Avg rental duration per vehicle type

**Output Paths**:

* `processed/location_metrics/`
* `processed/vehicle_metrics/`

---

### 2️⃣ job2\_user\_metrics.py

**Purpose**: Computes metrics related to users and daily trends

**Outputs**:

* Total/average spend per user
* Rental hours per user
* Daily revenue and transaction counts

**Output Paths**:

* `processed/user_transaction_metrics/user_metrics/`
* `processed/user_transaction_metrics/daily_metrics/`

---

## Glue Crawlers

### Database: `car_rental_db`

| Crawler Name               | S3 Target Path                                      | Table Name         |
| -------------------------- | --------------------------------------------------- | ------------------ |
| `crawler_location_metrics` | `processed/location_metrics/`                       | `location_metrics` |
| `crawler_vehicle_metrics`  | `processed/vehicle_metrics/`                        | `vehicle_metrics`  |
| `crawler_user_metrics`     | `processed/user_transaction_metrics/user_metrics/`  | `user_metrics`     |
| `crawler_daily_metrics`    | `processed/user_transaction_metrics/daily_metrics/` | `daily_metrics`    |

---

## Athena Setup

1. **Set Query Result Location**: `s3://car-rental-data-project/athena-results/`
2. **Select Database**: `car_rental_db`
3. **Sample Queries**:



```sql
-- Highest revenue location
SELECT pickup_location, total_revenue
FROM location_metrics
ORDER BY total_revenue DESC
LIMIT 1;

-- Most rented vehicle type
SELECT vehicle_type, revenue_by_vehicle_type
FROM vehicle_metrics
ORDER BY revenue_by_vehicle_type DESC
LIMIT 1;

-- Top 5 users
SELECT user_id, first_name, total_spent
FROM user_metrics
ORDER BY total_spent DESC
LIMIT 5;

-- Daily revenue trend
SELECT rental_date, total_transactions, daily_revenue
FROM daily_metrics
ORDER BY rental_date;
```

![Athena Queries](car-rental-pipeline/screenshots/TopSpendingUsers.png)

---

## Step Functions Automation

### Workflow:

1. Submit Spark job 1 (location metrics)
2. Submit Spark job 2 (user metrics)
3. Trigger 4 Glue Crawlers
4. (Optional) Terminate EMR cluster

### IAM Requirements:

* Role must allow:

  * `elasticmapreduce:AddStep`
  * `glue:StartCrawler`
 

### How to Run:

1. Go to Step Functions Console
2. Create new state machine → Author with JSON
3. Paste and modify the provided workflow definition
4. Provide EMR cluster ID if using an existing cluster
5. Start Execution

---

![Step functions](car-rental-pipeline/screenshots/EMR-Running-Step-Functions.png)

## Execution Checklist

| Task                          | Status |
| ----------------------------- | ------ |
| Upload raw files to S3        | ✅      |
| Upload Spark scripts to S3    | ✅      |
| Run Spark jobs on EMR         | ✅      |
| Write output to `processed/`  | ✅      |
| Create and run Glue Crawlers  | ✅      |
| Verify tables in Athena       | ✅      |
| Run queries and validate KPIs | ✅      |
| Automate with Step Functions  | ✅      |

---

##  Notes

* Ensure timestamps are parsed using `dd/MM/yyyy HH:mm`
* Partitioning by date can improve performance
* You can visualize KPIs in Amazon QuickSight or export results from Athena

---

##  Next Enhancements (Optional)

* Add data quality checks (e.g., using Deequ)
* Schedule runs using EventBridge + Step Functions
* Integrate with QuickSight dashboard

---

##  Contact / Support

For questions or contributions, reach out to the project team or your Data Engineering instructor.
