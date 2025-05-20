import React, { useRef, useEffect, useState } from 'react';
import { useAppContext } from '../../context/AppContext';
import Subnet from './Subnet';
import { CategoryType } from '../../types';
import { getCategoryColor } from '../../utils/colors';

interface GalaxyMapProps {
  categories: CategoryType[];
}

const GalaxyMap: React.FC<GalaxyMapProps> = ({ categories }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const { 
    zoomLevel, 
    setZoomLevel,
    selectedCategory,
    setSelectedCategory, 
    selectedSubnet,
    setSelectedSubnet
  } = useAppContext();
  
  const [mapDimensions, setMapDimensions] = useState({ width: 0, height: 0 });
  const [centerPosition, setCenterPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [mapOffset, setMapOffset] = useState({ x: 0, y: 0 });
  const [hoveredCategory, setHoveredCategory] = useState<string | null>(null);

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const { width, height } = containerRef.current.getBoundingClientRect();
        setMapDimensions({ width, height });
        setCenterPosition({ x: width / 2, y: height / 2 });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    const dx = (e.clientX - dragStart.x) * 0.5;
    const dy = (e.clientY - dragStart.y) * 0.5;
    setMapOffset(prev => ({ x: prev.x + dx, y: prev.y + dy }));
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const delta = -e.deltaY * 0.001;
    const newZoom = Math.min(Math.max(zoomLevel + delta, 0.5), 3);
    setZoomLevel(newZoom);
    
    const rect = containerRef.current?.getBoundingClientRect();
    if (rect) {
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      
      const dx = (mouseX - rect.width / 2) * delta * 0.5;
      const dy = (mouseY - rect.height / 2) * delta * 0.5;
      
      setMapOffset(prev => ({
        x: prev.x - dx,
        y: prev.y - dy
      }));
    }
  };

  const handleBackgroundClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      setSelectedCategory(null);
      setSelectedSubnet(null);
    }
  };

  const getCategoryRingSize = (category: CategoryType) => {
    const baseSize = mapDimensions.width * 0.15;
    const maxSubnets = Math.max(...categories.map(c => c.subnets.length));
    const subnetCount = category.subnets.length;
    const marketCapFactor = Math.sqrt(category.marketCapTotal / 130000);
    
    const size = baseSize * (1 + (subnetCount / maxSubnets) * 0.5) * marketCapFactor;
    return Math.max(size, baseSize);
  };

  const getCategoryCenter = (categoryIndex: number) => {
    const angle = (categoryIndex / categories.length) * Math.PI * 2;
    const distance = mapDimensions.width * 0.25;
    return {
      x: centerPosition.x + Math.cos(angle) * distance,
      y: centerPosition.y + Math.sin(angle) * distance
    };
  };

  const getSubnetPosition = (categoryIndex: number, subnetIndex: number, totalSubnets: number, ringSize: number) => {
    const center = getCategoryCenter(categoryIndex);
    const maxRadius = ringSize * 0.4;
    
    const a = 2;
    const b = maxRadius / (2 * Math.PI);
    
    const angle = subnetIndex * (2 * Math.PI) / a;
    const radius = Math.min(b * angle, maxRadius);
    
    return {
      x: center.x + radius * Math.cos(angle),
      y: center.y + radius * Math.sin(angle)
    };
  };

  return (
    <div 
      ref={containerRef}
      className="galaxy-container w-full h-full overflow-hidden cursor-move relative"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      onClick={handleBackgroundClick}
    >
      {/* Legend */}
      <div className="absolute top-4 left-4 bg-slate-800/90 backdrop-blur-sm rounded-lg border border-slate-700/50 p-4 z-20">
        <div className="text-sm font-medium mb-3">Categories</div>
        <div className="grid gap-2">
          {categories.map((category) => (
            <div 
              key={category.id} 
              className="flex items-center gap-2 cursor-pointer transition-all duration-200 hover:bg-slate-700/30 px-2 py-1 rounded-lg"
              onMouseEnter={() => setHoveredCategory(category.id)}
              onMouseLeave={() => setHoveredCategory(null)}
            >
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: getCategoryColor(category.id) }}
              />
              <span className="text-sm text-slate-300">{category.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div 
        className="transform transition-transform duration-300 ease-out h-full w-full"
        style={{ 
          transform: `scale(${zoomLevel}) translate(${mapOffset.x}px, ${mapOffset.y}px)`,
        }}
      >
        {/* Category rings and subnets */}
        {categories.map((category, categoryIndex) => {
          const center = getCategoryCenter(categoryIndex);
          const ringSize = getCategoryRingSize(category);
          const color = getCategoryColor(category.id);
          const isSelected = selectedCategory === category.id;
          const isHovered = hoveredCategory === category.id;
          
          return (
            <div key={`ring-${category.id}`} className="absolute">
              {/* Category ring */}
              <div
                className={`absolute rounded-full transition-all duration-300 ${isHovered ? 'scale-105' : ''}`}
                style={{
                  width: `${ringSize}px`,
                  height: `${ringSize}px`,
                  left: `${center.x - ringSize/2}px`,
                  top: `${center.y - ringSize/2}px`,
                  border: `4px solid ${color.replace('rgb', 'rgba').replace(')', isHovered ? ', 0.8)' : ', 0.4)')}`,
                  boxShadow: `
                    0 0 ${ringSize * (isHovered ? 0.2 : 0.1)}px ${color.replace('rgb', 'rgba').replace(')', isHovered ? ', 0.4)' : ', 0.2)')},
                    inset 0 0 ${ringSize * 0.05}px ${color.replace('rgb', 'rgba').replace(')', ', 0.1)')}
                  `,
                  backgroundColor: color.replace('rgb', 'rgba').replace(')', isHovered ? ', 0.15)' : ', 0.05)'),
                  zIndex: isSelected || isHovered ? 15 : 5,
                  opacity: hoveredCategory && !isHovered ? 0.3 : 1,
                  filter: isHovered ? 'brightness(1.2)' : 'none',
                }}
              >
                {/* Category name */}
                {zoomLevel > 0.8 && (
                  <div 
                    className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-8 text-center"
                  >
                    <span 
                      className="px-3 py-1 rounded-full text-sm font-medium"
                      style={{
                        backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.2)'),
                        color: color.replace('rgb', 'rgba').replace(')', ', 0.9)')
                      }}
                    >
                      {category.name}
                    </span>
                  </div>
                )}
              </div>
              
              {/* Subnets within category */}
              {category.subnets.map((subnet, subnetIndex) => {
                const position = getSubnetPosition(
                  categoryIndex,
                  subnetIndex,
                  category.subnets.length,
                  ringSize
                );
                
                return (
                  <Subnet
                    key={subnet.id}
                    subnet={subnet}
                    position={position}
                    categoryColor={color}
                    isVisible={true}
                    categoryName={category.name}
                  />
                );
              })}
            </div>
          );
        })}
        
        {/* Background stars */}
        {Array.from({ length: 100 }).map((_, index) => {
          const size = Math.random() * 2 + 1;
          const opacity = Math.random() * 0.7 + 0.3;
          const x = Math.random() * mapDimensions.width;
          const y = Math.random() * mapDimensions.height;
          
          return (
            <div 
              key={`star-${index}`}
              className="absolute rounded-full bg-white"
              style={{
                width: `${size}px`,
                height: `${size}px`,
                left: `${x}px`,
                top: `${y}px`,
                opacity,
              }}
            />
          );
        })}
      </div>
    </div>
  );
};

export default GalaxyMap;