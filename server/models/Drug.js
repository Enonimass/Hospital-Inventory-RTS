const db = require('../config/db');

class Drug {
  static createTable() {
    const sql = `
      CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER DEFAULT 0,
        threshold INTEGER DEFAULT 5
      )
    `;
    return db.exec(sql);
  }

  static getAll() {
    return db.prepare('SELECT * FROM drugs').all();
  }

  static getById(id) {
    return db.prepare('SELECT * FROM drugs WHERE id = ?').get(id);
  }

  static create({ name, quantity, threshold }) {
    const stmt = db.prepare('INSERT INTO drugs (name, quantity, threshold) VALUES (?, ?, ?)');
    return stmt.run(name, quantity, threshold);
  }

  static update(id, { name, quantity, threshold }) {
    const stmt = db.prepare('UPDATE drugs SET name = ?, quantity = ?, threshold = ? WHERE id = ?');
    return stmt.run(name, quantity, threshold, id);
  }

  static delete(id) {
    const stmt = db.prepare('DELETE FROM drugs WHERE id = ?');
    return stmt.run(id);
  }
}

module.exports = Drug;