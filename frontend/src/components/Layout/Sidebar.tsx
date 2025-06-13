import React, { useState, useEffect } from 'react';
import { Filter, ChevronDown, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import { CategoryType } from '../../types';

const Sidebar: React.FC = () => {
  const { sidebarOpen, filters, updateFilter, clearFilters } = useAppContext();
  const [filtersExpanded, setFiltersExpanded] = useState(true);
  const [collapsed, setCollapsed] = useState(false);
  const [categories, setCategories] = useState<CategoryType[]>([]);

  // Load categories for dynamic category filter
  useEffect(() => {
    fetch('/subnets_frontend_ready.json')
      .then(res => res.json())
      .then((data: CategoryType[]) => {
        setCategories(data);
      })
      .catch(err => {
        console.error('Sidebar: Error loading categories:', err);
      });
  }, []);

  // Dynamic filter options based on real data
  const getFilterOptions = () => [
    {
      name: 'category' as const,
      label: 'Category',
      options: [
        { value: 'all', label: 'All Categories' },
        ...categories.map(cat => ({
          value: cat.id,
          label: cat.name
        }))
      ]
    },
    {
      name: 'emissions' as const,
      label: 'Emissions (% TAO)',
      options: [
        { value: 'all', label: 'All Ranges' },
        { value: 'very_high', label: '>10%' },
        { value: 'high', label: '5-10%' },
        { value: 'medium', label: '1-5%' },
        { value: 'low', label: '0.1-1%' },
        { value: 'very_low', label: '<0.1%' }
      ]
    },
    {
      name: 'marketCap' as const,
      label: 'Market Cap ($)',
      options: [
        { value: 'all', label: 'All Ranges' },
        { value: 'very_high', label: '>100k' },
        { value: 'high', label: '50k-100k' },
        { value: 'medium', label: '10k-50k' },
        { value: 'low', label: '1k-10k' },
        { value: 'very_low', label: '<1k' }
      ]
    },
    {
      name: 'rating' as const,
      label: 'Rank',
      options: [
        { value: 'all', label: 'All Ranks' },
        { value: 'top_10', label: 'Top 10' },
        { value: 'top_25', label: 'Top 25' },
        { value: 'top_50', label: 'Top 50' },
        { value: 'bottom_50', label: 'Bottom 50' }
      ]
    },
    {
      name: 'age' as const,
      label: 'Days Since Registration',
      options: [
        { value: 'all', label: 'All Time' },
        { value: 'new', label: '<30 days' },
        { value: 'recent', label: '30-90 days' },
        { value: 'established', label: '90-365 days' },
        { value: 'mature', label: '>365 days' },
        { value: 'unknown', label: 'Unknown' }
      ]
    },
    {
      name: 'team' as const,
      label: 'Links Available',
      options: [
        { value: 'all', label: 'All' },
        { value: 'full', label: 'Website + GitHub + Discord' },
        { value: 'partial', label: 'Some Links' },
        { value: 'minimal', label: 'GitHub Only' },
        { value: 'none', label: 'No Links' }
      ]
    },
    {
      name: 'liveProduct' as const,
      label: 'Status',
      options: [
        { value: 'all', label: 'All Status' },
        { value: 'active', label: 'Active' },
        { value: 'inactive', label: 'Inactive' }
      ]
    },
    {
      name: 'doxxedFounders' as const,
      label: 'Price Change (1 Week)',
      options: [
        { value: 'all', label: 'All' },
        { value: 'positive', label: 'Positive (+)' },
        { value: 'negative', label: 'Negative (-)' },
        { value: 'stable', label: 'Stable (±2%)' }
      ]
    },
    {
      name: 'validators' as const,
      label: 'TAO Volume (24hr)',
      options: [
        { value: 'all', label: 'All Volumes' },
        { value: 'very_high', label: '>10k TAO' },
        { value: 'high', label: '1k-10k TAO' },
        { value: 'medium', label: '100-1k TAO' },
        { value: 'low', label: '<100 TAO' }
      ]
    }
  ];

  const handleFilterChange = (filterName: keyof typeof filters, value: string) => {
    updateFilter(filterName, value);
  };

  const hasActiveFilters = Object.values(filters).some(value => value !== 'all');

  return (
    <aside 
      className={`fixed left-0 top-0 bottom-0 bg-slate-900 border-r border-slate-800 pt-16 transition-all duration-300 z-0 flex flex-col ${collapsed ? 'w-4' : 'w-64'}`}
    >
      {/* Collapse/Expand Button at far right edge */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute top-6 -right-4 z-20 bg-slate-900 border border-slate-800 rounded-full p-1.5 shadow hover:bg-slate-800 transition-colors"
        style={{ width: 32, height: 32 }}
        aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
      </button>
      {!collapsed && sidebarOpen && (
        <div className="h-full py-4 flex flex-col px-4">
          <div className="card">
            <button
              onClick={() => setFiltersExpanded(!filtersExpanded)}
              className="w-full p-4 flex items-center justify-between text-left border-b border-slate-700/50"
            >
              <div className="flex items-center gap-2">
                <Filter size={16} className="text-indigo-400" />
                <h3 className="text-sm font-medium">Filters</h3>
                {hasActiveFilters && (
                  <span className="bg-indigo-500 text-white text-xs px-1.5 py-0.5 rounded-full">
                    {Object.values(filters).filter(v => v !== 'all').length}
                  </span>
                )}
              </div>
              <ChevronDown
                size={16}
                className={`transition-transform duration-200 ${
                  filtersExpanded ? 'rotate-180' : ''
                }`}
              />
            </button>
            <div
              className={`transition-all duration-200 ${
                filtersExpanded ? 'max-h-[calc(100vh-200px)] overflow-y-auto scrollbar-thin' : 'max-h-0 overflow-hidden'
              }`}
            >
              <div className="p-4 space-y-4">
                {/* Clear filters button */}
                {hasActiveFilters && (
                  <button
                    onClick={clearFilters}
                    className="w-full flex items-center justify-center gap-2 py-2 px-3 text-xs bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors duration-200"
                  >
                    <RotateCcw size={12} />
                    Clear All Filters
                  </button>
                )}
                
                {getFilterOptions().map((filter) => (
                  <div key={filter.name} className="filter-group">
                    <label className="text-xs text-slate-400 block mb-1.5">
                      {filter.label}
                    </label>
                    <select 
                      value={filters[filter.name]}
                      onChange={(e) => handleFilterChange(filter.name, e.target.value)}
                      className="w-full bg-slate-700/50 rounded-lg py-1.5 px-2.5 text-sm border border-slate-600/50 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-colors duration-200"
                    >
                      {filter.options.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      {collapsed && (
        <div className="flex-1 flex flex-col items-center justify-center">
          <Filter size={18} className="text-indigo-400 mb-2" />
          {hasActiveFilters && (
            <span className="bg-indigo-500 text-white text-xs px-1.5 py-0.5 rounded-full mt-1">
              {Object.values(filters).filter(v => v !== 'all').length}
            </span>
          )}
        </div>
      )}
    </aside>
  );
};

export default Sidebar;