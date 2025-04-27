const config = {
    apiUrl: process.env.VERCEL_API_URL || 'http://localhost:5000/api',
    apiKey: process.env.REACT_APP_API_KEY,
    environment: process.env.NODE_ENV || 'development'
};

export default config;