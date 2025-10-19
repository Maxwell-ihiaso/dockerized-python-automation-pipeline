# 🧩 Dockerized Python Automation Pipeline

A modular, production-grade **Python + Docker** automation pipeline that demonstrates how to turn manual or expert workflows into reproducible, API-driven pipe.

---

## 🚀 Overview

This project showcases how to:

- Integrate **open-source APIs** into production workflows  
- Build **reusable connectors** and **data adapters**  
- Design **reliable, testable Python pipelines**  
- **Containerize** everything for full reproducibility  

The pipeline fetches data from a public API, validates it with Pydantic models, transforms the dataset, and exports the result to multiple formats (CSV, JSON, Parquet).  
It’s fully CLI-driven and Dockerized for seamless deployment.

---

## 🏗️ Architecture
```
dockerized-python-automation-pipeline/
├── app/
│ ├── cli.py # Typer-based CLI entrypoint
│ ├── config.py # Centralized configuration (Pydantic)
│ ├── logger.py # Structured logger
│ ├── connectors/ # External API connectors
│ │ └── public_api.py
│ ├── transformers/ # Data transformation modules
│ │ └── public_entries.py
│ ├── flows/ # Orchestrated workflows
│ │ └── daily_flow.py
│ └── utils/
│ └── backoff.py # Exponential backoff retry helper
├── tests/ # Unit tests (pytest)
├── data/ # Local output directory
├── .env.example # Environment variables
├── Dockerfile # Container build definition
├── docker-compose.yml # Local dev orchestration
├── requirements.txt # Dependencies
├── Makefile # Dev utilities
└── README.md # Documentation
```


---



## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/dockerized-python-automation-pipeline.git
cd dockerized-python-automation-pipeline
```


### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows
```


### 3. install dependencies
```bash
make install
```


### 4. copy environment variables
```bash
cp .env.example .env
```
> Update any values as needed (e.g., LOG_LEVEL, API tokens).





---

## 🧠 Usage (Local)

### 1. Show configuration
```bash
python -m app.cli info
```

### 2. Fetch API data
```bash
python -m app.cli fetch --category Anime
```

### 3. Transform data
```bash
python -m app.cli transform data/outputs_<hash>.csv --out-format parquet
```
### 4. Run the full pipeline flow
```bash
python -m app.cli flow --category Animals
```


```bash
# Fetch all breeds as CSV
python -m app.cli fetch-breeds

# Get a random image URL
python -m app.cli random-image

# Get 8 retriever images as JSON
python -m app.cli images-by-breed --breed retriever --limit 8 --out-format json
```





---

## 🐳 Run in Docker
### 1. Build image
```bash
docker compose build
```

### 2. Run CLI commands inside container
```bash
docker compose run --rm pipeline python -m app.cli fetch --category Music
docker compose run --rm pipeline python -m app.cli transform data/outputs_<hash>.csv --out-format json
```

```bash
docker compose build

# Breeds table
docker compose run --rm pipeline python -m app.cli fetch-breeds

# Random image URL
docker compose run --rm pipeline python -m app.cli random-image

# Images by breed
docker compose run --rm pipeline python -m app.cli images-by-breed --breed hound --sub-breed afghan --limit 5 --out-format parquet

```


All environment variables are loaded automatically from .env.





---

##  🧪 Testing

Run tests with:

make test


Tests cover configuration loading, API connector functionality, and data transformations.




## 🧰 Configuration

All configuration is centralized in app/config.py and loaded from .env.

Variable                Description	                Default
ENV	Environment         (dev/staging/prod)      	dev
LOG_LEVEL               Logging level	            INFO
API_BASE_URL	        External API base URL	    https://api.publicapis.org
API_TIMEOUT_SECS	    Request timeout	            15
API_TOKEN	            Optional API token	        None



---
## 🧱 Extending the Pipeline

Add a new API connector

Create a new file under app/connectors/.

Implement a connector class with _get() methods and Pydantic models.

Register new commands in app/cli.py.

Add a new transformation

Create a new module in app/transformers/.

Import and apply it within the CLI or a Prefect/flow script.

Orchestrate with Prefect (optional)

You can wrap the daily flow inside a Prefect task or schedule it using cron for production environments.




---

## 🧾 Logging & Error Handling

Centralized logger: app/logger.py

Exponential backoff: app/utils/backoff.py

All exceptions are logged with timestamps and severity.

Sample log:

2025-10-18T16:24:12+0100 | INFO | public_api | Fetched 120 entries (count=120)
2025-10-18T16:24:12+0100 | INFO | cli | Wrote 120 rows to data/outputs_9a1b3e2f.csv




---





## 🧩 Why This Project Matters

This project demonstrates how to:

Translate manual tasks into automated, reproducible pipelines

Build intelligent connectors for open data or AI tools

Deliver clean, testable, Dockerized workflows that scale

It’s an ideal foundation for AI-assisted data labeling, workflow automation, and reproducible research pipelines.





> 👤 Author

> Maxwell C. Ihiaso  | 
> Senior Software Engineer — Backend & Automation Systems | 
> 📧 [ihiasomaxwellchukwuebuka@gmail.com]
> 🌍 LinkedIn | GitHub

🪄 License
MIT License © 2025 Maxwell C. Ihiaso



