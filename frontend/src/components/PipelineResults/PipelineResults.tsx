import React, { useState, useEffect, useMemo } from 'react';
import { CheckCircle, AlertCircle, ExternalLink, Github, Globe, MessageCircle, FileText, TrendingUp, TrendingDown, Activity, Shield, Users, BarChart3 } from 'lucide-react';

interface SubnetScore {
  netuid: number;
  name: string;
  description: string;
  overall_score: number;
  investment_recommendation: string;
  confidence_level: string;
  website_available: boolean;
  has_github: boolean;
  has_documentation: boolean;
  verified_sources_count: number;
  source_health: {
    health_score: number;
    total_sources: number;
    verified_sources: number;
    missing_sources: number;
    new_sources: number;
  };
  scores: {
    category_scores?: {
      team_strength?: { score: number; weight: number };
      product_viability?: { score: number; weight: number };
      market_opportunity?: { score: number; weight: number };
      execution_progress?: { score: number; weight: number };
      risk_management?: { score: number; weight: number };
    };
    strengths?: string[];
    weaknesses?: string[];
    risk_flags?: string[];
  };
  primary_links: {
    website?: string;
    github?: string;
    discord?: string;
    twitter?: string;
    documentation?: string;
  };
  research_status: string;
  scoring_status: string;
  last_updated: string;
}

interface PipelineResultsProps {
  data?: SubnetScore[];
  loading?: boolean;
}

