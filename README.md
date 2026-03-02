# ETL Pipeline — Orbital Simulation Data

A small, production-style ETL pipeline that processes orbital parameters into analytics-ready Parquet. Built to demonstrate data engineering patterns from the [vocal script](../interview-vocal-script.md).

## What This Demonstrates

| Skill (from resume/vocal script) | Where it shows up |
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

## Interview Talking Points

**"Can you walk me through a project?"**

"This is a small ETL pipeline I put together to show how I structure production data work. It ingests orbital simulation data—ties to my OSDR volunteer work—transforms it, runs validation checks for schema and physical constraints, and loads to Parquet. I containerized it with Docker and wired up GitHub Actions so the pipeline and tests run on every push. The validation layer is the same pattern I care about at Scale—making sure data feeding downstream systems is reliable."

**"How do you handle data quality?"**

"I use a validation layer that runs before load: schema checks, null checks on critical columns, and range validation for physical constraints—like eccentricity between 0 and 1. If any check fails, the pipeline stops and surfaces the failure. In production I'd extend this with something like Great Expectations or dbt tests."

**"Why Parquet?"**

"Columnar format, good compression, and native support in Glue, Redshift, Snowflake. It's what I'd use for analytics workloads in a data lake or warehouse."
