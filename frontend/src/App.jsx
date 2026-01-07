import { useState, useEffect } from 'react';
import { getStats, getLeads, generateLeads, runPipelineStep, resetDb } from './api';

function App() {
  const [stats, setStats] = useState({
    total_leads: 0, enriched: 0, messaged: 0, sent: 0, failed: 0
  });
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pipelineRunning, setPipelineRunning] = useState(false);

  const refreshData = async () => {
    const s = await getStats();
    setStats(s);
    const l = await getLeads();
    setLeads(l);
  };

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    await generateLeads(10);
    await refreshData();
    setLoading(false);
  };

  const handleReset = async () => {
    if (confirm("Are you sure? This will delete all leads.")) {
      await resetDb();
      await refreshData();
    }
  }

  // Client-side simple orchestration for demo (in case n8n is not used)
  const runOrchestrator = async () => {
    setPipelineRunning(true);

    // 1. Get all leads that need processing
    // For specific steps, we iterate.
    // This is a naive client-side runner to demonstrate the "Agent" behavior
    // "Reasoning": Find leads in state NEW -> Enrich. Find Enriched -> Message.

    const allLeads = await getLeads();

    for (const lead of allLeads) {
      if (lead.status === 'NEW') {
        await runPipelineStep(lead.id, 'enrich');
      } else if (lead.status === 'ENRICHED') {
        await runPipelineStep(lead.id, 'message');
      } else if (lead.status === 'MESSAGED') {
        await runPipelineStep(lead.id, 'send');
      }
    }

    await refreshData();
    setPipelineRunning(false);
  };

  return (
    <div className="dashboard">
      <div className="header-actions">
        <div>
          <h1>MCP Lead Gen Pipeline</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Monitoring Agent Actions & Status | Backend: Python/FastAPI | Frontend: React/Vite
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={handleReset} style={{ borderColor: 'var(--danger-color)', color: 'var(--danger-color)' }}>
            Reset DB
          </button>
          <button onClick={handleGenerate} disabled={loading || pipelineRunning}>
            {loading ? 'Generating...' : '+ Generate 10 Leads'}
          </button>
          <button className="primary" onClick={runOrchestrator} disabled={pipelineRunning}>
            {pipelineRunning ? 'Refining Pipeline...' : '▶ Run Agent Pipeline'}
          </button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Leads</div>
          <div className="stat-value">{stats.total_leads}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Enriched</div>
          <div className="stat-value" style={{ color: 'var(--warning-color)' }}>{stats.enriched}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Messaged</div>
          <div className="stat-value" style={{ color: 'var(--accent-color)' }}>{stats.messaged}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Sent</div>
          <div className="stat-value" style={{ color: 'var(--success-color)' }}>{stats.sent}</div>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Company</th>
              <th>Role</th>
              <th>Status</th>
              <th>Enrichment (Persona)</th>
              <th>Last Action</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(lead => (
              <tr key={lead.id}>
                <td style={{ color: 'var(--text-secondary)' }}>#{lead.id}</td>
                <td style={{ fontWeight: 'bold' }}>{lead.full_name}</td>
                <td>{lead.company_name}</td>
                <td>{lead.role}</td>
                <td>
                  <span className={`badge status-${lead.status.toLowerCase()}`}>
                    {lead.status}
                  </span>
                </td>
                <td>{lead.persona_tag || '-'}</td>
                <td style={{ color: 'var(--text-secondary)', fontSize: '0.85em' }}>
                  {lead.logs && lead.logs.length > 0 ?
                    `${lead.logs[lead.logs.length - 1].action} @ ${lead.logs[lead.logs.length - 1].timestamp}`
                    : 'Created'}
                </td>
              </tr>
            ))}
            {leads.length === 0 && (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>
                  No leads found. Click "Generate Leads" to start.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
