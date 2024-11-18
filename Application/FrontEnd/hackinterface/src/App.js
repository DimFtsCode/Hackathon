import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './login'; // Import του component login (Home)
import Dashboard from './chatbox'; // Το αρχικό component
import Header from './header'; // Import του Header component
import Demo from './demo'; // Νέο Demo Component
import Live from './live'; // Νέο Live Component
import Help from './help'; // Νέο Help Component

// Layout Component
const MainLayout = ({ children }) => {
    return (
        <>
            <Header /> {/* Header που εμφανίζεται μόνο στις σελίδες που το απαιτούν */}
            <div>{children}</div> {/* Περιεχόμενο της σελίδας */}
        </>
    );
};

function App() {
    return (
        <Router>
            <Routes>
                {/* Redirect to Login */}
                <Route path="/" element={<Navigate to="/login" replace />} />

                {/* Login Page (χωρίς Header) */}
                <Route path="/login" element={<Login />} />

                {/* Protected Routes with Header */}
                <Route
                    path="/chatbox"
                    element={
                        <MainLayout>
                            <Dashboard />
                        </MainLayout>
                    }
                />
                <Route
                    path="/demo"
                    element={
                        <MainLayout>
                            <Demo />
                        </MainLayout>
                    }
                />
                <Route
                    path="/live"
                    element={
                        <MainLayout>
                            <Live />
                        </MainLayout>
                    }
                />
                <Route
                    path="/help"
                    element={
                        <MainLayout>
                            <Help />
                        </MainLayout>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
