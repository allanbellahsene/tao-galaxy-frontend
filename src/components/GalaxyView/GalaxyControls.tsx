import React from 'react';
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';

interface GalaxyControlsProps {
  zoomLevel: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetZoom: () => void;
  onZoomChange: (value: number) => void;
}

const GalaxyControls: React.FC<GalaxyControlsProps> = ({
  zoomLevel,
  onZoomIn,
  onZoomOut,
  onResetZoom,
  onZoomChange
}) => {
  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    onZoomChange(value);
  };

  return (
    <div className="absolute bottom-8 right-8 flex flex-col items-center gap-2 bg-slate-800/80 backdrop-blur-sm rounded-lg border border-slate-700/50 shadow-lg p-2">
      <button 
        className="p-1.5 hover:bg-indigo-600/30 rounded-md transition-colors duration-200"
        onClick={onZoomIn}
        disabled={zoomLevel >= 2}
      >
        <ZoomIn size={16} className={zoomLevel >= 2 ? 'opacity-50' : ''} />
      </button>
      
      <div className="relative flex items-center">
        <input
          type="range"
          min="0.5"
          max="2"
          step="0.1"
          value={zoomLevel}
          onChange={handleSliderChange}
          className="h-24 w-1 bg-slate-600 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-indigo-500 [&::-webkit-slider-thumb]:hover:bg-indigo-400 [&::-webkit-slider-thumb]:transition-colors [&::-moz-range-thumb]:w-3 [&::-moz-range-thumb]:h-3 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-indigo-500 [&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:hover:bg-indigo-400 [&::-moz-range-thumb]:transition-colors [-webkit-appearance:slider-vertical] [writing-mode:bt-lr]"
        />
        <span className="absolute -left-7 top-1/2 -translate-y-1/2 text-xs font-medium min-w-[3ch] text-right">
          {Math.round(zoomLevel * 100)}%
        </span>
      </div>
      
      <button 
        className="p-1.5 hover:bg-indigo-600/30 rounded-md transition-colors duration-200"
        onClick={onZoomOut}
        disabled={zoomLevel <= 0.5}
      >
        <ZoomOut size={16} className={zoomLevel <= 0.5 ? 'opacity-50' : ''} />
      </button>
      
      <button 
        className="p-1.5 hover:bg-indigo-600/30 rounded-md transition-colors duration-200"
        onClick={onResetZoom}
      >
        <Maximize2 size={16} />
      </button>
    </div>
  );
};

export default GalaxyControls;