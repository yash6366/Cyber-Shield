// classifierAgent.js
// Classifier Agent for threat classification in JavaScript calling Python API

const axios = require('axios');

class ClassifierAgent {
    constructor() {
        this.apiUrl = '/api/classifier';
    }

    async classify(threatDescription) {
        try {
            const response = await axios.post(`${this.apiUrl}/classify`, { threat_description: threatDescription });
            const label = response.data.label;
            console.log(`Classified threat: "${threatDescription}" as ${label}`);
            return label;
        } catch (error) {
            console.error("Error classifying threat:", error.message);
            return null;
        }
    }

    async train(callback) {
        console.log("Requesting training of Classifier Agent via API...");
        try {
            const response = await axios.post(`${this.apiUrl}/train`);
            console.log("Classifier Agent training response:", response.data);
            if (callback) callback();
        } catch (error) {
            console.error("Error training Classifier Agent:", error.message);
        }
    }
}

module.exports = ClassifierAgent;

if (require.main === module) {
    const agent = new ClassifierAgent();
    agent.train();
}
