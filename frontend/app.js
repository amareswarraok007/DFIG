// ====================================================
// FINAL FIXED VERSION - frontend/app.js
// ====================================================

const form = document.getElementById("cropForm");
const result = document.getElementById("result");
const sampleBtn = document.getElementById("sample");

// Handle Predict
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    N: parseFloat(N.value),
    P: parseFloat(P.value),
    K: parseFloat(K.value),
    temperature: parseFloat(temperature.value),
    humidity: parseFloat(humidity.value),
    ph: parseFloat(ph.value),
    rainfall: parseFloat(rainfall.value),
  };

  const res = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const out = await res.json();

  if (out.prediction) {
    const color =
      out.confidence > 0.9 ? "green" :
      out.confidence > 0.7 ? "orange" : "red";

    result.innerHTML = `
      🌱 Predicted Crop: <b style="color:${color}">${out.prediction}</b><br>
      Confidence: ${(out.confidence * 100).toFixed(1)}%
    `;
  } else {
    result.innerText = "❌ Error: " + (out.error || "Unknown error");
  }
});

// Handle Sample Button
sampleBtn.addEventListener("click", () => {
  // Example mirchi values
  N.value = 80;
  P.value = 40;
  K.value = 60;
  temperature.value = 28;
  humidity.value = 75;
  ph.value = 6.5;
  rainfall.value = 120;
});
