import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7777/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const lasApi = {
    // Query the agent system
    query: async (prompt: string, provider?: string, model?: string) => {
        const response = await api.post('query', {
            query: prompt,
            provider,
            model
        });
        return response.data;
    },

    // Get available models for a provider
    getModels: async (provider: string) => {
        const response = await api.get(`models?provider=${provider}`);
        return response.data.models;
    },

    // Get system status (placeholder)
    getStatus: async () => {
        const response = await api.get('status'); // Endpoint to be implemented in backend
        return response.data;
    },

    // Get memory (placeholder)
    getMemory: async (sessionId: string) => {
        const response = await api.get(`memory/${sessionId}`);
        return response.data;
    },

    // Save workflow
    saveWorkflow: async (workflow: any) => {
        const response = await api.post('workflows', workflow);
        return response.data;
    },

    // Get knowledge graph
    getKnowledgeGraph: async () => {
        const response = await api.get('/memory/knowledge-graph');
        return response.data;
    },

    // Authentication methods
    register: async (username: string, email: string, password: string) => {
        const response = await api.post('/v1/auth/register', {
            username,
            email,
            password,
            role: 'user'
        });
        return response.data;
    },

    login: async (username: string, password: string) => {
        const response = await api.post('/v1/auth/login', null, {
            params: { username, password }
        });
        return response.data;
    },

    logout: async (accessToken: string) => {
        const response = await api.post('/v1/auth/logout', null, {
            params: { access_token: accessToken }
        });
        return response.data;
    },

    getCurrentUser: async () => {
        const response = await api.get('/v1/auth/me');
        return response.data;
    },

    refreshToken: async (refreshToken: string) => {
        const response = await api.post('/v1/auth/refresh', null, {
            params: { refresh_token: refreshToken }
        });
        return response.data;
    },
};

// Add request interceptor to inject JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add response interceptor for token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const response = await lasApi.refreshToken(refreshToken);
                    localStorage.setItem('access_token', response.access_token);
                    originalRequest.headers.Authorization = `Bearer ${response.access_token}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed, logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);
