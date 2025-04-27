// hunterAgent.js
// Hunter Agent for threat detection in JavaScript calling Python API

const axios = require('axios');

class HunterAgent {
    constructor() {
        this.apiUrl = '/api/hunter';
    }

    async train(callback) {
        console.log("Requesting training of Hunter Agent via API...");
        try {
            const response = await axios.post(`${this.apiUrl}/train`);
            console.log("Hunter Agent training response:", response.data);
            if (callback) callback();
        } catch (error) {
            console.error("Error training Hunter Agent:", error.message);
        }
    }

    async detectThreat(trafficLog) {
        try {
            // Extract features from trafficLog - placeholder example
            const features = this.extractFeatures(trafficLog);
            const response = await axios.post(`${this.apiUrl}/detect`, { features });
            const threatDetected = response.data.threat_detected;
            if (threatDetected) {
                console.log(`Threat detected in traffic from ${trafficLog.source_ip} to ${trafficLog.destination_ip}`);
            }
            return threatDetected;
        } catch (error) {
            console.error("Error detecting threat:", error.message);
            return false;
        }
    }

    extractFeatures(trafficLog) {
        // Placeholder: convert trafficLog to feature vector for model
        // For now, return dummy fixed-length array
        return new Array(100).fill(0).map(() => Math.random());
    }
}

module.exports = HunterAgent;

if (require.main === module) {
    const agent = new HunterAgent();
    agent.train();
}
