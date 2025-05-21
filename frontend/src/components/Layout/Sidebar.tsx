import React, { useState } from 'react';
import { Filter, ChevronDown, ChevronLeft, ChevronRight, ChevronUp } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';

const Sidebar: React.FC = () => {
  const { sidebarOpen } = useAppContext();
  const [filtersExpanded, setFiltersExpanded] = useState(true);
  const [collapsed, setCollapsed] = useState(false);

  const filters = [
    {
      name: 'category',
      label: 'Category',
      options: [
        { value: 'all', label: 'All Categories' },
        { value: 'genai', label: 'GenAI' },
        { value: 'defi', label: 'DeFi' },
        { value: 'infra', label: 'Infrastructure' },
        { value: 'training', label: 'Training' },
        { value: 'modeldev', label: 'Model Dev' },
        { value: 'predictions', label: 'Predictions' },
        { value: 'aitool', label: 'AI Tools' }
      ]
    },
    {
      name: 'emissions',
      label: 'Emissions (% TAO)',
      options: [
        { value: 'all', label: 'All Ranges' },
        { value: 'high', label: '>5%' },
        { value: 'medium', label: '1-5%' },
        { value: 'low', label: '<1%' }
      ]
    },
    {
      name: 'marketCap',
      label: 'Market Cap ($)',
      options: [
        { value: 'all', label: 'All Ranges' },
        { value: 'very_high', label: '>100M' },
        { value: 'high', label: '50M-100M' },
        { value: 'medium', label: '10M-50M' },
        { value: 'low', label: '<10M' }
      ]
    },
    {
      name: 'rating',
      label: 'Rating',
      options: [
        { value: 'all', label: 'All Ratings' },
        { value: 'aaa', label: 'AAA' },
        { value: 'aa', label: 'AA' },
        { value: 'a', label: 'A' },
        { value: 'bbb', label: 'BBB' },
        { value: 'bb', label: 'BB' },
        { value: 'b', label: 'B' }
      ]
    },
    {
      name: 'age',
      label: 'Days of Existence',
      options: [
        { value: 'all', label: 'All Time' },
        { value: 'new', label: '<30 days' },
        { value: 'recent', label: '30-90 days' },
        { value: 'established', label: '90-180 days' },
        { value: 'mature', label: '>180 days' }
      ]
    },
    {
      name: 'team',
      label: 'Team',
      options: [
        { value: 'all', label: 'All Teams' },
        { value: 'core', label: 'Core Team' },
        { value: 'community', label: 'Community' },
        { value: 'dao', label: 'DAO' }
      ]
    },
    {
      name: 'liveProduct',
      label: 'Live Product',
      options: [
        { value: 'all', label: 'All Status' },
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' },
        { value: 'unknown', label: 'Unknown' }
      ]
    },
    {
      name: 'doxxedFounders',
      label: 'Doxxed Founders',
      options: [
        { value: 'all', label: 'All Status' },
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' },
        { value: 'partially', label: 'Partially' },
        { value: 'unknown', label: 'Unknown' }
      ]
    },
    {
      name: 'validators',
      label: 'Validators',
      options: [
        { value: 'all', label: 'All Ranges' },
        { value: 'very_high', label: '>250' },
        { value: 'high', label: '150-250' },
        { value: 'medium', label: '50-150' },
        { value: 'low', label: '<50' }
      ]
    }
  ];

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
                {filters.map((filter) => (
                  <div key={filter.name} className="filter-group">
                    <label className="text-xs text-slate-400 block mb-1.5">
                      {filter.label}
                    </label>
                    <select 
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
        </div>
      )}
    </aside>
  );
};

export default Sidebar;