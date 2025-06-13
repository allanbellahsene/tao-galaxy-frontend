import React from 'react';
import { BrowserRouter as Router, Routes, Route, useParams, useNavigate } from 'react-router-dom';
import Layout from './components/Layout';
import GalaxyView from './components/GalaxyView';
import NewsView from './components/NewsView';
import ReportsView from './components/ReportsView';
import LandingPage from './components/LandingPage';
import SubnetReport from './components/SubnetReport';
import { AppProvider } from './context/AppContext';

// Wrapper component to extract URL params and pass to SubnetReport
const SubnetReportWrapper: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  // Extract subnet number from URL (e.g., "SN1" -> "1", "SN64" -> "64")
  const subnetId = id?.replace('SN', '') || '64';
  
  const handleBack = () => {
    navigate('/app');
  };
  
  return <SubnetReport subnetId={subnetId} onBack={handleBack} />;
};

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
              <Route path="/app/subnet/:id" element={<Layout><SubnetReportWrapper /></Layout>} />
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