import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import GalaxyView from './components/GalaxyView';
import NewsView from './components/NewsView';
import ReportsView from './components/ReportsView';
import LandingPage from './components/LandingPage';
import SubnetReport from './components/SubnetReport';
import { AppProvider } from './context/AppContext';

function App() {
  // Check if we're in development mode (localhost indicates development)
  const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  
  return (
    <Router>
      <AppProvider>
        <Routes>
          {/* Landing page - always available */}
          <Route path="/" element={<LandingPage />} />
          
          {/* Full app routes - only in development */}
          {isDevelopment && (
            <>
              <Route path="/app" element={<Layout><GalaxyView /></Layout>} />
              <Route path="/app/news" element={<Layout><NewsView /></Layout>} />
              <Route path="/app/reports" element={<Layout><ReportsView /></Layout>} />
              <Route path="/app/subnet/:id" element={<Layout><SubnetReport /></Layout>} />
            </>
          )}
          
          {/* Catch-all route for production - redirect to landing page */}
          {!isDevelopment && <Route path="*" element={<LandingPage />} />}
        </Routes>
      </AppProvider>
    </Router>
  );
}

export default App;