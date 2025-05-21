import React from 'react';
import { ArrowLeft, Users, DollarSign, BarChart3, Globe, Download, ExternalLink, GitBranch, Star, TrendingUp, Shield, Code, MessageSquare } from 'lucide-react';
import { Link } from 'react-router-dom';

const SubnetReport: React.FC = () => {
  const subnet = {
    id: 'subnet-64',
    name: 'SN64 Chutes',
    category: 'Compute',
    logo: 'https://images.pexels.com/photos/8370752/pexels-photo-8370752.jpeg',
    status: 'Fairly Valued',
    description: 'Decentralized alternative to major Web2 AI services like OpenAI\'s API, providing better accessibility, more model diversity, and superior performance.',
    metrics: {
      overall: 4.4,
      team: 3.8,
      product: 4.5,
      community: 4.8,
      mission: 4.3
    },
    stats: {
      users: '100,000+',
      revenue: 'Yes',
      tam: '$250B',
      validators: 245,
      marketCap: '$124M',
      weeklyChange: '+8.9%'
    }
  };

  const timelineEvents = [
    {
      date: 'Mar 15, 2025',
      title: 'Major Performance Update',
      description: 'Reduced latency by 25% and increased throughput significantly',
      type: 'update'
    },
    {
      date: 'Mar 10, 2025',
      title: 'Community Milestone',
      description: 'Reached 100,000 active users',
      type: 'milestone'
    },
    {
      date: 'Mar 5, 2025',
      title: 'New Partnership',
      description: 'Strategic partnership with major cloud provider announced',
      type: 'partnership'
    }
  ];

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center gap-1">
        {[...Array(5)].map((_, index) => (
          <Star
            key={index}
            size={16}
            className={index < Math.floor(rating) ? 'text-yellow-500 fill-yellow-500' : 'text-slate-600'}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-[calc(100vh-64px)] p-6 bg-gradient-to-b from-slate-900 to-slate-950">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <Link 
              to="/app" 
              className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-slate-300 transition-colors mb-4"
            >
              <ArrowLeft size={16} />
              <span>Back to Galaxy View</span>
            </Link>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-xl bg-slate-800 border border-slate-700/50 flex items-center justify-center">
                <img 
                  src={subnet.logo} 
                  alt={subnet.name}
                  className="w-10 h-10 rounded-lg object-cover"
                />
              </div>
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h1 className="text-2xl font-semibold">{subnet.name}</h1>
                  <span className="px-3 py-1 rounded-full text-sm font-medium bg-emerald-500/10 text-emerald-400">
                    {subnet.status}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-400">
                  <span>ID: {subnet.id}</span>
                  <span>•</span>
                  <span>{subnet.category}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button className="btn bg-slate-800 hover:bg-slate-700">
              <Download size={16} className="mr-2" />
              Download Report
            </button>
            <button className="btn btn-primary">
              <ExternalLink size={16} className="mr-2" />
              Visit Website
            </button>
          </div>
        </div>

        <div className="grid grid-cols-12 gap-6">
          {/* Main Content */}
          <div className="col-span-8 space-y-6">
            {/* Mission Statement */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold mb-4">Mission Statement</h2>
              <p className="text-slate-300 leading-relaxed">{subnet.description}</p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-3 gap-4">
              <div className="card p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400">
                    <Users size={20} />
                  </div>
                  <div>
                    <div className="text-sm text-slate-400">Active Users</div>
                    <div className="text-xl font-semibold">{subnet.stats.users}</div>
                  </div>
                </div>
                <div className="text-sm text-emerald-400">
                  +12.5% this month
                </div>
              </div>

              <div className="card p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                    <DollarSign size={20} />
                  </div>
                  <div>
                    <div className="text-sm text-slate-400">Market Cap</div>
                    <div className="text-xl font-semibold">{subnet.stats.marketCap}</div>
                  </div>
                </div>
                <div className="text-sm text-emerald-400">
                  {subnet.stats.weeklyChange} this week
                </div>
              </div>

              <div className="card p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400">
                    <Globe size={20} />
                  </div>
                  <div>
                    <div className="text-sm text-slate-400">TAM</div>
                    <div className="text-xl font-semibold">{subnet.stats.tam}</div>
                  </div>
                </div>
                <div className="text-sm text-emerald-400">
                  Expanding market
                </div>
              </div>
            </div>

            {/* Timeline */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold mb-6">Recent Updates</h2>
              <div className="space-y-6">
                {timelineEvents.map((event, index) => (
                  <div key={index} className="flex gap-4">
                    <div className="relative">
                      <div className="w-3 h-3 rounded-full bg-indigo-500 ring-4 ring-indigo-500/10" />
                      {index !== timelineEvents.length - 1 && (
                        <div className="absolute top-3 left-1.5 w-px h-full bg-slate-700" />
                      )}
                    </div>
                    <div>
                      <div className="text-sm text-slate-400 mb-1">{event.date}</div>
                      <h3 className="text-lg font-medium mb-2">{event.title}</h3>
                      <p className="text-slate-300">{event.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="col-span-4 space-y-6">
            {/* Rating Card */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold mb-6">Overall Score</h2>
              <div className="flex items-center justify-between mb-8">
                <div className="text-5xl font-bold">{subnet.metrics.overall}</div>
                <div className="text-4xl font-bold text-slate-400">/5</div>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Team</span>
                  <div className="flex items-center gap-2">
                    {renderStars(subnet.metrics.team)}
                    <span className="text-sm font-medium">{subnet.metrics.team}</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Product</span>
                  <div className="flex items-center gap-2">
                    {renderStars(subnet.metrics.product)}
                    <span className="text-sm font-medium">{subnet.metrics.product}</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Community</span>
                  <div className="flex items-center gap-2">
                    {renderStars(subnet.metrics.community)}
                    <span className="text-sm font-medium">{subnet.metrics.community}</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Mission</span>
                  <div className="flex items-center gap-2">
                    {renderStars(subnet.metrics.mission)}
                    <span className="text-sm font-medium">{subnet.metrics.mission}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold mb-4">Quick Stats</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-400">
                    <Shield size={16} />
                    <span>Validators</span>
                  </div>
                  <span className="font-medium">{subnet.stats.validators}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-400">
                    <Code size={16} />
                    <span>Open Source</span>
                  </div>
                  <span className="font-medium">Yes</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-400">
                    <GitBranch size={16} />
                    <span>Latest Version</span>
                  </div>
                  <span className="font-medium">v2.1.0</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-400">
                    <MessageSquare size={16} />
                    <span>Community Size</span>
                  </div>
                  <span className="font-medium">25,000+</span>
                </div>
              </div>
            </div>

            {/* Performance */}
            <div className="card p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Performance</h2>
                <select className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm">
                  <option>Last 30 days</option>
                  <option>Last 90 days</option>
                  <option>Last year</option>
                </select>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-400">Uptime</span>
                    <span className="text-sm font-medium text-emerald-400">99.9%</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full">
                    <div className="h-full w-[99.9%] bg-emerald-500 rounded-full" />
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-400">Response Time</span>
                    <span className="text-sm font-medium text-indigo-400">120ms</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full">
                    <div className="h-full w-[85%] bg-indigo-500 rounded-full" />
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-400">Success Rate</span>
                    <span className="text-sm font-medium text-purple-400">98.5%</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full">
                    <div className="h-full w-[98.5%] bg-purple-500 rounded-full" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubnetReport;