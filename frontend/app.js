document.getElementById('predict').onclick = async () => {
  const payload = {
    N: +document.getElementById('N').value,
    P: +document.getElementById('P').value,
    K: +document.getElementById('K').value,
    temperature: +document.getElementById('temperature').value,
    humidity: +document.getElementById('humidity').value,
    ph: +document.getElementById('ph').value,
    rainfall: +document.getElementById('rainfall').value
  };
  const res = await fetch('/api/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById('out').innerText = JSON.stringify(data, null, 2);
};
