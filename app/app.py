from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# ============================
# DATABASE CONNECTION
# ============================
conn = psycopg2.connect(
    host="localhost",
    database="anomaly_db",
    user="postgres",
    password="postgres123",
    port=5432
)
conn.autocommit = True

# ============================
# HOME / HEALTH CHECK
# ============================
@app.route("/")
def home():
    return jsonify({
        "status": "OK",
        "message": "AI Anomaly Detection Backend Running"
    })

# ============================
# DASHBOARD UI
# ============================
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ============================
# GET ANOMALIES (API)
# ============================
@app.route("/anomalies", methods=["GET"])
def get_anomalies():
    patient_id = request.args.get("patient_id")

    query = """
        SELECT patient_id, timestamp, anomaly_score, severity,
               heart_rate, spo2, temperature,
               systolic_bp, diastolic_bp
        FROM anomaly_logs
    """
    params = []

    if patient_id:
        query += " WHERE patient_id = %s"
        params.append(patient_id)

    query += " ORDER BY timestamp DESC LIMIT 50"

    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()

    data = []
    for r in rows:
        data.append({
            "patient_id": r[0],
            "timestamp": r[1],
            "score": float(r[2]),
            "severity": r[3],
            "heart_rate": r[4],
            "spo2": r[5],
            "temperature": r[6],
            "systolic_bp": r[7],
            "diastolic_bp": r[8]
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
