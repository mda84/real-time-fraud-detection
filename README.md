# Real-Time Fraud Detection System

## Overview
This project implements a real‑time fraud detection system for financial transactions. It includes:

- **Data Pipeline:** Ingest, preprocess, and transform raw transaction data.
- **Model Development:** Train and optimize a fraud detection classifier using machine learning algorithms (e.g., XGBoost or logistic regression).
- **Model Deployment:** Serve predictions via a REST API built with FastAPI. The API logs incoming transactions and prediction outcomes to a database.
- **Monitoring:** Basic logging and metrics are implemented to track model performance over time.
- **Containerization & Orchestration:** The system is containerized with Docker and includes Kubernetes manifests for scalable production deployment.
- **Interactive Experimentation:** A Jupyter Notebook is provided for exploring data, training experiments, and evaluating the model.

## Project Structure
```
real-time-fraud-detection/
├── README.md                   # Overview, installation, usage, deployment, etc.
├── requirements.txt            # Python dependencies.
├── Dockerfile                  # Container configuration.
├── data_pipeline/              
│   ├── ingest.py               # Downloads (or reads) and ingests raw transaction data.
│   ├── transform.py            # Cleans, normalizes, and feature-engineers the raw data.
│   └── config.yaml             # Pipeline configuration (e.g., hyperparameters, feature list).
├── model/                      
│   ├── train.py                # Trains and optimizes the fraud detection model.
│   ├── evaluate.py             # Evaluates the model and reports metrics.
│   └── predict.py              # Command-line inference script.
├── api/                        
│   ├── app.py                  # FastAPI app that serves predictions and logs them.
│   └── database.py             # SQLAlchemy database models and connection setup.
└── notebooks/                  
    └── Fraud_Detection_Development.ipynb   # Notebook for interactive experimentation.
```

## Installation

### Prerequisites
- Python 3.9 or later.
- A virtual environment is recommended.

### Setup

**Clone the Repository:**
```
   git clone https://github.com/mda84/real-time-fraud-detection.git
   cd real-time-fraud-detection
```

Create and Activate a Virtual Environment:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install Dependencies:
```
pip install -r requirements.txt
```

## Usage
Data Pipeline
Ingest Data:
```
python data_pipeline/ingest.py path/to/raw_transactions.csv
```

Transform Data:
```
python data_pipeline/transform.py path/to/raw_transactions.csv feature1 feature2 ...
```
The output is a cleaned CSV file ready for model training.

## Model Development
Training:
```
python model/train.py
```
This script trains the model and saves it (e.g., as model/fraud_model.pkl).

Evaluation:
```
python model/evaluate.py model/fraud_model.pkl path/to/test_data.csv
```

Prediction:
```
python model/predict.py feature1 feature2 ... 
```

## API Deployment
Run Locally:
```
uvicorn api.app:app --host 0.0.0.0 --port 8000
```
The prediction endpoint is available at http://localhost:8000/predict.

## Interactive Notebook
Open the Jupyter Notebook for interactive experimentation:
```
jupyter notebook notebooks/Fraud_Detection_Development.ipynb
```

## Docker Deployment
Build the Docker Image:
```
docker build -t real-time-fraud-detection .
```

Run the Docker Container:
```
docker run -it -p 8000:8000 real-time-fraud-detection
```

## Kubernetes Deployment
The kubernetes/ directory includes sample manifests for:
Deploying the FastAPI service.
Exposing the service via a LoadBalancer.
Deploying a PostgreSQL instance for logging.

Apply the manifests:
```
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

## Monitoring & Logging
The FastAPI API logs each transaction and prediction outcome to a database.
For production, integrate Prometheus and Grafana to monitor performance metrics and set up alerts.

## Collaboration & CI/CD
Use Git for version control.
Integrate GitHub Actions (or your CI/CD tool) to automate testing, model training, and deployment.
Detailed documentation and modular code support collaboration among data scientists, engineers, and product teams.

## Research & Experimentation
The provided notebook allows interactive exploration of the data, model performance, and sensitivity analysis.
Continuous experimentation is encouraged to refine features and model performance.

## License
This project is licensed under the MIT License.

## Contact
For questions, collaboration, or contributions, please contact dorkhah9@gmail.com