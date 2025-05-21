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
  return (
    <Router>
      <AppProvider>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/app" element={<Layout><GalaxyView /></Layout>} />
          <Route path="/app/news" element={<Layout><NewsView /></Layout>} />
          <Route path="/app/reports" element={<Layout><ReportsView /></Layout>} />
          <Route path="/app/subnet/:id" element={<Layout><SubnetReport /></Layout>} />
        </Routes>
      </AppProvider>
    </Router>
  );
}

export default App;