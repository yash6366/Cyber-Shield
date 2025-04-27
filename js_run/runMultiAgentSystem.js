// runMultiAgentSystem.js
// Main script to run the multi-agent system in JavaScript

const HunterAgent = require('../js_agents/hunterAgent');
const ClassifierAgent = require('../js_agents/classifierAgent');
const ResponseAgent = require('../js_agents/responseAgent');
const NetworkSimulation = require('../js_environment/networkSimulation');
const AttackInjection = require('../js_environment/attackInjection');
const DataCollector = require('../js_environment/dataCollector');

async function runSystem() {
    console.log("Starting Multi-Agent Cyber Defense System...");

    const networkSim = new NetworkSimulation();
    const attackInjector = new AttackInjection(networkSim);
    const dataCollector = new DataCollector(networkSim);

    const hunterAgent = new HunterAgent();
    const classifierAgent = new ClassifierAgent();
    const responseAgent = new ResponseAgent();

    // Await training completion
    await Promise.all([
        hunterAgent.train(),
        classifierAgent.train(),
        responseAgent.train()
    ]);

    // Await simulation and attack injection completion
    await Promise.all([
        new Promise(resolve => networkSim.startSimulation(10, resolve)),
        new Promise(resolve => attackInjector.startAttackInjection(10, 2, resolve))
    ]);

    console.log("Simulating threat detection and response...");
    for (const log of networkSim.trafficLogs) {
        const threatDetected = await hunterAgent.detectThreat(log);
        if (threatDetected) {
            const classification = await classifierAgent.classify("Suspicious traffic detected");
            await responseAgent.executeResponse(`Responding to ${classification}`);
        }
    }

    dataCollector.collectTrafficLogs();
    dataCollector.collectAttackEvents();

    console.log("Multi-Agent System run complete.");
}

runSystem();
