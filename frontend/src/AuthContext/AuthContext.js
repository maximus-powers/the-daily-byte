// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
    return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('isAuthenticated'));
    const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail') || '');

    const login = (email) => {
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('userEmail', email);
        setIsAuthenticated(true);
        setUserEmail(email);
    }

    const logout = () => {
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('userEmail');
        setIsAuthenticated(false);
        setUserEmail('');
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, userEmail, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}
