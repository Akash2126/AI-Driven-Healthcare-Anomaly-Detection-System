import json
import time
import psycopg2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from kafka import KafkaConsumer
from tensorflow.keras.models import load_model
import joblib

# =====================================================
# CONFIG
# =====================================================
TOPIC = "patient_vitals"
BOOTSTRAP_SERVERS = "localhost:9092"

WINDOW_SIZE = 30
EMAIL_COOLDOWN_SECONDS = 600  # 10 min
PATIENT_ID_FIELD = "patient_id"

FEATURES = [
    "Heart Rate",
    "Respiratory Rate",
    "Body Temperature",
    "Oxygen Saturation",
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Derived_HRV",
    "Derived_MAP"
]

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "kumarakash02401@gmail.com"
RECEIVER_EMAIL = "contact.akash.tiwari@gmail.com"
APP_PASSWORD = "gezsrqzqssukcvhm"

# =====================================================
# LOAD MODELS
# =====================================================
autoencoder = load_model("models/autoencoder_model.keras")
iso_forest = joblib.load("models/isolation_forest.pkl")
scaler = joblib.load("models/scaler.pkl")

# =====================================================
# POSTGRESQL
# =====================================================
conn = psycopg2.connect(
    host="localhost",
    database="anomaly_db",
    user="postgres",
    password="postgres123",
    port=5432
)
cursor = conn.cursor()

# =====================================================
# KAFKA CONSUMER
# =====================================================
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest"
)

# =====================================================
# STATE
# =====================================================
windows = {}
baselines = {}
last_email_time = {}

# =====================================================
# HELPERS
# =====================================================
def severity(score):
    if score < 1.2:
        return "LOW"
    elif score < 2.5:
        return "MEDIUM"
    return "HIGH"


def update_baseline(old, current, alpha=0.05):
    """Exponential Moving Average baseline"""
    for k in FEATURES:
        old[k] = (1 - alpha) * old[k] + alpha * current[k]
    return old


def compute_explainability(current, baseline):
    deviations = {k: abs(current[k] - baseline[k]) for k in FEATURES}
    total = sum(deviations.values()) + 1e-6

    contributions = {
        k: round((v / total) * 100, 1) for k, v in deviations.items()
    }

    primary_feature, primary_percent = max(contributions.items(), key=lambda x: x[1])

    reasons = []
    if current["Heart Rate"] > baseline["Heart Rate"]:
        reasons.append("Heart Rate elevated")
    if current["Oxygen Saturation"] < baseline["Oxygen Saturation"]:
        reasons.append("Oxygen saturation decreased")
    if current["Body Temperature"] > baseline["Body Temperature"]:
        reasons.append("Body temperature elevated")

    return reasons, primary_feature, primary_percent


def send_email(patient_id, score, record, reasons, primary_feature, primary_percent):
    now = time.time()
    last_time = last_email_time.get(patient_id, 0)

    if now - last_time < EMAIL_COOLDOWN_SECONDS:
        return

    last_email_time[patient_id] = now

    html = f"""
    <h2 style="color:red;">Critical Health Anomaly Detected</h2>
    <p><b>Patient ID:</b> {patient_id}</p>
    <p><b>Anomaly Score:</b> {score:.4f}</p>

    <table border="1" cellpadding="6">
        <tr><td>Heart Rate</td><td>{record['Heart Rate']}</td></tr>
        <tr><td>SpO₂</td><td>{record['Oxygen Saturation']}</td></tr>
        <tr><td>Temperature</td><td>{record['Body Temperature']}</td></tr>
        <tr><td>Blood Pressure</td>
            <td>{record['Systolic Blood Pressure']}/{record['Diastolic Blood Pressure']}</td>
        </tr>
    </table>

    <h3>Explainability</h3>
    <ul>{"".join(f"<li>{r}</li>" for r in reasons)}</ul>

    <p><b>Primary Contributor:</b> {primary_feature} ({primary_percent}%)</p>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = "Critical Patient Health Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# =====================================================
# STREAM LOOP
# =====================================================
for msg in consumer:
    record = msg.value
    patient_id = record.get(PATIENT_ID_FIELD, "UNKNOWN")

    if patient_id not in windows:
        windows[patient_id] = []
        baselines[patient_id] = record.copy()

    window = windows[patient_id]
    window.append([record[f] for f in FEATURES])

    if len(window) < WINDOW_SIZE:
        continue
    if len(window) > WINDOW_SIZE:
        window.pop(0)

    window_np = np.array(window)
    window_scaled = scaler.transform(window_np)
    window_flat = window_scaled.flatten().reshape(1, -1)

    recon = autoencoder.predict(window_flat, verbose=0)
    ae_error = np.mean(np.square(window_flat - recon))
    iso_score = -iso_forest.decision_function(window_flat)[0]

    score = ae_error + iso_score
    sev = severity(score)

    if sev == "LOW":
        baselines[patient_id] = update_baseline(baselines[patient_id], record)

    if sev == "HIGH":
        cursor.execute("""
            INSERT INTO anomaly_logs
            (timestamp, patient_id, anomaly_score, severity,
             heart_rate, spo2, temperature,
             systolic_bp, diastolic_bp)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            float(score),
            sev,
            record["Heart Rate"],
            record["Oxygen Saturation"],
            record["Body Temperature"],
            record["Systolic Blood Pressure"],
            record["Diastolic Blood Pressure"]
        ))
        conn.commit()

        reasons, primary_feature, primary_percent = compute_explainability(
            record, baselines[patient_id]
        )

        send_email(patient_id, score, record, reasons, primary_feature, primary_percent)

    print(f"{sev} | Patient={patient_id} | Score={score:.3f}")
