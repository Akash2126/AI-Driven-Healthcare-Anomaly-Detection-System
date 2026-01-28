from kafka import KafkaProducer
import json
import time
import random

# ---------------- Kafka Producer Setup ----------------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "patient_vitals"

PATIENT_IDS = ["P001", "P002", "P003"]

ANOMALY_DURATION = 20
anomaly_counter = 0
anomaly_patient = None

print("Kafka Producer started")
print("Streaming patient vitals...\n")

while True:
    # ---------------- Select Patient ----------------
    if anomaly_counter > 0:
        patient_id = anomaly_patient
    else:
        patient_id = random.choice(PATIENT_IDS)

    # ---------------- Trigger Anomaly ----------------
    if anomaly_counter == 0 and random.random() < 0.05:
        anomaly_counter = ANOMALY_DURATION
        anomaly_patient = patient_id
        print(f"\n🚨 Anomaly window started for {patient_id}\n")

    # ---------------- Generate Data ----------------
    if anomaly_counter > 0:
        vitals = {
            "patient_id": patient_id,
            "Heart Rate": random.randint(150, 190),
            "Respiratory Rate": random.randint(35, 45),
            "Body Temperature": random.uniform(39.5, 41.5),
            "Oxygen Saturation": random.uniform(75, 85),
            "Systolic Blood Pressure": random.randint(185, 215),
            "Diastolic Blood Pressure": random.randint(115, 135),
            "Derived_HRV": random.uniform(0.005, 0.02),
            "Derived_MAP": random.uniform(130, 155),
            "timestamp": time.time()
        }
        anomaly_counter -= 1

        if anomaly_counter == 0:
            anomaly_patient = None

        print("🚨 ANOMALY:", vitals)

    else:
        vitals = {
            "patient_id": patient_id,
            "Heart Rate": random.randint(60, 90),
            "Respiratory Rate": random.randint(12, 18),
            "Body Temperature": random.uniform(36.3, 37.2),
            "Oxygen Saturation": random.uniform(95, 99),
            "Systolic Blood Pressure": random.randint(110, 135),
            "Diastolic Blood Pressure": random.randint(70, 85),
            "Derived_HRV": random.uniform(0.05, 0.15),
            "Derived_MAP": random.uniform(85, 100),
            "timestamp": time.time()
        }

        print("🟢 NORMAL :", vitals)

    # ---------------- Send to Kafka ----------------
    producer.send(TOPIC, vitals)
    time.sleep(1)
