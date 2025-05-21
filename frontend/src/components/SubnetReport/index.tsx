import React from 'react';
import { ArrowLeft, Users, DollarSign, BarChart3, Globe, Download, ExternalLink, GitBranch, Star, TrendingUp, Shield, Code, MessageSquare, ChevronDown } from 'lucide-react';
import { Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

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

  const categoryAnalysis = [
    {
      name: 'Mission',
      score: 5,
      summary: 'Provide a decentralized alternative to major Web2 AI services like OpenAI\'s API, offering better accessibility, broader model diversity, and superior performance.',
      keyInsight: 'Clear mission with specific benchmarks against Web2 competitors.',
      criteria: [
        {
          question: 'Is the subnet\'s mission clearly stated and easy to understand?',
          answer: 'Yes. Focused on decentralizing AI compute with a clear value proposition.'
        },
        {
          question: 'Does the mission address a real-world need or opportunity?',
          answer: 'Yes. Addresses high AI compute costs and centralization issues.'
        },
        {
          question: 'Is the subnet\'s stated purpose differentiated from others in the ecosystem?',
          answer: 'Yes. Chutes aims to be the first fully decentralized OpenAI alternative.'
        }
      ]
    },
    {
      name: 'Team',
      score: 3,
      summary: 'Founded by experienced Bittensor developers Namoray and BonOliver (with Jon Durbin as a key contributor). Operated by Rayon Labs.',
      keyInsight: 'Strong technical team but limited public visibility of key members.',
      criteria: [
        {
          question: 'Is the team experienced and credible?',
          answer: 'Yes. Core members have strong Bittensor backgrounds.'
        },
        {
          question: 'Is the team public and transparent?',
          answer: 'Partially. Some members are public, but not all.'
        },
        {
          question: 'Is the team\'s track record verifiable?',
          answer: 'Limited public information, but strong technical output.'
        }
      ]
    },
    {
      name: 'Product & Revenue',
      score: 4,
      summary: 'The Chutes AI compute platform is live and has started generating revenue through paid access and enterprise integrations. The Squad AI agent platform, also built by the team, is currently in beta.',
      keyInsight: 'Live product with early revenue and enterprise traction.',
      criteria: [
        {
          question: 'Is the product live and accessible?',
          answer: 'Yes. Platform is live and in use.'
        },
        {
          question: 'Is there evidence of revenue or real usage?',
          answer: 'Yes. Paid access and enterprise integrations.'
        },
        {
          question: 'Is the product differentiated?',
          answer: 'Yes. Decentralized compute with unique agent platform.'
        }
      ]
    },
    {
      name: 'Community',
      score: 4,
      summary: 'Active Discord and Twitter presence. Community-driven development and regular updates.',
      keyInsight: 'Strong, growing community with regular engagement.',
      criteria: [
        {
          question: 'Is there an active community?',
          answer: 'Yes. Discord and Twitter are active.'
        },
        {
          question: 'Is the community engaged in development?',
          answer: 'Yes. Community feedback is incorporated.'
        },
        {
          question: 'Are there regular updates and events?',
          answer: 'Yes. Frequent updates and community calls.'
        }
      ]
    }
  ];

  const collaborations = [
    { name: 'Subnet-21 Compute Node', logo: '', description: 'Joint compute infrastructure' },
    { name: 'Subnet-10 Infinite Games', logo: '', description: 'AI-powered prediction markets' }
  ];

  // Sample data for the chart
  const chartData = [
    { date: '2024-01', emissions: 2.1, rating: 3.8 },
    { date: '2024-02', emissions: 2.3, rating: 4.0 },
    { date: '2024-03', emissions: 2.7, rating: 4.2 },
    { date: '2024-04', emissions: 3.0, rating: 4.3 },
    { date: '2024-05', emissions: 3.4, rating: 4.4 },
    { date: '2024-06', emissions: 3.8, rating: 4.5 },
    { date: '2024-07', emissions: 4.1, rating: 4.6 },
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

            {/* Category Analysis Section */}
            <div>
              <h2 className="text-2xl font-bold mb-6">Category Analysis</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {categoryAnalysis.map((cat, idx) => (
                  <CategoryCard key={cat.name} category={cat} />
                ))}
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

            {/* TAO Emissions & Rating Chart */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold mb-4">TAO Emissions & Rating Over Time</h2>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="date" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis yAxisId="left" orientation="left" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} domain={[0, 5]} />
                    <YAxis yAxisId="right" orientation="right" tick={{ fill: '#a5b4fc', fontSize: 12 }} axisLine={false} tickLine={false} domain={[0, 5]} hide />
                    <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: 8, color: '#fff' }} />
                    <Legend wrapperStyle={{ color: '#cbd5e1', fontSize: 14 }} />
                    <Line yAxisId="left" type="monotone" dataKey="emissions" name="TAO Emissions (%)" stroke="#6366f1" strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 7 }} />
                    <Line yAxisId="right" type="monotone" dataKey="rating" name="Subnet Rating" stroke="#10b981" strokeWidth={3} dot={{ r: 5 }} activeDot={{ r: 7 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Collaborations Section */}
                <div>
              <h2 className="text-2xl font-bold mb-4 mt-10">Collaborations</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {collaborations.map((collab, idx) => (
                  <div key={collab.name} className="card p-4 flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-slate-700 flex items-center justify-center">
                      {/* Optionally add logo here */}
                </div>
                <div>
                      <div className="font-semibold">{collab.name}</div>
                      <div className="text-slate-400 text-sm">{collab.description}</div>
                  </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// CategoryCard component
const CategoryCard = ({ category }: { category: any }) => {
  const [expanded, setExpanded] = React.useState(false);
  return (
    <div className="card p-6 relative">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-bold">{category.name}</h3>
        <span className={`rounded-full px-3 py-1 text-sm font-semibold ${category.score >= 4 ? 'bg-emerald-600/20 text-emerald-400' : category.score >= 3 ? 'bg-orange-500/20 text-orange-400' : 'bg-red-500/20 text-red-400'}`}>{category.score}</span>
      </div>
      <div className="mb-2 text-slate-200 font-medium">{category.summary}</div>
      <div className="mb-2 text-xs text-slate-400 uppercase tracking-wide">Key Insight</div>
      <div className="mb-4 text-slate-300">{category.keyInsight}</div>
      <button
        className="flex items-center gap-2 text-indigo-400 hover:text-indigo-300 text-sm mb-2"
        onClick={() => setExpanded((e) => !e)}
      >
        See {category.criteria.length} assessment criteria
        <ChevronDown size={16} className={`transition-transform ${expanded ? 'rotate-180' : ''}`} />
      </button>
      {expanded && (
        <div className="space-y-3 mt-2">
          {category.criteria.map((crit: any, idx: number) => (
            <div key={idx}>
              <div className="font-semibold text-slate-200">{crit.question}</div>
              <div className="text-slate-300">{crit.answer}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SubnetReport;