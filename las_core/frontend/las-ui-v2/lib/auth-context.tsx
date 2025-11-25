"""
Authentication Context Provider for Frontend.
"""

import React, { createContext, useContext, useState, useEffect } from 'react';
import { lasApi } from './api';

interface User {
    id: number;
    username: string;
    email: string;
    role: string;
    is_active: boolean;
    created_at: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (username: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    register: (username: string, email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check if user is logged in on mount
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                // Verify token by fetching user info
                const userData = await lasApi.getCurrentUser();
                setUser(userData);
            }
        } catch (error) {
            // Token invalid or expired
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (username: string, password: string) => {
        try {
            const response = await lasApi.login(username, password);
            localStorage.setItem('access_token', response.access_token);
            localStorage.setItem('refresh_token', response.refresh_token);

            // Fetch user info
            const userData = await lasApi.getCurrentUser();
            setUser(userData);
        } catch (error) {
            throw new Error('Login failed');
        }
    };

    const logout = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                await lasApi.logout(token);
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            setUser(null);
        }
    };

    const register = async (username: string, email: string, password: string) => {
        try {
            await lasApi.register(username, email, password);
            // Auto-login after registration
            await login(username, password);
        } catch (error) {
            throw new Error('Registration failed');
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                login,
                logout,
                register,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
