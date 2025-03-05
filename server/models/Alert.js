const db = require('../config/db');

class Alert {
  static createTable() {
    const sql = `
      CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_id INTEGER,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (drug_id) REFERENCES drugs(id)
      )
    `;
    return db.exec(sql);
  }

  static getAll() {
    return db.prepare('SELECT * FROM alerts').all();
  }

  static getByDrugId(drugId) {
    return db.prepare('SELECT * FROM alerts WHERE drug_id = ?').all(drugId);
  }

  static create({ drug_id, message }) {
    const stmt = db.prepare('INSERT INTO alerts (drug_id, message) VALUES (?, ?)');
    return stmt.run(drug_id, message);
  }
}

module.exports = Alert;