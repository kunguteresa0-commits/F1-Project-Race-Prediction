# 🏎️ F1 Podium Probability Predictor

An end-to-end machine learning platform that predicts which Formula 1 drivers are most likely to finish on the podium (Top 3).
This project covers the full pipeline — from raw data ingestion and database storage to model training and a live interactive dashboard.

---

## 📊 Dashboard Preview

![Dashboard](https://github.com/user-attachments/assets/72ccd03a-8261-4685-9a15-0afe3511fc40)

---

## 🎯 Project Goal

The goal of this project is to bridge the gap between historical Formula 1 data and real-time race insights.

By analyzing:

* Driver performance trends
* Grid positions
* Team/constructor strength

…across the **2021–2025 seasons**, the system generates **probability scores for podium finishes**, helping users understand likely race outcomes.

---

## 🧬 System Architecture

### 🔹 Data Layer

* Ingests historical race data from the **Jolpica API (Ergast-compatible)**
* Includes race results, qualifying data, and standings

### 🔹 Storage Layer

* PostgreSQL 15 database running in Docker
* Ensures efficient querying and structured storage

### 🔹 ML Pipeline

* Feature engineering includes:

  * Rolling driver performance
  * Qualifying gap metrics
  * Constructor performance trends
* Built using **Pandas** and **Scikit-learn**

### 🔹 Interface

* Interactive dashboard built with **Streamlit**
* Users can select a race and instantly view predicted podium probabilities

---

## 🛠️ Technical Stack

| Layer            | Tool                                        |
| ---------------- | ------------------------------------------- |
| Language         | Python 3.11+                                |
| Database         | PostgreSQL 15                               |
| Containerization | Docker & Docker Compose                     |
| ML Models        | Scikit-learn (Logistic Regression), XGBoost |
| Data Processing  | Pandas, NumPy, SQLAlchemy                   |
| UI Framework     | Streamlit                                   |

---

## ⚙️ Installation & Setup

### ✅ Prerequisites

* Docker Desktop installed
* Python 3.11 installed

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kunguteresa0-commits/F1-Project-Race-Prediction.git
cd F1-Project-Race-Prediction
```

---

### 2️⃣ Configure Environment

Create a `.env` file in the root directory:

```env
DB_USER=f1user
DB_PASSWORD=yourpassword
DB_NAME=f1db
DB_HOST=localhost
DB_PORT=5432
```

---

### 3️⃣ Launch Database (Docker)

```bash
docker-compose up -d
```

---

### 4️⃣ Run the Data Pipeline

#### 🔹 Ingest historical data (lighter version recommended)

```bash
python src/ingestion/ingest_ergast.py --start-season 2022 --end-season 2024
```

#### 🔹 Ingest lap/session data (recommended: one year for low RAM systems)

```bash
python src/ingestion/ingest_openf1.py --year 2024
```

#### 🔹 (Optional) FastF1 ingestion

```bash
python src/ingestion/ingest_fastf1.py --year 2025
```

---

### 5️⃣ Clean and Merge Data

```bash
python src/processing/clean_data.py
```

---

### 6️⃣ Feature Engineering

```bash
python src/features/build_features.py
```

---

### 7️⃣ Train Models

```bash
python src/models/train.py --target is_top3 is_winner
```

---

### 8️⃣ Evaluate Model

```bash
python src/models/evaluate.py --target is_top3 is_winner
```

---

### 9️⃣ Launch Dashboard

```bash
streamlit run app/streamlit_app.py
```

---

## 🌐 Service URLs

| Service       | URL                   |
| ------------- | --------------------- |
| Streamlit App | http://localhost:8501 |
| PostgreSQL    | localhost:5432        |

---

## 📸 Visualizations

### 🔹 Probability Table

![Probability Table](https://github.com/user-attachments/assets/8e8ee62e-7bbe-4fa2-8038-65fb342105fd)

---

### 🔹 Visualized Odds

![Odds Chart](https://github.com/user-attachments/assets/a06e0372-cba7-4264-97d6-96fc6bbd207e)

---

## 📂 Project Structure

```
F1-Project-Race-Prediction/
│
├── app/
│   └── streamlit_app.py       # Interactive dashboard
│
├── src/
│   ├── ingestion/             # Data ingestion scripts
│   ├── processing/            # Data cleaning & merging
│   ├── features/              # Feature engineering
│   ├── models/                # Training & evaluation
│   └── utils/                 # DB + helper functions
│
├── data/
│   ├── raw/                   # Raw ingested data
│   └── processed/             # Cleaned & model-ready data
│
├── artifacts/                 # Trained models (.pkl)
├── metrics/                   # Evaluation results
├── docker-compose.yml         # PostgreSQL container
├── requirements.txt
└── README.md
```

---

## 🚀 Key Highlights

* End-to-end ML pipeline (data → model → dashboard)
* Time-aware training (prevents data leakage)
* Real-world data integration from multiple APIs
* Interactive visualization for decision insights
* Optimized to run on low-resource machines (8GB RAM)

---

## 📌 Future Improvements

* Add live race prediction (real-time updates)
* Hyperparameter tuning for better accuracy
* Deploy dashboard online (Streamlit Cloud / Render)
* Add driver comparison analytics

---

## 👩‍💻 Author

**Teresa Kungu**

---

## ⭐ If you found this useful

Give the repo a star and feel free to fork it!

   
