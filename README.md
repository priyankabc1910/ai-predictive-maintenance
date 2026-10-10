# AI Predictive Maintenance System

An end-to-end predictive maintenance platform that combines Remaining Useful Life (RUL) prediction, sensor anomaly detection, fleet monitoring, explainability, and maintenance decision support using NASA C-MAPSS FD001 data.

## Overview

Unexpected equipment failures can increase maintenance costs and operational downtime. This project explores how machine-learning models and sensor analytics can help identify unusual engine behavior, estimate remaining useful life, and prioritize maintenance actions.

The system combines an LSTM-based RUL prediction model with an Isolation Forest anomaly detector and a FastAPI backend, presented through an industrial-style React dashboard.

## Key Features

- **RUL prediction:** Estimates remaining useful life using an LSTM model.
- **Anomaly detection:** Uses Isolation Forest to identify unusual sensor observations.
- **Fleet monitoring:** Summarizes engine health, anomaly patterns, and risk indicators.
- **Maintenance prioritization:** Calculates maintenance scores and assigns action priorities.
- **Explainability:** Provides evidence and reasons supporting maintenance recommendations.
- **Cost intelligence:** Produces illustrative maintenance cost estimates in INR.
- **Sensor analysis:** Examines sensor trends and anomaly behavior over engine cycles.
- **Model comparison:** Evaluates the LSTM model against Random Forest and XGBoost baselines.
- **Interactive dashboard:** Provides Overview, Fleet, RUL, Anomalies, Maintenance, Intelligence, and Reports views.

## Technology Stack

| Component | Technology |
|---|---|
| Machine learning | TensorFlow/Keras, scikit-learn |
| Data processing | Python, pandas, NumPy |
| Backend | FastAPI, Uvicorn |
| Frontend | React, TypeScript, Vite |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Testing | pytest, FastAPI TestClient |
| Dataset | NASA C-MAPSS FD001 |

## System Architecture

1. NASA C-MAPSS sensor data is loaded and processed.
2. The LSTM model estimates remaining useful life.
3. Isolation Forest identifies anomalous sensor observations.
4. The backend combines predictions, anomaly metrics, and sensor evidence.
5. Maintenance scoring and priority reasoning generate decision-support recommendations.
6. Illustrative cost estimates provide additional planning context.
7. The frontend presents engine-level and fleet-level information.

## Machine-Learning Results

### RUL prediction

| Model | MAE | RMSE |
|---|---:|---:|
| LSTM | 22.11 | 32.98 |
| Random Forest | 24.12 | 33.49 |
| XGBoost | 24.73 | 33.96 |

The LSTM achieved the lowest MAE and RMSE among these reported model results.

*Evaluation figures are from the project's previously recorded evaluation. Re-run the evaluation scripts to reproduce them before making a formal benchmark claim.*

### Anomaly detection

The Isolation Forest model is trained using early-life observations from the training engines, with standardized sensor features.

In the latest recorded test-window analysis:
- 100 test engines were analyzed.
- 69 engines had at least one flagged cycle.
- The average per-engine anomaly rate was approximately 32.67%.
- 32 engines had at least 50% of their latest 30 cycles flagged.

These are **model-generated anomaly indicators, not confirmed engine failures**. The difference between early and late sensor windows indicates a distribution shift that warrants further validation.

## Maintenance Intelligence

The maintenance intelligence module combines:
- Predicted RUL
- Risk level
- Anomaly rate and severity
- Critical and high-priority sensor counts

It produces a maintenance score, a priority category, supporting reasons, and an illustrative cost estimate.

The default cost estimates are examples for demonstration, not actual industry quotations:
- Immediate: ₹50,000
- Urgent: ₹25,000
- Planned: ₹10,000
- Routine: ₹2,000

Actual costs depend on the equipment, parts, labor, and maintenance conditions.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Backend health check |
| `GET /model/info` | Model and dataset information |
| `GET /predict/{engine_id}` | RUL prediction |
| `GET /fleet` | Fleet information |
| `GET /fleet/summary` | Fleet summary |
| `GET /anomaly/fleet` | Fleet anomaly results |
| `GET /anomaly/fleet/summary` | Fleet anomaly summary |
| `GET /anomaly/fleet/trends` | Fleet anomaly trends |
| `GET /anomaly/fleet/top` | Highest-ranked anomalies |
| `GET /anomaly/{engine_id}` | Engine anomaly details |
| `GET /sensors/{engine_id}/trends` | Sensor trends |
| `GET /maintenance/{engine_id}` | Maintenance assessment |
| `GET /explain/{engine_id}` | Prediction explanation |
| `GET /knowledge/{engine_id}` | Maintenance guidance |
| `GET /maintenance/fleet` | Fleet maintenance overview |
| `GET /maintenance/intelligence/{engine_id}` | Integrated maintenance intelligence |
| `GET /evaluation/rul` | RUL evaluation |
| `GET /models/comparison` | Model comparison |

FastAPI's interactive API documentation is available at `/docs` while the backend is running.

## Installation and Setup

### Prerequisites
- Python and pip
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-predictive-maintenance
```

### 2. Create and activate a Python virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

Use the repository's dependency file if present:

```powershell
pip install -r requirements.txt
```

### 4. Start the backend

```powershell
python -m uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

### 5. Start the frontend

Open a second terminal in the repository root:

```powershell
npm install
npm run dev
```

Open the local URL printed by Vite.

Check the repository's existing configuration for any additional environment variables or frontend API URL settings.

## Testing

Run the backend test suite:

```powershell
python -m pytest -q
```

Latest recorded result: **79 passed, 1 warning**.

Build the frontend:

```powershell
npm run build
```

The previously recorded production build completed successfully. Re-run both commands after any code changes.

## Limitations

- Anomaly detection identifies statistical outliers; it does not independently confirm mechanical faults.
- Maintenance priority thresholds are rule-based and require validation against operational data.
- Cost estimates are illustrative.
- Model performance on NASA C-MAPSS data does not guarantee equivalent performance on real industrial equipment.
- The project is a decision-support prototype, not a replacement for engineering inspection or safety procedures.

## Future Improvements

- Validate anomaly detection against labeled fault events.
- Evaluate the model on additional engine operating conditions.
- Add model monitoring and data-drift alerts.
- Calibrate maintenance priorities against actual maintenance outcomes.
- Replace illustrative costs with configurable, equipment-specific estimates.
- Optimize inference performance and add deployment monitoring.

## Dataset

NASA Commercial Modular Aero-Propulsion System Simulation (C-MAPSS), FD001 subset.

Dataset source: NASA Prognostics Center of Excellence — https://www.nasa.gov/

## Disclaimer

This project is intended for educational and research purposes. Predictions and recommendations should be validated before use in real maintenance operations.
