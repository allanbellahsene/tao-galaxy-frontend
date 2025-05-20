import React from 'react';
import { useAppContext } from '../../context/AppContext';
import { SubnetType, Position } from '../../types';

interface SubnetProps {
  subnet: SubnetType;
  position: Position;
  categoryColor: string;
  isVisible: boolean;
  categoryName: string;
}

const Subnet: React.FC<SubnetProps> = ({ subnet, position, categoryColor, isVisible }) => {
  const { setSelectedSubnet, selectedSubnet, zoomLevel } = useAppContext();
  
  // Scale based on market cap - using 130000 as max reference (PTN's market cap)
  const baseSize = 50;
  const maxMarketCap = 130000;
  const scaleFactor = Math.sqrt(subnet.marketCap / maxMarketCap); // Square root for more balanced scaling
  const finalSize = Math.max(25, baseSize * scaleFactor);
  
  const isSelected = selectedSubnet === subnet.id;
  const pulseColor = categoryColor.replace(')', ', 0.4)').replace('rgb', 'rgba');
  
  const handleSubnetClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedSubnet(isSelected ? null : subnet.id);
  };

  // Extract subnet number from ID and format as SN{number}
  const subnetNumber = subnet.id.match(/\d+/)?.[0] || '';
  const subnetId = `SN${subnetNumber}`;

  if (!isVisible) return null;

  return (
    <div
      className={`absolute subnet-node transition-all duration-300 ${isSelected ? 'animate-pulse' : ''}`}
      style={{
        width: `${finalSize}px`,
        height: `${finalSize}px`,
        left: `${position.x - finalSize / 2}px`,
        top: `${position.y - finalSize / 2}px`,
        background: `radial-gradient(circle at 30% 30%, 
          ${categoryColor.replace('rgb', 'rgba').replace(')', ', 0.9)')} 0%,
          ${categoryColor} 45%,
          ${categoryColor.replace('rgb', 'rgba').replace(')', ', 0.6)')} 65%,
          ${pulseColor} 85%,
          transparent 100%
        )`,
        boxShadow: `
          0 0 ${finalSize * 0.3}px ${pulseColor},
          inset 0 0 ${finalSize * 0.15}px rgba(255, 255, 255, 0.2)
        `,
        zIndex: isSelected ? 20 : 15,
        opacity: isSelected ? 1 : 0.9,
      }}
      onClick={handleSubnetClick}
    >
      <div className="absolute inset-0 flex flex-col items-center justify-center text-white">
        {/* Subnet ID - always visible */}
        <div 
          className="font-bold"
          style={{ fontSize: Math.max(12, finalSize * 0.3) }}
        >
          {subnetId}
        </div>
        
        {/* Subnet name - only visible when zoomed in */}
        {zoomLevel > 1.2 && (
          <div 
            className="text-xs opacity-80 mt-1"
            style={{ fontSize: Math.max(10, finalSize * 0.2) }}
          >
            {subnet.name}
          </div>
        )}
      </div>
    </div>
  );
};

export default Subnet;