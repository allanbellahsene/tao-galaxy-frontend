import React, { useState, useEffect } from 'react';
import { X, Search } from 'lucide-react';
import GalaxyMap from './GalaxyMap';
import GalaxyControls from './GalaxyControls';
import SubnetDetail from './SubnetDetail';
import { useAppContext } from '../../context/AppContext';
import { CategoryType } from '../../types';

const GalaxyView: React.FC = () => {
  const { 
    zoomLevel, 
    setZoomLevel,
    selectedCategory,
    selectedSubnet,
    showWelcome,
    setShowWelcome
  } = useAppContext();
  
  const [isLoading, setIsLoading] = useState(true);
  const [categories, setCategories] = useState<CategoryType[]>([]);

  useEffect(() => {
    fetch('/subnets_frontend_ready.json')
      .then(res => res.json())
      .then((data: CategoryType[]) => {
        setCategories(data);
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin inline-block w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full mb-4"></div>
          <p className="text-lg">Loading Galaxy Map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-[calc(100vh-64px)] overflow-hidden">
      {/* Search bar */}
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 w-full max-w-md px-4">
        <div className="flex items-center bg-slate-800/90 backdrop-blur-sm rounded-lg px-3 py-2 w-full border border-slate-700/50">
          <Search size={16} className="text-slate-400 mr-2" />
          <input 
            type="search" 
            placeholder="Search subnets, categories..." 
            className="bg-transparent border-none outline-none text-sm w-full"
          />
        </div>
      </div>

      {categories.length > 0 && <GalaxyMap categories={categories} />}
      <GalaxyControls 
        zoomLevel={zoomLevel}
        onZoomIn={() => setZoomLevel(Math.min(zoomLevel + 0.2, 2))}
        onZoomOut={() => setZoomLevel(Math.max(zoomLevel - 0.2, 0.5))}
        onResetZoom={() => setZoomLevel(0.7)}
        onZoomChange={setZoomLevel}
      />
      
      {selectedSubnet && <SubnetDetail />}
      
      {!selectedSubnet && !selectedCategory && showWelcome && (
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-center max-w-md">
          <div className="card p-4 relative">
            <button 
              onClick={() => setShowWelcome(false)}
              className="absolute top-2 right-2 p-1 hover:bg-slate-700/50 rounded-full transition-colors duration-200"
            >
              <X size={16} />
            </button>
            <h3 className="text-lg font-medium mb-2">Welcome to TAO Galaxy</h3>
            <p className="text-slate-300 text-sm">
              Explore the Bittensor ecosystem by navigating through subnet categories. 
              Zoom in to discover more details, or click on nodes to see specifics.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GalaxyView;