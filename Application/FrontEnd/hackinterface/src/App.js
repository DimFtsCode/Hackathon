import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import WeatherList from './Weather';  // Σωστό path για το component

function App() {
  return (
    <Router>
      <div>
        <Routes>
          {/* Ανακατεύθυνση από τη ρίζα ("/") στο "/weather" */}
          <Route path="/" element={<Navigate to="/weather" replace />} />
          <Route path="/weather" element={<WeatherList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
