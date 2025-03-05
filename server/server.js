//SERVER ENTRY POINT

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const app = express();
const drugRoutes = require('./routes/drugRoutes');

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/drugs', drugRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));