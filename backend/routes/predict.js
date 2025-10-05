// ===================================================
// FINAL FIXED VERSION - backend/routes/predict.js
// ===================================================

const express = require("express");
const axios = require("axios");
const validate = require("../validators/predictSchema");

const router = express.Router();
const PYTHON_URL = process.env.PYTHON_URL || "http://predict-service:8000";

// ---------------------------------------------
// POST /api/predict  → calls FastAPI ML service
// ---------------------------------------------
router.post("/", async (req, res) => {
  // Validate inputs
  const { error } = validate(req.body);
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }

  try {
    const r = await axios.post(`${PYTHON_URL}/predict`, req.body, { timeout: 15000 });
    const data = r.data;

    // Pass only useful fields to frontend
    return res.json({
      prediction: data.prediction,
      confidence: data.confidence,
    });
  } catch (err) {
    console.error("Prediction service error:", err.message);
    if (err.response) {
      return res.status(err.response.status).json({
        error: err.response.data.detail || "Prediction failed on backend.",
      });
    }
    return res.status(500).json({
      error: "Prediction service unavailable. Check FastAPI container logs.",
    });
  }
});

module.exports = router;
// Example frontend code for calling this endpoint: