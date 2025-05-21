import React, { useState, useEffect } from 'react';
import { X, ArrowUpRight, TrendingUp, Zap, Users, Clock, ChevronDown, Github, Twitter, ExternalLink } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import { CategoryType } from '../../types';
import { formatNumber } from '../../utils/format';
import { getCategoryColor } from '../../utils/colors';

const SubnetDetail: React.FC = () => {
  const { selectedSubnet, setSelectedSubnet } = useAppContext();
  const [showEli5, setShowEli5] = useState(false);
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  const [categories, setCategories] = useState<CategoryType[]>([]);

  useEffect(() => {
    fetch('/subnets_frontend_ready.json')
      .then(res => res.json())
      .then((data: CategoryType[]) => setCategories(data));
  }, []);
  
  let subnet = null;
  let category = null;
  
  categories.forEach(cat => {
    const found = cat.subnets.find(sub => sub.id === selectedSubnet);
    if (found) {
      subnet = found;
      category = cat;
    }
  });
  
  if (!subnet || !category) return null;

  const categoryColor = getCategoryColor(category.id);
  const subnetNumber = subnet.id.match(/\d+/)?.[0] || '';
  const subnetId = `SN${subnetNumber}`;
  
  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="absolute top-4 right-4 w-96 card overflow-hidden transform transition-all duration-300 animate-in slide-in-from-right">
      {/* Header with gradient overlay */}
      <div 
        className="relative p-4 border-b border-slate-700"
        style={{
          background: `linear-gradient(45deg, ${categoryColor}20, transparent)`
        }}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium py-1 px-2 rounded-full" 
              style={{ backgroundColor: `${categoryColor}20` }}>
              {category.name}
            </span>
            <span className="text-sm text-slate-400">{subnetId}</span>
          </div>
          <button 
            onClick={() => setSelectedSubnet(null)}
            className="p-1.5 rounded-full hover:bg-slate-700/50 transition-colors duration-200"
          >
            <X size={16} />
          </button>
        </div>
        <h3 className="text-xl font-semibold mb-2">{subnet.name}</h3>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-1.5">
            <TrendingUp size={14} className="text-slate-400" />
            <span className="text-slate-300">${formatNumber(subnet.marketCap)}M</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Zap size={14} className="text-slate-400" />
            <span className="text-slate-300">{subnet.emissions}% TAO</span>
            <span className="text-xs text-slate-400">(8/103)</span>
          </div>
        </div>
      </div>

      <div className="max-h-[calc(100vh-320px)] overflow-y-auto scrollbar-thin">
        {/* About Section */}
        <div className="p-4 border-b border-slate-700/50">
          <button 
            onClick={() => toggleSection('about')}
            className="flex items-center justify-between w-full text-left group"
          >
            <h4 className="font-medium group-hover:text-slate-300 transition-colors">What is this subnet about?</h4>
            <ChevronDown 
              size={16} 
              className={`transition-transform duration-200 ${
                expandedSection === 'about' ? 'rotate-180' : ''
              }`}
            />
          </button>
          
          {expandedSection === 'about' && (
            <div className="mt-4 space-y-3">
              <p className="text-sm text-slate-300 leading-relaxed">{subnet.description}</p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowEli5(!showEli5)}
                  className={`text-xs font-medium px-3 py-1.5 rounded-full transition-colors ${
                    showEli5 
                      ? 'bg-indigo-500/20 text-indigo-400' 
                      : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                  }`}
                >
                  {showEli5 ? 'Technical Version' : 'Explain Like I\'m 5'}
                </button>
              </div>
              {showEli5 && (
                <div className="text-sm text-slate-300 bg-slate-700/30 p-4 rounded-lg border border-slate-600/30">
                  This subnet helps computers understand and create text just like humans do, making it easier for people to chat with AI and get help with writing.
                </div>
              )}
            </div>
          )}
        </div>

        {/* Value Proposition */}
        <div className="p-4 border-b border-slate-700/50">
          <button 
            onClick={() => toggleSection('value')}
            className="flex items-center justify-between w-full text-left group"
          >
            <h4 className="font-medium group-hover:text-slate-300 transition-colors">Why should I care?</h4>
            <ChevronDown 
              size={16} 
              className={`transition-transform duration-200 ${
                expandedSection === 'value' ? 'rotate-180' : ''
              }`}
            />
          </button>
          
          {expandedSection === 'value' && (
            <div className="mt-4">
              <ul className="space-y-3 text-sm text-slate-300">
                <li className="flex items-start gap-3 p-2 rounded-lg bg-slate-700/30 border border-slate-600/30">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2"></div>
                  <p className="flex-1">High-performance infrastructure for AI applications with proven scalability</p>
                </li>
                <li className="flex items-start gap-3 p-2 rounded-lg bg-slate-700/30 border border-slate-600/30">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2"></div>
                  <p className="flex-1">Strong validator network with 99.9% uptime and robust security measures</p>
                </li>
                <li className="flex items-start gap-3 p-2 rounded-lg bg-slate-700/30 border border-slate-600/30">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2"></div>
                  <p className="flex-1">Growing ecosystem with over 1000 active developers and rising demand</p>
                </li>
              </ul>
            </div>
          )}
        </div>

        {/* Team Section */}
        <div className="p-4 border-b border-slate-700/50">
          <button 
            onClick={() => toggleSection('team')}
            className="flex items-center justify-between w-full text-left group"
          >
            <h4 className="font-medium group-hover:text-slate-300 transition-colors">Who's building this?</h4>
            <ChevronDown 
              size={16} 
              className={`transition-transform duration-200 ${
                expandedSection === 'team' ? 'rotate-180' : ''
              }`}
            />
          </button>
          
          {expandedSection === 'team' && (
            <div className="mt-4">
              <div className="bg-slate-700/30 rounded-lg border border-slate-600/30 p-4">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 rounded-full bg-slate-600 flex items-center justify-center">
                    <Users size={16} />
                  </div>
                  <div>
                    <div className="font-medium">Core Team</div>
                    <div className="text-sm text-slate-400">5 members</div>
                  </div>
                </div>
                <p className="text-sm text-slate-300">
                  Experienced team with background in ML and distributed systems. 3 members are publicly known.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Strengths & Challenges */}
        <div className="p-4 border-b border-slate-700/50">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="font-medium">Strengths</h4>
            </div>
            <div className="grid gap-2">
              <div className="bg-emerald-500/10 rounded-lg p-3">
                <div className="text-sm text-emerald-400">Strong technical foundation</div>
              </div>
              <div className="bg-emerald-500/10 rounded-lg p-3">
                <div className="text-sm text-emerald-400">Active community</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <h4 className="font-medium">Challenges</h4>
            </div>
            <div className="grid gap-2">
              <div className="bg-amber-500/10 rounded-lg p-3">
                <div className="text-sm text-amber-400">High requirements</div>
              </div>
              <div className="bg-amber-500/10 rounded-lg p-3">
                <div className="text-sm text-amber-400">Early stage</div>
              </div>
            </div>
          </div>
        </div>

        {/* Latest Updates */}
        <div className="p-4 border-b border-slate-700/50">
          <button 
            onClick={() => toggleSection('updates')}
            className="flex items-center justify-between w-full text-left group"
          >
            <h4 className="font-medium group-hover:text-slate-300 transition-colors">Latest Updates</h4>
            <ChevronDown 
              size={16} 
              className={`transition-transform duration-200 ${
                expandedSection === 'updates' ? 'rotate-180' : ''
              }`}
            />
          </button>
          
          {expandedSection === 'updates' && (
            <div className="mt-4 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Twitter size={16} className="text-sky-400" />
                  <a href="#" className="text-sky-400 hover:text-sky-300 transition-colors text-sm font-medium">
                    @{subnet.name}
                  </a>
                </div>
                <a href="#" className="text-xs text-slate-400 hover:text-slate-300 transition-colors">
                  View All
                </a>
              </div>
              
              <div className="space-y-2">
                <div className="bg-slate-700/30 rounded-lg border border-slate-600/30 p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium">Release v2.1.0</div>
                    <span className="text-xs text-slate-400">2h ago</span>
                  </div>
                  <p className="text-sm text-slate-300">Improved validator performance and reduced latency by 25%</p>
                </div>
                
                <div className="bg-slate-700/30 rounded-lg border border-slate-600/30 p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium">Community Update</div>
                    <span className="text-xs text-slate-400">1d ago</span>
                  </div>
                  <p className="text-sm text-slate-300">Join our weekly community call this Friday!</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <a 
                  href="#" 
                  className="flex items-center gap-1.5 text-sm hover:text-slate-300 transition-colors"
                >
                  <Github size={14} />
                  <span>GitHub</span>
                </a>
                <a 
                  href="#" 
                  className="flex items-center gap-1.5 text-sm hover:text-slate-300 transition-colors"
                >
                  <ExternalLink size={14} />
                  <span>Documentation</span>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 bg-slate-800/50">
        <a 
          href="#" 
          className="flex items-center justify-center gap-1.5 py-2 px-4 rounded-lg bg-indigo-500/10 text-indigo-400 hover:bg-indigo-500/20 transition-colors"
        >
          <span className="font-medium">Explore Full Analysis</span>
          <ArrowUpRight size={16} />
        </a>
      </div>
    </div>
  );
};

export default SubnetDetail;