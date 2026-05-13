# 📦 Amazon Last-Mile Delivery Analytics
## Global Transportation & Logistics — Germany Operations

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)

---

## 📌 Project Overview

An end-to-end supply chain analytics project simulating Amazon GTL operations across Germany. Built from the perspective of an **Ops Logistics Specialist** responsible for monitoring delivery performance, identifying operational bottlenecks, performing root cause analysis, and surfacing cost saving opportunities.

### Business Task
Monitor and improve last-mile delivery performance across the German logistics network by:
- Tracking SLA compliance across all carriers and warehouses
- Identifying root causes of delivery failures
- Surfacing cost saving opportunities across routes and carriers
- Supporting data-driven operational decision-making

> **Note:** An 88% on-time delivery rate is used as the SLA benchmark target throughout this analysis, based on industry standard logistics performance thresholds.

---

## 📊 Dataset

| Field | Detail |
|---|---|
| Orders | 1,875 simulated delivery orders |
| Period | January – June 2024 |
| Warehouses | Berlin, Hamburg, Munich, Frankfurt, Cologne |
| Carriers | DHL, DPD, Hermes, UPS, FedEx |
| Customer Cities | 20 German cities |
| Columns | 19 (order details, cost, SLA, delay info) |

*Data is fully simulated for portfolio purposes using realistic logistics parameters.*

---

## 🔍 Key Findings

- **Overall on-time rate: 87.9%** — just below the 88% SLA target, triggering operational review
- **Hermes worst performer** at 85% on-time rate — below SLA threshold
- **Top delay cause: Carrier Delay (19.9%)** followed by Traffic Congestion (19.0%)
- **48.3% of delays are fully preventable** — wrong routing, warehouse delays, address issues
- **Weekend orders 45% more likely to be late** — 16.7% vs 11.5% on weekdays
- **May best month (7.6% late rate)**, June worst (13.7%) — inconsistent operations
- **Total potential savings: €9,454/year** across 3 identified opportunities

---

## 💡 Cost Savings Opportunities

| Opportunity | Affected Orders | Annual Saving |
|---|---|---|
| Switch UPS to DHL | 369 orders | €701 |
| Fix Wrong Routing Defects | 37 orders | €821 |
| Reassign Long Distance Routes | 641 orders | €7,932 |
| **Total** | | **€9,454/year** |

---

## 📂 Repository Structure

```
amazon-logistics-analytics/
├── app.py                              # Streamlit KPI dashboard
├── Amazon_Logistics_Analytics.ipynb   # Full analysis notebook
├── deliveries.csv                      # Simulated dataset (1,875 orders)
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/ayhambokli/amazon-logistics-analytics.git
cd amazon-logistics-analytics
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deploy on Streamlit Cloud
1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo and set main file as `app.py`
5. Click Deploy

---

## 📓 Notebook Structure

| Section | Description |
|---|---|
| 1. Data Loading | Load and inspect the dataset |
| 2. Data Cleaning | Type conversion, quality checks |
| 3. Feature Engineering | is_late, cost_per_km, is_weekend |
| 4. EDA | Orders by month, carrier, status, delay severity |
| 5. KPI Analysis | On-time rate, cost by carrier, warehouse, month |
| 6. Root Cause Analysis | Delay reasons, carrier breakdown, weekend vs weekday, monthly trend |
| 7. Cost Analysis | Total cost, cost by carrier, cost by route |
| 8. Recommendations | Quantified cost savings and operational improvements |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data cleaning & analysis |
| NumPy | Calculations |
| Plotly | Interactive charts |
| Streamlit | Dashboard deployment |
| openpyxl | Excel report export |

---

**Ayham Bokli** | MSc Information & Operations Management | Supply Chain & Logistics Analytics
*Data is simulated for portfolio purposes*
