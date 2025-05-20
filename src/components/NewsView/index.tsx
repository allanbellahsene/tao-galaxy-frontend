import React, { useState } from 'react';
import { TrendingUp, Star, Clock, Filter, Table, Grid, ChevronDown, Search } from 'lucide-react';
import NewsCard from './NewsCard';
import NewsTable from './NewsTable';
import DailyRecap from './DailyRecap';
import FilterDropdown from './FilterDropdown';
import { mockNews } from '../../data/mockNews';
import { mockCategories } from '../../data/mockData';

const NewsView: React.FC = () => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['all']);
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('24h');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('table');
  const [selectedSubnets, setSelectedSubnets] = useState<string[]>(['bittensor']);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [showRecaps, setShowRecaps] = useState<boolean>(true);

  const categories = [
    { id: 'all', name: 'All News' },
    { id: 'subnet-updates', name: 'Subnet Updates' },
    { id: 'governance', name: 'Governance' },
    { id: 'development', name: 'Development' },
    { id: 'community', name: 'Community' },
    { id: 'research', name: 'Research' }
  ];

  const sources = [
    { id: 'blog', name: 'Bittensor Blog' },
    { id: 'forum', name: 'TAO Forum' },
    { id: 'research', name: 'TAO Research' },
    { id: 'community', name: 'TAO Community' },
    { id: 'dev', name: 'Dev News' }
  ];

  // Create subnet options from mockCategories
  const subnetOptions = [
    { id: 'bittensor', name: 'Bittensor Ecosystem' },
    ...mockCategories.flatMap(category => 
      category.subnets.map(subnet => ({
        id: subnet.id,
        name: `${subnet.name} (SN${subnet.id.match(/\d+/)?.[0] || ''})`,
        category: category.name
      }))
    )
  ];

  return (
    <div className="min-h-[calc(100vh-64px)] p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-6">
            <h2 className="text-2xl font-semibold">Latest News</h2>
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="search"
                placeholder="Search news..."
                className="w-64 bg-slate-800/80 rounded-lg pl-10 pr-4 py-2 text-sm border border-slate-700/50 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-colors duration-200"
              />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowRecaps(!showRecaps)}
              className={`px-4 py-2 rounded-lg text-sm transition-colors duration-200 ${
                showRecaps ? 'bg-indigo-600/20 text-indigo-400' : 'hover:bg-slate-800/60 text-slate-300'
              }`}
            >
              Daily Recaps
            </button>
            <div className="flex items-center bg-slate-800 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-md transition-colors duration-200 ${
                  viewMode === 'grid' ? 'bg-slate-700' : 'hover:bg-slate-700/50'
                }`}
              >
                <Grid size={16} />
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`p-2 rounded-md transition-colors duration-200 ${
                  viewMode === 'table' ? 'bg-slate-700' : 'hover:bg-slate-700/50'
                }`}
              >
                <Table size={16} />
              </button>
            </div>
          </div>
        </div>

        {/* Filters Bar */}
        <div className="card p-4 mb-6">
          <div className="flex items-center gap-6">
            {/* Subnets selector */}
            <div className="flex-1">
              <FilterDropdown
                label="Subnets"
                options={subnetOptions}
                selectedValues={selectedSubnets}
                onChange={setSelectedSubnets}
                grouped={true}
              />
            </div>

            {/* Source selector */}
            <div className="flex-1">
              <FilterDropdown
                label="Source"
                options={sources}
                selectedValues={selectedSources}
                onChange={setSelectedSources}
              />
            </div>

            {/* Category selector */}
            <div className="flex-1">
              <FilterDropdown
                label="Category"
                options={categories}
                selectedValues={selectedCategories}
                onChange={setSelectedCategories}
              />
            </div>

            {/* Time selector */}
            <div className="flex-1">
              <FilterDropdown
                label="Time Range"
                options={[
                  { id: '24h', name: 'Last 24h' },
                  { id: '7d', name: 'Last 7 days' },
                  { id: '30d', name: 'Last 30 days' }
                ]}
                selectedValues={[selectedTimeframe]}
                onChange={(values) => setSelectedTimeframe(values[0])}
              />
            </div>
          </div>
        </div>

        {/* Daily Recap */}
        {showRecaps && (
          <div className="mb-8">
            <DailyRecap />
          </div>
        )}

        {/* News Content */}
        {viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockNews.map(news => (
              <NewsCard key={news.id} news={news} />
            ))}
          </div>
        ) : (
          <NewsTable news={mockNews} />
        )}
      </div>
    </div>
  );
};

export default NewsView;