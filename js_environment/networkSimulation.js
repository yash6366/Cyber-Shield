// networkSimulation.js
// Simulated network environment in JavaScript

class NetworkSimulation {
    constructor() {
        this.hosts = [];
        for (let i = 1; i <= 10; i++) {
            this.hosts.push(`192.168.1.${i}`);
        }
        this.trafficLogs = [];
    }

    generateTraffic() {
        const src = this.hosts[Math.floor(Math.random() * this.hosts.length)];
        let dst = this.hosts[Math.floor(Math.random() * this.hosts.length)];
        while (dst === src) {
            dst = this.hosts[Math.floor(Math.random() * this.hosts.length)];
        }
        const trafficTypes = ["normal", "scan", "malware", "ddos"];
        const trafficType = trafficTypes[Math.floor(Math.random() * trafficTypes.length)];
        const logEntry = {
            source_ip: src,
            destination_ip: dst,
            traffic_type: trafficType,
            timestamp: Date.now()
        };
        this.trafficLogs.push(logEntry);
        console.log("Generated traffic:", logEntry);
    }

    startSimulation(durationSeconds = 10, callback) {
        console.log("Starting network simulation...");
        const interval = setInterval(() => {
            this.generateTraffic();
        }, 1000);

        setTimeout(() => {
            clearInterval(interval);
            console.log("Network simulation ended.");
            if (callback) callback();
        }, durationSeconds * 1000);
    }
}

module.exports = NetworkSimulation;

if (require.main === module) {
    const sim = new NetworkSimulation();
    sim.startSimulation(10);
}
