import React from 'react';
import ThreatDashboard from './components/ThreatDashboard';
import AgentInteractionPanel from './components/AgentInteractionPanel';
import AttackSimulationWorkspace from './components/AttackSimulationWorkspace';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ backgroundColor: '#222', color: 'white', padding: '10px', textAlign: 'center' }}>
        <h1>CyberShield - Autonomous Defense System</h1>
      </header>
      <main style={{ display: 'flex', flex: 1, gap: '10px', padding: '10px', backgroundColor: '#f0f2f5' }}>
        <section style={{ flex: 1, backgroundColor: 'white', borderRadius: '8px', padding: '10px', overflowY: 'auto' }}>
          <ThreatDashboard />
        </section>
        <section style={{ flex: 1, backgroundColor: 'white', borderRadius: '8px', padding: '10px', overflowY: 'auto' }}>
          <AgentInteractionPanel />
        </section>
        <section style={{ flex: 1, backgroundColor: 'white', borderRadius: '8px', padding: '10px', overflowY: 'auto' }}>
          <AttackSimulationWorkspace />
        </section>
      </main>
    </div>
  );
}

export default App;
