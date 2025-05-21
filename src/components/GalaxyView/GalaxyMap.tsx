import React, { useRef, useEffect, useState } from 'react';
import { useAppContext } from '../../context/AppContext';
import Subnet from './Subnet';
import { CategoryType } from '../../types';
import { getCategoryColor } from '../../utils/colors';
import Category from './Category';
import * as d3 from 'd3';
import { X } from 'lucide-react';

interface GalaxyMapProps {
  categories: CategoryType[];
}

// Helper for random star positions
const generateStars = (count: number, width: number, height: number) => {
  return Array.from({ length: count }).map(() => ({
    x: Math.random() * width,
    y: Math.random() * height,
    size: Math.random() * 1.8 + 0.7,
    opacity: Math.random() * 0.7 + 0.3,
    twinkle: Math.random() > 0.7
  }));
};

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
  // D3 circle packing layout
  const [packedData, setPackedData] = useState<any>(null);
  const [starfield, setStarfield] = useState<any[]>([]);
  const [nebulae, setNebulae] = useState<any[]>([]);
  const [legendVisible, setLegendVisible] = useState(true);

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

  useEffect(() => {
    if (mapDimensions.width === 0 || mapDimensions.height === 0) return;
    // Build correct D3 hierarchy: root -> categories -> subnets (with value)
    const d3Data = {
      name: 'root',
      children: categories.map(cat => ({
        ...cat,
        children: cat.subnets.map(subnet => ({
          ...subnet,
          value: subnet.marketCap || 1
        }))
      }))
    };
    const root = d3.hierarchy(d3Data)
      .sum((d: any) => d.value)
      .sort((a, b) => (b.value || 0) - (a.value || 0));
    const pack = d3.pack()
      .size([mapDimensions.width, mapDimensions.height])
      .padding(8);
    setPackedData(pack(root));
  }, [categories, mapDimensions]);

  useEffect(() => {
    if (mapDimensions.width && mapDimensions.height) {
      setStarfield(generateStars(180, mapDimensions.width, mapDimensions.height));
      // Generate 2-3 nebulae (radial gradients)
      setNebulae([
        {
          x: mapDimensions.width * 0.25,
          y: mapDimensions.height * 0.3,
          r: 320,
          color: 'rgba(99,102,241,0.18)'
        },
        {
          x: mapDimensions.width * 0.7,
          y: mapDimensions.height * 0.7,
          r: 260,
          color: 'rgba(168,85,247,0.13)'
        },
        {
          x: mapDimensions.width * 0.55,
          y: mapDimensions.height * 0.18,
          r: 180,
          color: 'rgba(14,165,233,0.10)'
        }
      ]);
    }
  }, [mapDimensions]);

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
    // Set a specific max size in pixels
    const maxAllowedSize = 320; // px, adjust as needed
    const minAllowedSize = 80; // px, for visibility
    const maxMarketCapTotal = Math.max(...categories.map(c => c.marketCapTotal), 1);
    // Linear scaling based on market cap
    let size = (category.marketCapTotal / maxMarketCapTotal) * maxAllowedSize;
    size = Math.max(size, minAllowedSize);
    size = Math.min(size, maxAllowedSize);
    return size;
  };

  const getCategoryCenter = (categoryIndex: number) => {
    // Use a larger ellipse and more offset for even more space
    const angle = (categoryIndex / categories.length) * Math.PI * 2;
    const xRadius = mapDimensions.width * 0.45; // much wider
    const yRadius = mapDimensions.height * 0.38; // much taller
    // Offset center further up and left
    const offsetX = centerPosition.x - mapDimensions.width * 0.15;
    const offsetY = centerPosition.y - mapDimensions.height * 0.12;
    return {
      x: offsetX + Math.cos(angle) * xRadius,
      y: offsetY + Math.sin(angle) * yRadius
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

  // Compute top N subnets globally for gradual reveal
  let topGlobalSubnetIds: string[] = [];
  if (packedData && packedData.descendants) {
    // Get all leaf nodes (subnets)
    const allSubnetNodes = packedData.leaves();
    // Sort by marketCap descending
    const sorted = [...allSubnetNodes].sort((a, b) => (b.data.marketCap || 0) - (a.data.marketCap || 0));
    let showCount = 5;
    if (zoomLevel >= 1.05 && zoomLevel < 1.1) showCount = 10;
    else if (zoomLevel >= 1.1 && zoomLevel < 1.5) showCount = 15;
    else if (zoomLevel >= 1.5 && zoomLevel < 1.7) showCount = 20;
    else if (zoomLevel >= 1.7) showCount = sorted.length;
    topGlobalSubnetIds = sorted.slice(0, showCount).map(n => n.data.id);
  }

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
      {/* Animated starfield background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        {/* Nebulae */}
        {nebulae.map((neb, i) => (
          <svg key={i} className="absolute" style={{ left: 0, top: 0, width: '100%', height: '100%' }}>
            <defs>
              <radialGradient id={`nebula-${i}`} cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor={neb.color} stopOpacity="1" />
                <stop offset="100%" stopColor={neb.color} stopOpacity="0" />
              </radialGradient>
            </defs>
            <circle cx={neb.x} cy={neb.y} r={neb.r} fill={`url(#nebula-${i})`} />
          </svg>
        ))}
        {/* Stars */}
        {starfield.map((star, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              width: `${star.size}px`,
              height: `${star.size}px`,
              left: `${star.x}px`,
              top: `${star.y}px`,
              opacity: star.opacity,
              filter: star.twinkle ? 'blur(0.5px) drop-shadow(0 0 2px #fff)' : 'none',
              animation: star.twinkle ? `twinkle 2.5s infinite ${i % 7 * 0.3}s` : undefined,
              pointerEvents: 'none',
              zIndex: 1
            }}
          />
        ))}
        <style>{`
          @keyframes twinkle {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
          }
        `}</style>
      </div>
      {/* Legend - fixed, outside zoomable map, always bottom left of main area, now compact and toggleable */}
      {legendVisible ? (
        <div className="fixed left-72 bottom-8 bg-slate-800/70 backdrop-blur-sm rounded-md border border-slate-700/40 p-2 z-30 shadow pointer-events-auto flex flex-col min-w-[160px] max-w-xs" style={{ fontSize: '12px' }}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-300">Categories</span>
            <button onClick={() => setLegendVisible(false)} className="p-1 rounded hover:bg-slate-700/40 transition-colors text-slate-400" title="Hide legend"><X size={14} /></button>
          </div>
          <div className="grid gap-1">
            {categories.map((category) => (
              <div 
                key={category.id} 
                className="flex items-center gap-1 cursor-pointer transition-all duration-200 hover:bg-slate-700/20 px-1.5 py-0.5 rounded"
                onMouseEnter={() => setHoveredCategory(category.id)}
                onMouseLeave={() => setHoveredCategory(null)}
              >
                <div 
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: getCategoryColor(category.id) }}
                />
                <span className="text-xs text-slate-300">{category.name}</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <button
          className="fixed left-72 bottom-8 bg-slate-800/70 text-xs text-slate-300 rounded-md border border-slate-700/40 px-3 py-1 z-30 shadow hover:bg-slate-700/60 transition-colors"
          style={{ fontSize: '12px' }}
          onClick={() => setLegendVisible(true)}
        >
          Show Legend
        </button>
      )}
      {/* Main map content (z-10) */}
      <div 
        className="transform transition-transform duration-300 ease-out h-full w-full z-10"
        style={{ 
          transform: `scale(${zoomLevel}) translate(${mapOffset.x}px, ${mapOffset.y}px)`,
        }}
      >
        {packedData && packedData.children && packedData.children.map((catNode: any) => {
          // Find the largest subnet in this category
          let largestSubnetId = null;
          if (catNode.children && catNode.children.length > 0) {
            const sorted = [...catNode.children].sort((a, b) => (b.data.marketCap || 0) - (a.data.marketCap || 0));
            largestSubnetId = sorted[0].data.id;
          }
          // Highlight if hovered
          const isHighlighted = hoveredCategory === catNode.data.id;
          // Soft colored glow for each cluster
          const clusterGlow = getCategoryColor(catNode.data.id).replace('rgb', 'rgba').replace(')', ',0.25)');
          return (
            <div key={catNode.data.id || catNode.data.name} className="absolute">
              {/* Cluster glow */}
              <div
                style={{
                  position: 'absolute',
                  left: catNode.x - catNode.r * 1.18,
                  top: catNode.y - catNode.r * 1.18,
                  width: catNode.r * 2.36,
                  height: catNode.r * 2.36,
                  borderRadius: '50%',
                  background: `radial-gradient(circle, ${clusterGlow} 0%, transparent 80%)`,
                  filter: 'blur(16px)',
                  zIndex: 2,
                  pointerEvents: 'none',
                }}
              />
              {/* Category circle (optional, for background) */}
              <div
                style={{
                  position: 'absolute',
                  left: catNode.x - catNode.r,
                  top: catNode.y - catNode.r,
                  width: catNode.r * 2,
                  height: catNode.r * 2,
                  borderRadius: '50%',
                  background: 'rgba(120,100,255,0.08)',
                  pointerEvents: 'none',
                  boxShadow: isHighlighted ? `0 0 32px 12px ${getCategoryColor(catNode.data.id)}, 0 0 0 6px rgba(255,255,255,0.25)` : undefined,
                  outline: isHighlighted ? `3px solid ${getCategoryColor(catNode.data.id)}` : undefined,
                  outlineOffset: isHighlighted ? '2px' : undefined,
                  transition: 'box-shadow 0.2s, outline 0.2s',
                  zIndex: isHighlighted ? 100 : 1,
                }}
              />
              {/* Subnets as packed children */}
              {catNode.children && catNode.children.map((subnetNode: any) => (
                <Subnet
                  key={subnetNode.data.id}
                  subnet={subnetNode.data}
                  position={{ x: subnetNode.x, y: subnetNode.y }}
                  categoryColor={getCategoryColor(catNode.data.id)}
                  isVisible={true}
                  categoryName={catNode.data.name}
                  packedRadius={subnetNode.r}
                  isLargestSubnet={subnetNode.data.id === largestSubnetId}
                  showSubnetId={topGlobalSubnetIds.includes(subnetNode.data.id)}
                />
              ))}
              {/* Category label */}
              <div
                style={{
                  position: 'absolute',
                  left: catNode.x - catNode.r,
                  top: catNode.y + catNode.r - 28,
                  width: catNode.r * 2,
                  textAlign: 'center',
                  color: '#fff',
                  fontWeight: 600,
                  fontSize: 14,
                  pointerEvents: 'none',
                  textShadow: '0 1px 8px #000',
                  filter: isHighlighted ? 'brightness(1.5) drop-shadow(0 0 8px #fff)' : undefined,
                  transition: 'filter 0.2s',
                  zIndex: isHighlighted ? 101 : 2,
                }}
              >
                {catNode.data.name}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default GalaxyMap;