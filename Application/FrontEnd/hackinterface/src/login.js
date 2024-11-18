import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './login.css'; // Προαιρετικό CSS αν θέλεις να το διαμορφώσεις περαιτέρω

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate(); // useNavigate hook για redirect

    // Σταθερά username και password
    const localUsername = 'admin';
    const localPassword = 'admin';

    const handleSubmit = (e) => {
        e.preventDefault();
        // Έλεγχος τοπικών διαπιστευτηρίων
        if (email === localUsername && password === localPassword) {
            navigate('/chatbox'); // Redirect στη σελίδα Dashboard
        } else {
            setError('Invalid username or password');
        }
    };

    return (
        <div className="home-container">
            <div className="intro-section text-center mb-5">
                <h1>Welcome to Fire Monitoring Dashboard</h1>
                <p>
                    This application empowers organizations, such as firefighting agencies, to monitor and protect regions at risk using cutting-edge AI technologies.
                    Harness the power of Machine Learning (ML) and Large Language Models (LLM) to predict and analyze critical scenarios in real time.
                </p>
                <p>
                    Enter your credentials below to access the platform and take the first step toward proactive fire prevention and environmental safety!
                </p>
            </div>
            <div className="login-section d-flex justify-content-center align-items-center">
                <div className="login-form-container">
                    <h3 className="text-center">Please Log In</h3>
                    <form onSubmit={handleSubmit} className="mt-4">
                        <div className="form-group">
                            <label htmlFor="email">Username</label>
                            <input
                                type="text"
                                className="form-control"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter username"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                className="form-control"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter password"
                                required
                            />
                        </div>
                        <div className="d-flex justify-content-center">
                            <button type="submit" className="btn btn-primary w-50">
                                Log In
                            </button>
                        </div>
                        {error && <p className="text-danger mt-2 text-center">{error}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
