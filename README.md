
# Public Tender Analysis & Visualization Dashboard (Nova Scotia)

A one‑stop, interactive dashboard that turns **raw Nova Scotia Open Data** tender records into actionable insights. Built as the final project for Dalhousie’s *CSCI 6612 – Visual Analytics*, it blends modern data‑processing, machine‑learning and visualization tooling into a single Docker‑deployable app.

## ✨ TL;DR
* **Dash + Plotly** UI with two complementary lenses  
  * **Cluster View** – macro patterns across 15 clusters (plus a curated *Health* super‑cluster).  
  * **Entity View** – micro drill‑downs for a single public entity.  
* **Machine Learning**  
  * *K‑Means &amp; Agglomerative* clustering on entity behaviour.  
  * Context‑aware **BERTopic** modelling of 125 k+ descriptions to surface procurement themes.  
* **Dynamic UX** – modal pop‑ups, cross‑filtering, category toggles, topic timelines.  
* **One‑click deploy** via **Docker Compose**; hot‑reload for development.  

---

## Table of Contents
1. [Features](#1-features)
2. [Quick Start](#2-quick-start)
3. [Local Development](#3-local-development)
4. [Folder Structure](#4-folder-structure)
5. [Data Pipeline](#5-data-pipeline)
6. [License](#6-license)

---

## 1. Features
### 📊 Interactive Visual Analytics
* Real‑time filters for **cluster, entity, year, category** (Goods | Services | Construction).
* Linked bar &amp; line charts (awarded amount, tender counts, vendor concentration).
* **Modal drill‑downs** with full tender meta‑data.
* Hover &amp; click callbacks for instant contextual narratives.

### 🧠 Machine‑Learning Modules
| Task | Algorithm | Purpose |
|------|-----------|---------|
| Clustering | K‑Means (k = 15 via Elbow) + Agglomerative check | Group entities by spend behaviour |
| Topic modelling | **BERTopic** (BERT embeddings + HDBSCAN) | Extract procurement themes &amp; trend over time |

---

## 2. Quick Start

### Docker (recommended)
```bash
git clone https://github.com/samshad/public-tender-analysis-dashboard.git
cd public-tender-analysis-dashboard
docker-compose up --build
# open http://localhost:8050
```

### Local Python
```bash
python -m venv .venv && source .venv/bin/activate   # or `.\.venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py
```

---

## 3. Local Development
* **Hot‑reload:** edit code and Dash restarts automatically.
* **Linting:** `ruff .`

---

## 4. Folder Structure
```text
├── app.py                # Dash entry‑point
├── docker-compose.yml    # One‑command deployment
├── Dockerfile            # Light‑weight image (python:3.12‑slim)
├── data/                 # Raw & cleaned tender CSVs
├── data_cleaning/        # Pre‑processing scripts
├── utils/                # ML helpers (clustering, topic model)
├── layouts/              # Reusable Dash layout builders
├── callbacks/            # All Dash callback wiring
├── visualizations/       # Plotly figure factories
├── assets/               # Dash static assets (CSS, images, icons)
└── requirements.txt
```

---

## 5. Data Pipeline
1. **Cleaning & Standardisation**  
   * Resolve 12 594 vendor spellings → **5 600 unique** names.  
   * Reduce 225 entity labels → **215 standardised** entities.  
   * Drop incomplete rows &lt; \$1 000 or with missing descriptions.  
2. **Feature Engineering** – tender **duration**, category dummies, inflation‑adjusted spend.  
3. **ML** – cluster entities, assign topics, persist artefacts.  
4. **Dashboard** – load artefacts, render interactive views.

---

## 6. License
[MIT](LICENSE) © 2025 Md Samshad Rahman
