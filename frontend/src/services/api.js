import axios from 'axios';
import config from '../config';

const api = axios.create({
    baseURL: config.apiUrl,
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': config.apiKey
    }
});

export const healthCheck = () => api.get('/health');
export const detectThreat = (features) => api.post('/hunter/detect', { features });
export const classifyThreat = (description) => api.post('/classifier/classify', { threat_description: description });
export const executeResponse = (action) => api.post('/response/execute', { action });

export default api;