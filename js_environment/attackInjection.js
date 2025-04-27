// attackInjection.js
// Simulated attack injection module in JavaScript

class AttackInjection {
    constructor(networkSimulation) {
        this.networkSimulation = networkSimulation;
        this.attackTypes = ["brute_force", "phishing", "ransomware", "ddos"];
    }

    injectAttack() {
        const attack = this.attackTypes[Math.floor(Math.random() * this.attackTypes.length)];
        const target = this.networkSimulation.hosts[Math.floor(Math.random() * this.networkSimulation.hosts.length)];
        const attackEvent = {
            attack_type: attack,
            target_ip: target,
            timestamp: Date.now()
        };
        console.log("Injecting attack:", attackEvent);
        this.networkSimulation.trafficLogs.push(attackEvent);
    }

    startAttackInjection(durationSeconds = 10, intervalSeconds = 2, callback) {
        console.log("Starting attack injection...");
        const interval = setInterval(() => {
            this.injectAttack();
        }, intervalSeconds * 1000);

        setTimeout(() => {
            clearInterval(interval);
            console.log("Attack injection ended.");
            if (callback) callback();
        }, durationSeconds * 1000);
    }
}

module.exports = AttackInjection;

if (require.main === module) {
    const NetworkSimulation = require('./networkSimulation');
    const sim = new NetworkSimulation();
    sim.startSimulation(5);
    const injector = new AttackInjection(sim);
    injector.startAttackInjection(5);
}
