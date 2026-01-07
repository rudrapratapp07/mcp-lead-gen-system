import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const getStats = async () => {
    const res = await axios.get(`${API_BASE}/tools/get_stats`);
    return res.data;
};

export const getLeads = async () => {
    const res = await axios.get(`${API_BASE}/api/leads`);
    return res.data;
};

export const generateLeads = async (count = 10) => {
    const res = await axios.post(`${API_BASE}/tools/generate_leads`, { count });
    return res.data;
};

// Orchestrator Simulation (Client-side loop for demo purposes)
export const runPipelineStep = async (leadId, step) => {
    if (step === 'enrich') {
        return axios.post(`${API_BASE}/tools/enrich_lead`, { lead_id: leadId });
    }
    if (step === 'message') {
        return axios.post(`${API_BASE}/tools/generate_messages`, { lead_id: leadId });
    }
    if (step === 'send') {
        return axios.post(`${API_BASE}/tools/send_message`, { lead_id: leadId, mode: 'live' });
    }
};

export const resetDb = async () => {
    return axios.post(`${API_BASE}/api/reset`);
}
