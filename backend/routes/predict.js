const express = require('express');
const axios = require('axios');
const validate = require('../validators/predictSchema');

const router = express.Router();
const PYTHON_URL = process.env.PYTHON_URL || 'http://localhost:8000';

router.post('/predict', async (req, res) => {
  const { error, value } = validate(req.body);
  if (error) return res.status(400).json({ error: error.details.map(d => d.message) });

  try {
    const r = await axios.post(`${PYTHON_URL}/predict`, value, { timeout: 15000 });
    return res.json(r.data);
  } catch (err) {
    console.error('Prediction error:', err.toString());
    if (err.response) return res.status(err.response.status).json(err.response.data);
    return res.status(500).json({ error: 'Prediction service error' });
  }
});

module.exports = router;
