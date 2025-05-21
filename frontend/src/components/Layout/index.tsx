import React from 'react';
import { useLocation } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import { useAppContext } from '../../context/AppContext';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { sidebarOpen } = useAppContext();
  const location = useLocation();
  const showSidebar = location.pathname === '/app';

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        {showSidebar && <Sidebar />}
        <main className={`flex-1 transition-all duration-300 ${showSidebar && sidebarOpen ? 'md:ml-64' : 'ml-0'}`}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;