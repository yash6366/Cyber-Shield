import axios from 'axios';
import config from '../config';

const api = axios.create({
    baseURL: config.apiUrl,
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': config.apiKey
    }
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Server responded with error status
            switch (error.response.status) {
                case 401:
                    console.error('Authentication failed. Please check your API key.');
                    break;
                case 429:
                    console.error('Rate limit exceeded. Please try again later.');
                    break;
                default:
                    console.error(`API Error: ${error.response.data.error || 'Unknown error'}`);
            }
        } else if (error.request) {
            // Request made but no response received
            console.error('No response received from server. Please check your connection.');
        } else {
            // Error in request configuration
            console.error('Error in request:', error.message);
        }
        return Promise.reject(error);
    }
);

export const healthCheck = () => api.get('/health');
export const detectThreat = (features) => api.post('/hunter/detect', { features });
export const classifyThreat = (description) => api.post('/classifier/classify', { threat_description: description });
export const executeResponse = (action) => api.post('/response/execute', { action });

export default api;