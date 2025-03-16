npm init -y
npm install express cors body-parser openai dotenv

// Load environment variables
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { OpenAI } = require('openai');

const app = express();
app.use(cors()); // Allow frontend requests
app.use(bodyParser.json());

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY, // Uses a secure environment variable
});

// API route to get job recommendations
app.post('/get-jobs', async (req, res) => {
    const { skills } = req.body;
    if (!skills) {
        return res.status(400).json({ error: "Please enter your skills." });
    }

    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: `Suggest 5-7 job roles for someone with these skills: ${skills}` }],
        });

        const jobs = response.choices[0].message.content.split("\n").filter(line => line.trim() !== "");
        res.json({ jobs });

    } catch (error) {
        console.error("OpenAI API Error:", error);
        res.status(500).json({ error: "Failed to retrieve job recommendations." });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
OPENAI_API_KEY=your-new-api-key-here

