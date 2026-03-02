# ETL Pipeline — Orbital Simulation Data

A small, production-style ETL pipeline that processes orbital parameters into analytics-ready Parquet.

## What This Demonstrates

| Skill | Where it shows up |
|----------------------------------|-------------------|
| **ETL pipelines** | Extract → Transform → Load flow |
| **Data quality & validation** | `validate.py` — schema, nulls, range checks |
| **Parquet / columnar storage** | Output format; compatible with Glue, Redshift, Snowflake |
| **Python, Pandas** | Core implementation |
| **Docker** | Containerized run |
| **CI/CD (GitHub Actions)** | Automated test + pipeline run on push |
| **OSDR / scientific data** | Orbital params tie to open-science data infrastructure |

## Quick Start

```bash
# Local
pip install -r requirements.txt
python -m src.pipeline

# Docker
docker build -t etl-demo .
docker run etl-demo

# Tests
pytest tests/ -v
```

## Structure

```
demo-etl-pipeline/
├── src/
│   ├── extract.py    # Read from source (CSV; in prod: S3, API, stream)
│   ├── transform.py  # Clean, enrich, derive fields
│   ├── validate.py   # Data quality gates
│   ├── load.py       # Write to Parquet
│   └── pipeline.py   # Orchestration
├── data/
│   ├── raw_orbital_params.csv   # Input
│   └── output/                  # Parquet output
├── tests/
├── Dockerfile
├── .github/workflows/ci.yml
└── requirements.txt
```

## Data Quality

The pipeline runs validation before load: schema checks, null checks on critical columns, and range validation for physical constraints (e.g., eccentricity between 0 and 1). If any check fails, the pipeline stops and surfaces the failure. In production this could be extended with Great Expectations or dbt tests.

## Why Parquet?

Columnar format, good compression, and native support in AWS Glue, Redshift, and Snowflake. Well-suited for analytics workloads in a data lake or warehouse.