const PipelineResults: React.FC<PipelineResultsProps> = ({ data, loading = false }) => {
  const [sortBy, setSortBy] = useState<keyof SubnetScore>('overall_score');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filter, setFilter] = useState('all');
  const [selectedSubnet, setSelectedSubnet] = useState<SubnetScore | null>(null);

  // Sort and filter data
  const processedData = useMemo(() => {
    if (!data) return [];
    
    let filtered = data;
    
    // Apply filters
    switch (filter) {
      case 'excellent':
        filtered = data.filter(s => s.overall_score >= 4.0);
        break;
      case 'good':
        filtered = data.filter(s => s.overall_score >= 3.0 && s.overall_score < 4.0);
        break;
      case 'concerns':
        filtered = data.filter(s => s.overall_score < 3.0);
        break;
      case 'verified':
        filtered = data.filter(s => s.source_health.health_score >= 75);
        break;
      case 'research_ready':
        filtered = data.filter(s => s.website_available);
        break;
    }
    
    // Sort data
    return filtered.sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];
      
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
      }
      
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortOrder === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      }
      
      return 0;
    });
  }, [data, sortBy, sortOrder, filter]);

  // Statistics
  const stats = useMemo(() => {
    if (!data) return {};
    
    return {
      total: data.length,
      excellent: data.filter(s => s.overall_score >= 4.0).length,
      good: data.filter(s => s.overall_score >= 3.0 && s.overall_score < 4.0).length,
      average: data.filter(s => s.overall_score >= 2.0 && s.overall_score < 3.0).length,
      poor: data.filter(s => s.overall_score < 2.0).length,
      verified: data.filter(s => s.source_health.health_score >= 75).length,
      researchReady: data.filter(s => s.website_available).length,
      avgScore: data.reduce((sum, s) => sum + s.overall_score, 0) / data.length,
      avgSourceHealth: data.reduce((sum, s) => sum + s.source_health.health_score, 0) / data.length
    };
  }, [data]);

  const getScoreColor = (score: number) => {
    if (score >= 4.0) return 'text-green-600 bg-green-50';
    if (score >= 3.0) return 'text-blue-600 bg-blue-50';
    if (score >= 2.0) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getRecommendationIcon = (recommendation: string) => {
    if (recommendation.includes('Strong Buy') || recommendation.includes('Buy')) {
      return <TrendingUp className="w-4 h-4 text-green-600" />;
    }
    if (recommendation.includes('Hold')) {
      return <Activity className="w-4 h-4 text-yellow-600" />;
    }
    return <TrendingDown className="w-4 h-4 text-red-600" />;
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
          <div className="h-96 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Automated Subnet Analysis Results
        </h1>
        <p className="text-gray-600">
          Comprehensive AI-powered analysis of Bittensor subnets with verified sources and objective scoring
        </p>
      </div>

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg p-6 shadow-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Subnets</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <BarChart3 className="h-8 w-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-6 shadow-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.avgScore?.toFixed(1) || '0.0'}</p>
            </div>
            <TrendingUp className="h-8 w-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-6 shadow-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Excellent (4.0+)</p>
              <p className="text-2xl font-bold text-green-600">{stats.excellent}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-6 shadow-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Source Health</p>
              <p className="text-2xl font-bold text-gray-900">{stats.avgSourceHealth?.toFixed(0) || '0'}%</p>
            </div>
            <Shield className="h-8 w-8 text-blue-600" />
          </div>
        </div>
      </div>

      {/* Filters and Controls */}
      <div className="bg-white rounded-lg p-6 shadow-lg border">
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div className="flex flex-wrap gap-2">
            {[
              { key: 'all', label: 'All Subnets' },
              { key: 'excellent', label: 'Excellent (4.0+)' },
              { key: 'good', label: 'Good (3.0+)' },
              { key: 'concerns', label: 'Concerns (<3.0)' },
              { key: 'verified', label: 'Verified Sources' },
              { key: 'research_ready', label: 'Research Ready' }
            ].map(({ key, label }) => (
              <button
                key={key}
                onClick={() => setFilter(key)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  filter === key
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
          
          <div className="flex gap-2 items-center">
            <span className="text-sm text-gray-600">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as keyof SubnetScore)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option value="overall_score">Overall Score</option>
              <option value="name">Name</option>
              <option value="netuid">NetUID</option>
              <option value="source_health.health_score">Source Health</option>
            </select>
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="px-2 py-1 border border-gray-300 rounded-md text-sm hover:bg-gray-50"
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-white rounded-lg shadow-lg border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Subnet
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Score & Recommendation
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sources
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Links
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {processedData.map((subnet) => (
                <tr key={subnet.netuid} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        SN{subnet.netuid}: {subnet.name}
                      </div>
                      <div className="text-sm text-gray-500 max-w-xs truncate">
                        {subnet.description}
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreColor(subnet.overall_score)}`}>
                        {subnet.overall_score.toFixed(1)}
                      </span>
                      {getRecommendationIcon(subnet.investment_recommendation)}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {subnet.investment_recommendation.split(' - ')[0]}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-1">
                      <div className="text-sm text-gray-900">
                        {subnet.source_health.health_score.toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-500">
                        ({subnet.source_health.verified_sources}/{subnet.source_health.total_sources})
                      </div>
                    </div>
                    <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${subnet.source_health.health_score}%` }}
                      ></div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex space-x-2">
                      {subnet.primary_links.website && (
                        <a href={subnet.primary_links.website} target="_blank" rel="noopener noreferrer">
                          <Globe className="w-4 h-4 text-blue-600 hover:text-blue-800" />
                        </a>
                      )}
                      {subnet.primary_links.github && (
                        <a href={subnet.primary_links.github} target="_blank" rel="noopener noreferrer">
                          <Github className="w-4 h-4 text-gray-700 hover:text-gray-900" />
                        </a>
                      )}
                      {subnet.primary_links.discord && (
                        <a href={subnet.primary_links.discord} target="_blank" rel="noopener noreferrer">
                          <MessageCircle className="w-4 h-4 text-indigo-600 hover:text-indigo-800" />
                        </a>
                      )}
                      {subnet.primary_links.documentation && (
                        <a href={subnet.primary_links.documentation} target="_blank" rel="noopener noreferrer">
                          <FileText className="w-4 h-4 text-green-600 hover:text-green-800" />
                        </a>
                      )}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex flex-col space-y-1">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        subnet.research_status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {subnet.research_status === 'completed' ? 'Researched' : 'Pending'}
                      </span>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        subnet.confidence_level === 'High' ? 'bg-green-100 text-green-800' :
                        subnet.confidence_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {subnet.confidence_level} Confidence
                      </span>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      onClick={() => setSelectedSubnet(subnet)}
                      className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detailed Modal */}
      {selectedSubnet && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl max-h-screen overflow-y-auto p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                SN{selectedSubnet.netuid}: {selectedSubnet.name}
              </h2>
              <button
                onClick={() => setSelectedSubnet(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Category Scores */}
              <div>
                <h3 className="text-lg font-semibold mb-4">Category Scores</h3>
                <div className="space-y-3">
                  {selectedSubnet.scores.category_scores && Object.entries(selectedSubnet.scores.category_scores).map(([category, data]) => (
                    <div key={category} className="flex items-center justify-between">
                      <span className="text-sm font-medium capitalize">
                        {category.replace('_', ' ')}
                      </span>
                      <span className={`px-2 py-1 rounded text-sm ${getScoreColor(data.score)}`}>
                        {data.score}/5
                      </span>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Strengths & Weaknesses */}
              <div>
                <h3 className="text-lg font-semibold mb-4">Analysis</h3>
                {selectedSubnet.scores.strengths && selectedSubnet.scores.strengths.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-medium text-green-700 mb-2">Strengths</h4>
                    <ul className="text-sm space-y-1">
                      {selectedSubnet.scores.strengths.map((strength, idx) => (
                        <li key={idx} className="flex items-start">
                          <CheckCircle className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {selectedSubnet.scores.weaknesses && selectedSubnet.scores.weaknesses.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-medium text-red-700 mb-2">Areas of Concern</h4>
                    <ul className="text-sm space-y-1">
                      {selectedSubnet.scores.weaknesses.map((weakness, idx) => (
                        <li key={idx} className="flex items-start">
                          <AlertCircle className="w-4 h-4 text-red-600 mr-2 mt-0.5 flex-shrink-0" />
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
            
            {/* Investment Recommendation */}
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">Investment Recommendation</h3>
              <p className="text-gray-700">{selectedSubnet.investment_recommendation}</p>
              <p className="text-sm text-gray-500 mt-2">
                Confidence Level: {selectedSubnet.confidence_level}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PipelineResults; 