const config = {
    apiUrl: process.env.VERCEL_API_URL || 'http://localhost:5000/api',
    environment: process.env.NODE_ENV || 'development'
};

export default config;