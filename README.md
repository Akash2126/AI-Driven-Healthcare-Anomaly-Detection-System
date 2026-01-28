🧠 AI-Driven Healthcare Anomaly Detection System

An end-to-end real-time healthcare monitoring system that detects critical anomalies in patient vitals using machine learning, stream processing, and automated alerting.

The system simulates live patient vitals, processes them through ML models, detects anomalies, stores results in a database, triggers alerts via email, and visualizes everything on a real-time dashboard.

🚀 Key Features

Real-time patient vital streaming using Apache Kafka

Anomaly detection using Autoencoder + Isolation Forest

Patient-wise monitoring and explainability

PostgreSQL database for anomaly logs

Automated email alerts for critical conditions

Interactive dark-themed Flask dashboard

Scalable architecture (multiple patients supported)

🏗 System Architecture

Data Flow:

Health Sensors / Simulated Producer
⬇
Kafka Producer → Kafka Topic
⬇
Kafka Consumer (ML Engine)
⬇
Anomaly Detection Models
⬇
PostgreSQL Database
⬇
Alert & Explainability Layer
⬇
Flask Dashboard + Email Notifications

📌 Architecture Diagram (How it was created)

Architecture diagram was generated using Gemini AI based on the following prompt:

Create a professional system architecture diagram for an 
AI-driven healthcare anomaly detection system using Kafka, 
Autoencoder, Isolation Forest, PostgreSQL, email alerts, 
and a web dashboard. Show real-time data flow.


📸 Screenshot to add in documentation

Architecture diagram image

🛠 Technologies Used (Explained)
1️⃣ Python

Used for:

Kafka producer & consumer

Machine learning inference

Backend logic

2️⃣ Apache Kafka

Used for real-time streaming of patient vitals.
Kafka decouples data generation and data processing, enabling scalability.

Producer → sends patient vitals

Consumer → processes vitals using ML models

3️⃣ Machine Learning Models

Autoencoder

Learns normal patterns of patient vitals

High reconstruction error → anomaly

Isolation Forest

Detects outliers in feature space

Complements autoencoder for robustness

4️⃣ PostgreSQL

Used to store:

Patient ID

Anomaly score

Severity level

Vital signs

Timestamp

5️⃣ Flask

Used to build:

REST APIs

Real-time dashboard

Patient-wise anomaly views

6️⃣ Email Alert System

Gmail SMTP with App Password

Sends alerts only for HIGH severity

Includes explainability in email body

📂 Project Structure
AI-Driven_Healthcare_Anomaly_Detection_System/
│
├── app/                    
│   ├── templates/           
│   ├── static/              
│   └── app.py               
│
├── models/                  
│
├── utils/                   
│
├── data/                    
│
├── streaming_consumer_ml.py 
│
├── start_kafka.bat          
├── start_producer.bat       
├── start_consumer.bat       
├── start_all.bat           
│
└── README.md


Project folder structure

⚙️ Prerequisites
1️⃣ Python 3.9 or higher

Download:
https://www.python.org/downloads/

2️⃣ Apache Kafka (with Zookeeper)

Download:
https://kafka.apache.org/downloads

Kafka is required for real-time data streaming.

3️⃣ PostgreSQL Database

Download:
https://www.postgresql.org/download/

Used to store anomaly logs.

4️⃣ Git (Optional)

Download:
https://git-scm.com/downloads

5️⃣ Gmail App Password

Guide:
https://support.google.com/accounts/answer/185833

Required for sending automated email alerts.

📦 Dependencies

All dependencies are listed in requirements.txt.

Example:

flask
flask-cors
kafka-python
psycopg2
numpy
tensorflow
scikit-learn
joblib

Install dependencies:
pip install -r requirements.txt



pip install command output

▶️ How to Run the Project
Step 1: Start Kafka & Zookeeper
start_kafka.bat


Step 2: Start Kafka Producer
start_producer.bat



Step 3: Start Kafka Consumer (ML Engine)
start_consumer.bat


Anomaly detected logs

Email sent log

Step 4: Start Flask Dashboard
cd app
python app.py


Open browser:

http://127.0.0.1:5000/dashboard



Dashboard UI

Charts

KPI cards

📧 Email Alert Sample

When a critical anomaly is detected, an automated email is sent containing:

Patient ID

Anomaly score

Vital signs

Explainability

Primary contributing factor

Email alert

📊 Dashboard Features

Dark-themed professional UI

KPI cards (Active Patients, High Risk Alerts, Avg Score)

Severity color coding

Auto-refresh

Patient-wise filtering

Charts for vitals trend


Full dashboard

🌐 GitHub Repository

Repository URL:
https://github.com/Akash2126/AI-Driven-Healthcare-Anomaly-Detection-System

GitHub repo home page

🔮 Future Enhancements

Authentication (Doctor / Admin roles)

SHAP-based explainability

Docker deployment

Real sensor integration

Mobile dashboard

🖼️ DOCUMENTATION SCREENSHOT CHECKLIST (VERY IMPORTANT)

Use this exact order in your PDF:

1️⃣ Project Folder Structure
2️⃣ Architecture Diagram
3️⃣ Kafka Running
4️⃣ Producer Output
5️⃣ Consumer Output (Anomaly detected)
6️⃣ PostgreSQL Table View
7️⃣ Email Alert
8️⃣ Dashboard UI
9️⃣ GitHub Repository Page

