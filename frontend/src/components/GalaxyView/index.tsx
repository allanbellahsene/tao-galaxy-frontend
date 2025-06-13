import React, { useState, useEffect, useMemo, useRef } from 'react';
import { X, Search, ArrowRight, ArrowLeft } from 'lucide-react';
import GalaxyMap from './GalaxyMap';
import GalaxyControls from './GalaxyControls';
import SubnetDetail from './SubnetDetail';
import { useAppContext } from '../../context/AppContext';
import { CategoryType, SubnetType } from '../../types';

const GalaxyView: React.FC = () => {
  const { 
    zoomLevel, 
    setZoomLevel,
    selectedCategory,
    selectedSubnet,
    showWelcome,
    setShowWelcome,
    searchQuery,
    setSearchQuery,
    filters
  } = useAppContext();
  
  const [isLoading, setIsLoading] = useState(true);
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [welcomeStep, setWelcomeStep] = useState(0);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const [inputValue, setInputValue] = useState('');
  const [activeSearchQuery, setActiveSearchQuery] = useState('');

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

  // Add keyboard shortcut to focus search (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
      // ESC to clear search
      if (e.key === 'Escape' && (inputValue || activeSearchQuery)) {
        setInputValue('');
        setActiveSearchQuery('');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [inputValue, activeSearchQuery]);

  // Filter subnet based on filter criteria
  const matchesFilters = (subnet: SubnetType): boolean => {
    // Emissions filter
    if (filters.emissions !== 'all') {
      const emissions = subnet.emissions || 0;
      switch (filters.emissions) {
        case 'very_high':
          if (emissions <= 10) return false;
          break;
        case 'high':
          if (emissions <= 5 || emissions > 10) return false;
          break;
        case 'medium':
          if (emissions <= 1 || emissions > 5) return false;
          break;
        case 'low':
          if (emissions <= 0.1 || emissions > 1) return false;
          break;
        case 'very_low':
          if (emissions > 0.1) return false;
          break;
      }
    }

    // Market Cap filter
    if (filters.marketCap !== 'all') {
      const marketCap = subnet.marketCap || 0;
      switch (filters.marketCap) {
        case 'very_high':
          if (marketCap <= 100000) return false;
          break;
        case 'high':
          if (marketCap <= 50000 || marketCap > 100000) return false;
          break;
        case 'medium':
          if (marketCap <= 10000 || marketCap > 50000) return false;
          break;
        case 'low':
          if (marketCap <= 1000 || marketCap > 10000) return false;
          break;
        case 'very_low':
          if (marketCap > 1000) return false;
          break;
      }
    }

    // Rank filter
    if (filters.rating !== 'all') {
      const rank = subnet.rank || Infinity;
      switch (filters.rating) {
        case 'top_10':
          if (rank > 10) return false;
          break;
        case 'top_25':
          if (rank > 25) return false;
          break;
        case 'top_50':
          if (rank > 50) return false;
          break;
        case 'bottom_50':
          if (rank <= 50) return false;
          break;
      }
    }

    // Age filter
    if (filters.age !== 'all') {
      const age = subnet.daysSinceRegistration || 0;
      switch (filters.age) {
        case 'new':
          if (age >= 30 && age > 0) return false;
          break;
        case 'recent':
          if (age < 30 || age >= 90) return false;
          break;
        case 'established':
          if (age < 90 || age >= 365) return false;
          break;
        case 'mature':
          if (age < 365) return false;
          break;
        case 'unknown':
          if (age > 0) return false;
          break;
      }
    }

    // Links filter (team)
    if (filters.team !== 'all') {
      const hasWebsite = !!(subnet.website && subnet.website.trim());
      const hasGithub = !!(subnet.github && subnet.github.trim());
      const hasDiscord = !!(subnet.discord && subnet.discord.trim());
      
      switch (filters.team) {
        case 'full':
          if (!hasWebsite || !hasGithub || !hasDiscord) return false;
          break;
        case 'partial':
          if (!hasWebsite && !hasGithub && !hasDiscord) return false;
          if (hasWebsite && hasGithub && hasDiscord) return false;
          break;
        case 'minimal':
          if (!hasGithub || hasWebsite || hasDiscord) return false;
          break;
        case 'none':
          if (hasWebsite || hasGithub || hasDiscord) return false;
          break;
      }
    }

    // Status filter
    if (filters.liveProduct !== 'all') {
      switch (filters.liveProduct) {
        case 'active':
          if (subnet.status !== 'active') return false;
          break;
        case 'inactive':
          if (subnet.status !== 'inactive') return false;
          break;
      }
    }

    // Price change filter
    if (filters.doxxedFounders !== 'all') {
      const weeklyChange = subnet.weeklyChange || 0;
      switch (filters.doxxedFounders) {
        case 'positive':
          if (weeklyChange <= 0) return false;
          break;
        case 'negative':
          if (weeklyChange >= 0) return false;
          break;
        case 'stable':
          if (Math.abs(weeklyChange) > 2) return false;
          break;
      }
    }

    // TAO Volume filter
    if (filters.validators !== 'all') {
      const volume = subnet.taoVolume24hr || 0;
      switch (filters.validators) {
        case 'very_high':
          if (volume <= 10000) return false;
          break;
        case 'high':
          if (volume <= 1000 || volume > 10000) return false;
          break;
        case 'medium':
          if (volume <= 100 || volume > 1000) return false;
          break;
        case 'low':
          if (volume > 100) return false;
          break;
      }
    }

    return true;
  };

  // Filter categories and subnets based on active search query and filters
  const filteredCategories = useMemo(() => {
    if (!categories.length) {
      return categories;
    }

    let filtered = categories;

    // Apply category filter first
    if (filters.category !== 'all') {
      filtered = filtered.filter(category => category.id === filters.category);
    }

    // Then apply search query and other filters
    const query = activeSearchQuery.toLowerCase().trim();
    
    filtered = filtered
      .map(category => {
        // Filter subnets within this category
        let filteredSubnets = category.subnets;

        // Apply filter criteria
        filteredSubnets = filteredSubnets.filter(subnet => matchesFilters(subnet));

        // Apply search query if present
        if (query) {
          filteredSubnets = filteredSubnets.filter(subnet => {
          // Basic text matching with null checks
          const basicMatch = 
            (subnet.name && subnet.name.toLowerCase().includes(query)) ||
            (subnet.id && subnet.id.toLowerCase().includes(query)) ||
            (subnet.description && subnet.description.toLowerCase().includes(query));

          // Subnet number matching (e.g., "1" matches "SN1", "subnet 1" matches "SN1")
          const subnetNumberMatch = () => {
            if (!subnet.id) return false;
            const subnetNumber = subnet.id.match(/\d+/)?.[0];
            if (!subnetNumber) return false;
            
            // Direct number match
            if (query === subnetNumber) return true;
            
            // "sn" + number format (e.g., "sn1", "sn 1")
            const snMatch = query.match(/sn\s*(\d+)/i);
            if (snMatch && snMatch[1] === subnetNumber) return true;
            
            // "subnet" + number format (e.g., "subnet1", "subnet 1")
            const subnetMatch = query.match(/subnet\s*(\d+)/i);
            if (subnetMatch && subnetMatch[1] === subnetNumber) return true;
            
            return false;
          };

          // Name parts matching (e.g., "prompting" matches "Prompting / Apex")
          const namePartsMatch = () => {
            if (!subnet.name) return false;
            const nameParts = subnet.name.split(/[\s\/\-_,]+/).filter(part => part.length > 0);
            return nameParts.some(part => part.toLowerCase().includes(query));
          };

            return basicMatch || subnetNumberMatch() || namePartsMatch();
          });
          }

        // Check if category itself matches search (only if searching)
        const categoryMatches = query && (
          (category.name && category.name.toLowerCase().includes(query)) ||
          (category.description && category.description.toLowerCase().includes(query))
        );

        // Include category if it matches or has matching subnets
        if (categoryMatches || filteredSubnets.length > 0) {
          return {
            ...category,
            subnets: categoryMatches ? category.subnets.filter(subnet => matchesFilters(subnet)) : filteredSubnets,
            marketCapTotal: filteredSubnets.reduce((sum, subnet) => sum + (subnet.marketCap || 0), 0)
          };
        }

        return null;
      })
      .filter((category): category is CategoryType => category !== null);

    // If no results found and we have active filters, show empty instead of all
    const hasActiveFilters = Object.values(filters).some(value => value !== 'all') || query;
    if (filtered.length === 0 && !hasActiveFilters) {
      return categories;
    }
    
    return filtered;
  }, [categories, activeSearchQuery, filters]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSearchExecute = () => {
    setActiveSearchQuery(inputValue.trim());
  };

  const handleSearchKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSearchExecute();
    }
  };

  const handleSearchClear = () => {
    setInputValue('');
    setActiveSearchQuery('');
  };

  // Calculate filtering stats
  const totalSubnets = categories.reduce((sum, cat) => sum + cat.subnets.length, 0);
  const filteredSubnets = filteredCategories.reduce((sum, cat) => sum + cat.subnets.length, 0);
  const hasActiveFilters = Object.values(filters).some(value => value !== 'all');
  const hasActiveQuery = !!activeSearchQuery.trim();

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
        <div className="flex items-center bg-slate-800/90 backdrop-blur-sm rounded-lg px-3 py-2 w-full border border-slate-700/50 hover:border-slate-600/50 transition-colors">
          <Search size={16} className="text-slate-400 mr-2" />
          <input 
            type="search" 
            placeholder="Search subnets, categories... (Press Enter)" 
            className="bg-transparent border-none outline-none text-sm w-full text-white placeholder-slate-400 focus:placeholder-slate-500"
            value={inputValue}
            onChange={handleSearchChange}
            onKeyDown={handleSearchKeyPress}
            ref={searchInputRef}
          />
          {inputValue && (
            <>
              <button
                onClick={handleSearchExecute}
                className="ml-2 p-1 hover:bg-slate-700/50 rounded-full transition-colors"
                aria-label="Execute search"
                title="Search (Enter)"
              >
                <Search size={14} className="text-slate-400 hover:text-slate-300" />
              </button>
              <button
                onClick={handleSearchClear}
                className="ml-1 p-1 hover:bg-slate-700/50 rounded-full transition-colors"
                aria-label="Clear search"
              >
                <X size={14} className="text-slate-400 hover:text-slate-300" />
              </button>
            </>
          )}
        </div>
        {/* Search and filter results indicator */}
        {(hasActiveQuery || hasActiveFilters) && (
          <div className="mt-2 text-xs text-slate-400 text-center bg-slate-800/60 rounded px-2 py-1">
            {(() => {
              if (inputValue && !activeSearchQuery) {
                return `Type and press Enter to search for "${inputValue}"`;
              }
              
              const parts = [];
              if (hasActiveQuery) parts.push(`search: "${activeSearchQuery}"`);
              if (hasActiveFilters) parts.push(`${Object.values(filters).filter(v => v !== 'all').length} filter(s)`);
              
              if (parts.length > 0) {
                return `Showing ${filteredSubnets}/${totalSubnets} subnets (${parts.join(', ')})`;
              }
              
              return null;
            })()}
          </div>
        )}
      </div>

      <GalaxyMap categories={filteredCategories} />
      
      <GalaxyControls 
        zoomLevel={zoomLevel}
        onZoomIn={() => setZoomLevel(Math.min(zoomLevel + 0.2, 2))}
        onZoomOut={() => setZoomLevel(Math.max(zoomLevel - 0.2, 0.5))}
        onResetZoom={() => setZoomLevel(0.7)}
        onZoomChange={setZoomLevel}
      />
      
      {selectedSubnet && <SubnetDetail categories={categories} />}
      
      {!selectedSubnet && !selectedCategory && showWelcome && !activeSearchQuery && !hasActiveFilters && (
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
                  : 'Use filters in the sidebar and zoom in to discover more details.'}
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