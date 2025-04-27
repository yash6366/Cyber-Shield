// responseAgent.js
// Response Agent for executing response actions in JavaScript calling Python API

const axios = require('axios');

class ResponseAgent {
    constructor() {
        this.apiUrl = '/api/response';
    }

    async executeResponse(action) {
        try {
            const response = await axios.post(`${this.apiUrl}/execute`, { action });
            const success = response.data.success;
            if (success) {
                console.log(`Executed response action: ${action}`);
            }
            return success;
        } catch (error) {
            console.error("Error executing response action:", error.message);
            return false;
        }
    }

    async train(callback) {
        console.log("Requesting training of Response Agent via API...");
        try {
            const response = await axios.post(`${this.apiUrl}/train`);
            console.log("Response Agent training response:", response.data);
            if (callback) callback();
        } catch (error) {
            console.error("Error training Response Agent:", error.message);
        }
    }
}

module.exports = ResponseAgent;

if (require.main === module) {
    const agent = new ResponseAgent();
    agent.train();
}
