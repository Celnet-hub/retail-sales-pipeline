# Retail Sales Data Pipeline

## Overview

This project is an end-to-end fundamental Data Engineering pipeline that simulates, processes, and visualizes retail sales data for a mock store chain (Argos).

The system generates realistic synthetic transaction data, performs high-performance batch ingestion into a PostgreSQL data warehouse, and serves real-time business insights via an interactive Streamlit dashboard. It demonstrates core ETL principles including idempotent schema design, bulk data loading, and containerized database management.

## Problem Statement

A small retail chain operates across multiple locations (e.g., Hendon, Mill Hill, Barnet). Currently, sales data is scattered across distinct systems or files, making it difficult to:
- Understand daily sales performance.
- Identify popular products.

## Architecture

The pipeline follows a standard ETL workflows:

[Python Generator] -> [Raw CSV Staging] -> [PostgreSQL (Docker)] -> [Streamlit Dashboard]

1. Extract: Python script generates synthetic sales data (Customer, Store, Category, Price, Date) using `Faker` libary.

2. Load: Data is ingested into PostgreSQL using psycopg2 and the COPY command for high-throughput performance (handling 1M rows instantly).

3. Analyze: A Streamlit application connects to the database to calculate KPIs (Revenue, Avg Transaction) and visualizes trends.


## Tech Stack

-   **Language**: Python 3.x
-   **Database**: PostgreSQL (on Docker)
-   **Libraries**:
    -   `pandas` for data manipulation and staging.
    -   `faker` for synthetic data generation.
    -   `Psycopg2` an PostgreSQL adapter for high-performance data loading.
    -   `Streamlit` for interactive web-based dashboarding.
    -   `Python-Dotenv`: Environment variable management for security.

## Key Features

1. **Scalable Data Generation:** Configurable script to generate 100 to 1M+ rows of realistic retail data.

2. **Optimized Ingestion:** Uses the PostgreSQL COPY protocol instead of standard SQL INSERT statements, reducing load time by ~90% for large datasets.

3. **Idempotency:** The database loader checks for table existence (IF NOT EXISTS) and handles transaction rollbacks to prevent data corruption.

4. **Interactive UI:** Dashboard allows filtering by Store and Product Category with instant recalculation of metrics.


## Project Structure

```bash
sales_project/
├── main.py          # Entry point for the pipeline / Data generation (currently)
└── README.md        # Project documentation
```

## Getting Started

### Prerequisites

Ensure you have Python installed and Docker running for DB.

**Step 1: Clone the Repository:**

```bash
git clone https://github.com/yourusername/retail-sales-pipeline.git

cd retail-sales-pipeline
```
**Step 2: Install dependencies**

Install the required dependencies from `requirements.txt` using pip:

```bash
pip install -r requirements.txt
```

**Step 3: Configure Environment Variable**

Create a .env file in the root directory and add your database credentials:

```
DB_NAME=postgres
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Usage

Run the main script to execute the pipeline for generating the data, transforming and staging into a CSV file:

```bash
python3 generate_data.py
```

Load Data - Ingest the CSV file into the PostgreSQL warehouse.

```bash
python3 load_data.py
```

Launch Dashboard Start the visualization app.

```bash
streamlit run dashboard.py
```

## Key Learnings & Objectives

-   **Data Ingestion**: Reading from CSV/Raw sources.
-   **Data Transformation**: Aggregating sales per store/product.
-   **Orchestration**: Automating the flow with Python scripts.

## Future Improvements

-   Containerization: Dockerize the Python scripts and Streamlit app for full portability.
-   Add automated orchestration (Airflow).
