# AI-Driven Healthcare Anomaly Detection System

A real-time healthcare monitoring system that detects abnormal patient vitals using machine learning, Kafka streaming, PostgreSQL storage, and a Flask-based dashboard.

---

## 🔍 Key Features
- Real-time patient vitals streaming (Apache Kafka)
- Anomaly detection using Autoencoder + Isolation Forest
- Patient-wise anomaly tracking
- PostgreSQL logging of alerts
- Email alerts for critical conditions
- Flask dashboard with charts and dark UI

---

## 🛠 Tech Stack
- Python
- Apache Kafka & Zookeeper
- Machine Learning (Autoencoder, Isolation Forest)
- PostgreSQL
- Flask
- Chart.js
- Git & GitHub

---

## ▶️ How to Run (Quick)
```bash
start_all.bat
start_kafka.bat
start_producer.bat
start_consumer.bat
cd app
python app.py
http://127.0.0.1:5000/dashboard
