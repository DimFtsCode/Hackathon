import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const Header = () => {
    const navigate = useNavigate();

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                {/* ChatBox - Τέρμα Αριστερά */}
                <a
                    className="navbar-brand"
                    onClick={() => navigate('/chatbot')}
                    style={{ cursor: 'pointer', fontWeight: 'normal' }}
                >
                    ChatBot
                </a>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse justify-content-between" id="navbarNav">
                    {/* Κεντραρισμένα Στοιχεία */}
                    <ul className="navbar-nav mx-auto">
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => navigate('/demo')}
                                style={{ cursor: 'pointer', fontWeight: 'normal' }}
                            >
                                Fire Monitor Demo
                            </a>
                        </li>
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => navigate('/live')}
                                style={{ cursor: 'pointer', fontWeight: 'normal' }}
                            >
                                Fire Monitor Live
                            </a>
                        </li>
                    </ul>
                    {/* Help και Log Out - Τέρμα Δεξιά */}
                    <ul className="navbar-nav">
                        <li className="nav-item me-3">
                            <a
                                className="nav-link"
                                onClick={() => navigate('/help')}
                                style={{ cursor: 'pointer', fontWeight: 'normal' }}
                            >
                                Help
                            </a>
                        </li>
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => navigate('/login')} // Ανακατεύθυνση στο Login Page
                                style={{ cursor: 'pointer', fontWeight: 'bold' }}
                            >
                                Log Out
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Header;
