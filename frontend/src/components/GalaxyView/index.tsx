import React, { useState, useEffect } from 'react';
import { X, Search, ArrowRight, ArrowLeft } from 'lucide-react';
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
  const [welcomeStep, setWelcomeStep] = useState(0);

  useEffect(() => {
    fetch('/subnets_frontend_ready.json')
      .then(res => res.json())
      .then((data: CategoryType[]) => {
        setCategories(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error('GalaxyView: Error loading data:', err);
        setIsLoading(false);
      });
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
      
      {selectedSubnet && <SubnetDetail categories={categories} />}
      
      {!selectedSubnet && !selectedCategory && showWelcome && (
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-center max-w-xs">
          <div className="bg-slate-800/60 rounded-lg border border-slate-700/40 shadow px-3 py-2 text-xs flex flex-col items-center relative min-w-[220px]">
            <button 
              onClick={() => setShowWelcome(false)}
              className="absolute top-1 right-1 p-1 hover:bg-slate-700/40 rounded-full transition-colors duration-200 text-slate-400"
              aria-label="Close welcome message"
            >
              <X size={12} />
            </button>
            <h3 className="text-base font-semibold mb-1 text-slate-100">Welcome to TAO Galaxy</h3>
            <div className="flex items-center justify-center gap-2 w-full">
              {welcomeStep === 1 && (
                <button onClick={() => setWelcomeStep(0)} className="p-1 rounded hover:bg-slate-700/40 transition-colors text-slate-400" aria-label="Previous">
                  <ArrowLeft size={14} />
                </button>
              )}
              <p className="text-slate-300 text-xs leading-snug flex-1 text-center">
                {welcomeStep === 0
                  ? 'Explore the Bittensor ecosystem by navigating through subnets.'
                  : 'Zoom in to discover more details, or click on nodes to see specifics.'}
                <span className="ml-2 text-[10px] text-slate-400 align-middle">{welcomeStep + 1}/2</span>
              </p>
              {welcomeStep === 0 && (
                <button onClick={() => setWelcomeStep(1)} className="p-1 rounded hover:bg-slate-700/40 transition-colors text-slate-400" aria-label="Next">
                  <ArrowRight size={14} />
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GalaxyView;