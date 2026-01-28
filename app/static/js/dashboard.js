let hrChart, spo2Chart;
let timer = null;

async function loadData() {
    const patient = document.getElementById("patientSelect").value;
    let url = "/anomalies";
    if (patient) url += "?patient_id=" + patient;

    const res = await fetch(url);
    const data = await res.json();

    renderKPIs(data);
    renderTable(data);
    renderCharts(data);
}

function renderKPIs(data) {
    document.getElementById("totalAlerts").innerText = data.length;

    const high = data.filter(d => d.severity === "HIGH").length;
    document.getElementById("highCount").innerText = high;

    const avg = data.reduce((s, d) => s + d.score, 0) / (data.length || 1);
    document.getElementById("avgScore").innerText = avg.toFixed(2);

    if (data.length)
        document.getElementById("lastTime").innerText =
            new Date(data[0].timestamp).toLocaleTimeString();
}

function renderTable(data) {
    const body = document.getElementById("tableBody");
    body.innerHTML = "";

    data.forEach(r => {
        body.innerHTML += `
        <tr>
            <td>${new Date(r.timestamp).toLocaleString()}</td>
            <td>${r.patient_id}</td>
            <td>${r.score.toFixed(2)}</td>
            <td class="sev-${r.severity}">${r.severity}</td>
            <td>${r.heart_rate}</td>
            <td>${r.spo2}</td>
            <td>${r.temperature.toFixed(1)}</td>
            <td>${r.systolic_bp}/${r.diastolic_bp}</td>
        </tr>`;
    });
}

function renderCharts(data) {
    const labels = data.map(d =>
        new Date(d.timestamp).toLocaleTimeString()).reverse();
    const hr = data.map(d => d.heart_rate).reverse();
    const spo2 = data.map(d => d.spo2).reverse();

    if (hrChart) hrChart.destroy();
    if (spo2Chart) spo2Chart.destroy();

    hrChart = new Chart(document.getElementById("hrChart"), {
        type: "line",
        data: { labels, datasets: [{ label: "Heart Rate", data: hr, borderColor: "red" }] }
    });

    spo2Chart = new Chart(document.getElementById("spo2Chart"), {
        type: "line",
        data: { labels, datasets: [{ label: "SpO₂", data: spo2, borderColor: "cyan" }] }
    });
}

document.getElementById("autoRefresh").addEventListener("change", e => {
    if (e.target.checked) {
        timer = setInterval(loadData, 10000);
    } else {
        clearInterval(timer);
    }
});

loadData();
function updateKPIs(data) {
    if (data.length === 0) return;

    const patients = new Set(data.map(d => d.patient_id));
    const highRisk = data.filter(d => d.severity === "HIGH");
    const avgScore = (
        data.reduce((a, b) => a + b.score, 0) / data.length
    ).toFixed(2);

    document.getElementById("kpiPatients").innerText = patients.size;
    document.getElementById("kpiHighRisk").innerText = highRisk.length;
    document.getElementById("kpiAvgScore").innerText = avgScore;
    document.getElementById("kpiLastAlert").innerText =
        new Date(data[0].timestamp).toLocaleTimeString();
}
