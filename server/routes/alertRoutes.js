const express = require('express');
const router = express.Router();
const db = require('../config/db');

// GET all alerts
router.get('/', (req, res) => {
  const alerts = db.prepare('SELECT * FROM alerts').all();
  res.json(alerts);
});

module.exports = router;