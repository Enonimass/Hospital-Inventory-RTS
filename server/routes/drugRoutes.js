const express = require('express');
const router = express.Router();
const db = require('../config/db');
const Drug = require("../models/Drug")

// GET all drugs
router.get('/', (req, res) => {
  const drugs = db.prepare('SELECT * FROM drugs').all();
  res.json(drugs);
});

// POST new drug
router.post('/', (req, res) => {
  const { name, quantity, threshold } = req.body;
  const stmt = db.prepare('INSERT INTO drugs (name, quantity, threshold) VALUES (?, ?, ?)');
  stmt.run(name, quantity, threshold);
  res.sendStatus(201);
});

module.exports = router;