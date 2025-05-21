import React from 'react';
import { useAppContext } from '../../context/AppContext';
import Subnet from './Subnet';
import { CategoryType, Position } from '../../types';
import { getCategoryColor } from '../../utils/colors';

interface CategoryProps {
  category: CategoryType;
  position: Position;
  isExpanded: boolean;
  allCategories: CategoryType[];
  packedSubnets?: any[]; // D3 packed children
  radius?: number; // D3 packed radius
}

const Category: React.FC<CategoryProps> = ({ category, position, isExpanded, allCategories, packedSubnets, radius }) => {
  const { setSelectedCategory, zoomLevel, selectedSubnet } = useAppContext();
  
  // Dynamically calculate the max market cap from all subnets in all categories
  const allSubnets = allCategories.flatMap(cat => cat.subnets);
  const maxMarketCap = Math.max(...allSubnets.map(subnet => subnet.marketCap || 0), 1); // avoid division by zero
  const baseSubnetSize = 50; // Base size for subnets
  const padding = 10; // Padding between subnets
  
  // Calculate the total diameter of all subnets
  const totalDiameter = category.subnets.reduce((total, subnet) => {
    const scaleFactor = Math.sqrt(subnet.marketCap / maxMarketCap);
    const subnetDiameter = Math.max(25, baseSubnetSize * scaleFactor);
    return total + subnetDiameter;
  }, 0);
  
  // Ring diameter should be slightly larger than the total diameter of all subnets
  // Adding padding for each subnet and a base padding
  const ringDiameter = totalDiameter + (padding * (category.subnets.length + 1));
  
  // If packedSubnets is provided, use D3 layout
  if (packedSubnets && radius) {
    const color = getCategoryColor(category.id);
    const glowColor = color.replace(')', ', 0.3)').replace('rgb', 'rgba');
    const handleCategoryClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      setSelectedCategory(isExpanded ? null : category.id);
    };
    return (
      <div
        className={`absolute category-node rounded-full transition-all duration-500 overflow-hidden ${isExpanded ? 'animate-glow' : ''}`}
        style={{
          width: `${radius * 2}px`,
          height: `${radius * 2}px`,
          left: `${position.x - radius}px`,
          top: `${position.y - radius}px`,
          background: `radial-gradient(circle at 30% 30%, 
            ${color.replace('rgb', 'rgba').replace(')', ', 0.9)')} 0%,
            ${color} 45%,
            ${color.replace('rgb', 'rgba').replace(')', ', 0.6)')} 65%,
            ${glowColor} 85%,
            transparent 100%
          )`,
          boxShadow: `
            0 0 ${radius * 0.3}px ${glowColor},
            inset 0 0 ${radius * 0.15}px rgba(255, 255, 255, 0.2)
          `,
          zIndex: isExpanded ? 10 : 5,
          opacity: selectedSubnet ? 0.8 : 1,
        }}
        onClick={handleCategoryClick}
      >
        {/* Category name */}
        {zoomLevel > 0.8 && (
          <div 
            className="absolute inset-0 flex items-center justify-center text-white font-medium"
            style={{ fontSize: Math.min(18, radius * 0.1) }}
          >
            {category.name}
          </div>
        )}
        {/* Subnets container - D3 packed */}
        <div className="absolute inset-0 rounded-full overflow-hidden">
          {packedSubnets.map((subnetNode: any) => (
            <Subnet
              key={subnetNode.data.id}
              subnet={subnetNode.data}
              position={{ x: subnetNode.x, y: subnetNode.y }}
              categoryColor={color}
              isVisible={true}
              categoryName={category.name}
              packedRadius={subnetNode.r}
            />
          ))}
        </div>
      </div>
    );
  }

  const color = getCategoryColor(category.id);
  const glowColor = color.replace(')', ', 0.3)').replace('rgb', 'rgba');
  
  const handleCategoryClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedCategory(isExpanded ? null : category.id);
  };

  // Calculate subnet positions in a circular layout
  const getSubnetPosition = (index: number) => {
    const subnet = category.subnets[index];
    const scaleFactor = Math.sqrt(subnet.marketCap / maxMarketCap);
    const subnetDiameter = Math.max(25, baseSubnetSize * scaleFactor);
    
    // Calculate position in a circle
    const angleStep = (2 * Math.PI) / category.subnets.length;
    const angle = index * angleStep;
    
    // Position subnets at 70% of the ring's radius to ensure they stay within bounds
    const radius = (ringDiameter * 0.35) - (subnetDiameter / 2);
    
    return {
      x: position.x + (Math.cos(angle) * radius),
      y: position.y + (Math.sin(angle) * radius)
    };
  };

  return (
    <div
      className={`absolute category-node rounded-full transition-all duration-500 overflow-hidden ${isExpanded ? 'animate-glow' : ''}`}
      style={{
        width: `${ringDiameter}px`,
        height: `${ringDiameter}px`,
        left: `${position.x - ringDiameter / 2}px`,
        top: `${position.y - ringDiameter / 2}px`,
        background: `radial-gradient(circle at 30% 30%, 
          ${color.replace('rgb', 'rgba').replace(')', ', 0.9)')} 0%,
          ${color} 45%,
          ${color.replace('rgb', 'rgba').replace(')', ', 0.6)')} 65%,
          ${glowColor} 85%,
          transparent 100%
        )`,
        boxShadow: `
          0 0 ${ringDiameter * 0.3}px ${glowColor},
          inset 0 0 ${ringDiameter * 0.15}px rgba(255, 255, 255, 0.2)
        `,
        zIndex: isExpanded ? 10 : 5,
        opacity: selectedSubnet ? 0.8 : 1,
      }}
      onClick={handleCategoryClick}
    >
      {/* Category name */}
      {zoomLevel > 0.8 && (
        <div 
          className="absolute inset-0 flex items-center justify-center text-white font-medium"
          style={{ fontSize: Math.min(18, ringDiameter * 0.1) }}
        >
          {category.name}
        </div>
      )}
      
      {/* Subnets container */}
      <div className="absolute inset-0 rounded-full overflow-hidden">
        {category.subnets.map((subnet, index) => (
          <Subnet
            key={subnet.id}
            subnet={subnet}
            position={getSubnetPosition(index)}
            categoryColor={color}
            isVisible={true}
            categoryName={category.name}
          />
        ))}
      </div>
    </div>
  );
};

export default Category;