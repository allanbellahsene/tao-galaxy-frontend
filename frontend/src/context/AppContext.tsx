import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AppContextType {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  zoomLevel: number;
  setZoomLevel: (level: number) => void;
  selectedCategory: string | null;
  setSelectedCategory: (category: string | null) => void;
  selectedSubnet: string | null;
  setSelectedSubnet: (subnet: string | null) => void;
  showWelcome: boolean;
  setShowWelcome: (show: boolean) => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(0.7); // Set default zoom to 70%
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedSubnet, setSelectedSubnet] = useState<string | null>(null);
  const [showWelcome, setShowWelcome] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const value = {
    sidebarOpen,
    toggleSidebar,
    zoomLevel,
    setZoomLevel,
    selectedCategory,
    setSelectedCategory,
    selectedSubnet,
    setSelectedSubnet,
    showWelcome,
    setShowWelcome,
    searchQuery,
    setSearchQuery,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};