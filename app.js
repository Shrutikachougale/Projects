const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 5500; // You can change the port if needed

// Middleware to parse JSON bodies
app.use(bodyParser.json());


app.use(express.static(path.join(__dirname, 'public')));

// Route to handle recommendations
app.post('/recommend', (req, res) => {
    const { region, subcategory, subtype } = req.body;

    // Call the Python script with user selections
    const pythonProcess = spawn('python', ['recommend.py', region, subcategory, subtype]);

    pythonProcess.stdout.on('data', (data) => {
        const recommendations = JSON.parse(data);
        res.json(recommendations);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
        res.status(500).send('An error occurred while processing your request.');
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
