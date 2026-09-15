# ETL-Pipeline-Using-Python-And-MySQL

# E-Commerce Data ETL Pipeline

A mini **ETL (Extract, Transform, Load) data pipeline** built using **CSV, Python, and MySQL**.

## Project Overview

This project demonstrates how raw e-commerce data can be extracted from a CSV file, cleaned and validated using Python, and loaded into a MySQL database for further analysis.

## Pipeline

```text
Raw CSV (500 records)
        ↓
     Extract
   Python CSV
        ↓
 Clean & Validate
        ↓
Clean CSV (460 records)
        ↓
      Load
 Python + MySQL
        ↓
   MySQL Database
```

## Technologies Used

* Python
* CSV / `csv.DictReader`
* MySQL
* MySQL Connector for Python
* SQL

## Data Cleaning

The raw dataset contained intentionally introduced data-quality issues such as:

* Missing values
* Duplicate records
* Invalid numeric values
* Invalid quantities/prices
* Inconsistent text values
* Invalid or missing dates

After cleaning and validation, **460 valid records** were loaded into MySQL.

## Project Structure

```text
ecommerce-etl-pipeline/
│
├── raw_ecommerce_data.csv
├── clean_ecommerce_data.csv
├── clean_data.py
├── load_data.py
└── README.md
```

## Key Learning

This project helped me understand the fundamentals of a real-world data pipeline:

**Extract → Clean/Transform → Load → Analyze**

It also provided practical experience with Python data processing, data validation, CSV handling, MySQL schema design, and loading data into a relational database.
