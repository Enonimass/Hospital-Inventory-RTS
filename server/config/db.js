const Database = require('better-sqlite3');
const Drug = require('../models/Drug');
const Alert = require('../models/Alert');


// Connect to SQLite database
const db = new Database('./database/inventory.db');

Drug.createTable();
Alert.createTable();

module.exports = db

// Initialize database (create tables if they don't exist)
db.exec(`
  CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER DEFAULT 0,
    threshold INTEGER DEFAULT 5
  );

  CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
  );
`);

module.exports = db;