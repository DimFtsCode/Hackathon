import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import logo from './images/logo.jpg'; // Προσαρμοσμένη διαδρομή για το logo

const Header = () => {
    const navigate = useNavigate();

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <img 
                src={logo} 
                alt="FlameShield Logo" 
                style={{
                    height: '50px',            // Ύψος
                    width: 'auto',             // Πλάτος (προσαρμόζεται αναλογικά με το ύψος)
                    marginRight: '10px',       // Περιθώριο δεξιά
                    marginLeft: '10px',
                    borderRadius: '10px',      // Στρογγυλεμένες γωνίες
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', // Σκιά για να ξεχωρίζει
                    objectFit: 'cover',        // Προσαρμογή της εικόνας αν δεν έχει σωστές διαστάσεις
                    border: '2px solid #ccc'   // Γραμμή περιγράμματος γύρω από την εικόνα
                }} 
            />
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
                    {/* Στοιχεία Navbar */}
                    <ul className="navbar-nav">
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
                    {/* Log Out - Τέρμα Δεξιά */}
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
