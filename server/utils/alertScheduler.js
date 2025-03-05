const db = require('../config/db');
const db = require('../models/Alert');
const db = require('../models/Drug');
const db = require('twilio');
const db = require('../@sendrid/mail');

function checkStockLevels() {
  const drugs = db.prepare('SELECT * FROM drugs').all();
  drugs.forEach((drug) => {
    if (drug.quantity <= drug.threshold) {
      const stmt = db.prepare('INSERT INTO alerts (drug_id, message) VALUES (?, ?)');
      stmt.run(drug.id, `${drug.name} is critically low! Current stock: ${drug.quantity}`);
    }
  });
}


// Initialize Twilio
const twilioClient = twilio(
    process.env.TWILIO_ACCOUNT_SID,
    process.env.TWILIO_AUTH_TOKEN
  );
  
  // Initialize SendGrid
  sgMail.setApiKey(process.env.SENDGRID_API_KEY);
  
  async function checkStockLevels() {
    const drugs = Drug.getAll();
    drugs.forEach(async (drug) => {
      if (drug.quantity <= drug.threshold) {
        // Log alert to database
        Alert.create({ drug_id: drug.id, message: `${drug.name} is critically low!` });
  
        // Send SMS via Twilio
        await twilioClient.messages.create({
          body: `ALERT: ${drug.name} stock is CRITICALLY LOW (${drug.quantity} left)!`,
          from: process.env.TWILIO_PHONE_NUMBER,
          to: '+1234567890' // Replace with your phone number
        });
  
        // Send Email via SendGrid
        const msg = {
          to: process.env.ADMIN_EMAIL,
          from: 'inventory@hospital.com',
          subject: 'Drug Stock Alert',
          text: `${drug.name} stock is CRITICALLY LOW (${drug.quantity} left)!`
        };
        await sgMail.send(msg);
      }
    });
  }

// Run every 5 minutes
setInterval(checkStockLevels, 300000);