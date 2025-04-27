// dataCollector.js
// Simulated data collection module in JavaScript

class DataCollector {
    constructor(networkSimulation) {
        this.networkSimulation = networkSimulation;
    }

    collectTrafficLogs() {
        console.log("Collecting traffic logs...");
        this.networkSimulation.trafficLogs.forEach(log => {
            console.log(log);
        });
    }

    collectAttackEvents() {
        console.log("Collecting attack events...");
        const attackEvents = this.networkSimulation.trafficLogs.filter(log => log.attack_type !== undefined);
        attackEvents.forEach(event => {
            console.log(event);
        });
    }
}

module.exports = DataCollector;

if (require.main === module) {
    const NetworkSimulation = require('./networkSimulation');
    const AttackInjection = require('./attackInjection');
    const sim = new NetworkSimulation();
    sim.startSimulation(3, () => {
        const injector = new AttackInjection(sim);
        injector.startAttackInjection(3, 1, () => {
            const collector = new DataCollector(sim);
            collector.collectTrafficLogs();
            collector.collectAttackEvents();
        });
    });
}
